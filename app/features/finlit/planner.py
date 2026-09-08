
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

CURRENCIES: dict[str, dict[str, Any]] = {
    "USD": {"symbol": "$", "name": "US dollar", "decimals": 2},
    "EUR": {"symbol": "€", "name": "Euro", "decimals": 2},
    "GBP": {"symbol": "£", "name": "British pound", "decimals": 2},
    "NGN": {"symbol": "₦", "name": "Nigerian naira", "decimals": 0},
    "KES": {"symbol": "KSh", "name": "Kenyan shilling", "decimals": 0},
    "GHS": {"symbol": "GH₵", "name": "Ghanaian cedi", "decimals": 2},
    "ZAR": {"symbol": "R", "name": "South African rand", "decimals": 2},
    "INR": {"symbol": "₹", "name": "Indian rupee", "decimals": 0},
    "PKR": {"symbol": "Rs", "name": "Pakistani rupee", "decimals": 0},
    "PHP": {"symbol": "₱", "name": "Philippine peso", "decimals": 0},
    "BRL": {"symbol": "R$", "name": "Brazilian real", "decimals": 2},
    "MXN": {"symbol": "MX$", "name": "Mexican peso", "decimals": 0},
    "IDR": {"symbol": "Rp", "name": "Indonesian rupiah", "decimals": 0},
    "BDT": {"symbol": "৳", "name": "Bangladeshi taka", "decimals": 0},
    "EGP": {"symbol": "E£", "name": "Egyptian pound", "decimals": 0},
}

CATEGORIES: dict[str, str] = {
    "transport": "needs",
    "food": "needs",
    "data_airtime": "needs",
    "school": "needs",
    "rent_family": "needs",
    "toiletries": "needs",
    "clothes": "wants",
    "eating_out": "wants",
    "entertainment": "wants",
    "subscriptions": "wants",
    "gifts": "wants",
    "other_wants": "wants",
    "savings_goal": "savings",
    "emergency_fund": "savings",
    "debt_payment": "savings",
}

CATEGORY_LABELS: dict[str, str] = {
    "transport": "Transport",
    "food": "Food & groceries",
    "data_airtime": "Data & airtime",
    "school": "School supplies / fees",
    "rent_family": "Rent or family contribution",
    "toiletries": "Toiletries & health",
    "clothes": "Clothes & shoes",
    "eating_out": "Eating out & snacks",
    "entertainment": "Entertainment & games",
    "subscriptions": "Subscriptions",
    "gifts": "Gifts & giving",
    "other_wants": "Other wants",
    "savings_goal": "Savings goal",
    "emergency_fund": "Emergency fund",
    "debt_payment": "Paying off debt",
}

TARGET_SPLIT = {"needs": 0.50, "wants": 0.30, "savings": 0.20}
PERIODS = {"weekly": 52, "biweekly": 26, "monthly": 12}

@dataclass(slots=True)
class PlanLine:
    category: str
    amount: float

    @property
    def bucket(self) -> str:
        return CATEGORIES[self.category]

@dataclass(slots=True)
class PlanResult:
    income: float
    period: str
    currency: str
    buckets: dict[str, float]
    shares: dict[str, float]
    unallocated: float
    overspend: float
    health: int
    verdict: str
    tips: list[str]
    lines: list[dict[str, Any]] = field(default_factory=list)
    annual: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "income": round(self.income, 2),
            "period": self.period,
            "currency": self.currency,
            "symbol": CURRENCIES.get(self.currency, {"symbol": ""})["symbol"],
            "buckets": {k: round(v, 2) for k, v in self.buckets.items()},
            "shares": {k: round(v, 3) for k, v in self.shares.items()},
            "target_shares": TARGET_SPLIT,
            "unallocated": round(self.unallocated, 2),
            "overspend": round(self.overspend, 2),
            "health": self.health,
            "verdict": self.verdict,
            "tips": self.tips,
            "lines": self.lines,
            "annual": {k: round(v) for k, v in self.annual.items()},
        }

def build_plan(
    income: float, period: str, currency: str, lines: list[PlanLine]
) -> PlanResult:
    if income <= 0:
        raise ValueError("Income must be above zero.")
    if period not in PERIODS:
        raise ValueError("period must be weekly, biweekly or monthly")
    if currency not in CURRENCIES:
        raise ValueError("Unknown currency")
    buckets = {"needs": 0.0, "wants": 0.0, "savings": 0.0}
    for line in lines:
        if line.category not in CATEGORIES:
            raise ValueError(f"Unknown category '{line.category}'")
        if line.amount < 0:
            raise ValueError("Amounts cannot be negative")
        buckets[line.bucket] += line.amount
    total = sum(buckets.values())
    unallocated = max(0.0, income - total)
    overspend = max(0.0, total - income)
    shares = {k: (v / income) for k, v in buckets.items()}
    health, verdict, tips = _score(
        income, buckets, shares, unallocated, overspend, currency, lines
    )
    periods = PERIODS[period]
    annual = {
        "income": income * periods,
        "savings": buckets["savings"] * periods,
        "wants": buckets["wants"] * periods,
        "unallocated": unallocated * periods,
    }
    return PlanResult(
        income=income,
        period=period,
        currency=currency,
        buckets=buckets,
        shares=shares,
        unallocated=unallocated,
        overspend=overspend,
        health=health,
        verdict=verdict,
        tips=tips,
        lines=[
            {
                "category": l.category,
                "label": CATEGORY_LABELS[l.category],
                "bucket": l.bucket,
                "amount": round(l.amount, 2),
            }
            for l in lines
            if l.amount > 0
        ],
        annual=annual,
    )

