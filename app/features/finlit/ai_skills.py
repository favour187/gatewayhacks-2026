
from __future__ import annotations

import json
from typing import Any

from app.core.ai import AIMessage
from app.features.finlit import content
from app.features.finlit.planner import CATEGORY_LABELS, CURRENCIES

SYSTEM_PROMPT = (
    "You are PocketPath's money coach for students aged 13-22. Explain money ideas in plain, "
    "friendly language (max 150 words), never judgemental. Use ONLY the numbers in COACH CONTEXT "
    "JSON when talking about the student's own plan, goals or scores; if a number is missing say "
    "so. Never give investment product recommendations or tax/legal advice; suggest talking to a "
    "trusted adult for anything beyond budgeting basics. End with one concrete next step. "
    "Reply in plain text only: no markdown, no asterisks, no bullet symbols."
)

MARKER = "COACH CONTEXT JSON:"

def _ctx(system: str) -> dict[str, Any]:
    if MARKER not in system:
        return {}
    try:
        return json.loads(system.split(MARKER, 1)[1].strip())
    except json.JSONDecodeError:
        return {}

def _money(ctx: dict[str, Any], value: float | None) -> str:
    if value is None:
        return "n/a"
    cur = ctx.get("plan", {}).get("currency") or "USD"
    meta = CURRENCIES.get(cur, CURRENCIES["USD"])
    return (
        f"{meta['symbol']}{value:,.0f}"
        if meta["decimals"] == 0
        else f"{meta['symbol']}{value:,.2f}"
    )

class PlanReviewSkill:
    id = "plan-review"

    def can_handle(self, user_text: str, system: str) -> bool:
        t = user_text.lower()
        return any(
            k in t
            for k in (
                "my plan",
                "budget",
                "review",
                "how am i doing",
                "50/30/20",
                "split",
                "spend",
            )
        )

    def respond(
        self, user_text: str, system: str, context: dict[str, Any] | None
    ) -> str:
        ctx = _ctx(system)
        plan = ctx.get("plan")
        if not plan:
            return (
                "Build a plan first: enter what you receive per week or month, then add the lines you spend on. "
                "I'll compare it with the 50/30/20 guide (needs / wants / savings) and show the exact amount to move."
            )
        sh = plan["shares"]
        parts = [
            f"Your plan puts {sh['needs']:.0%} into needs, {sh['wants']:.0%} into wants and {sh['savings']:.0%} into savings "
            f"(guide: 50 / 30 / 20). Health score {plan['health']}/100 — {plan['verdict'].lower()}."
        ]
        if plan.get("overspend", 0) > 0:
            parts.append(
                f"First fix: you are {_money(ctx, plan['overspend'])} over your income, so trim wants until it balances."
            )
        elif sh["savings"] < 0.20:
            gap = (0.20 - sh["savings"]) * plan["income"]
            parts.append(
                f"Moving {_money(ctx, gap)} from wants to savings each {plan['period'].replace('ly', '')} reaches the 20% target — over a year that is {_money(ctx, gap * (52 if plan['period']=='weekly' else 26 if plan['period']=='biweekly' else 12))}."
            )
        else:
            parts.append(
                f"You are saving {_money(ctx, plan['annual']['savings'])} a year at this rate. Next step: name what it is for so it stays untouched."
            )
        if plan.get("tips"):
            parts.append("Coach note: " + plan["tips"][0])
        return "\n\n".join(parts)

class GoalSkill:
    id = "goal"

    def can_handle(self, user_text: str, system: str) -> bool:
        t = user_text.lower()
        return any(
            k in t for k in ("goal", "save for", "how long", "weeks", "afford", "reach")
        )

    def respond(
        self, user_text: str, system: str, context: dict[str, Any] | None
    ) -> str:
        ctx = _ctx(system)
        goals = ctx.get("goals") or []
        if not goals:
            return (
                "Set a goal with three numbers: the target, what you can put aside each week, and the date that gives you. "
                "Example: 600 at 50 a week is 12 weeks. Add one in Goals and I'll track the maths for you."
            )
        lines = []
        for g in goals[:3]:
            eta = (
                f"reaches {g['target_eta']}"
                if g.get("target_eta")
                else "has no weekly amount yet, so no date"
            )
            lines.append(
                f"• {g['name']}: {_money(ctx, g['contributed'])} of {_money(ctx, g['target'])} ({g['progress']:.0f}%), {_money(ctx, g['remaining'])} to go — at {_money(ctx, g['weekly'])}/week it {eta}."
            )
        slowest = max(goals, key=lambda g: g.get("months_to_target") or 0)
        nxt = f"Next step: add a small automatic transfer for '{slowest['name']}' the day money arrives, before anything else."
        return "Where your goals stand:\n" + "\n".join(lines) + "\n\n" + nxt

