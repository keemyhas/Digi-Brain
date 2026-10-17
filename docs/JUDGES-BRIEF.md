# Digi-Brain Judge's Brief (10-Minute Reading Path)

Deliberately short. This repo rewards the judge who reads, then verifies. The full spec chain lives in `docs/ARCHITECTURE.md`; this page only tells you what to look at and why it matters for a hackathon verdict.

## The Thesis

AI coding agents are powerful but amnesiac and unsupervised: they forget decisions between sessions, re-litigate settled issues, and can silently execute irreversible actions. Digi-Brain's proposal: persistent operating memory with a separation of authority — what the agent *believes* (memory) is structurally distinct from what it is *allowed to do* (policy) and from what *technically blocks misuse* (enforcement).

## The Three Layers (read it once, judge it forever)

```
Layer C  Enforcement   tools/policy_engine.py, harness permission gates
        ^ evaluates & gates
Layer B  Policy        rules/policy-enforcement.md — 6-state machine, single-use grants
        ^ guides & informs
Layer A  Memory        memory/ — provenance-tagged, append-only, anatomy-routed
```

Design guarantee: no amount of memory content can ever authorize a sensitive action. Git commit/push/rebase/destructive ops are *never* autonomous — each needs a fresh, single-use human grant.

## What Was Engineered, Not Prompted

- **Installer hardening**: the shell/PowerShell installer is eval-free, whitelist-gated (43 keys), stages before committing, rolls back atomically on verification failure, and runs a 6-check verification (structure, bootstrap, safety, placeholders, fingerprints, secrets). REPL's baseline audit (`docs/BASELINE-REPORT.md`) documents the pre-hardening defects, including a critical `eval` injection, and `docs/SECURITY-REPORT.md` the afterward.
- **Memory integrity**: provenance headers (SourceClass, Confidence, Status), append-only project log, supersession chains that never erase — poison-document detection heuristics included.
- **Cognition tools**: 4-stage retrieval router (50.6% token reduction, recall 1.0), task-state continuity across session resets, persona divergence exporter with heuristics-based secret quarantine.

## Evidence You Can Run Yourself

| Command | What it proves |
|---|---|
| `python tests/run_tests.py` | 35 deterministic security/reliability/cognition tests, all passing |
| `./installer/install.sh /tmp/x --defaults --verify-only` | install + verify in ~1s, 6 checks pass |
| `python benchmarks/run_benchmark.py` | controlled 10-scenario comparison: Digi-Brain 100% vs no-memory 80% vs minimal-rules 90% completion |
| `grep -c "eval" installer/install.sh` | 0 — the injection vector is structurally gone |

## Honest Limitations

Stateful "enforcement" is tooling-level: `policy_engine.py` blocks at the tool/gate layer where a harness permits (Layer C), while Layer B policy is behavioral contract where a harness has no hook surface (documented in `template/rules/policy-enforcement.md`, not overstated).

## Structure Map (what's where)

- `installer/` — hardened cross-platform installers + templates
- `template/` — the brain: memory rules, policies, agents, workflows
- `tools/` — policy engine, memory guard, retrieval router, task state, exporters
- `tests/` — 35-test suite (pass 1 security, pass 2 cognition)
- `benchmarks/` — comparative evaluation harness + scenarios
- `docs/` — architecture, baseline audit, security report, benchmark spec, final summary

## Build Identity

Created by a medical doctor who is a part-time developer. MIT-licensed. Zero telemetry.
