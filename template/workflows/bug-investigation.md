# Workflow: Bug Investigation

## 1. When used

Any unexpected error, wrong computation, UI glitch, or data inconsistency.

## 2. Root-cause principle: 8 questions, no symptom-patching

1. **What failed?** (exact message, code, or broken state)
2. **Where?** (file, function, line, or query)
3. **Why?** (logic error, race, missing null check, unhandled edge)
4. **Why was it possible?** (missing constraint, untyped value, no validation)
5. **Why wasn't it caught?** (missing test, untested path, no assertion)
6. **Does the pattern exist elsewhere?** (scan peer modules/endpoints/forms)
7. **Smallest correct architectural fix?** (root layer, no workarounds)
8. **Which regression test?** (reproduces the bug, pins the fix)

## 3. Relevant agents

`orchestrator`, `codebase-researcher`, `backend-engineer` / `frontend-engineer` / `database-engineer`, `qa-engineer`, `adversarial-reviewer`, `memory-manager`

## 4. Execution sequence

1. Reproduce & isolate (minimal case). 2. Run the 8 questions + peer-pattern search. 3. Fix at the root. 4. Add regression test (`{{TESTS_DIR}}`). 5. Verify (suite + live environment). 6. Record in `bugs.md` + `agent-lessons.md`.
