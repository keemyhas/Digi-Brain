# Adapter: Antigravity - DRAFT, UNVERIFIED (no cold-boot run on this harness yet)

> Conforms to `ADAPTER-INTERFACE.md` in structure only. Every row below is a best-effort
> mapping from the harness's documented behavior. Do not rely on it until the conformance
> checklist passes on a real Antigravity session; when it does, delete this banner.

| Behavior | Antigravity mapping (to verify) |
|---|---|
| Turn-1 identity gate | `ask_question` modal prompt ("Kindly confirm who I am working with"), known contributors as options + write-in. Gate work on the answer. |
| Working conditions | Turn-1 text header, same format as core (`[x]/[ ]` + reasons). |
| File read / write / edit / search | Native file tools (verify names); shell fallback otherwise. |
| Command execution | Shell tool; verify OS/shell + quoting rules on first run and record here. |
| Skills invocation | `SKILLS-MANIFEST.md` rows resolve to native skills where present, else prose fallback. |
| Task tracking | Native tracker if present, else `TASKS.md`-style file. |
| Session bootstrap file | `AGENTS.md` at repo root (verify the harness reads it). |
| Memory sync | Single tree default; mirrors verified by hash. |
| Autonomy + git gates | Refusal in plain text + logged; commit/push only on explicit owner order. |

## Verification debt

- [ ] Cold-boot run on Antigravity (conformance checklist in `ADAPTER-INTERFACE.md`).
- [ ] Confirm bootstrap file discovery + picker availability headless.
