# Architectural Decisions Record

> Setup: no placeholders. New decisions append here (or `{{ADR_DIR}}`); the project log links them. Read this before revisiting any architectural choice.

## ADR-001: {Title}

- **Context**: {what forced the decision}
- **Decision**: {what we chose}
- **Status**: {Proposed | Accepted | Deprecated | Superseded by ADR-XXX}
- **Consequences**: {what this obliges future work to do / not do}

---

## EXAMPLE - DELETE (unnumbered on purpose - never copy the ADR-001 above)

### Domain folders for backend modules (Ada Example)

- **Context**: Route handlers were sprawling across a single file as features grew.
- **Decision**: Organize backend code under `src/domains/<domain>/` with routes + service per domain.
- **Status**: Accepted.
- **Consequences**: New features live inside a domain folder, never in global route files.
