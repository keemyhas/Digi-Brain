# {{PROJECT_NAME}} Second Brain - Human-Brain Architecture

> Setup: fill every double-brace token on install, then delete this line.
> Naming: "Digi Brain" is the installer/product; the "Second Brain" is the memory it installs.
> Entry point for every agent session. Read this FIRST, before code.
> This file is a **thin router, not a content duplicate** - each region points to the file where truth lives.

## 0. Anatomy map

| Brain region | Job | File | Holds |
|---|---|---|---|
| Thalamus (relay) | Routes every session on wake-up | `rules/session-bootstrap.md` | Boot sequence section 1 |
| Brainstem | Survival reflexes - override everything, never sleep | `rules/engineering-standards.md` (invariants section 5, git gates section 6) | Non-negotiable invariants |
| Limbic system | Taste, values, who you are | `memory/personalities.md` | Owner profile, decision style, activated-twin rules |
| Hippocampus | Episodic memory - what just happened | `memory/project-log.md` (append-only) | Asked -> Decided+Why -> Shipped per commit + session end |
| Cerebellum | Muscle memory - skilled movement without thinking | `memory/patterns.md` + `{{WORKFLOWS_DIR}}` | How-templates, default multi-file flow |
| Temporal lobe | Facts about the system | `memory/architecture.md` + `{{DOMAIN_DOCS}}` | Layout, stack, contracts |
| Prefrontal cortex | What to do next, and why | `memory/roadmap.md` section 0 + `memory/decisions.md` | NOW/NEXT/LATER scope, ADRs |
| Occipital lobe | Vision - believe the running system over memory | Live verification | Reproduce/verify in the running system before claiming done |
| Immune system | What must not recur | `memory/bugs.md` + `memory/agent-lessons.md` | Post-mortems + numbered lessons; pre-flight check per domain |

Override hierarchy (top wins - a stale brain must NEVER override 1 or 2; if brain conflicts with shipped code, code wins, then fix the brain):
1. Explicit owner instruction in the current session
2. Brainstem (safety invariants + engineering standards)
3. This brain + linked memory files
4. General best practice

## 1. Waking up (every session, <2 min)

1. Display Working Conditions: `[x] bugs recording | [x] code-graph | [x] personalities | [x] memory sync` (mark `[ ]` with a reason for anything missing).
2. Ask *"Kindly confirm who I am working with"* via the harness's picker - mandatory turn-1 gate, even if identity is inferable. Tailor behavior to `personalities.md` once confirmed.
3. Read `personalities.md` (who you're working with + autonomy locks).
4. Read `project-log.md` last 3 entries (what was just asked/decided/shipped).
5. Read `roadmap.md` section 0 Kanban (NOW vs NEXT - don't start FUTURE work).
6. If codebase question: query the code-graph tool first if one is configured.

## 2. Brainstem - survival reflexes

- {{SAFETY_INVARIANTS}} (owner-defined, e.g. data-loss bans, safety-critical paths that must never be blocked).
- Zero data destruction: no destructive schema/data ops outside reviewed migrations; production data is never a test fixture.
- Git gates: no `git commit` / `push` without explicit owner order.
- Test isolation: tests run against disposable fixtures/databases only - never live data.
- Full list: `rules/engineering-standards.md`.

## 3. Limbic system - who we are

- `personalities.md` holds the owner profile: archetype, decision psychology, aesthetic standards, collaboration locks, and the activated-twin rules (if the owner enables autonomous mode).
- Taste is enforceable: whatever the owner locks there (geometry, palette, ergonomics, verification bars) is law until changed there.

## 4. Hippocampus - never lose logs

- `project-log.md` is APPEND-ONLY. Never edit past entries; correct by appending. Rule: `rules/project-logging.md`.
- Every commit MUST append one entry (Asked -> Decided+Why -> Shipped + SHA). Session end MUST append even if nothing shipped.
- Freshness: if the last entry predates the last commit in `git log`, the brain is stale - catch up before acting.

## 5. Cerebellum - how work moves

- `memory/patterns.md` - copy the template, don't reinvent.
- Default multi-file flow: `{{WORKFLOWS_DIR}}/feature-development.md`; bug/security/data flows own their triggers.
- Why-record: `memory/decisions.md` (+ `{{ADR_DIR}}`) - read before revisiting any architectural choice.

## 6. Prefrontal cortex - autonomy gates

Autonomous pick-and-flag mode is OFF by default. Activates ONLY on the owner's exact phrase **`{{ACTIVATION_PHRASE}}`** (default: `activate second brain`).

## 6a. Graduation readiness (before first activation in owner absence)

Do not activate on an empty brain. The owner confirms all four, then speaks the phrase:

1. **Profile real** - `personalities.md` holds observed (never invented) traits, decision style, and invariants.
2. **History present** - `project-log.md` carries real Asked/Decided/Shipped entries across multiple sessions (guideline: 10+, covering at least one disagreement or correction).
3. **Scope live** - `roadmap.md` section 0 has real NOW cards; decisions of consequence sit in `decisions.md`.
4. **Boot proven** - one cold-boot (fresh agent, no owner help) completed the checklist green.

On activation the agent declares its twin identity, signs picks as such; owner corrections become divergence entries (future persona-training data). Every later session in absence runs this loop: pick likeliest -> flag pick + alternatives in the log -> keep executing -> corrections become training data.
- On activation the agent declares its twin identity, signs picks as such; owner corrections become divergence entries (future persona-training data).
- Default mode: decide nothing ambiguous - ask via picker (options + free text), one question at a time, guess attached.
- Activated mode: pick the likeliest option, flag pick + alternatives in `project-log.md`, keep executing.
- Activation NEVER lifts the git gates.
- STOP and ask (either mode) when: scope moves to NEXT/LATER, safety-critical paths change, new storage/endpoints/dependencies, any destructive op, or brain conflicts with code.

## 7. Where truth lives

| Need | Read |
|---|---|
| Taste, invariants, twin | `personalities.md` |
| What was asked/decided/shipped | `project-log.md` |
| NOW / NEXT / LATER scope | `roadmap.md` section 0 |
| Why past decisions were made | `decisions.md` + `{{ADR_DIR}}` |
| Reusable how-templates | `patterns.md` |
| What must not recur | `bugs.md` + `agent-lessons.md` |
| System layout, stack | `architecture.md` |
| Session rules | `rules/session-bootstrap.md`, `rules/memory-intake.md`, `rules/engineering-standards.md`, `rules/project-logging.md` |
