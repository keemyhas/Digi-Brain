# Code Commenting, Documentation ... Onboarding Protocol

> Setup: fill every double-brace token, adapt Tier 1-2 snippets to your language, then delete this line.

## 1. Core principle: the future-developer invariant

> Code is read ten times more often than it is written. Every line must be self-explanatory to a developer or agent who joins months later without the original author present.

Whenever code is created, edited, refactored, or fixed:
1. **Zero undocumented slices**: no function, class, route, validator, or non-trivial block ships without comments and documentation.
2. **Synchronized documentation**: changing behavior without updating its docs (`{{DOCS_DIR}}`, ADRs, `.agents/memory/`) is an incomplete task.
3. **Write for the onboarding engineer**: comments explain domain context and *why* the code exists, what edge cases it prevents, and how to modify it safely.

## 2. Three required tiers

### Tier 1: File header (mandatory on all source files)

```text
Purpose: What this file does and its role in the system.
Module: Exact subsystem path.
Used By: Key consumers that depend on this file.
Dependencies: Libraries, helpers, or connections imported.
Domain Context: How this code affects {{OWNER_DOMAIN}} or data governance (where applicable).
```

### Tier 2: Function/export docs (mandatory on all exports)

Document purpose, params (ranges/constraints), returns (success vs failure), thrown errors, side effects (or 'None'), and security implications (access controls, sanitization).

### Tier 3: Inline WHY comments (mandatory on complex logic)

- Explain WHY, never restate code. Bad: `// increment counter`. Good: why the counter exists and what rule necessitates it.
- Document edge cases and defensive decisions (fallbacks, null-checks, platform-quirk workarounds) with the reason.
- Document rejected alternatives when the intuitive approach hides a failure mode.

## 3. Docs actions per change type

| What changed | Required action |
|---|---|
| New file | Tier 1 + 2 + 3, update docs index / barrel export |
| Function modified | Update docs/params/comments - never leave stale comments |
| Bug fixed | Inline root-cause comment + post-mortem in `bugs.md` + `agent-lessons.md` |
| Architectural decision | ADR in `{{ADR_DIR}}` + summary in `decisions.md` |
| Endpoint added/updated | Update `{{API_DOCS}}` |
| Schema changed | Document upgrade migration AND base schema (fresh-install parity) |
| UI modified | Update design docs + `patterns.md` |

## 4. Prohibited (zero-tolerance)

1. Undocumented PRs - green tests do not excuse missing docs.
2. Commented-out dead code - delete it; git keeps history.
3. Stale TODOs - implement now or track as a formal roadmap task.
4. Obsolete comments contradicting the code beneath - worse than no comment.
