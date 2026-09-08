# PocketPath — video pitch script (target 3:00, max 5:00)

Start the stack (`uvicorn app.main:app --reload --port 8000`, `cd web && npm run dev`), open http://localhost:5173, log in with the demo account or a fresh account so the baseline flow is visible.

| Time | On screen | Say |
|---|---|---|
| 0:00 | Landing | "Financial literacy is the life skill most schools skip — and the students who miss it pay for it with the first 'only forty a month' phone plan. Free resources are dollar-only, reading-heavy, and never check whether anyone learned anything. PocketPath fixes all three." |
| 0:20 | Dashboard → **Take baseline** | "It starts by measuring. Six questions, no studying — the 'before' photo." |
| 0:35 | Answer, submit, show explanations | "Every answer is explained, right or wrong. Baseline saved." |
| 0:50 | Learn → Budgeting basics → grade | "Eight four-minute modules. Each check explains every option — a wrong answer becomes the lesson, not a penalty." |
| 1:10 | Money Moves → The phone upgrade → choose *Finance it* | "Knowing isn't doing. Money Moves puts real situations in front of you and tracks wallet, debt, confidence, and a decision-quality score. Financing the phone: 960 of debt and the score drops." |
| 1:35 | Planner: currency NGN, income 40,000, template, tweak a line | "Then you apply it to *your* money. Pick your currency — naira here — enter what you actually get, and the planner scores it against the 50/30/20 guide with a concrete fix: exactly how much to move, and where." |
| 2:05 | Financing check: 900 / 45 / 24 → Reveal | "And the most common trap gets its own tool: 'only 45 a month' is actually 1,080 for a 900 phone — 20 % extra, about 18 % APR — or you save the same 45 a month and own it outright in 20 months." |
| 2:25 | Goals → add "New laptop" | "Goals get weekly maths and a date." |
| 2:35 | Dashboard → Coach: "How is my budget looking?", "Where do my goals stand?" | "The coach answers from your own numbers — plan, goals, scores — and never invents any. It runs fully offline; add an API key and the same grounded prompt drives an LLM." |
| 2:55 | Post-assessment → dashboard shows gain | "Finally the 'after' photo: the post-assessment, and the gain is on the dashboard. That number is the point of the whole app." |
| 3:10 | Terminal: `pytest` (15 passed); repo tree | "FastAPI, SQLAlchemy, React, fifteen tests, one Docker container, fifteen currencies, zero external dependencies at runtime — so a school can run it on a laptop. PocketPath: money skills for students, with the results measured." |

## Screenshots (in `docs/screenshots/`)

`01-landing.png`, `02-baseline.png`, `03-learn-graded.png`, `04-money-moves.png`, `05-planner.png` (use as the Devpost cover visual), `06-dashboard-coach.png`, `07-mobile-planner.png`.

## Devpost copy blocks

**Tagline:** Learn → decide → apply. Money skills for students, in their own currency, with the learning gain measured.

**Track:** Equity in Education.

**Built with:** Python, FastAPI, Pydantic, SQLAlchemy, SQLite, React, TypeScript, Vite, Docker.
