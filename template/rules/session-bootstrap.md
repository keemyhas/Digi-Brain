# Session Bootstrapping Protocol

> Setup: fill every double-brace token, wire the turn-1 prompt to your harness's picker, then delete this line.

## 1. Mandatory first-turn working conditions

On the first turn of every session, display before or alongside the response:

```text
Working Conditions: [x] bugs recording | [x] code-graph | [x] personalities | [x] memory sync
```

Mark `[ ]` with a one-line reason for anything missing or disabled.

## 2. Identity confirmation (mandatory turn-1 gate)

Ask *"Kindly confirm who I am working with"* via the harness picker **before any research, reads, or edits** - even if identity is inferable from history. Execution is gated on the answer.

- Offer known contributors (e.g. `{{OWNER_NAME}} ({{OWNER_ROLE}})`) plus a free-text option.
- Attribute all subsequently recorded traits/decisions to the confirmed identity in `memory/personalities.md`.
- If a new contributor appears, create their profile section before proceeding.
- No-picker fallback (headless/CLI harnesses): when no interactive picker exists, state the assumed identity in plain text (e.g. "Proceeding as {{OWNER_NAME}} - no picker available"), log the assumption in the session's first log entry, and continue. Never deadlock waiting for a picker that cannot appear.

## 3. Memory auto-initialization

1. Read `memory/brain.md` (router), `memory/personalities.md`, last 3 `project-log.md` entries, `memory/roadmap.md` section 0.
2. If a code-graph tool is configured and its index exists, refresh it so it reflects the latest tree.
3. Code-graph first for codebase structure/relationship questions.
