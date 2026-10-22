# Workflow: Plan Execution & Living Checklist

## 1. When used

Whenever executing an approved multi-phase feature plan, PRD, or major refactor following a "Proceed" confirmation or autonomous twin activation.

## 2. Relevant agents

- `orchestrator` or `operative-twin` (lead)
- `backend-engineer`, `frontend-engineer`, `database-engineer` (specialists)
- `qa-engineer` (test & regression verifier)
- `memory-manager` (persistence & sync)

## 3. Execution sequence

1. **Initialize Checklist**: Create `execution_checklist.md` in the artifact/scratch directory with all phases, tasks, and acceptance criteria mapped.
2. **Phase Execution Loop**:
   - For each phase:
     1. Mark active subtask as `[-]` In Progress.
     2. Implement code changes with surgical precision.
     3. Run targeted unit/integration tests.
     4. Transition subtask to `[✓]` Verified Complete upon green tests.
     5. Update `execution_checklist.md`.
3. **Full Quality Gate Verification**: Run project test suite (`{{TEST_COMMAND}}`), type checker (`{{TYPE_CHECK}}`), and domain checks.
4. **Memory Intake**: Record decisions in `memory/decisions.md` and bugs in `memory/bugs.md`.
5. **Project Log Append**: Add four-line entry to `memory/project-log.md` with commit SHA and driving invariants.
6. **Final Report**: Deliver concise summary to user linking to verified checklist.

## 4. Quality Gates

1. 100% of checklist items resolved (`[✓]` or explicitly superseded).
2. Zero regressions across existing test suites.
3. No unverified assumptions or unhandled errors.
4. Memory synchronized across canonical and mirror directories.
