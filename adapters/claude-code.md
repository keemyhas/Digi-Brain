# Adapter: Claude Code - DRAFT, UNVERIFIED (no cold-boot run on this harness yet)

> Conforms to `ADAPTER-INTERFACE.md` in structure only. Best-effort mapping; delete this
> banner only after the conformance checklist passes on a real Claude Code session.

| Behavior | Claude Code mapping (to verify) |
|---|---|
| Turn-1 identity gate | `AskUserQuestion` tool (options + free text). Gate work on the answer. |
| Working conditions | Turn-1 text header, same format as core. |
| File read / write / edit / search | `Read`, `Write`, `Edit`, `Glob`, `Grep` tools. |
| Command execution | `Bash` tool; verify shell + quoting on first run and record here. |
| Skills invocation | Native skills (`Skill` tool) resolve `SKILLS-MANIFEST.md` rows; missing rows use prose fallback. |
| Task tracking | `TodoWrite` (one `in_progress`, real-time updates). |
| Session bootstrap file | `CLAUDE.md` at repo root pointing at `.agents/memory/brain.md` (verify discovery order vs `AGENTS.md`). |
| Memory sync | Single tree default; mirrors verified by hash. |
| Autonomy + git gates | Refusal in plain text + logged; commit/push only on explicit owner order. |

## Verification debt

- [ ] Cold-boot run on Claude Code (conformance checklist in `ADAPTER-INTERFACE.md`).
- [ ] Confirm `CLAUDE.md` vs `AGENTS.md` precedence for the bootstrap pointer.
