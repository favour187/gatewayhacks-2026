from __future__ import annotations
import math
from typing import Any
from sqlalchemy.orm import Session
from app.core.ai import AIGateway, get_gateway
from app.features.finlit import ai_skills, content, planner, repository
from app.features.finlit.core import outcome_delta

def overview(db: Session, user_id: str) -> dict[str, Any]:
    profile = repository.get_or_create_profile(db, user_id)
    progress = repository.module_progress(db, str(user_id))
    goals = repository.list_goals(db, str(user_id))
    modules = [
        {
            **content.module_dict(module),
            "progress": (
                progress.get(module.module_id).to_dict()
                if module.module_id in progress
                else None
            ),
        }
        for module in content.MODULES.values()
    ]
    return {
        "profile": profile.to_dict(),
        "modules": modules,
        "modules_done": sum(
            1 for m in modules if m.get("progress") and m["progress"]["completed"]
        ),
        "modules_total": len(modules),
        "goals": [g.to_dict() for g in goals],
        "sim_history_count": len(repository.sim_history(db, str(user_id))),
    }

def assess(
    db: Session, user_id: str, answers: list[dict[str, Any]], kind: str
) -> dict[str, Any]:
    profile = repository.get_or_create_profile(db, user_id)
    bank = {q["question_id"]: q for q in content.ASSESSMENT}
    pairs = [(a["question_id"], int(a["chosen_index"])) for a in answers]
    graded = _grade_bank(pairs, bank)
    score = graded["score"]
    if kind == "pre":
        profile.pre_score = score if profile.pre_attempts == 0 else profile.pre_score
        profile.pre_attempts += 1
    else:
        profile.post_score = max(profile.post_score, score)
        profile.post_attempts += 1
    repository.touch_profile(db, profile)
    db.commit()
    chosen = dict(pairs)
    explanations = [
        {
            "question_id": q["question_id"],
            "chosen_index": chosen.get(q["question_id"]),
            "correct": chosen.get(q["question_id"]) == q["answer_index"],
            "correct_answer": q["options"][q["answer_index"]],
            "explanation": q["explanation"],
        }
        for q in content.ASSESSMENT
    ]
    return {
        "kind": kind,
        **graded,
        "explanations": explanations,
        "profile": profile.to_dict(),
    }

def grade_module(
    db: Session, user_id: str, module_id: str, answers: list[dict[str, Any]]
) -> dict[str, Any]:
    module = content.MODULES.get(module_id)
    if module is None:
        raise ValueError("unknown module_id")
    bank = {q["question_id"]: q for q in module.quiz}
    pairs = [(a["question_id"], int(a["chosen_index"])) for a in answers]
    graded = _grade_bank(pairs, bank)
    passed = graded["score"] >= 60.0
    row = repository.upsert_module_score(
        db, str(user_id), module_id, graded["score"], passed
    )
    repository.touch_profile(db, repository.get_or_create_profile(db, str(user_id)))
    explanations = [
        {
            "question_id": q["question_id"],
            "chosen_index": next(
                (c for qid, c in pairs if qid == q["question_id"]), None
            ),
            "correct_answer": q["options"][q["answer_index"]],
            "explanation": q["explanation"],
        }
        for q in module.quiz
    ]
    return {
        "module_id": module_id,
        "title": module.title,
        "passed": passed,
        "detail": graded,
        "explanations": explanations,
        "progress": row.to_dict(),
    }

def simulate(
    db: Session, user_id: str, scenario_id: str, choice_id: str
) -> dict[str, Any]:
    scenario = content.SCENARIOS.get(scenario_id)
    if scenario is None:
        raise ValueError("unknown scenario_id")
    choice = next((c for c in scenario.choices if c["choice_id"] == choice_id), None)
    if choice is None:
        raise ValueError("unknown choice_id")
    profile = repository.get_or_create_profile(db, str(user_id))
    state = _state_from_profile(profile)
    outcome = outcome_delta(
        choice["money"], choice["debt"], choice["confidence"], choice["quality"]
    )
    state = outcome.apply(state)
    profile.sim_balance = state.balance
    profile.sim_debt = state.debt
    profile.sim_confidence = state.confidence
    profile.sim_decisions = state.decisions
    profile.sim_quality_sum = state.quality_sum
    repository.touch_profile(db, profile)
    repository.record_sim_decision(
        db,
        str(user_id),
        scenario_id,
        choice_id,
        {
            "money": outcome.money,
            "debt": outcome.debt,
            "confidence": outcome.confidence,
            "quality": outcome.quality,
        },
    )
    return {
        "scenario_id": scenario_id,
        "choice_id": choice_id,
        "label": choice["label"],
        "explanation": choice["explanation"],
        "delta": {
            "money": outcome.money,
            "debt": outcome.debt,
            "confidence": outcome.confidence,
            "quality": outcome.quality,
        },
        "state": state.to_dict(),
        "history": [h.to_dict() for h in repository.sim_history(db, str(user_id))],
    }

