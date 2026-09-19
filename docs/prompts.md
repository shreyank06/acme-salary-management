# Prompts and instructions used with the AI tool

Tool: Claude Code. These are the actual instructions given during the build, lightly condensed.
Wording of my own replies is omitted; what matters is what was asked, and what I decided.

## 1. Understand the brief
- "What is this about, in short" (attached the assessment PDF) → summary of deliverables.
- "What about any 3rd party service integration?" → confirmed none required; only component library,
  hosting, AI tools. Decision: no integrations in v1, listed as out of scope.
- "What tech stack to use?" then pasted the job description (Python + TypeScript, TDD, CI/CD, Docker,
  AI/LLM good-to-have) → chose FastAPI + SQLAlchemy + SQLite and Next.js + TypeScript + shadcn/ui.

## 2. Build
> "As a senior full-stack AI/ML engineer, go ahead with development keeping architecture clean,
> modular, well documented."

Constraints I set, which shaped every step:
- Requirements doc first (goal, scope, what is deliberately left out).
- Incremental commits so the evolution is visible.
- Tests first, in slices: domain → repository → services → API → seed → frontend.
- Layered backend (API → service → repository → domain), pure functions for statistics.
- Measure, don't assume: seed 10k rows, time the endpoints, load the UI in a real browser.

## 3. Deploy and verify (driven interactively)
- Deploy the API on Render (Docker, free tier) and the UI on Vercel; set `NEXT_PUBLIC_API_URL`.
- Diagnosed a 404 on Vercel: Framework Preset had been left as "Other" → set to Next.js, redeployed.
- Turned off Vercel deployment protection so reviewers can open the site without a login.
- Tightened CORS from `["*"]` to the exact Vercel origin and re-verified in an incognito window.

## 4. Where I overrode or corrected the AI
See `docs/ai-workflow.md`. In short: reserved `.test` email TLD in test data, lint-flagged
`setState`-in-effect hooks (redesigned), Vitest 4/oxc JSX config, and a self-referential font variable.
