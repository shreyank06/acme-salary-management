# Salary Management — Requirements (one page)

## Goal
Give ACME's HR Manager a web app to **manage salary data for ~10,000 employees across multiple countries** and to **answer "how do we pay people?"** — replacing the Excel workflow.

## Persona
**HR Manager** (single trusted user). Needs to find a person fast, correct a record, and get a defensible answer to questions such as *"What is the median engineer salary in India?"*, *"Which country has the highest payroll?"*, *"How is pay distributed?"*.

## In scope (v1)
| # | Feature | Why |
|---|---------|-----|
| 1 | **Employee CRUD** (name, email, job title, department, country, salary, hire date) | Core replacement for the spreadsheet |
| 2 | **Search, filter (country, department, job title, salary range), sort, server-side pagination** | 10k rows: must stay fast, cannot ship all rows to the browser |
| 3 | **Insights dashboard**: headcount, total payroll, avg/median, min/max, per-country and per-department breakdowns, salary distribution | The actual business question |
| 4 | **Multi-currency aware**: each employee has a currency derived from country; per-country stats in local currency, org-wide stats in USD | Comparing INR to USD raw is wrong; hiding currency is worse |
| 5 | **Seed script** for 10,000 realistic employees (deterministic via seed) | Required; also reproducible demos/tests |
| 6 | **Dockerised, CI-tested, deployed** | Production-readiness |

## Deliberately left out (and why)
- **Authentication / RBAC** — single persona; adds surface area without adding insight into design. Would be first follow-up (SSO + audit trail).
- **Live FX rates** — a static, versioned rate table is deterministic and testable; live rates add an external dependency and non-reproducible reports. Clearly labelled "approximate".
- **Payroll runs, tax, bonuses/equity, salary history** — different problem (compensation *management* vs. payroll). Salary history is the natural v2.
- **Bulk Excel import UI** — seed covers initial load; import needs validation/rollback UX worth its own iteration.
- **Multi-tenant / soft-delete / audit** — out of scope for one org; noted in trade-offs.
- **LLM "ask in English" analytics** — tempting, but free-text-to-SQL on salary data raises correctness and privacy risk; deterministic insights come first.

## Key decisions & trade-offs (detail in `docs/architecture.md`)
- **Python/FastAPI + SQLite (Postgres-ready via SQLAlchemy)**, **Next.js/TypeScript** frontend — matches the role's Python + TypeScript stack.
- **Salary = integer annual amount in local currency** (no floats for money).
- **Layered backend** (API → service → repository) with pure statistics functions so the core logic is trivially unit-testable.
- Aggregates computed on demand (10k rows is cheap; indexed columns). Caching/materialisation is a documented next step if data grows 100×.

## Success criteria
- List/filter/search responds < 200 ms on 10k rows; insights < 500 ms.
- Core logic covered by fast, deterministic unit tests; CI green.
- HR can create, edit, delete an employee and see insights update.
