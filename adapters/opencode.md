# Adapter: OpenCode (Dev Harness - Verified)

> Conforms to `ADAPTER-INTERFACE.md`. Verified by cold-boot proxy test and test suite.

| Behavior | OpenCode mapping |
|---|---|
| Installation method | `powershell -File installer/install.ps1 -Defaults` or `bash installer/install.sh --defaults` |
| Session bootstrap file | `AGENTS.md` at repo root pointing at `.agents/memory/brain.md` |
| Turn-1 identity gate | `question` tool: single question, known contributors as options, free-text enabled. Asked before any research/reads/edits. |
| Working conditions | Plain-text header on turn 1: `[[x]] bugs recording | [[x]] code-graph | [[x]] personalities | [[x]] memory sync`, `[ ]` + reason when missing. |
| Staged context retrieval | Supported via `python tools/retrieval_router.py --stage <boot|task|verification|consolidation>`. |
| File read / write / edit / search | `read`, `write`, `edit` (exact-string replace), `glob`, `grep` tools. Absolute paths. |
| Command execution | `bash` tool (Windows PowerShell 5.1 - `; if ($?)` chaining, quoted paths, `workdir` param instead of `cd`). |
| Skills invocation | `skill` tool by name; `SKILLS-MANIFEST.md` rows map 1:1 to native skills. Missing => prose fallback. |
| Task tracking | `todowrite` tool (exactly one `in_progress`; real-time updates) + `tools/task_state.py`. |
| Memory sync | Single tree default; multi-mirror setups verified by file hash comparison. |
| Autonomy + git gates | Refusal stated in plain text + logged; `git commit`/`push` only on explicit owner order. Evaluated via `tools/policy_engine.py`. |
| Layer C technical enforcement level | **Low**: Harness provides raw command execution without tool denial. Enforcement relies on Layer B policy compliance and pre-execution checks. |
| Verification status | **Verified** |

## Known harness constraints (shape adapter behavior)

- No interactive terminal prompts in tool-executed shells (non-interactive): installer-style CLIs must offer `--defaults` / `--answers-file` equivalents.
- Scripts should stay pure-ASCII: PS 5.1 tooling misparses multibyte punctuation in `.ps1` files.
- Subagents (`task` tool) start with fresh context: usable as cold-boot proxies, but report them as proxies, never as independent-machine proof.
