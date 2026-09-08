# Compliance & rules notes — GatewayHacks 2026

*Repository created:* 2026-09-07 (inside the event window; registration opened Sep 1). All project work is committed on or after that date.

## Event facts (verified from the official Devpost pages on 2026-09-08)

| Field | Value |
|---|---|
| Event | GatewayHacks 2026 — Software & AI — https://gatewayhacks-2026.devpost.com/ (rules: `/rules`) |
| Organiser | Gateway (non-profit); judges include Jonathan Chang (GatewayGS CTO) and Yaokai Jiang (Momen CEO) |
| Window | Registration Sep 1, 2026 → **submissions due Oct 1, 2026, 11:59 pm EDT** (Devpost shows Oct 2 12:00 am EDT); judging Oct 2–20; winners Oct 21 |
| Eligibility | Open worldwide, all skill levels; teams of 1–4, solo allowed. (The Devpost listing header says "students only, ages 13+", the rules page says open to everyone — the author should confirm eligibility from the organiser if not a student.) |
| Mandatory | **Join the event Discord**: https://discord.gg/XgsX3f7JV |
| Track | **Track 2 — Equity in Education** |
| Submission | Devpost project page with problem + solution and **at least one visual**; **video pitch ≤ 5 min**; repository / live site optional but recommended; AI tools allowed; working code, no-code, or design mock-ups all accepted |
| Judging | Social Impact 40 % · Technical Execution 30 % · Innovation 20 % · Design/UX 10 % |
| Originality | Must be original work created for the event |

## How this repository satisfies the rules

- **Created for the event, inside the window.** First commit 2026-09-07. `app/core/` is the author's generic infrastructure shared with other projects (no domain logic); everything in `app/features/finlit/`, `web/src/features/finlit/`, tests and docs is specific to PocketPath and was written for GatewayHacks.
- **Track fit (Equity in Education).** Free, offline-capable financial-literacy curriculum with measurable learning outcomes, localised to 15 currencies so it is usable by students outside the US.
- **Working software.** Full stack runs with zero API keys; 17 automated tests; browser-verified end-to-end flows (screenshots in `docs/screenshots/`).
- **AI tools disclosed** (below and in the README).
- **Not submitted elsewhere.** This project is entered only in GatewayHacks 2026.

## Judging-criteria mapping

| Criterion | Where it shows |
|---|---|
| Social Impact (40) | Measured learning gain (pre/post), decision-quality score, plan health; currency localisation; works on low-end phones without connectivity |
| Technical Execution (30) | Typed FastAPI + SQLAlchemy backend, deterministic + LLM-ready coach with grounded context, APR solver, test suite, CI, Docker |
| Innovation (20) | Learn → decide → apply loop with outcomes measured, the "real price of only-X-a-month" reveal, coach that refuses to invent numbers |
| Design / UX (10) | Four-minute modules, explained answers, one-screen planner with live health score, responsive UI |

## AI tool disclosure (reproduce on the submission form)

> Development was assisted by AI coding tools (Claude-based agent tooling on the Arena.ai platform). All architecture, content, formulas and code were directed, reviewed and are understood by the author. The in-app "money coach" uses a deterministic rule-based local provider by default; an optional OpenAI-compatible LLM can be enabled by configuration.

## Submission checklist

- [ ] Join the Discord (mandatory) — https://discord.gg/XgsX3f7JV
- [x] Public repo with README, screenshots — https://github.com/favour187/gatewayhacks-2026
- [ ] Video pitch ≤ 5 min (script: `docs/DEMO_SCRIPT.md`) — recorded by the author
- [ ] Devpost page: problem, solution, ≥ 1 visual (use `docs/screenshots/05-planner.png`), track = Equity in Education, AI-tools disclosure
- [ ] Submit before **Oct 1, 2026, 11:59 pm EDT**
- [ ] Eligibility confirmed by the author (see note above)
