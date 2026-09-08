from datetime import date
from app.core.testing import auth_headers, create_user
from app.features.finlit.content import ASSESSMENT, MODULES, SCENARIOS
from app.features.finlit.core import months_to_target, progress_pct, target_date


def test_projection_math():
    assert months_to_target(600, 50) == 3
    assert months_to_target(600, 0) is None
    assert months_to_target(0, 10) == 0
    assert progress_pct(250, 1000) == 25.0
    assert progress_pct(1200, 1000) == 100.0


def test_target_date():
    d = target_date(600, 50, date(2026, 9, 6))
    assert d is not None
    assert d == date(2026, 12, 6)


def test_content_complete():
    for module in MODULES.values():
        assert len(module.quiz) >= 3
        for q in module.quiz:
            assert 0 <= q["answer_index"] < len(q["options"])
            assert q["explanation"]
    assert len(ASSESSMENT) >= 6
    for s in SCENARIOS.values():
        assert len(s.choices) >= 3
        for c in s.choices:
            assert "quality" in c and "explanation" in c


def test_full_api_flow(client):
    headers = auth_headers(create_user(client, email="pocket@example.com")["token"])
    overview = client.get("/api/finance/overview", headers=headers)
    assert overview.status_code == 200
    body = overview.json()
    assert body["modules_total"] == len(MODULES)
    assert body["profile"]["sim"]["balance"] == 100.0
    pre = client.post(
        "/api/finance/assess",
        headers=headers,
        json={
            "kind": "pre",
            "answers": [
                {"question_id": q["question_id"], "chosen_index": q["answer_index"]}
                for q in ASSESSMENT[:4]
            ],
        },
    )
    assert pre.status_code == 200
    assert pre.json()["score"] == 100.0
    mod = client.get("/api/finance/modules/budgeting", headers=headers)
    assert mod.status_code == 200
    assert "lessons" in mod.json()
    assert "answer_index" not in mod.json()["quiz"][0]
    grade = client.post(
        "/api/finance/modules/budgeting/grade",
        headers=headers,
        json={
            "answers": [
                {"question_id": q["question_id"], "chosen_index": q["answer_index"]}
                for q in MODULES["budgeting"].quiz
            ],
        },
    )
    assert grade.status_code == 200
    assert grade.json()["passed"] is True
    assert grade.json()["progress"]["completed"] is True
    sim = client.get("/api/finance/sim", headers=headers).json()
    assert len(sim["scenarios"]) == len(SCENARIOS)
    scenario = sim["scenarios"][0]
    choice = SCENARIOS[scenario["scenario_id"]].choices[0]
    outcome = client.post(
        "/api/finance/simulate",
        headers=headers,
        json={
            "scenario_id": scenario["scenario_id"],
            "choice_id": choice["choice_id"],
        },
    )
    assert outcome.status_code == 200
    res = outcome.json()
    assert res["state"]["decisions"] == 1
    assert res["delta"]["quality"] > 0
    assert res["explanation"]
    goal = client.post(
        "/api/finance/goals",
        headers=headers,
        json={
            "name": "New laptop",
            "target": 600,
            "weekly": 50,
        },
    )
    assert goal.status_code == 201
    g = goal.json()
    assert g["months_to_target"] == 3
    assert g["target_eta"]
    contrib = client.post(
        f"/api/finance/goals/{g ['id']}/contribute",
        headers=headers,
        json={"amount": 150},
    )
    assert contrib.status_code == 200
    assert contrib.json()["progress"] == 25.0
    bad = client.post(
        "/api/finance/simulate",
        headers=headers,
        json={"scenario_id": "nope", "choice_id": "x"},
    )
    assert bad.status_code == 422
    assert client.get("/api/finance/overview").status_code == 401


def test_quiz_answers_are_not_always_first_option():
    """Guards against a guessable quiz: the correct option must move around."""
    positions = {q["answer_index"] for m in MODULES.values() for q in m.quiz}
    assert len(positions) >= 3
    assert len({q["answer_index"] for q in ASSESSMENT}) >= 2
    for module in MODULES.values():
        for q in module.quiz:
            assert len(q["options"]) == 4
            assert len(set(q["options"])) == 4
    for scenario in SCENARIOS.values():
        ids = [c["choice_id"] for c in scenario.choices]
        assert len(ids) == len(set(ids))
        assert max(c["quality"] for c in scenario.choices) >= 0.8


def test_coach_scam_question_is_grounded_offline(client):
    headers = auth_headers(create_user(client, email="scam@example.com")["token"])
    res = client.post(
        "/api/finance/coach",
        headers=headers,
        json={
            "message": "Someone says they can double my money in two weeks, is it a scam?"
        },
    )
    assert res.status_code == 200
    text = res.json()["reply"].lower()
    assert "scheme" in text or "scam" in text
    assert "next step" in text
