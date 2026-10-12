# Workflow: Engineering Health Review

## 1. When used

Periodically - hygiene, coverage, dependencies, security posture, architectural health.

## 2. Relevant agents

`orchestrator` (lead), `codebase-researcher`, `qa-engineer`, `security-reviewer`, `database-engineer`, `memory-manager`

## 3. Execution sequence

1. **Static analysis ... type checks** (`{{TYPE_CHECK}}`) across the tree. 2. **Full test suite** (`{{TEST_COMMAND}}`). 3. **Data-layer health** - migrations apply cleanly, no orphaned constraints. 4. **Debt review** - audit `known-issues.md` for items ready to refactor. 5. **Scorecard** - health metrics, coverage, prioritized maintenance for the owner.
