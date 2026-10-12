# Engineering Lessons & Durable Knowledge
<!-- APPEND-ONLY: new entries go at the bottom. Never edit past entries. Enforced by rules/project-logging.md and tools/memory_guard.py -->

> Setup: no placeholders. Numbered, append-only in spirit (never rewrite a lesson - supersede with a new entry). Seed below with the starter set; add yours as they are earned.

### [LES-001] Respect the blast radius
- **Type**: Procedural
- **SourceClass**: ExplicitUser
- **Status**: Current
- **Scope**: universal
- **Confidence**: verified
- **CreatedAt**: 2026-10-11
- **Observation**: Every fix gets a neighbor audit: if an anti-pattern bit once, search all sibling implementations before declaring done.

### [LES-002] Never patch symptoms
- **Type**: Procedural
- **SourceClass**: ExplicitUser
- **Status**: Current
- **Scope**: universal
- **Confidence**: verified
- **CreatedAt**: 2026-10-11
- **Observation**: Diagnose root cause, record why it was possible, and check whether the same class exists in other domains.

### [LES-003] No autonomous git writes
- **Type**: Procedural
- **SourceClass**: ExplicitUser
- **Status**: Current
- **Scope**: universal
- **Confidence**: verified
- **CreatedAt**: 2026-10-11
- **Observation**: Never `git commit` or `git push` unless the owner explicitly orders it. Prepare locally; wait for the order.

### [LES-004] Tests must never touch live data
- **Type**: Procedural
- **SourceClass**: ExplicitUser
- **Status**: Current
- **Scope**: universal
- **Confidence**: verified
- **CreatedAt**: 2026-10-11
- **Observation**: Disposable fixtures/databases only, created and destroyed deterministically by the test run.

### [LES-005] Verify in the running system
- **Type**: Procedural
- **SourceClass**: ExplicitUser
- **Status**: Current
- **Scope**: universal
- **Confidence**: verified
- **CreatedAt**: 2026-10-11
- **Observation**: "Implemented" means observed working in the live environment, not merely edited in source.
