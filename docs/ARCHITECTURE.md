# Digi-Brain Comprehensive Architecture Specification

## 1. Architectural Philosophy & Vision

Digi-Brain is a portable, local-first operating memory framework designed for AI coding agents. Unlike ephemeral prompt wrappers or monolithic context dumps, Digi-Brain organizes persistent knowledge using an anatomical human-brain architecture that separates what is believed from what is enforced.

### Core Design Principles
1. **Security by Design**: Zero dynamic shell evaluation; inputs treated strictly as data; destructive operations barred by non-negotiable invariants.
2. **Layered Separation of Authority**: Clear demarcation between informational memory, contractual policy, and runtime technical enforcement.
3. **Auditability & Append-Orientation**: Historical engineering decisions and lessons cannot be silently rewritten or erased. Changes occur via explicit supersession links.
4. **Local-First & Privacy-Centric**: Operates 100% on the developer machine without telemetry, cloud dependencies, or external credential leakage.
5. **Staged Context Efficiency**: Scoped retrieval loads only relevant facts, cutting token overhead by over 50% compared to monolithic instruction files.

---

## 2. The Human-Brain Anatomy Map

Every session entry begins at `memory/brain.md`, which functions as a thin anatomical router directing attention to the appropriate locus of truth:

| Brain Region | Biological Role | Digi-Brain Repository Component | Operational Function |
|---|---|---|---|
| **Thalamus** | Sensory relay & wake-up | `rules/session-bootstrap.md` | Boot sequence, working conditions verification, turn-1 identity gate |
| **Brainstem** | Autonomic survival reflexes | `rules/engineering-standards.md` + `rules/policy-enforcement.md` | Invariants, destructive operation bans, Git commit/push gates |
| **Limbic System** | Emotion, values & taste | `memory/personalities.md` | Developer archetype, decision-making psychology, communication style |
| **Hippocampus** | Episodic memory | `memory/project-log.md` (append-only) | Commit-level history: Asked -> Decided+Why -> Shipped |
| **Cerebellum** | Muscle memory & motor patterns | `memory/patterns.md` + `workflows/` | Reusable workflows (bug investigation, migrations, QA, health review) |
| **Temporal Lobe** | Semantic facts & knowledge | `memory/architecture.md` + domain docs | System stack, directory layout, service contracts, data schemas |
| **Prefrontal Cortex** | Executive function & planning | `memory/roadmap.md` + `memory/decisions.md` | NOW/NEXT/LATER roadmap, Architectural Decision Records (ADRs) |
| **Occipital Lobe** | Visual verification & perception | Test runner + live environment checks | Mandate to verify in running runtime; never trust unexecuted source edits |
| **Immune System** | Antibodies & pathogens | `memory/agent-lessons.md` + `memory/bugs.md` | Root-cause post-mortems and durable lessons preventing recurring defects |

---

## 3. The Three Layers of Control

To ensure clarity between behavioral expectations and technical guarantees, Digi-Brain defines three distinct layers:

```
+-------------------------------------------------------------------------+
|                        LAYER C: ENFORCEMENT                             |
|  Host Sandboxes | Shell Permission Wrappers | tools/policy_engine.py    |
+-------------------------------------------------------------------------+
                                   ^
                                   | Evaluates & Gating
+-------------------------------------------------------------------------+
|                         LAYER B: POLICY                                 |
|  rules/policy-enforcement.md | rules/engineering-standards.md           |
|  - Non-Negotiable Invariants  - 8-Step Decision Procedure               |
|  - Authorization States       - Scoped Single-Use Grants                |
+-------------------------------------------------------------------------+
                                   ^
                                   | Guides & Informs
+-------------------------------------------------------------------------+
|                         LAYER A: MEMORY                                 |
|  memory/ (brain.md, decisions.md, project-log.md, personalities.md)    |
|  - Episodic History           - Semantic System Facts                   |
|  - Procedural Workflows       - Limbic Preferences                      |
+-------------------------------------------------------------------------+
```

1. **Layer A (Memory)**: Informational content. Contains lessons, past decisions, developer traits, and current architectural layout. Memory informs choices but possesses zero inherent authorization authority.
2. **Layer B (Policy)**: Explicit, contractual operational rules. Defines permitted vs forbidden actions, authorization states, and decision procedures.
3. **Layer C (Enforcement)**: Technical execution barriers. Uses harness-level tool filters, command interception, or CLI guards (`tools/policy_engine.py`). Where a host harness lacks tool blocking, policies are strictly contractual and behavioral.

---

## 4. Authorization States & Decision Procedure

