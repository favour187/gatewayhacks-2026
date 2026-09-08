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
                "options": [
                    "Rent",
                    "Wants",
                    "Savings",
                    "Needs",
                ],
                "answer_index": 1,
                "explanation": "50% goes to needs, 30% to wants, 20% to savings and debt.",
            },
            {
                "question_id": "q_bud_2",
                "stem": "Why pay yourself first?",
                "options": [
                    "Banks require it",
                    "It removes all wants",
                    "It increases your income",
                    "Saving becomes automatic before spending",
                ],
                "answer_index": 3,
                "explanation": "Moving savings out of reach first protects the goal from impulse spending.",
            },
            {
                "question_id": "q_bud_3",
                "stem": "A budget is best described as…",
                "options": [
                    "A way to stop spending entirely",
                    "A tax form",
                    "A plan for your money",
                    "A list only of bills",
                ],
                "answer_index": 2,
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
                    "Buying new shoes",
                    "Investment returns",
                    "Unexpected expenses",
                    "Daily coffee",
                ],
                "answer_index": 2,
                "explanation": "It absorbs surprises so a shock does not become debt.",
            },
            {
                "question_id": "q_sav_2",
                "stem": "A realistic first target is…",
                "options": [
                    "Six years of expenses",
                    "One week of expenses",
                    "One million dollars",
                    "Zero",
                ],
                "answer_index": 1,
                "explanation": "Start tiny and consistent; the buffer grows over time.",
            },
            {
                "question_id": "q_sav_3",
                "stem": "Which makes a savings goal stick?",
                "options": [
                    "Using the same jar for everything",
                    "Keeping it secret",
                    "Naming it and scheduling contributions",
                    "Waiting for spare money",
                ],
                "answer_index": 2,
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
                    "When you pay the minimum",
                    "Never",
                    "When you pay the full statement by the due date",
                    "When you use it often",
                ],
                "answer_index": 2,
                "explanation": "Full payment within the grace period means the loan cost is zero.",
            },
            {
                "question_id": "q_cre_2",
                "stem": "Paying only the minimum usually means…",
                "options": [
                    "Debt stretches for a long time with interest",
                    "Your score drops to zero",
                    "Your limit doubles",
                    "No interest is charged",
                ],
                "answer_index": 0,
                "explanation": "Minimum payments mostly cover interest, barely touching the principal.",
            },
            {
                "question_id": "q_cre_3",
                "stem": "A strong credit history is built by…",
                "options": [
                    "Maxing out cards",
                    "On-time payments and low usage",
                    "Many late payments",
                    "Closing all accounts",
                ],
                "answer_index": 1,
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
                    "Doubled your budget",
                    "Earned money",
                    "Still spent more than zero",
                    "Saved money",
                ],
                "answer_index": 2,
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
                    "Savings transfers",
                    "Rent",
                    "Small repeated purchases",
                    "Big planned bills",
                ],
                "answer_index": 2,
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
                    "Avoid all risk",
                    "Guarantee profits",
                    "Double money monthly",
                ],
                "answer_index": 0,
                "explanation": "Diversify broadly with one low-cost holding.",
            },
            {
                "question_id": "q_inv_2",
                "stem": "Higher expected returns usually mean…",
                "options": [
                    "Instant cash",
                    "Fixed interest",
                    "Higher risk of losing value",
                    "No risk at all",
                ],
                "answer_index": 2,
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
                "options": [
                    "24 weeks",
                    "3 weeks",
                    "12 weeks",
                    "6 weeks",
                ],
                "answer_index": 2,
                "explanation": "$600 / $50 per week = 12 weeks.",
            },
            {
                "question_id": "q_goa_2",
                "stem": "A good goal is…",
                "options": [
                    "Only for adults",
                    "Vague and flexible",
                    "Named, quantified, and scheduled",
                    "Hidden away",
                ],
                "answer_index": 2,
                "explanation": "Concrete goals get funded; vague ones do not.",
            },
            {
                "question_id": "q_goa_3",
                "stem": "Why start saving early even with small amounts?",
                "options": [
                    "It removes risk",
                    "Growth compounds over time",
                    "It avoids all budgets",
                    "Banks require it",
                ],
                "answer_index": 1,
                "explanation": "Early money has the longest time to grow.",
            },
        ],
    ),
    "earning": Module(
        "earning",
        "Earning & your first income",
        "Side hustles, payslips, and what 'net' really means",
        [
            "Income is anything that comes in: allowance, a weekend job, tutoring, selling things you make, a stipend.",
            "Gross is what you are promised; net is what lands in your account after deductions like tax or pension. Plan with net.",
            "Irregular income (gigs, holiday work) needs a smoother: pay yourself a fixed 'salary' from it and bank the rest.",
            "Your time has a price. Divide any purchase by your hourly rate: a $60 pair of shoes at $6/hour is ten hours of work.",
        ],
        [
            {
                "question_id": "q_ear_1",
                "stem": "You should build your budget on…",
                "options": [
                    "Your gross pay",
                    "Your net pay (after deductions)",
                    "What a friend earns",
                    "Next year's expected raise",
                ],
                "answer_index": 1,
                "explanation": "Only net pay actually arrives; gross includes money that is deducted before you see it.",
            },
            {
                "question_id": "q_ear_2",
                "stem": "Your gig income is $300 one month and $60 the next. The smart move is…",
                "options": [
                    "Spend it all in the good month",
                    "Stop working gigs",
                    "Pay yourself a fixed amount and bank the rest in good months",
                    "Borrow in the bad month",
                ],
                "answer_index": 2,
                "explanation": "A fixed 'salary' from irregular income smooths the ups and downs and builds a buffer automatically.",
            },
            {
                "question_id": "q_ear_3",
                "stem": "At $5/hour, a $75 jacket costs you…",
                "options": [
                    "5 hours of work",
                    "75 hours of work",
                    "1 hour of work",
                    "15 hours of work",
                ],
                "answer_index": 3,
                "explanation": "$75 / $5 = 15 hours. Pricing things in hours makes wants easier to judge.",
            },
        ],
    ),
    "safety": Module(
        "safety",
        "Scams & digital money safety",
        "Spotting the tricks that target young people first",
        [
            "'Double your money in two weeks' is not an investment; it is a scheme paid by the next person who joins. Guaranteed high returns do not exist.",
            "Never share an OTP, PIN or password — no bank, app or 'agent' will ever need it. Urgency ('act now!') is the scammer's main tool.",
            "'Buy now, pay later' and 'only X per month' are loans. Multiply the payment by the months before you tap.",
            "Check before you trust: official app stores, verified accounts, a second opinion from a trusted adult. Slowing down is free.",
        ],
        [
            {
                "question_id": "q_saf_1",
                "stem": "A message promises a guaranteed 50% return in 14 days. This is most likely…",
                "options": [
                    "A scheme that pays early joiners with later joiners' money",
                    "A normal savings account",
                    "An index fund",
                    "A government bond",
                ],
                "answer_index": 0,
                "explanation": "No legitimate product guarantees high returns fast; that pattern is the classic pyramid or Ponzi scheme.",
            },
            {
                "question_id": "q_saf_2",
                "stem": "Someone calling from 'your bank' asks for the code just sent to your phone. You should…",
                "options": [
                    "Read it out — they said it was urgent",
                    "Send it by text instead",
                    "Hang up and call the bank's official number yourself",
                    "Ask them to call back later",
                ],
                "answer_index": 2,
                "explanation": "A one-time code is the key to your account; nobody legitimate will ever ask for it.",
            },
            {
                "question_id": "q_saf_3",
                "stem": "'Only $30 a month for 12 months' on a $300 gadget means you pay…",
                "options": [
                    "$300",
                    "$30",
                    "$360 — $60 more than the price",
                    "Nothing extra if you're on time",
                ],
                "answer_index": 2,
                "explanation": "$30 × 12 = $360. The extra $60 is interest with a friendlier name.",
            },
        ],
    ),
}
ASSESSMENT: list[dict[str, Any]] = [
    {
        "question_id": "a_1",
        "stem": "In the 50/30/20 rule, the 20% is for…",
        "options": [
            "Savings and debt",
            "Needs",
            "Wants",
            "Shopping",
        ],
        "answer_index": 0,
        "explanation": "The final slice funds your future.",
    },
    {
        "question_id": "a_2",
        "stem": "An emergency fund protects you from…",
        "options": [
            "Sales",
            "Free time",
            "Unexpected expenses",
            "Rising income",
        ],
        "answer_index": 2,
        "explanation": "It is the buffer between a shock and debt.",
    },
    {
        "question_id": "a_3",
        "stem": "Credit card interest starts when…",
        "options": [
            "You open the card",
            "You pay in full",
            "You check the app",
            "You carry a balance past the due date",
        ],
        "answer_index": 3,
        "explanation": "Cleared balances in the grace period charge nothing.",
    },
    {
        "question_id": "a_4",
        "stem": "A 'best deal' on something unwanted is…",
        "options": [
            "Still a waste of money",
            "Free money",
            "Savings",
            "An investment",
        ],
        "answer_index": 0,
        "explanation": "The baseline to compare against is zero.",
    },
    {
        "question_id": "a_5",
        "stem": "Diversification means…",
        "options": [
            "Keeping cash under a mattress",
            "Borrowing to invest",
            "Investing in one stock",
            "Spreading money across many investments",
        ],
        "answer_index": 3,
        "explanation": "Many holdings smooth the ride.",
    },
    {
        "question_id": "a_6",
        "stem": "$400 at $40/week reaches the goal in…",
        "options": [
            "4 weeks",
            "1 week",
            "40 weeks",
            "10 weeks",
        ],
        "answer_index": 3,
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
    "investment_dm": Scenario(
        "investment_dm",
        "The 'investment' DM",
        "A classmate's cousin is 'helping people double their money in two weeks'. Everyone seems to be joining. You have $100.",
        [
            {
                "choice_id": "decline_report",
                "label": "Say no, and warn your classmate it looks like a pyramid scheme",
                "money": 0.0,
                "debt": 0.0,
                "confidence": 10.0,
                "quality": 0.95,
                "explanation": "Guaranteed fast returns are the signature of a scheme. You kept your money and maybe a friend's.",
            },
            {
                "choice_id": "ask_adult",
                "label": "Ask a trusted adult or check the regulator's warning list first",
                "money": 0.0,
                "debt": 0.0,
                "confidence": 6.0,
                "quality": 0.8,
                "explanation": "Slowing down beats the scammer's urgency. A second opinion usually ends it.",
            },
            {
                "choice_id": "test_small",
                "label": "Put in $30 'just to test it'",
                "money": -30.0,
                "debt": 0.0,
                "confidence": -5.0,
                "quality": 0.25,
                "explanation": "Early 'wins' are bait to make you put in more. Small tests are how schemes recruit.",
            },
            {
                "choice_id": "all_in",
                "label": "Put in the full $100 before the 'slots' close",
                "money": -100.0,
                "debt": 0.0,
                "confidence": -10.0,
                "quality": 0.05,
                "explanation": "Artificial scarcity is the trick. Most joiners lose everything when the chain stops.",
            },
        ],
    ),
    "subscriptions": Scenario(
        "subscriptions",
        "The subscription pile",
        "Three streaming and gaming subscriptions cost you $24 a month. You really use one of them.",
        [
            {
                "choice_id": "cancel_redirect",
                "label": "Cancel the two you don't use and auto-move the $16 to savings",
                "money": 16.0,
                "debt": 0.0,
                "confidence": 8.0,
                "quality": 0.95,
                "explanation": "$16 a month is $192 a year. Redirecting it, not just cancelling, is what makes it stick.",
            },
            {
                "choice_id": "family_plan",
                "label": "Switch to a shared/family plan with siblings and split the cost",
                "money": 8.0,
                "debt": 0.0,
                "confidence": 5.0,
                "quality": 0.75,
                "explanation": "Cheaper per person and you keep what you use — a solid compromise.",
            },
            {
                "choice_id": "keep_all",
                "label": "Keep everything — it's only $24",
                "money": -24.0,
                "debt": 0.0,
                "confidence": -3.0,
                "quality": 0.3,
                "explanation": "Small recurring charges are exactly what quietly breaks budgets.",
            },
            {
                "choice_id": "add_one",
                "label": "Add a fourth service that just launched a student discount",
                "money": -32.0,
                "debt": 0.0,
                "confidence": -5.0,
                "quality": 0.15,
                "explanation": "A discount on something you didn't need is still a new monthly cost.",
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