def _fmt(amount: float, currency: str) -> str:
    meta = CURRENCIES[currency]
    if meta["decimals"] == 0:
        return f"{meta['symbol']}{amount:,.0f}"
    return f"{meta['symbol']}{amount:,.2f}"

def _score(
    income, buckets, shares, unallocated, overspend, currency, lines
) -> tuple[int, str, list[str]]:
    tips: list[str] = []
    score = 100.0
    if overspend > 0:
        score -= min(60.0, overspend / income * 200)
        tips.append(
            f"You are planning to spend {_fmt(overspend, currency)} more than you earn. Cut wants first — every plan must balance before it can grow."
        )
    sav = shares["savings"]
    if sav >= 0.20:
        tips.append(
            f"Saving {sav:.0%} — you are at or above the 20% target. That is the habit that compounds."
        )
    elif sav >= 0.10:
        score -= (0.20 - sav) * 150
        tips.append(
            f"Saving {sav:.0%}. Nudge it toward 20%: moving {_fmt((0.20 - sav) * income, currency)} from wants gets you there."
        )
    else:
        score -= 25 + (0.10 - sav) * 150
        tips.append(
            f"Saving only {sav:.0%}. Even {_fmt(0.10 * income, currency)} per period, moved *before* you spend, changes the story."
        )
    if shares["wants"] > 0.40:
        score -= (shares["wants"] - 0.40) * 120
        top = max(
            (l for l in lines if l.bucket == "wants"),
            key=lambda l: l.amount,
            default=None,
        )
        if top:
            tips.append(
                f"Wants are {shares['wants']:.0%} of income; the biggest is {CATEGORY_LABELS[top.category].lower()} at {_fmt(top.amount, currency)}. Halving that alone frees {_fmt(top.amount / 2, currency)}."
            )
    if shares["needs"] > 0.65:
        tips.append(
            f"Needs take {shares['needs']:.0%} — tight, and common for students. Protect a small savings line anyway; the amount matters less than the habit."
        )
    if unallocated > 0.05 * income:
        score -= min(15.0, unallocated / income * 50)
        tips.append(
            f"{_fmt(unallocated, currency)} has no job. Unassigned money leaks — give it a name (emergency fund is a good first one)."
        )
    emergency = sum(l.amount for l in lines if l.category == "emergency_fund")
    if emergency <= 0 and overspend == 0:
        tips.append(
            "No emergency-fund line yet. A buffer of one period's needs is what stops a broken phone from becoming debt."
        )
    score = int(max(0, min(100, round(score))))
    if score >= 85:
        verdict = "Sharp plan"
    elif score >= 65:
        verdict = "Solid — a couple of tweaks"
    elif score >= 40:
        verdict = "Leaky — fixable this week"
    else:
        verdict = "Needs a reset"
    return score, verdict, tips[:4]

def suggest_split(income: float, currency: str, period: str) -> dict[str, Any]:
    if currency not in CURRENCIES:
        raise ValueError("Unknown currency")
    return {
        "income": income,
        "period": period,
        "currency": currency,
        "symbol": CURRENCIES[currency]["symbol"],
        "needs": round(income * 0.50, 2),
        "wants": round(income * 0.30, 2),
        "savings": round(income * 0.20, 2),
    }

def financing_cost(price: float, monthly_payment: float, months: int) -> dict[str, Any]:
    if price <= 0 or monthly_payment <= 0 or months <= 0:
        raise ValueError("price, monthly_payment and months must be positive")
    total = monthly_payment * months
    extra = total - price
    apr = _implied_apr(price, monthly_payment, months)
    return {
        "price": price,
        "total_paid": round(total, 2),
        "extra_paid": round(extra, 2),
        "extra_pct": round(extra / price * 100, 1),
        "implied_apr": round(apr * 100, 1) if apr is not None else None,
        "months": months,
    }

def _implied_apr(price: float, payment: float, months: int) -> float | None:
    if payment * months <= price:
        return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        pv = payment * (1 - (1 + mid) ** -months) / mid if mid > 0 else payment * months
        if pv > price:
            lo = mid
        else:
            hi = mid
    return lo * 12

def weeks_to_goal(target: float, weekly: float, already: float = 0.0) -> int | None:
    remaining = max(0.0, target - already)
    if remaining <= 0:
        return 0
    if weekly <= 0:
        return None
    return math.ceil(remaining / weekly)
