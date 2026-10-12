# Adapter: Claude Code - Draft (Unverified Locally)

> Conforms to `ADAPTER-INTERFACE.md` in structure. Best-effort mapping; delete this
> banner only after the cold-boot conformance checklist passes on a live Claude Code instance.

| Behavior | Claude Code mapping |
|---|---|
| Installation method | `bash installer/install.sh --defaults` or manual clone |
| Session bootstrap file | `CLAUDE.md` at repo root pointing at `.agents/memory/brain.md` (takes precedence over `AGENTS.md`) |
| Turn-1 identity gate | `AskUserQuestion` tool (options + free text). Gate work on the answer. |
| Working conditions | Turn-1 text header, same format as core (`[x]/[ ]` + reasons). |
| Staged context retrieval | Supported via `python tools/retrieval_router.py` or selective reading. |
| File read / write / edit / search | `Read`, `Write`, `Edit`, `Glob`, `Grep` tools. |
| Command execution | `Bash` tool with harness approval prompts. |
| Skills invocation | Native skills (`Skill` tool) resolve `SKILLS-MANIFEST.md` rows; missing rows use prose fallback. |
| Task tracking | `TodoWrite` (one `in_progress`, real-time updates) + `tools/task_state.py`. |
| Memory sync | Single tree default; mirrors verified by hash. |
| Autonomy + git gates | Refusal in plain text + logged; commit/push only on explicit owner order. Evaluated via `tools/policy_engine.py`. |
| Layer C technical enforcement level | **Medium**: Interactive approval prompts required before dangerous bash executions (e.g. `git push`). |
| Verification status | **Draft / Unverified Locally** |

## Verification debt

- [ ] Cold-boot run on Claude Code (conformance checklist in `ADAPTER-INTERFACE.md`).
- [ ] Confirm `CLAUDE.md` discovery order vs `AGENTS.md`.
