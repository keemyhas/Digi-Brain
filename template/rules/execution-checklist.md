# Plan Execution & Concurrent Checklist Protocol

> Setup: no placeholders. Enforce across all agentic execution loops.

## 1. Core Principle

> **Never execute an approved multi-step plan blindly.**
> An agent executing a multi-phase task must maintain continuous, transparent, real-time accountability through an active `execution_checklist.md`.

## 2. Trigger Conditions

An active checklist is **mandatory** whenever:
1. The user approves an implementation plan or PRD (e.g., clicking "Proceed", saying "proceed with plan", or "/orch-execute").
2. A task touches multiple subsystems (database, backend, frontend, tests).
3. The Operative Twin (`{{TWIN_NAME}}`) is executing an autonomous multi-step workflow.

## 3. Checklist Location & Lifecycle

1. **Pre-Flight Creation**: The agent must initialize `execution_checklist.md` in the IDE's artifact directory or workspace scratch space **before** editing any production code.
2. **Living Updates**: The file is updated in real-time as each subtask transitions.
3. **Post-Flight Archival**: The final green state of the checklist is referenced in the task summary.

## 4. Checklist Item Schema

Every task item in `execution_checklist.md` must use one of four standardized status indicators:

| Status Indicator | Meaning | Description |
|---|---|---|
| `[ ]` | **Pending** | Scheduled work, not yet started. |
| `[-]` | **In Progress** | Currently active step (only 1–2 items active concurrently). |
| `[✓]` | **Verified Complete** | Implemented, tested, and passed quality gates. |
| `[!]` | **Blocked / Tripped** | Failed gate, unexpected regression, or requiring human clearance. |

## 5. Structural Format

```markdown
# Execution Checklist — <Task Title>

- **Status**: IN PROGRESS | COMPLETED | BLOCKED
- **Lead Agent**: <orchestrator | operative-twin | developer>
- **Started**: YYYY-MM-DD HH:MM

---

### Phase 1: Schema & Backend
- [✓] Task 1.1: Database migration and seed parity
- [✓] Task 1.2: Service layer implementation & input validation
- [-] Task 1.3: Unit test suite for new endpoints

### Phase 2: Frontend & Client Integration
- [ ] Task 2.1: UI component layout & styling
- [ ] Task 2.2: State management & API wiring

### Phase 3: Verification & Quality Gates
- [ ] Task 3.1: Automated test suite (`{{TEST_COMMAND}}`)
- [ ] Task 3.2: Type checking (`{{TYPE_CHECK}}`)
- [ ] Task 3.3: Memory intake & project log sync
```

## 6. Execution Rules

1. **No Silent Drops**: An agent may not silently abandon an item on the checklist. If a step becomes obsolete, it must be struck through with an explicit note (`~~Task~~ [Superseded: reason]`).
2. **Verification Bound**: A task may not transition from `[-]` to `[✓]` without automated test or runtime verification evidence.
3. **Continuous Re-rendering**: When using IDE artifact systems, re-render or update the artifact after every phase transition so the human supervisor has instant visual status.
