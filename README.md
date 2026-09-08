# PocketPath

A financial-literacy app that helps students learn money skills, test decisions, and build a practical budget.

## Features

- Baseline and post-learning assessments
- Short financial-literacy modules
- Real-life decision simulator
- Multi-currency budget planner
- Savings goals and progress tracking
- Optional grounded AI coach

## Stack

- Python, FastAPI, SQLAlchemy
- React, TypeScript, Vite
- SQLite/PostgreSQL
- Docker

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

In another terminal:

```bash
cd web
npm install
npm run dev
```

Run tests:

```bash
python -m pytest
```

Optional AI variables: `AI_MODE`, `AI_API_KEY`, `AI_BASE_URL`, and `AI_MODEL`.

## Demo

https://pocketpath-ctbb.onrender.com

## License

MIT — see `LICENSE`.
