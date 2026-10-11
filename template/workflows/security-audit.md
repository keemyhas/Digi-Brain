# Workflow: Security Audit

## 1. When used

Periodically, before releases, or when touching auth, permissions, encryption, or sensitive-data access.

## 2. Relevant agents

`security-reviewer` (lead), `adversarial-reviewer`, `backend-engineer`, `database-engineer`, `orchestrator`

## 3. Execution sequence

1. **Route authorization scan** — every route/mutation path enforces authentication + least-privilege permission checks; no unguarded endpoints.
2. **Injection check** — zero unparameterized query/command construction across services.
3. **Sensitive-data check** — regulated fields encrypted at rest per `{{DATA_PROTECTION_STANDARD}}`; no plaintext leakage into logs, errors, or responses.
4. **Audit-trail check** — every mutation attributable to actor + session + timestamp.
5. **IDOR & escalation probes** — adversarial cross-tenant/cross-role read/write attempts.
6. **Report** — severity-rated findings with required remediation steps.
