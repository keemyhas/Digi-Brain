# Skills Manifest - which skills each gate expects

> Digi Brain ships NO skill pack. Skills live in the owner's harness (OpenCode, Claude Code, ...).
> This manifest is the contract: each gate names the skill it expects, the harness provides an
> equivalent. If a skill is missing, the gate still runs - with extra owner scrutiny, not skipped.

## Gate -> skill mapping

| Gate (where) | Expected skill | Covers | If missing |
|---|---|---|---|
| New project/feature, ambiguous requirements (`brain.md` section 1) | `spec-driven-development` | Spec before code; assumptions surfaced | Owner answers a written Q...A before build starts |
| Plan execution & checklist (`workflows/plan-execution.md`) | `planning-and-task-breakdown`, `verification-loop` | Real-time execution tracking, phase-by-phase proof | Manual `execution_checklist.md` with status indicators |
| Multi-file build (`workflows/feature-development.md`) | `incremental-implementation`, `test-driven-development` | Thin vertical slices; red-green-refactor | Smaller slices + mandatory live verification per slice |
| Bug fix (`workflows/bug-investigation.md`) | `debugging-and-error-recovery`, `test-driven-development` | 8-question RCA; regression test pins fix | 8 questions answered in prose in `bugs.md` entry |
| Adversarial pass (`agents/adversarial-reviewer.md`) | `doubt-driven-development` | Fresh-context challenge of decisions | Second-pass review by a different agent/persona |
| API/module boundaries (`agents/backend-engineer.md`) | `api-and-interface-design` | Stable contracts at module edges | Contract written in `decisions.md` before code |
| UI work (`agents/frontend-engineer.md`) | `frontend-ui-engineering` | Accessible, responsive, production-grade UI | Manual viewport + keyboard sweep checklist |
| Schema changes (`workflows/database-change-review.md`) | `database-review` | Migration safety, index/plan checks | Dry-run + owner sign-off mandatory |
| Security gates (`workflows/security-audit.md`) | `security-review`, `security-and-hardening` | AuthZ, injection, leakage, hardening | Full checklist run in prose, owner reviews |
| Shipping (`workflows/qa-audit.md` section 6-7) | `shipping-and-launch` | Release readiness, rollout, rollback | Written readiness statement + rollback note |
| Perf-sensitive changes | `performance-optimization` | Budgets, profiling, N+1 elimination | State the budget + measured result in the log |
| Release hygiene (any gate) | `code-review-and-quality`, `code-simplification` | Multi-axis review; clarity without behavior change | Owner reads the full diff before merge |
| Test planning (`agents/qa-engineer.md`) | `testing-strategy` | Levels, coverage, isolation | Per-task verify steps |
| Breaking changes | `deprecation-and-migration` | Expand/contract, no flag-days | Owner-approved migration note required |
| Decisions with lasting weight | `documentation-and-adrs` | ADRs that future readers can trust | Decision recorded in `decisions.md` regardless |
| Stuck / unfamiliar territory | `context-engineering` | Right context, right size, per step | Narrower task slices until unstuck |

## Owner setup (one-time, Phase 2 installer step)

1. Map each row to the harness's closest native skill (or `none - prose fallback`).
2. Record the mapping in the installed repo (e.g. `.agents/skills-map.md`).
3. Cold-boot test must exercise at least one fallback path to prove gates hold without skills (the generated `skills-map.md` starts all-prose-fallback and orders the exercise).
