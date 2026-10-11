# Future Planning Protocol - document the future before building the future

> Setup: replace `{{FUTURE_PLANS_DIR}}` (default `docs/future-plans/`), then delete this line.
> Condensed generic port: the principle and status machine transfer; expand with your own gates as needed.

## 1. Core principle

Not every discussed idea should become code. Default action for out-of-scope ideas is **documentation, not implementation**. An idea becomes a task only when its prerequisites and roadmap status justify it.

## 2. Status classification (check before touching code)

| Status | Meaning | Action |
|---|---|---|
| EXISTING | Already implemented | Inspect it; no duplicates; update docs if needed |
| CURRENT | Approved for current scope | Follow the standard dev workflow |
| DESIGNED | Spec'd but not started | Maintain the design doc; do not implement |
| FUTURE | Relevant but deferred | Write/update a future-plan doc (dependencies, risks, open questions); do not touch production code |
| REJECTED / SUPERSEDED | Decided against | Record the decision + why, link the superseding item; do not revive without re-approval |

## 3. Future-plan doc minimum

Each deferred concept gets a doc under `{{FUTURE_PLANS_DIR}}` with: problem, proposed approach, dependencies/prerequisites, risks, open questions, and the roadmap gate that would promote it to CURRENT.

## 4. Guards

- No production code "because it was discussed."
- No speculative scaffolding (tables, endpoints, deps) for FUTURE items.
- Promoting FUTURE -> CURRENT requires owner approval + a project-log entry.
