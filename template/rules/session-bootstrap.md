# Session Bootstrapping Protocol

> Setup: replace `{{PLACEHOLDERS}}`, wire the turn-1 prompt to your harness's picker, then delete this line.

## 1. Mandatory first-turn working conditions

On the first turn of every session, display before or alongside the response:

```text
Working Conditions: [✓] bugs recording | [✓] code-graph | [✓] personalities | [✓] memory sync
```

Mark `[ ]` with a one-line reason for anything missing or disabled.

## 2. Identity confirmation (mandatory turn-1 gate)

Ask *"Kindly confirm who I am working with"* via the harness picker **before any research, reads, or edits** — even if identity is inferable from history. Execution is gated on the answer.

- Offer known contributors (e.g. `{{OWNER_NAME}} ({{OWNER_ROLE}})`) plus a free-text option.
- Attribute all subsequently recorded traits/decisions to the confirmed identity in `memory/personalities.md`.
- If a new contributor appears, create their profile section before proceeding.

## 3. Memory auto-initialization

1. Read `memory/brain.md` (router), `memory/personalities.md`, last 3 `project-log.md` entries, `memory/roadmap.md` §0.
2. If a code-graph tool is configured and its index exists, refresh it so it reflects the latest tree.
3. Code-graph first for codebase structure/relationship questions.