class DebtSkill:
    id = "debt"

    def can_handle(self, user_text: str, system: str) -> bool:
        t = user_text.lower()
        ctx = _ctx(system)
        if ctx.get("financing"):
            return True
        return any(
            k in t
            for k in (
                "debt",
                "credit",
                "loan",
                "borrow",
                "interest",
                "financ",
                "installment",
                "instalment",
                "bnpl",
                "pay later",
                "per month",
                "monthly payment",
            )
        )

    def respond(
        self, user_text: str, system: str, context: dict[str, Any] | None
    ) -> str:
        ctx = _ctx(system)
        fin = ctx.get("financing")
        base = (
            "Rule of thumb: borrowing is fine for things that grow in value or earn income (education, a work tool), "
            "risky for things that lose value (phones, clothes). 'Only X per month' hides the total — multiply it out and compare with the sticker price."
        )
        if fin:
            return (
                f"That offer: {fin['months']} payments make {_money(ctx, fin['total_paid'])} for something priced {_money(ctx, fin['price'])} — "
                f"{_money(ctx, fin['extra_paid'])} extra ({fin['extra_pct']}%), roughly {fin['implied_apr']}% APR. "
                f"Saving the same monthly amount first would buy it in about {fin['months_to_save']} months with nothing extra paid.\n\n{base}"
            )
        sim = ctx.get("sim") or {}
        if sim.get("debt", 0) > 0:
            return f"In Money Moves you are carrying {_money(ctx, sim['debt'])} of debt. Clear it before adding to savings — interest on debt almost always costs more than savings earn.\n\n{base}"
        return (
            base
            + "\n\nNext step: before any 'pay later' button, write down the total you would actually pay."
        )

class ProgressSkill:
    id = "progress"

    def can_handle(self, user_text: str, system: str) -> bool:
        t = user_text.lower()
        return any(
            k in t
            for k in (
                "progress",
                "score",
                "learn",
                "module",
                "assessment",
                "improve",
                "next",
                "what should i",
            )
        )

    def respond(
        self, user_text: str, system: str, context: dict[str, Any] | None
    ) -> str:
        ctx = _ctx(system)
        prof = ctx.get("profile") or {}
        modules_done = ctx.get("modules_done", 0)
        total = ctx.get("modules_total", len(content.MODULES))
        if not prof:
            return "Start with the pre-assessment (6 quick questions) so we can measure how much you learn, then do the Budgeting module."
        pre, post = prof.get("pre_score", 0), prof.get("post_score", 0)
        sim = prof.get("sim", {})
        msg = [
            f"Modules completed: {modules_done}/{total}. Assessment: baseline {pre:.0f}% → latest {post:.0f}%"
            + (f" (+{post - pre:.0f} points)." if post > pre else ".")
        ]
        if sim.get("decisions"):
            msg.append(
                f"Money Moves: {sim['decisions']} decisions, quality {sim['quality']:.2f}/1.00, wallet {_money(ctx, sim['balance'])}, debt {_money(ctx, sim['debt'])}."
            )
        weakest = ctx.get("weakest_module")
        if weakest:
            msg.append(
                f"Next step: retry '{weakest}' — it is your lowest module score and the quiz explains each answer."
            )
        elif modules_done < total:
            remaining = [
                m.title
                for m in content.MODULES.values()
                if m.module_id not in (ctx.get("completed_ids") or [])
            ]
            if remaining:
                msg.append(
                    f"Next step: the '{remaining[0]}' module takes about four minutes."
                )
        else:
            msg.append(
                "Next step: take the post-assessment to lock in your gain, then build a real plan in Planner."
            )
        return "\n\n".join(msg)

