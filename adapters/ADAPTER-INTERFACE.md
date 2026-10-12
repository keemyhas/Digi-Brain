# Adapter Interface - what "supports Digi Brain" means for any harness

> A harness adapter is a MAPPING document, not code. It states how each harness-touching
> behavior in the core template executes on that harness. If a behavior has no equivalent,
> the adapter declares the prose fallback - gates never silently skip.

## Required mappings (every adapter documents all rows)

| Behavior (core reference) | Adapter must state |
|---|---|
| Installation method | How Digi-Brain is deployed (`install.sh`, `install.ps1`, or harness plugin) |
| Session bootstrap file | Where the "read brain first" pointer lives (`AGENTS.md`, `CLAUDE.md`, ...) |
| Turn-1 identity gate (`rules/session-bootstrap.md` sec 2) | Exact picker mechanism + the question text + free-text option |
| Working-conditions display (bootstrap sec 1) | Where it renders (turn-1 header) + `[ ]` fallback wording |
| Staged context retrieval (`rules/session-bootstrap.md` sec 3) | How Stages 1 to 4 are loaded (`tools/retrieval_router.py` or selective file reading) |
| File read / write / edit / search | Tool or command equivalents (incl. shell fallback) |
| Command execution | Shell + quoting rules (spaces in paths, chaining) |
| Skills invocation | How `SKILLS-MANIFEST.md` rows resolve (native skill name or `none - prose fallback`) |
| Task tracking | Todo-list mechanism (native or `TASKS.md`-style file / `task-state.json`) |
| Memory sync | How multi-mirror sync is verified (default: single tree, no-op) |
| Autonomy + git gates (`brain.md` sec 6, `rules/policy-enforcement.md`) | How refusal is expressed; commit/push always need explicit owner order |
| Layer C technical enforcement level | Harness capabilities: sandbox, tool whitelisting, approval prompts, or none |
| Verification status | Verified, Experimental, or Draft |
| Known harness constraints | Specific limitations shaping adapter behavior |

## Conformance checklist (cold-boot must prove)

- [ ] Turn-1 gate fires unprompted in a fresh session.
- [ ] Orientation reads complete; first log entry appended.
- [ ] Activation phrase -> twin declaration + pick-flagging in the log.
- [ ] Unprompted commit/push refused and logged.
- [ ] At least one skill-fallback path exercised (proves gates hold without skills).
- [ ] Staged context retrieval loads Boot Context without full-brain dump.

## Fallback law

Missing capability => named prose fallback + extra owner scrutiny. Never silent skipping, never gate removal.
