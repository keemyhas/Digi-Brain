# Adapter: Claude Code - Verified (Native Workspace Support)

> Conforms to `ADAPTER-INTERFACE.md`. Verified in native Claude Code CLI execution environments.

| Behavior | Claude Code mapping |
|---|---|
| Installation method | `powershell -File installer/install.ps1 -Target <repo> -Defaults` or `bash installer/install.sh <repo> --defaults` |
| Customization discovery | Automatic bootstrap discovery via root `CLAUDE.md` and `AGENTS.md` pointing to `.agents/memory/brain.md` and `.agents/rules/session-bootstrap.md`. |
| Session bootstrap file | `CLAUDE.md` at repo root (auto-created on fresh install; takes precedence in Claude Code over `AGENTS.md`). |
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
| Verification status | **Verified (Native Claude Code Support)** |

## Fresh Install Behavior in Claude Code

1. When installed into a target repo, Digi-Brain populates `<workspace>/.agents/` and creates root bootstrap pointers `CLAUDE.md` and `AGENTS.md`.
2. Claude Code CLI automatically discovers `CLAUDE.md` upon session startup, loading project instructions and the pointer to `.agents/rules/session-bootstrap.md`.
3. On Turn 1, the agent reads `session-bootstrap.md`, outputs the working conditions header, and calls `AskUserQuestion` (or equivalent interactive prompt) to confirm developer identity before executing tasks.

## Verification Checklist

- [x] Cold-boot run on Claude Code (conformance checklist in `ADAPTER-INTERFACE.md`).
- [x] Confirm `CLAUDE.md` discovery order vs `AGENTS.md`.
