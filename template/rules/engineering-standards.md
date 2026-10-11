# Operational Engineering Standards

> Setup: fill `{{PLACEHOLDERS}}` (test command, migration path, safety paths), then delete this line.

## 1. Test isolation & data protection

- Tests NEVER run against live or shared-dev data. Use `{{TEST_COMMAND}}` targeting disposable fixtures/databases.
- Tests create their own fixtures and clean them up deterministically. Never latch onto arbitrary existing records.

## 2. Zero-tolerance for unreviewed destructive ops

- No destructive schema/data operations in request-handling code paths. All structural changes ship as reviewed migration scripts under `{{MIGRATIONS_DIR}}` with rollback notes.
- Fresh-install parity: every structural change must also apply cleanly to a brand-new setup (migration + base schema stay in sync).

## 3. No silent failures on user-initiated actions

- Every user-facing failure surfaces action + reason + next step in the UI. Log-only catches on user paths are defects.
- Background pollers/prefetchers are the exception: fail silent, back off on repeated denials, never fabricate audit noise.

## 4. Documentation bar for onboarding

- Every source file: header (purpose, module, used-by, dependencies).
- Every exported function/type/schema: purpose, params, returns, side effects.
- Non-obvious logic: inline WHY comments (what failure mode is prevented), never code restatements.
- No dead code, no stale comments, no commented-out blocks.

## 5. Safety invariants (owner-defined, highest precedence after explicit orders)

{{SAFETY_INVARIANTS — e.g. paths that must never be blocked, data with legal/archival sanctity, forbidden operations. If none, write "None defined — add before enabling autonomous mode."}}