class ConceptSkill:
    id = "concept"

    def can_handle(self, user_text: str, system: str) -> bool:
        t = user_text.lower()
        return any(
            k in t
            for k in (
                "what is",
                "what's",
                "explain",
                "mean",
                "why",
                "compound",
                "emergency fund",
                "inflation",
                "diversif",
                "scam",
                "pyramid",
                "ponzi",
                "double your money",
                "otp",
            )
        )

    def respond(
        self, user_text: str, system: str, context: dict[str, Any] | None
    ) -> str:
        t = user_text.lower()
        if "compound" in t:
            return "Compound growth means your savings earn a return, and then that return earns its own return. 1,000 growing at 8% a year is 1,080 after one year, 1,166 after two, 2,159 after ten — the early years do the most work, which is why starting small now beats starting big later. Next step: pick any amount and set it to move automatically."
        if "emergency" in t:
            return "An emergency fund is money you do not touch except for real shocks — a broken phone, a medical bill, a lost job. Aim for one period's needs first, then build toward three months. It is what stops a shock from becoming debt. Next step: add an 'Emergency fund' line to your plan, even a small one."
        if "inflation" in t:
            return "Inflation is prices rising over time, so the same money buys less. Cash under a mattress silently shrinks; that is why savings should at least sit somewhere that pays interest. Next step: check what your savings account actually pays."
        if "diversif" in t:
            return "Diversification means not putting all your money in one thing. If one investment drops, the others cushion it. Index funds are the simplest way to hold many things at once — ask a trusted adult before opening any account. Next step: finish the Investing module."
        if "50/30/20" in t or "budget" in t:
            return "A budget is a plan for money before it arrives: about 50% to needs (transport, food, data), 30% to wants (fun), 20% to savings and debt. The percentages are a guide, the habit is the point. Next step: build yours in Planner."
        for module in content.MODULES.values():
            if module.module_id in t or module.title.lower().split()[0] in t:
                return (
                    f"{module.title} — {module.topic}. "
                    + " ".join(module.lessons[:2])
                    + " Next step: open the module and take the 3-question check."
                )
        return "Good question. The short version: know what comes in, decide where it goes before you spend it, keep a buffer for shocks, and let saving run on autopilot. Ask me about your plan, your goals, debt, or any of the eight modules."

class ScamSkill:
    id = "scam-safety"
    TRIGGERS = (
        "scam",
        "double my money",
        "double your money",
        "double our money",
        "pyramid",
        "ponzi",
        "otp",
        "guaranteed return",
        "guaranteed profit",
        "too good to be true",
    )

    def can_handle(self, user_text: str, system: str) -> bool:
        t = user_text.lower()
        return any(k in t for k in self.TRIGGERS)

    def respond(
        self, user_text: str, system: str, context: dict[str, Any] | None
    ) -> str:
        return (
            "Anything promising guaranteed or very fast returns is a scheme, not an investment — early joiners are paid with later joiners' money until it collapses. "
            "Never share an OTP, PIN or password with anyone, and treat urgency ('slots closing today') as the warning sign itself. "
            "Next step: finish the Scams & digital money safety module and check any offer with a trusted adult before sending money."
        )

class _ConceptFirst(ConceptSkill):

    id = "concept-definition"

    def can_handle(self, user_text: str, system: str) -> bool:
        t = user_text.lower().strip()
        return (
            t.startswith(
                ("what is", "what's", "whats", "explain", "define", "what does")
            )
            and "my " not in t
        )

LOCAL_SKILLS: list[Any] = [
    ScamSkill(),
    _ConceptFirst(),
    DebtSkill(),
    GoalSkill(),
    PlanReviewSkill(),
    ProgressSkill(),
    ConceptSkill(),
]

def build_messages(user_text: str, ctx: dict[str, Any] | None) -> list[AIMessage]:
    system = SYSTEM_PROMPT
    if ctx:
        system += (
            "\n\n" + MARKER + "\n" + json.dumps(ctx, separators=(",", ":"), default=str)
        )
    return [
        AIMessage(role="system", content=system),
        AIMessage(role="user", content=user_text),
    ]

__all__ = ["LOCAL_SKILLS", "SYSTEM_PROMPT", "build_messages", "CATEGORY_LABELS"]
