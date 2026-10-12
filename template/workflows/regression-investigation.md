# Workflow: Regression Investigation

## 1. When used

Previously working behavior breaks after a commit, migration, or dependency upgrade.

## 2. Relevant agents

`orchestrator`, `codebase-researcher`, `qa-engineer`, `adversarial-reviewer`, `backend-engineer` / `frontend-engineer`

## 3. Execution sequence

1. **History ... diff analysis** - trace recent commits/changes touching the broken subsystem. 2. **Blast-radius map** - shared models, schema changes, middleware edits. 3. **Regression test** - automated test reproducing the failure. 4. **Fix** - architectural fix at the root, without rolling back unrelated new behavior. 5. **Full verification** - suite + live environment. 6. **Memory** - log the regression mechanism in `agent-lessons.md`.
