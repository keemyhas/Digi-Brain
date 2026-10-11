# Workflow: Database Change Review

## 1. When used

Any proposed schema change: new tables, altered columns, constraints, or migration scripts.

## 2. Relevant agents

`database-engineer` (lead), `backend-engineer`, `adversarial-reviewer`, `orchestrator`

## 3. Execution sequence

1. **Design review** — names, types, keys, defaults, normalization. 2. **Idempotency & reversibility** — migrations re-runnable without failure; rollback path stated. 3. **Index & plan analysis** — high-traffic columns (e.g. `{{KEY_COLUMNS}}`) indexed; plans checked. 4. **Sensitive-column check** — no computation applied to protected/encoded columns at the storage layer; transform in application space. 5. **Dry run** — migrate a disposable environment, verify schema state, run integration tests. 6. **Memory** — update `database.md` / `api-contracts.md` as needed.
