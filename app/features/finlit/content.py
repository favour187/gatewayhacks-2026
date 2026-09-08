from __future__ import annotations
from typing import Any


class Module:
    def __init__(
        self,
        module_id: str,
        title: str,
        topic: str,
        lessons: list[str],
        quiz: list[dict[str, Any]],
    ):
        self.module_id = module_id
        self.title = title
        self.topic = topic
        self.lessons = lessons
        self.quiz = quiz


class Scenario:
    def __init__(
        self, scenario_id: str, title: str, setup: str, choices: list[dict[str, Any]]
    ):
        self.scenario_id = scenario_id
        self.title = title
        self.setup = setup
        self.choices = choices


MODULES: dict[str, Module] = {
    "budgeting": Module(
        "budgeting",
        "Budgeting basics",
        "Income, needs, wants, and a plan for every dollar",
        [
            "A budget is a plan for your money, not a punishment. It answers: where does it come from, where does it go.",
            "Split income into needs (rent, food, transport), savings (pay yourself first), and wants (fun stuff).",
            "The 50/30/20 rule is a starting point: 50% needs, 30% wants, 20% savings and debt.",
            "Track small spending for one week first — awareness comes before control.",
        ],
        [
            {
                "question_id": "q_bud_1",
                "stem": "In the 50/30/20 rule, what does the 30% cover?",
                "options": ["Wants", "Needs", "Savings", "Rent"],
                "answer_index": 0,
                "explanation": "50% goes to needs, 30% to wants, 20% to savings and debt.",
            },
            {
                "question_id": "q_bud_2",
                "stem": "Why pay yourself first?",
                "options": [
                    "Saving becomes automatic before spending",
                    "Banks require it",
                    "It increases your income",
                    "It removes all wants",
                ],
                "answer_index": 0,
                "explanation": "Moving savings out of reach first protects the goal from impulse spending.",
            },
            {
                "question_id": "q_bud_3",
                "stem": "A budget is best described as…",
                "options": [
                    "A plan for your money",
                    "A list only of bills",
                    "A way to stop spending entirely",
                    "A tax form",
                ],
                "answer_index": 0,
                "explanation": "Budgets are plans: they give every dollar a job instead of letting spending decide for you.",
            },
        ],
    ),
    "saving": Module(
        "saving",
        "Saving & emergency funds",
        "Why a buffer comes before big goals",
        [
            "An emergency fund is money for surprises: a broken phone, a lost job, a medical bill.",
            "Start small: one week of expenses, then grow toward 3-6 months.",
            "Savings goals work best when they are named, quantified, and scheduled.",
            "Separate accounts help: one for emergencies, one for fun goals.",
        ],
        [
            {
                "question_id": "q_sav_1",
                "stem": "What is an emergency fund for?",
                "options": [
                    "Unexpected expenses",
                    "Buying new shoes",
                    "Investment returns",
                    "Daily coffee",
                ],
                "answer_index": 0,
                "explanation": "It absorbs surprises so a shock does not become debt.",
            },
            {
                "question_id": "q_sav_2",
                "stem": "A realistic first target is…",
                "options": [
                    "One week of expenses",
                    "Six years of expenses",
                    "One million dollars",
                    "Zero",
                ],
                "answer_index": 0,
                "explanation": "Start tiny and consistent; the buffer grows over time.",
            },
            {
                "question_id": "q_sav_3",
                "stem": "Which makes a savings goal stick?",
                "options": [
                    "Naming it and scheduling contributions",
                    "Keeping it secret",
                    "Waiting for spare money",
                    "Using the same jar for everything",
                ],
                "answer_index": 0,
                "explanation": "Named goals with scheduled transfers automate progress.",
            },
        ],
    ),
    "credit": Module(
        "credit",
        "Credit & cards",
        "How credit works and how it can work against you",
        [
            "A credit card is a short loan: the balance is what you borrow each month.",
            "Pay the full statement by the due date to avoid interest entirely.",
            "The minimum payment is a trap: it stretches debt for years.",
            "Your credit score grows with on-time payments and low usage of your limit.",
        ],
        [
            {
                "question_id": "q_cre_1",
                "stem": "When do you pay zero interest on a card?",
                "options": [
                    "When you pay the full statement by the due date",
                    "When you pay the minimum",
                    "When you use it often",
                    "Never",
                ],
                "answer_index": 0,
                "explanation": "Full payment within the grace period means the loan cost is zero.",
            },
            {
                "question_id": "q_cre_2",
                "stem": "Paying only the minimum usually means…",
                "options": [
                    "Debt stretches for a long time with interest",
                    "No interest is charged",
                    "Your limit doubles",
                    "Your score drops to zero",
                ],
                "answer_index": 0,
                "explanation": "Minimum payments mostly cover interest, barely touching the principal.",
            },
            {
                "question_id": "q_cre_3",
                "stem": "A strong credit history is built by…",
                "options": [
                    "On-time payments and low usage",
                    "Many late payments",
                    "Maxing out cards",
                    "Closing all accounts",
                ],
                "answer_index": 0,
                "explanation": "Reliability over time is what lenders look for.",
            },
        ],
    ),
    "spending": Module(
        "spending",
        "Spending traps",
        "Needs vs wants, sales, and impulse buying",
        [
            "Ask one question before buying: is this a need, a want, or a trap?",
            "Sales create urgency; most 'deals' still cost more than doing nothing.",
            "The 48-hour rule: put non-essential buys on a waiting list.",
            "Small daily spending is what actually busts budgets — track it once and see.",
        ],
        [
            {
                "question_id": "q_spe_1",
                "stem": "'50% off' of something you didn't need means you…",
                "options": [
                    "Still spent more than zero",
                    "Saved money",
                    "Earned money",
                    "Doubled your budget",
                ],
                "answer_index": 0,
                "explanation": "The discount only helps if you needed it at all.",
            },
            {
                "question_id": "q_spe_2",
                "stem": "The 48-hour rule helps you…",
                "options": [
                    "Avoid impulse purchases",
                    "Spend more confidently",
                    "Earn interest",
                    "Skip budgeting",
                ],
                "answer_index": 0,
                "explanation": "Waiting removes the urgency; many wants fade.",
            },
            {
                "question_id": "q_spe_3",
                "stem": "What usually breaks a budget most?",
                "options": [
                    "Small repeated purchases",
                    "Big planned bills",
                    "Rent",
                    "Savings transfers",
                ],
                "answer_index": 0,
                "explanation": "Daily small spends add up fast — awareness is the fix.",
            },
        ],
    ),
    "investing": Module(
        "investing",
        "Investing basics",
        "Growing money slowly and boringly",
        [
            "Investing means owning a slice of something that can grow: shares, index funds, bonds.",
            "Risk and reward go together: higher possible returns mean higher possible drops.",
            "Diversification (many things at once) smooths the ride.",
            "For beginners, boring index funds and time beat hot tips and timing.",
        ],
        [
            {
                "question_id": "q_inv_1",
                "stem": "An index fund lets you…",
                "options": [
                    "Own a little of many companies at once",
                    "Guarantee profits",
                    "Avoid all risk",
                    "Double money monthly",
                ],
                "answer_index": 0,
                "explanation": "Diversify broadly with one low-cost holding.",
            },
            {
                "question_id": "q_inv_2",
                "stem": "Higher expected returns usually mean…",
                "options": [
                    "Higher risk of losing value",
                    "No risk at all",
                    "Fixed interest",
                    "Instant cash",
                ],
                "answer_index": 0,
                "explanation": "Risk and reward trade off; nothing high-return is safe.",
            },
            {
                "question_id": "q_inv_3",
                "stem": "What matters most over years for a beginner?",
                "options": [
                    "Time in the market",
                    "Timing the market",
                    "Hot tips",
                    "One perfect stock",
                ],
                "answer_index": 0,
                "explanation": "Consistent investing over time beats lucky timing.",
            },
        ],
    ),
    "goals": Module(
        "goals",
        "Money goals & the math",
        "Turning dreams into deadlines you can compute",
        [
            "A money goal needs three numbers: target amount, weekly amount, and a date.",
            "Split the goal: big goals become weekly 'micro-goals' you can actually hit.",
            "Interest compounds: money you save early does double duty.",
            "Progress tracking beats motivation — a visible bar keeps you honest.",
        ],
        [
            {
                "question_id": "q_goa_1",
                "stem": "Saving $600 at $50/week takes…",
                "options": ["12 weeks", "6 weeks", "24 weeks", "3 weeks"],
                "answer_index": 0,
                "explanation": "$600 / $50 per week = 12 weeks.",
            },
            {
                "question_id": "q_goa_2",
                "stem": "A good goal is…",
                "options": [
                    "Named, quantified, and scheduled",
                    "Vague and flexible",
                    "Hidden away",
                    "Only for adults",
                ],
                "answer_index": 0,
                "explanation": "Concrete goals get funded; vague ones do not.",
            },
            {
                "question_id": "q_goa_3",
                "stem": "Why start saving early even with small amounts?",
                "options": [
                    "Growth compounds over time",
                    "Banks require it",
                    "It avoids all budgets",
                    "It removes risk",
                ],
                "answer_index": 0,
                "explanation": "Early money has the longest time to grow.",
            },
        ],
    ),
}
ASSESSMENT: list[dict[str, Any]] = [
    {
        "question_id": "a_1",
        "stem": "In the 50/30/20 rule, the 20% is for…",
        "options": ["Savings and debt", "Wants", "Needs", "Shopping"],
        "answer_index": 0,
        "explanation": "The final slice funds your future.",
    },
    {
        "question_id": "a_2",
        "stem": "An emergency fund protects you from…",
        "options": ["Unexpected expenses", "Rising income", "Free time", "Sales"],
        "answer_index": 0,
        "explanation": "It is the buffer between a shock and debt.",
    },
    {
        "question_id": "a_3",
        "stem": "Credit card interest starts when…",
        "options": [
            "You carry a balance past the due date",
            "You open the card",
            "You pay in full",
            "You check the app",
        ],
        "answer_index": 0,
        "explanation": "Cleared balances in the grace period charge nothing.",
    },
    {
        "question_id": "a_4",
        "stem": "A 'best deal' on something unwanted is…",
        "options": ["Still a waste of money", "Free money", "Savings", "An investment"],
        "answer_index": 0,
        "explanation": "The baseline to compare against is zero.",
    },
    {
        "question_id": "a_5",
        "stem": "Diversification means…",
        "options": [
            "Spreading money across many investments",
            "Investing in one stock",
            "Keeping cash under a mattress",
            "Borrowing to invest",
        ],
        "answer_index": 0,
        "explanation": "Many holdings smooth the ride.",
    },
    {
        "question_id": "a_6",
        "stem": "$400 at $40/week reaches the goal in…",
        "options": ["10 weeks", "4 weeks", "40 weeks", "1 week"],
        "answer_index": 0,
        "explanation": "$400 / $40 = 10 weeks.",
    },
]
SCENARIOS: dict[str, Scenario] = {
    "birthday": Scenario(
        "birthday",
        "Birthday money",
        "You just received $100 for your birthday. What moves first?",
        [
            {
                "choice_id": "save_all",
                "label": "Put $80 in your savings goal, spend $20 on one thing you love",
                "money": -80.0,
                "debt": 0.0,
                "confidence": 8.0,
                "quality": 0.95,
                "explanation": "Auto-saving most of it still leaves joy — the classic win-win.",
            },
            {
                "choice_id": "spend_all",
                "label": "Spend it all on a shopping trip today",
                "money": -100.0,
                "debt": 0.0,
                "confidence": -6.0,
                "quality": 0.25,
                "explanation": "The fun evaporates; the goal stays empty.",
            },
            {
                "choice_id": "lend_friend",
                "label": "Lend it all to a friend who asked",
                "money": -100.0,
                "debt": 0.0,
                "confidence": -4.0,
                "quality": 0.4,
                "explanation": "Lending money you need is a common early trap.",
            },
            {
                "choice_id": "split",
                "label": "Split it evenly: $50 save, $50 spend",
                "money": -50.0,
                "debt": 0.0,
                "confidence": 4.0,
                "quality": 0.7,
                "explanation": "A fine middle path, a little weaker on the saving habit.",
            },
        ],
    ),
    "phone": Scenario(
        "phone",
        "The phone upgrade",
        "Your phone works fine, but the new model is everywhere and it is $900.",
        [
            {
                "choice_id": "wait",
                "label": "Wait 30 days and revisit",
                "money": 0.0,
                "debt": 0.0,
                "confidence": 8.0,
                "quality": 0.9,
                "explanation": "The 48-hour rule scaled up: most urges fade.",
            },
            {
                "choice_id": "finance_24",
                "label": "Finance it: $40/month for 24 months",
                "money": -960.0,
                "debt": 960.0,
                "confidence": -8.0,
                "quality": 0.2,
                "explanation": "Financed purchases are debt with a marketing accent.",
            },
            {
                "choice_id": "buy_refurb",
                "label": "Buy a certified refurbished model for $380",
                "money": -380.0,
                "debt": 0.0,
                "confidence": 4.0,
                "quality": 0.75,
                "explanation": "Nearly new, far cheaper — a smart compromise.",
            },
            {
                "choice_id": "upgrade_now",
                "label": "Buy it now because you 'deserve it'",
                "money": -900.0,
                "debt": 900.0,
                "confidence": -6.0,
                "quality": 0.3,
                "explanation": "Deserve-based spending is the trap wearing a disguise.",
            },
        ],
    ),
    "paycheck": Scenario(
        "paycheck",
        "First paycheck",
        "Your first paycheck lands: $400 after tax. Divide it up.",
        [
            {
                "choice_id": "budget_split",
                "label": "50/30/20: $200 needs, $120 wants, $80 savings",
                "money": -400.0,
                "debt": 0.0,
                "confidence": 10.0,
                "quality": 0.95,
                "explanation": "The whole plan in one action.",
            },
            {
                "choice_id": "save_100",
                "label": "Save $100, spend the rest as it comes",
                "money": -400.0,
                "debt": 0.0,
                "confidence": 5.0,
                "quality": 0.65,
                "explanation": "Saving without a plan often leaks.",
            },
            {
                "choice_id": "all_wants",
                "label": "Treat yourself — the next one can be serious",
                "money": -400.0,
                "debt": 0.0,
                "confidence": -8.0,
                "quality": 0.2,
                "explanation": "'Next time' is how saving never starts.",
            },
        ],
    ),
    "sale": Scenario(
        "sale",
        "The 70% sale",
        "A giant flash sale: headphones you never planned for are 70% off.",
        [
            {
                "choice_id": "skip",
                "label": "Skip — you never wanted them",
                "money": 0.0,
                "debt": 0.0,
                "confidence": 8.0,
                "quality": 0.95,
                "explanation": "Saving 100% by buying nothing.",
            },
            {
                "choice_id": "budget_check",
                "label": "Check your budget, buy only if a want-line exists",
                "money": -45.0,
                "debt": 0.0,
                "confidence": 7.0,
                "quality": 0.8,
                "explanation": "Budget-first buying is the healthy approach.",
            },
            {
                "choice_id": "impulse",
                "label": "Buy now, regret later",
                "money": -45.0,
                "debt": 45.0,
                "confidence": -6.0,
                "quality": 0.25,
                "explanation": "Urgency is engineered; the wallet wins.",
            },
        ],
    ),
    "friend_loan": Scenario(
        "friend_loan",
        "The friend loan",
        "A close friend asks for $60 'just until Friday'.",
        [
            {
                "choice_id": "decline_kind",
                "label": "Say no kindly, offer help without cash",
                "money": 0.0,
                "debt": 0.0,
                "confidence": 6.0,
                "quality": 0.8,
                "explanation": "Protecting your goal is not a betrayal.",
            },
            {
                "choice_id": "give_small",
                "label": "Give $20 you can spare, call it a gift",
                "money": -20.0,
                "debt": 0.0,
                "confidence": 4.0,
                "quality": 0.7,
                "explanation": "Gifting small is honest; lending large is a trap.",
            },
            {
                "choice_id": "lend_all",
                "label": "Lend $60 from your emergency fund",
                "money": -60.0,
                "debt": 0.0,
                "confidence": -6.0,
                "quality": 0.2,
                "explanation": "Never fund others' emergencies with your own buffer.",
            },
        ],
    ),
    "emergency": Scenario(
        "emergency",
        "The real emergency",
        "Your laptop just died two weeks before exams. Repair is $150.",
        [
            {
                "choice_id": "use_fund",
                "label": "Use your emergency fund, then rebuild it",
                "money": -150.0,
                "debt": 0.0,
                "confidence": 10.0,
                "quality": 0.95,
                "explanation": "This is exactly what the buffer is for.",
            },
            {
                "choice_id": "credit_card",
                "label": "Put it on the card and pay minimums",
                "money": -150.0,
                "debt": 150.0,
                "confidence": -6.0,
                "quality": 0.35,
                "explanation": "A shock becomes expensive interest.",
            },
            {
                "choice_id": "ignore",
                "label": "Do nothing and hope it recovers",
                "money": 0.0,
                "debt": 0.0,
                "confidence": -5.0,
                "quality": 0.15,
                "explanation": "Avoiding it makes the exam problem bigger.",
            },
        ],
    ),
}


def module_dict(module: Module) -> dict[str, Any]:
    return {
        "module_id": module.module_id,
        "title": module.title,
        "topic": module.topic,
        "lessons": module.lessons,
        "quiz_count": len(module.quiz),
    }


def quiz_public(module: Module) -> list[dict[str, Any]]:
    return [
        {"question_id": q["question_id"], "stem": q["stem"], "options": q["options"]}
        for q in module.quiz
    ]


def quiz_answer(module: Module, question_id: str) -> dict[str, Any] | None:
    return next((q for q in module.quiz if q["question_id"] == question_id), None)


def scenario_dict(scenario: Scenario) -> dict[str, Any]:
    return {
        "scenario_id": scenario.scenario_id,
        "title": scenario.title,
        "setup": scenario.setup,
        "choices": [
            {"choice_id": c["choice_id"], "label": c["label"]} for c in scenario.choices
        ],
    }
