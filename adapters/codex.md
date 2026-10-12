# Adapter: Codex - DRAFT, UNVERIFIED (no cold-boot run on this harness yet)

> Conforms to `ADAPTER-INTERFACE.md` in structure only. Best-effort mapping; delete this
> banner only after the conformance checklist passes on a real Codex session.

| Behavior | Codex mapping (to verify) |
|---|---|
| Turn-1 identity gate | Interactive prompt for identity confirmation; where the harness is non-interactive, use the documented no-picker fallback (state assumed identity, log it, continue). |
| Working conditions | Turn-1 text header, same format as core. |
| File read / write / edit / search | Native file tools (verify names); shell fallback otherwise. |
| Command execution | Shell tool with the harness's approval policy; record the effective policy here on first run. |
| Skills invocation | `SKILLS-MANIFEST.md` rows resolve to native skills where present, else prose fallback. |
| Task tracking | Native tracker if present, else `TASKS.md`-style file. |
| Session bootstrap file | `AGENTS.md` at repo root (verify discovery). |
| Memory sync | Single tree default; mirrors verified by hash. |
| Autonomy + git gates | Refusal in plain text + logged; commit/push only on explicit owner order. Note: align with the harness's own approval policy - the stricter of the two wins. |

## Verification debt

- [ ] Cold-boot run on Codex (conformance checklist in `ADAPTER-INTERFACE.md`).
- [ ] Record effective approval policy and non-interactive behavior.
