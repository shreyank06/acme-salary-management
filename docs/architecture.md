# Architecture & Trade-offs

```
┌────────────────────┐   REST/JSON   ┌───────────────────────────────────────────┐
│ Next.js (TS)       │ ────────────▶ │ FastAPI                                   │
│ shadcn/ui          │               │  api/      thin routers, HTTP mapping     │
│  views → hooks →   │ ◀──────────── │  services/ business rules (no HTTP/SQL)   │
│  typed api client  │               │  repositories/ all SQL lives here         │
└────────────────────┘               │  domain/   pure functions (stats, FX)     │
                                     └───────────────┬───────────────────────────┘
                                                     ▼
                                          SQLite (SQLAlchemy 2.0)
```

## Layers and why
| Layer | Responsibility | Tested with |
|---|---|---|
| `domain/` | Country→currency, static FX, median/histogram. No I/O. | Pure unit tests (ms) |
| `repositories/` | Filter/sort/paginate SQL; narrow projections for analytics | In-memory SQLite |
| `services/` | Rules: email uniqueness, currency derivation, USD-vs-local policy | In-memory SQLite |
| `api/` | Validation (Pydantic), status codes, DI | FastAPI `TestClient` |

Dependency direction is one-way (api → services → repositories → models); services never see HTTP, so
they could be reused from a CLI or job.

## Key decisions
1. **Currency policy** — every employee stores local currency (derived from country, never client-supplied).
   Scoped to one country ⇒ local currency; org-wide ⇒ USD via a *static* FX table. Reproducible reports beat
   live-but-shifting numbers for an HR question like "how do we pay?". Labelled "approximate" in the UI.
2. **Money as integers** — annual salary in whole currency units; no float rounding drift.
3. **Median in Python, not SQL** — SQLite lacks a median aggregate. Analytics fetch a 5-column projection
   (~10k rows, ~60–105 ms measured) and reduce in pure, tested functions. Postgres would use `percentile_cont`.
4. **Server-side pagination/sort/filter** — the browser never receives 10k rows. Stable ordering with an `id`
   tiebreaker so pages don't shuffle.
5. **Indexes** — `(country, department)`, `job_title`, `salary`, `full_name`. Free-text search uses
   `LIKE '%q%'` (not index-assisted); fine at 10k rows, see improvements.
6. **`create_all` instead of migrations** — single table, single deployer. Alembic is the first step if the
   schema starts to evolve.
7. **App factory + injected session factory** — tests get an isolated in-memory DB, no globals, no files.
8. **Frontend** — `useAsync` (last-request-wins, keeps stale data while loading), debounced search,
   validation mirrored client-side for instant feedback while the server stays the authority.

## Performance (10,000 rows, local, measured)
List+search+sort ≈ 10–60 ms · summary ≈ 80 ms · breakdown ≈ 105 ms · distribution ≈ 50 ms.

## Known limitations / next steps
- No auth/RBAC or audit log (salary data is sensitive — first thing before real use).
- Text search: move to FTS5 / Postgres `pg_trgm` beyond ~100k rows.
- Analytics: cache or materialise per-group aggregates if data grows 100×; push aggregation into SQL.
- Salary history (effective-dated rows) to answer "how has pay changed?".
- Optional natural-language Q&A over the insights API (LLM calling *these tested endpoints* as tools, not
  free-form SQL) — deliberately deferred; see requirements.
