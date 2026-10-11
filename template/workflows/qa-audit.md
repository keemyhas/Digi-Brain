# Workflow: QA Audit

## 1. When used

Comprehensive quality audits — before major releases, after large cross-cutting changes, or for end-to-end validation. This is an AUDIT: it discovers, reproduces, classifies, and plans remediation. It does NOT modify source, schema, config, or production data.

## 2. Relevant agents

- `orchestrator` (lead — coverage matrix, dedup, final report)
- `codebase-researcher` (read-only recon: routes, roles, schema, views)
- `browser-tester` (persona execution: {{OWNER_PERSONAS}}, incl. mobile/responsive)
- `security-reviewer` (authz/IDOR/escalation)
- `adversarial-reviewer` (negative testing, races, boundaries, malicious inputs)
- `{{DOMAIN_REVIEWER}}` (owner-defined invariant gates, if any)
- `database-engineer` (read-only integrity analysis)
- `qa-engineer` (runs existing suites; post-approval regression tests)

## 3. Workspace

All artifacts under `{{QA_DIR}}` (default `.qa/`): test plan, coverage matrix, shared fixtures, `findings/P0..P4/`, final report, remediation plan. Persona briefs live there — NOT as new agent definitions.

## 4. Execution sequence

1. **Recon** — map modules, roles, routes, schema, tests, seeds, regression watchlist. 2. **Environment** — app boots against disposable test data; never production. 3. **Persona delegation** — isolated briefs; shared fixtures registered centrally so runs don't invalidate each other. 4. **Verify** — every defect reproduced twice with expected-vs-actual from code/docs; non-reproducible ⇒ UNCONFIRMED. 5. **Consolidate** — dedup, severity P0–P4, coverage matrix. 6. **Report** — final report, Top-N list, quick wins, systemic issues, release recommendation. 7. **Remediation plan** (planning only) — group by root cause, sequence, then STOP for explicit owner approval.

## 5. Safety invariants

No destructive/load attacks on shared systems; fixtures namespaced (`{{FIXTURE_PREFIX}}`); no real user data; no secrets committed; negative tests must not destroy data; a hidden button is NOT security — verify server-side authorization.
