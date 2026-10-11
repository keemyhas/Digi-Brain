# Project Logging Rule

> Setup: no placeholders. Enforce as-is.

## 1. When to append to `memory/project-log.md`

1. **After every commit** (mandatory, before declaring done): one entry with the commit SHA.
2. **At session end** (mandatory, even if nothing shipped): one entry recording what was asked, decided, and why nothing shipped.
3. One commit = one entry. Never batch.

## 2. Entry format (fixed)

```text
## YYYY-MM-DD — <short title> (commit <sha or `uncommitted`) — <who>
- Asked: <owner intent>
- Decided: <choice made>
- Why: <driving trade-off / invariant>
- Shipped: <files + SHA, or "not shipped because ...">
```

## 3. Never-lose guarantees

- APPEND-ONLY: never edit or delete past entries. Corrections are new entries referencing the old date.
- Sync to all mirrors immediately on every append (see `memory-intake.md` §4).
- Staleness check: if `git log --oneline -1` is newer than the last entry, append the missing entry before starting new work.
- Keep entries terse (4 bullets). Long rationale belongs in `decisions.md` — link it from the Why line.
