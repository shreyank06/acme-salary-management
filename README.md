# ACME Salary Management

Web app for an HR Manager to manage salaries for ~10,000 employees across 10 countries and answer
"how do we pay people?" — replacing Excel.

- **Requirements (1 page):** [docs/requirements.md](docs/requirements.md)
- **Architecture & trade-offs:** [docs/architecture.md](docs/architecture.md)
- **AI workflow:** [docs/ai-workflow.md](docs/ai-workflow.md)

## Live demo
- **App:** https://acme-salary-management-nine.vercel.app
- **API docs:** https://acme-salary-api-pcrm.onrender.com/docs

> The API runs on Render's free tier and sleeps when idle, so the first request can take ~50 seconds.
> Data resets to the seeded 10,000 employees whenever the API restarts (free tier has no persistent disk).

## Features
- Employee CRUD; search, filter (country / department / title / salary range), sort, server-side pagination
- Insights: headcount, payroll, avg/median/min/max by country, department, job title; salary distribution
- Multi-currency aware (local currency per country; USD-normalised org-wide, static FX)

## Stack
Python 3.12 · FastAPI · SQLAlchemy · SQLite · pytest — Next.js · TypeScript · Tailwind · shadcn/ui · Vitest

## Run locally
```bash
# API
cd backend
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
python -m scripts.seed              # 10,000 employees (deterministic, idempotent; --reset to redo)
uvicorn app.main:create_app --factory --reload      # http://localhost:8000/docs

# UI (another terminal)
cd frontend && npm install && npm run dev            # http://localhost:3000
```
Or everything with Docker: `docker compose up --build` (API :8000, UI :3000; DB is seeded on first start).

## Tests
```bash
cd backend  && pytest --cov=app     # 57 tests, ~98% coverage, <2s
cd frontend && npm test && npm run lint && npm run typecheck
```

## Config
`SALARY_DATABASE_URL` (default `sqlite:///./salary.db`), `SALARY_CORS_ORIGINS` (JSON list),
`NEXT_PUBLIC_API_URL` (frontend → API base URL, build-time).

## API (see `/docs` for OpenAPI)
`GET/POST /api/employees` · `GET/PATCH/DELETE /api/employees/{id}` · `GET /api/employees/facets` ·
`GET /api/insights/{summary,breakdown,distribution}` · `GET /api/countries` · `GET /health`
