# Architectural Decisions Record
<!-- APPEND-ONLY: new entries go at the bottom. Never edit past entries. Enforced by rules/project-logging.md and tools/memory_guard.py -->

> Setup: no placeholders. New decisions append here (or `{{ADR_DIR}}`); the project log links them. Read this before revisiting any architectural choice.

### [ADR-001] {Title}
- **Type**: Semantic
- **SourceClass**: ExplicitUser
- **Status**: Proposed
- **Scope**: project
- **Confidence**: verified
- **CreatedAt**: YYYY-MM-DD
- **Supersedes**: none

- **Context**: {what forced the decision}
- **Decision**: {what we chose}
- **Consequences**: {what this obliges future work to do / not do}
- **Verification Evidence**: {how compliance was proved}

---

## Historical Examples (Preserved Append-Only)

### [ADR-000] Domain folders for backend modules (Ada Example)
- **Type**: Semantic
- **SourceClass**: ExplicitUser
- **Status**: Accepted
- **Scope**: project
- **Confidence**: verified
- **CreatedAt**: 2026-10-11
- **Supersedes**: none

- **Context**: Route handlers were sprawling across a single file as features grew.
- **Decision**: Organize backend code under `src/domains/<domain>/` with routes + service per domain.
- **Consequences**: New features live inside a domain folder, never in global route files.
