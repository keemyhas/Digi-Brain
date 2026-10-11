# Adapter Interface - what "supports Digi Brain" means for any harness

> A harness adapter is a MAPPING document, not code. It states how each harness-touching
> behavior in the core template executes on that harness. If a behavior has no equivalent,
> the adapter declares the prose fallback - gates never silently skip.

## Required mappings (every adapter documents all rows)

| Behavior (core reference) | Adapter must state |
|---|---|
| Turn-1 identity gate (`rules/session-bootstrap.md` section 2) | Exact picker mechanism + the question text + free-text option |
| Working-conditions display (bootstrap section 1) | Where it renders (turn-1 header) + `[ ]` fallback wording |
| File read / write / edit / search | Tool or command equivalents (incl. shell fallback) |
| Command execution | Shell + quoting rules (spaces in paths, chaining) |
| Skills invocation | How `SKILLS-MANIFEST.md` rows resolve (native skill name or `none - prose fallback`) |
| Task tracking | Todo-list mechanism (native or `TASKS.md`-style file) |
| Session bootstrap file | Where the "read brain first" pointer lives (`AGENTS.md`, `CLAUDE.md`, ...) |
| Memory sync | How multi-mirror sync is verified (default: single tree, no-op) |
| Autonomy + git gates (`brain.md` section 6) | How refusal is expressed; commit/push always need explicit owner order |

## Conformance checklist (cold-boot must prove)

- [ ] Turn-1 gate fires unprompted in a fresh session.
- [ ] Orientation reads complete; first log entry appended.
- [ ] Activation phrase -> twin declaration + pick-flagging in the log.
- [ ] Unprompted commit/push refused and logged.
- [ ] At least one skill-fallback path exercised (proves gates hold without skills).

## Fallback law

Missing capability => named prose fallback + extra owner scrutiny. Never silent skipping, never gate removal.
