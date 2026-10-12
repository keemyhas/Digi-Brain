# Workflow: Feature Development

## 1. When used

Adding new modules, endpoints, views, dialogs, or multi-step user flows. Default workflow for multi-file work.

## 2. Relevant agents

- `orchestrator` (lead), `codebase-researcher`, `backend-engineer`, `frontend-engineer`, `database-engineer`, domain safety reviewer ({{DOMAIN_REVIEWER}}), `security-reviewer`, `qa-engineer`, `browser-tester`, `memory-manager`

## 3. Execution sequence

1. Requirement discovery -> 2. Codebase ... schema research -> 3. Implementation plan ... data design -> 4. Safety ... security pre-review -> 5. Backend ... data implementation -> 6. Frontend ... UI implementation -> 7. Automated tests ... type checks (`{{TYPE_CHECK}}`, `{{TEST_COMMAND}}`) -> 8. Live-environment verification -> 9. Adversarial ... regression review -> 10. Memory update ... final report.

## 4. Gates

1. Type checks and test suite pass.
2. Domain/safety reviewer (if configured) confirms no invariant violations.
3. Security reviewer verifies authz on new routes + parameterized queries.
4. Browser tester confirms interactive flows.
5. Durable lessons appended to `memory/agent-lessons.md`.
