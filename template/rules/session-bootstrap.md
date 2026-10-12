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
## 4. Staged Retrieval Architecture

To prevent context bloat and hallucination, retrieval executes in four structured stages:

1. **Stage 1 (Boot Context)**:
   - Identity confirmation, safety invariants, working conditions, active project layout.
   - Files: `rules/session-bootstrap.md`, `rules/engineering-standards.md`, `rules/policy-enforcement.md`.
2. **Stage 2 (Task Context)**:
   - Scoped retrieval of relevant architectural decisions and lessons matching the current task.
   - Avoids dumping entire historical logs into turn-1 context.
   - Files: relevant entries from `memory/decisions.md`, `memory/agent-lessons.md`, `memory/patterns.md`.
3. **Stage 3 (Verification Context)**:
   - Test suites, verification commands, and acceptance criteria relevant to the task domain.
   - Files: `BOOT-CHECKLIST.md`, test command configs, domain verification scripts.
4. **Stage 4 (Memory Consolidation)**:
   - At task completion, distill durable lessons or decisions into memory.
   - Never copy entire transcripts or conversational chatter into permanent files.

## 5. Session Task-State Continuity

On session start, check for active or interrupted work:
1. Read `memory/task-state.json` (managed by `tools/task_state.py`) or the last entry of `memory/project-log.md`.
2. Determine:
   - What task was in progress?
   - What steps were verified as complete?
   - What steps remain?
   - What tests ran and which failed?
   - What actions require human authorization before proceeding?
3. Never mark incomplete tasks as finished merely because an earlier session attempted them.