### 4.1 State Machine
Sessions operate across six formal states:
- `SUPERVISED` (Default on boot): Asks for clarification on ambiguous decisions; permits safe local reads, tests, and edits.
- `AUTONOMOUS` (Activated Twin): Activated exclusively by user speech of `{{ACTIVATION_PHRASE}}`. Twin picks on ambiguity, signs decisions under `{{TWIN_NAME}}`, and logs picks + alternatives. Never lifts Git restrictions.
- `PENDING`: Sensitive operation awaiting human confirmation.
- `DENIED`: Human rejected action or readiness check failed.
- `EXPIRED`: Single-use action grant consumed or TTL elapsed.
- `RESTRICTED`: Tripwire engaged upon safety invariant failure; permits recovery operations only.

### 4.2 Git Operation Boundaries
The following operations are non-negotiably blocked by policy:
- `git commit`
- `git push`
- `git rebase` / `git commit --amend`
- `git reset` (destructive history rewriting)
- `git branch -D` / `git branch -d`
- Force-push (`git push --force`)

Autonomous mode **never** broadens authority to include Git writes. Each Git operation requires an explicit, single-use, action-scoped human command.

### 4.3 Eight-Step Decision Procedure
Before any sensitive operation, the policy engine validates:
1. **Action**: Exactly what command or mutation is requested?
2. **Resource**: What target file, branch, or database is affected?
3. **Policy**: Is the action permitted by engineering standards?
4. **Explicit Grant**: Does this action require human confirmation?
5. **Freshness**: Is the authorization grant valid, unused, and unexpired?
6. **Scope**: Does the grant cover this exact resource without scope broadening?
7. **Enforcement**: Can the host environment technically enforce this boundary?
8. **Audit Trail**: How will the decision and its outcome be logged in `project-log.md`?

---

## 5. Memory Provenance & Integrity

### 5.1 Structured Provenance Header
All durable entries record:
- `entry_id`: Unique identifier (e.g., `[ADR-001]`, `[LES-001]`).
- `Type`: `Episodic` | `Semantic` | `Procedural` | `Preference` | `Inference`.
- `SourceClass`: `ExplicitUser` | `VerifiedDoc` | `ObservedTool` | `TestEvidence` | `UntrustedContent` | `AIInference`.
- `Status`: `Current` | `Unverified` | `Superseded` | `Expired` | `Disputed`.
- `Scope`: `project` | `universal` | `module:<name>`.
- `Confidence`: `verified` | `high` | `medium` | `low`.
- `CreatedAt`: Timestamp or date.
- `Supersedes`: Identifier of earlier entry being replaced.

### 5.2 Append-Oriented Decision History & Supersession
Historical decisions are never deleted. When architectural direction shifts:
1. The new decision appends as a new ADR (e.g. `ADR-002`).
2. The new entry records `Supersedes: ADR-001`.
3. The validation guard (`tools/memory_guard.py`) updates `ADR-001` to `Status: Superseded by ADR-002`.
4. Append-only integrity checks verify that no historical entries have been dropped.

### 5.3 Memory Poisoning Defense
External documentation, third-party source files, and transcripts are classified as `UntrustedContent`.
The memory guard rejects instructions attempting to:
- Override safety invariants or Git gates.
- Disable secret scanning or fingerprint detection.
- Grant unrestricted mode.

---

## 6. Staged Context Retrieval & Session Continuity

### 6.1 Four-Stage Retrieval
1. **Stage 1 (Boot Context)**: Minimal identity, working conditions, and safety invariants.
2. **Stage 2 (Task Context)**: Keyword-targeted ADRs and lessons matching task keywords.
3. **Stage 3 (Verification Context)**: Domain-specific test commands and acceptance criteria.
4. **Stage 4 (Consolidation)**: Post-task filtering of durable insights into permanent files.

### 6.2 Explicit Task-State Continuity
`tools/task_state.py` tracks active tasks in `memory/task-state.json`:
- Completed vs remaining steps.
- Files changed during the task.
- Tests executed and test failures observed.
- Unverified items awaiting proof.
On session wake-up, the agent inspects this state to resume work without repeating completed work or assuming broken work succeeded.

---

## 7. Persona Learning & Privacy

- Corrections vs Preferences: Project-specific corrections are tagged with `Scope: project` and do not automatically become universal developer preferences.
- Exporter Engine: Dual Python (`tools/export_persona.py`) and PowerShell (`exporter/export-persona.ps1`) CLIs produce schema-valid JSONL (`digi-brain-divergence-pair-v2`).
- Secret Quarantine: Comprehensive regex and heuristic scanning detects API keys, passwords, database URIs, and JWTs, quarantining matched records to `<out>.quarantine.jsonl` for owner inspection.
