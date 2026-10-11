# Autonomous Memory & Lesson Intake Rules

> Setup: replace `{{PLACEHOLDERS}}`, then delete this line.

## 1. When to write memory (immediately, unprompted)

1. **Design decisions** — tokens, layout standards, naming → update `patterns.md` + `decisions.md`.
2. **Root causes** — any non-obvious bug/defect diagnosed and fixed → update `bugs.md` + `agent-lessons.md`.
3. **Invariants** — any constraint that must hold forever → update `patterns.md` + `agent-lessons.md`.
4. **Corrections/preferences** — owner corrects an assumption or states a workflow policy → update `agent-lessons.md`.
5. **Pre-commit profile sync (mandatory)** — before every commit/task completion, record newly revealed owner traits in `personalities.md`.

## 2. Memory map

| File | Purpose |
|---|---|
| `memory/patterns.md` | Reusable code/architecture templates |
| `memory/decisions.md` | Decision records: context, decision, consequences |
| `memory/bugs.md` | Post-mortems: symptom, root cause, resolution, prevention |
| `memory/agent-lessons.md` | Numbered durable heuristics |
| `memory/architecture.md` | System overview: boundaries, stack, topology |
| `memory/roadmap.md` | Product/engineering roadmap; §0 Kanban is the scope gate |
| `memory/personalities.md` | Owner cognitive profile + collaboration preferences |
| `memory/project-log.md` | Append-only Asked/Decided/Shipped log |

## 3. Pre-completion self-check

1. *"Did this task introduce a rule, fix a non-obvious bug, or set a standard?"* → YES: update bugs/lessons/patterns/decisions.
2. *"Did this reveal an owner preference or trait?"* → YES: update personalities before committing or declaring done.

## 4. Synchronization invariant

{{SYNC_RULE — default for solo devs: single `.agents/` tree in the repo. Multi-checkout setups: define all mirrors here; every memory write syncs to all of them immediately, verified by hash.}}
