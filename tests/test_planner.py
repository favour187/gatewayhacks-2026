import pytest

from app.features.finlit.content import ASSESSMENT
from app.core.testing import auth_headers, create_user
from app.features.finlit.planner import (
    PlanLine,
    build_plan,
    financing_cost,
    suggest_split,
    weeks_to_goal,
)


def lines(**amounts):
    return [PlanLine(category=k, amount=v) for k, v in amounts.items()]


def test_plan_buckets_and_shares():
    res = build_plan(
        1000,
        "monthly",
        "USD",
        lines(
            transport=200,
            food=300,
            entertainment=200,
            savings_goal=200,
            emergency_fund=100,
        ),
    )
    assert res.buckets == {"needs": 500.0, "wants": 200.0, "savings": 300.0}
    assert res.shares["savings"] == pytest.approx(0.3)
    assert res.unallocated == 0
    assert res.overspend == 0
    assert res.health >= 85
    assert res.verdict == "Sharp plan"
    assert res.annual["savings"] == pytest.approx(3600)


def test_overspend_is_penalised_and_explained():
    res = build_plan(500, "weekly", "NGN", lines(food=300, clothes=300, eating_out=100))
    assert res.overspend == 200
    assert res.health < 50
    assert any("more than you earn" in t for t in res.tips)


def test_low_savings_gets_a_concrete_nudge():
    res = build_plan(
        40000,
        "monthly",
        "NGN",
        lines(transport=12000, food=15000, entertainment=9000, savings_goal=2000),
    )
    assert res.shares["savings"] == pytest.approx(0.05)
    assert any("Saving only 5%" in t for t in res.tips)
    assert res.health < 85


def test_unallocated_money_flagged():
    res = build_plan(1000, "monthly", "EUR", lines(food=200, savings_goal=200))
    assert res.unallocated == 600
    assert any("no job" in t for t in res.tips)


def test_plan_validation():
    with pytest.raises(ValueError):
        build_plan(0, "monthly", "USD", [])
    with pytest.raises(ValueError):
        build_plan(100, "yearly", "USD", [])
    with pytest.raises(ValueError):
        build_plan(100, "monthly", "XXX", [])
    with pytest.raises(ValueError):
        build_plan(100, "monthly", "USD", lines(caviar=10))


def test_suggest_split_and_weeks():
    split = suggest_split(200, "GBP", "weekly")
    assert (split["needs"], split["wants"], split["savings"]) == (100, 60, 40)
    assert weeks_to_goal(600, 50) == 12
    assert weeks_to_goal(600, 50, already=300) == 6
    assert weeks_to_goal(600, 0) is None
    assert weeks_to_goal(100, 50, already=100) == 0


def test_financing_cost_reveals_the_extra_and_apr():
    offer = financing_cost(900, 45, 24)
    assert offer["total_paid"] == 1080
    assert offer["extra_paid"] == 180
    assert offer["extra_pct"] == 20.0
    assert 15 < offer["implied_apr"] < 25
    zero = financing_cost(900, 75, 12)
    assert zero["extra_paid"] == 0 and zero["implied_apr"] == 0.0


def test_planner_api_preview_save_and_coach(client):
    meta = client.get("/api/finance/planner/meta").json()
    assert "NGN" in meta["currencies"] and any(
        c["key"] == "emergency_fund" for c in meta["categories"]
    )

    payload = {
        "income": 30000,
        "period": "monthly",
        "currency": "NGN",
        "lines": [
            {"category": "transport", "amount": 8000},
            {"category": "food", "amount": 9000},
            {"category": "data_airtime", "amount": 3000},
            {"category": "eating_out", "amount": 6000},
            {"category": "savings_goal", "amount": 2000},
        ],
    }
    preview = client.post("/api/finance/planner/preview", json=payload)
    assert preview.status_code == 200
    body = preview.json()
    assert body["symbol"] == "₦"
    assert body["buckets"]["needs"] == 20000
    assert body["unallocated"] == 2000

    user = create_user(client, email="planner@example.com")
    headers = auth_headers(user["token"])
    assert client.get("/api/finance/planner", headers=headers).json()["plan"] is None
    saved = client.put("/api/finance/planner", json=payload, headers=headers)
    assert saved.status_code == 200
    assert saved.json()["result"]["health"] == body["health"]
    again = client.put(
        "/api/finance/planner", json={**payload, "income": 35000}, headers=headers
    ).json()
    assert again["result"]["income"] == 35000
    assert (
        client.get("/api/finance/planner", headers=headers).json()["plan"]["result"][
            "income"
        ]
        == 35000
    )

    coach = client.post(
        "/api/finance/coach",
        json={"message": "How is my budget looking?"},
        headers=headers,
    )
    assert coach.status_code == 200
    reply = coach.json()
    assert reply["provider"] == "local-demo"
    assert "Health score" in reply["reply"]

    offer = client.post(
        "/api/finance/coach",
        json={
            "message": "Should I finance the phone?",
            "financing": {"price": 900, "monthly_payment": 45, "months": 24},
        },
        headers=headers,
    ).json()
    assert "₦1,080" in offer["reply"] and "APR" in offer["reply"]

    concept = client.post(
        "/api/finance/coach",
        json={"message": "what is compound interest?"},
        headers=headers,
    ).json()
    assert "Compound growth" in concept["reply"]

    bad = client.post(
        "/api/finance/planner/preview", json={**payload, "period": "yearly"}
    )
    assert bad.status_code == 422


def test_assessment_endpoint_and_pre_post_gain(client):
    user = create_user(client, email="assess@example.com")
    headers = auth_headers(user["token"])
    qs = client.get("/api/finance/assessment", headers=headers).json()["questions"]
    assert len(qs) >= 6 and "answer_index" not in qs[0]
    bank = {q["question_id"]: q["answer_index"] for q in ASSESSMENT}
    wrong = [
        {
            "question_id": q["question_id"],
            "chosen_index": (bank[q["question_id"]] + 1) % 4,
        }
        for q in qs
    ]
    pre = client.post(
        "/api/finance/assess", json={"kind": "pre", "answers": wrong}, headers=headers
    ).json()
    assert pre["score"] == 0 and pre["explanations"][0]["correct"] is False
    assert pre["profile"]["pre_taken"] is True and pre["profile"]["post_taken"] is False
    assert pre["profile"]["score_gain"] == 0
    right = [
        {"question_id": q["question_id"], "chosen_index": bank[q["question_id"]]}
        for q in qs
    ]
    post = client.post(
        "/api/finance/assess", json={"kind": "post", "answers": right}, headers=headers
    ).json()
    assert post["score"] == 100
    assert post["profile"]["score_gain"] == 100
