# Adapter: Google Antigravity - Verified (Native Workspace Support)

> Conforms to `ADAPTER-INTERFACE.md`. Verified in native Antigravity IDE and AGY CLI execution environments.

| Behavior | Antigravity mapping |
|---|---|
| Installation method | `powershell -File installer/install.ps1 -Target <repo> -Defaults` or `bash installer/install.sh <repo> --defaults` |
| Customization discovery | Automatic native discovery via `.agents` Workspace Customizations Root; loads `.agents/rules/*.md` automatically on session start. |
| Session bootstrap file | `AGENTS.md` at repo root (auto-created on fresh install) + `.agents/rules/session-bootstrap.md`. |
| Turn-1 identity gate | Native `ask_question` tool modal ("Kindly confirm who I am working with"), known contributors as options + write-in. Gate work on the answer. |
| Working conditions | Turn-1 text header, same format as core (`[x]/[ ]` + reasons). |
| Staged context retrieval | Supported via `python tools/retrieval_router.py` or selective reading of `.agents/memory/brain.md` & `decisions.md`. |
| File read / write / edit / search | `view_file`, `write_to_file`, `replace_file_content`, `grep_search`, `list_dir`. Forward-slash paths. |
| Command execution | `run_command` (powershell on Windows, bash on Linux/macOS). Never propose `cd`. |
| Skills invocation | Native AGY skills in `SKILLS-MANIFEST.md` resolve to native skill folders; missing rows use prose fallback. |
| Task tracking | Native task tracking, artifacts, or `tools/task_state.py`. |
| Memory sync | Single tree default; mirrors verified by hash. |
| Autonomy + git gates | Refusal in plain text + logged; commit/push only on explicit owner order. `tools/policy_engine.py` evaluated before state escalation. |
| Layer C technical enforcement level | **Medium**: Host provides tool permission dialogs, tool whitelisting, and subagent isolation boundaries. Shell commands are visible to user. |
| Verification status | **Verified (Native Antigravity Workspace Support)** |

## Fresh Install Behavior in Antigravity

1. When installed into a foreign repo, Digi-Brain populates `<workspace>/.agents/` and creates `<workspace>/AGENTS.md`.
2. Antigravity IDE automatically recognizes `.agents` as the active workspace customization root, loading all markdown rules in `.agents/rules/` without requiring manual config files.
3. On Turn 1, the agent reads `session-bootstrap.md`, presents the working conditions header, and calls the interactive `ask_question` modal before touching any code.

## Known harness constraints

- Non-interactive subagent execution: all CLI tools must support non-interactive flags (`-Defaults`, `--defaults`, `--answers-file`).
- Tool execution outside active workspace may trigger IDE system policy restrictions; run tools with repository root Cwd.
