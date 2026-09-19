# How AI was used

Tool: Claude Code (agentic CLI) acting as a pair, with me making the decisions.

**Process**
1. Read the brief + job description → decided on Python/FastAPI + Next.js/TS (matches the role).
2. Wrote the one-page requirements *before* code, including what is out of scope and why.
3. TDD in slices: tests first (confirmed red), then implementation (green), then commit —
   domain → repository → services → API → seed → frontend.
4. Verified beyond unit tests: seeded 10k rows, timed endpoints, exercised the built UI in a real browser.

**Where I overrode / corrected the AI's output**
- Reserved `.test` TLD rejected by `email-validator` in test data → switched to a real domain.
- Lint caught `setState`-in-effect patterns in generated hooks → redesigned `useAsync` to derive `loading`
  from a request key and moved page-reset into event handlers.
- Vitest 4 needed `oxc` JSX config, and `@vitejs/plugin-react` had a Babel peer conflict → dropped the plugin.
- Fonts fell back to serif because generated CSS referenced itself (`--font-sans: var(--font-sans)`).

**Guardrails**: ruff + pytest + eslint + tsc + CI on every push; commits kept small and reviewable.
