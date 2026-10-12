# Adapter: Codex CLI - Draft (Unverified Locally)

> Conforms to `ADAPTER-INTERFACE.md` in structure. Best-effort mapping; delete this
> banner only after the cold-boot conformance checklist passes on a live Codex CLI session.

| Behavior | Codex mapping |
|---|---|
| Installation method | `powershell -File installer/install.ps1 -Defaults` or `bash installer/install.sh --defaults` |
| Session bootstrap file | `AGENTS.md` at repo root pointing at `.agents/memory/brain.md` |
| Turn-1 identity gate | Interactive prompt for identity confirmation; in non-interactive mode, use no-picker fallback (state assumed identity, log it, continue). |
| Working conditions | Turn-1 text header, same format as core (`[x]/[ ]` + reasons). |
| Staged context retrieval | Supported via `python tools/retrieval_router.py` or selective reading. |
| File read / write / edit / search | Native file tools or shell fallback. |
| Command execution | Shell tool with the harness approval policy (`--approval-policy`). |
| Skills invocation | Native skills or prose fallback based on `SKILLS-MANIFEST.md`. |
| Task tracking | Native tracker or `TASKS.md` / `tools/task_state.py`. |
| Memory sync | Single tree default; mirrors verified by hash. |
| Autonomy + git gates | Refusal in plain text + logged; commit/push only on explicit owner order. Note: stricter of harness policy and Digi-Brain policy wins. |
| Layer C technical enforcement level | **Variable**: Low under `--full-auto`, High under `--manual-approval`. |
| Verification status | **Draft / Unverified Locally** |

## Verification debt

- [ ] Cold-boot run on Codex (conformance checklist in `ADAPTER-INTERFACE.md`).
- [ ] Record effective approval policy and non-interactive behavior.
