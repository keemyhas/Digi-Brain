# Project Log - Asked / Decided / Shipped

<!-- APPEND-ONLY: new entries go at the bottom. Never edit past entries. Enforced by rules/project-logging.md. -->

> Setup: no placeholders. APPEND-ONLY from the first entry. Rule: `rules/project-logging.md`. Router: `memory/brain.md`.

## Entry template (copy, do not alter past entries)

```text
## YYYY-MM-DD - <short title> (commit <sha or `uncommitted`) - <who>
- Asked: <what the owner asked for, verbatim intent>
- Decided: <what we chose>
- Why: <trade-off / invariant that drove it>
- Shipped: <files + commit SHA, or "not shipped because ...">
```

---

## EXAMPLE - DELETE (Ada Example's first commit)

```text
## 2026-01-05 - Second brain installed (commit a1b2c3d) - Ada Example
- Asked: Give my agent persistent memory across sessions.
- Decided: Installed Digi Brain core template with default gates.
- Why: Router pattern prevents content drift; append-only log makes staleness detectable.
- Shipped: `.agents/memory/*`, `.agents/rules/*` (commit a1b2c3d, not pushed).
```