def reset_sim(db: Session, user_id: str) -> dict[str, Any]:
    profile = repository.get_or_create_profile(db, str(user_id))
    profile.sim_balance = 100.0
    profile.sim_debt = 0.0
    profile.sim_confidence = 0.0
    profile.sim_decisions = 0
    profile.sim_quality_sum = 0.0
    db.commit()
    return profile.to_dict()

def _state_from_profile(profile: Any) -> Any:
    from app.features.finlit.core import SimState

    return SimState(
        balance=profile.sim_balance,
        debt=profile.sim_debt,
        confidence=profile.sim_confidence,
        decisions=profile.sim_decisions,
        quality_sum=profile.sim_quality_sum,
    )

def _grade_bank(pairs: list[tuple[str, int]], bank: dict[str, Any]) -> dict[str, Any]:
    correct = 0
    for qid, chosen in pairs:
        q = bank.get(qid)
        if q and chosen == q["answer_index"]:
            correct += 1
    total = len(pairs)
    return {
        "correct": correct,
        "total": total,
        "score": round(correct / total * 100.0, 1) if total else 0.0,
    }

def build_plan(payload: dict[str, Any]) -> dict[str, Any]:
    lines = [
        planner.PlanLine(category=str(l["category"]), amount=float(l["amount"]))
        for l in payload.get("lines", [])
        if l.get("amount") not in (None, "")
    ]
    result = planner.build_plan(
        float(payload["income"]),
        str(payload.get("period", "monthly")),
        str(payload.get("currency", "USD")),
        lines,
    )
    return result.to_dict()

def save_plan(db: Session, user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    result = build_plan(payload)
    row = repository.upsert_plan(db, user_id, payload, result)
    repository.touch_profile(db, repository.get_or_create_profile(db, user_id))
    return row.to_dict()

def financing(payload: dict[str, Any]) -> dict[str, Any]:
    out = planner.financing_cost(
        float(payload["price"]),
        float(payload["monthly_payment"]),
        int(payload["months"]),
    )
    out["months_to_save"] = planner.weeks_to_goal(
        out["price"], float(payload["monthly_payment"])
    )
    return out

def coach_context(
    db: Session, user_id: str, extra: dict[str, Any] | None = None
) -> dict[str, Any]:
    profile = repository.get_or_create_profile(db, user_id)
    progress = repository.module_progress(db, user_id)
    goals = repository.list_goals(db, user_id)
    saved = repository.get_plan(db, user_id)
    completed = [m for m, p in progress.items() if p.completed]
    weakest = None
    if progress:
        worst = min(progress.values(), key=lambda p: p.best_score)
        if worst.best_score < 100:
            weakest = content.MODULES[worst.module_id].title
    ctx: dict[str, Any] = {
        "profile": profile.to_dict(),
        "sim": profile.to_dict()["sim"],
        "modules_done": len(completed),
        "modules_total": len(content.MODULES),
        "completed_ids": completed,
        "weakest_module": weakest,
        "goals": [g.to_dict() for g in goals],
        "plan": saved.result if saved else None,
    }
    if extra:
        ctx.update({k: v for k, v in extra.items() if v is not None})
    return ctx

def coach(
    db: Session,
    user_id: str,
    *,
    message: str,
    plan: dict[str, Any] | None = None,
    financing_offer: dict[str, Any] | None = None,
    gateway: AIGateway | None = None,
) -> dict[str, Any]:
    gateway = gateway or get_gateway()
    extra: dict[str, Any] = {}
    if plan:
        extra["plan"] = build_plan(plan)
    if financing_offer:
        extra["financing"] = financing(financing_offer)
    ctx = coach_context(db, user_id, extra)
    messages = ai_skills.build_messages(message, ctx)
    result = gateway.chat(system=messages[0].content, user=message, max_tokens=400)
    return {
        "reply": result.text,
        "provider": result.provider,
        "used_fallback": result.used_fallback,
    }
