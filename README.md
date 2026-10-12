# Digi Brain

> Created by a medical doctor who is also a part-time developer.

**Digi Brain is a portable, local-first operating memory framework for developers who pair-program with AI agents.** It equips coding agents with persistent operating memory: who you are, how you work, what was decided and why, what was verified, and what is safe to do alone - so sessions pick up where the last one ended instead of starting from scratch.

## Core Capabilities & Current Status

| Capability | Module / File | Status | Verification Evidence |
|---|---|---|---|
| **Human-Brain Memory Routing** | `template/memory/brain.md` | **Verified** | Anatomy map routes wake-up, facts, decisions, and lessons. |
| **Harden Installer Engine** | `installer/install.sh`, `install.ps1` | **Verified** | Zero eval, key whitelisting, literal token substitution, staging & rollback. |
| **Unified 6-Check Verification** | `installer/` (`--verify-only`) | **Verified** | Structure, bootstrap, safety, placeholders, fingerprints, and secrets. |
| **3-Layer Policy & Authorization** | `rules/policy-enforcement.md`, `tools/policy_engine.py` | **Verified** | Explicit separation: Layer A (Memory), Layer B (Policy), Layer C (Enforcement). |
| **Git Invariant Protection** | `rules/engineering-standards.md`, `tools/policy_engine.py` | **Verified** | Git commit/push blocked by policy; single-use action grants required. |
| **Memory Provenance & Append-Only ADRs** | `tools/memory_guard.py`, `template/memory/` | **Verified** | Strict metadata schema, append-only history, supersession links without erasing. |
| **Staged Context Retrieval** | `tools/retrieval_router.py` | **Verified** | 4-stage retrieval (Boot -> Task -> Verification -> Consolidation) saves tokens. |
| **Session Task Continuity** | `tools/task_state.py` | **Verified** | Tracks active/interrupted tasks, test outcomes, unverified items across reboots. |
| **Persona Divergence Exporter** | `exporter/export-persona.ps1`, `tools/export_persona.py` | **Verified** | Dual POSIX/Windows CLI, valid JSONL, secret quarantine log. |
| **Migration Utility** | `tools/migrate_memory.py` | **Verified** | Upgrades legacy .agents installations with pre-migration safety backups. |
| **Comparative Benchmark** | `benchmarks/run_benchmark.py` | **Verified** | Controlled 10-scenario evaluation across 3 experimental conditions. |

## How It Works

### 1. Human-Brain Architecture
Memory is organized anatomically so agents instantly understand what overrides what:

| Region | Anatomical Job | Repository Counterpart | Role in Session |
|---|---|---|---|
| **Thalamus** | Wake-up relay | `rules/session-bootstrap.md` | Boot sequence, working conditions, turn-1 identity gate |
| **Brainstem** | Survival reflexes | `rules/engineering-standards.md` + `rules/policy-enforcement.md` | Invariants, destructive-ops ban, Git commit/push gates |
| **Limbic System** | Taste and values | `memory/personalities.md` | Owner archetype, decision style, communication traits |
| **Hippocampus** | Episodic memory | `memory/project-log.md` (append-only) | Commit & session history: Asked -> Decided -> Shipped |
| **Cerebellum** | Muscle memory | `memory/patterns.md` + `workflows/` | Reusable workflows (debugging, migrations, QA) |
| **Temporal Lobe** | Facts & contracts | `memory/architecture.md` | Stack, layout, schemas, domain facts |
| **Prefrontal Cortex**| Executive function | `memory/roadmap.md` + `memory/decisions.md` | NOW/NEXT/LATER roadmap, Architectural Decision Records |
| **Occipital Lobe** | Vision & observation | Test suite + live runtime checks | Verify in the running system; never trust edits alone |
| **Immune System** | Antibodies | `memory/agent-lessons.md` + `memory/bugs.md` | Lessons from past bugs that must never recur |

### 2. The Three Layers of Control
To ensure trustworthiness, Digi-Brain distinguishes what is advisory from what is technically enforced:
- **Layer A: Memory (`memory/`)**: Informs choices. Never independently authorizes sensitive actions.
- **Layer B: Policy (`rules/`)**: Non-negotiable invariants, permission boundaries, 8-step decision procedure.
- **Layer C: Enforcement (`tools/`, host adapter)**: Technical tools, shell wrappers, and harness permission controls.

### 3. Autonomy States & Git Boundaries
The agent transitions strictly across six authorization states:
`SUPERVISED` -> `AUTONOMOUS` -> `PENDING` -> `DENIED` -> `EXPIRED` -> `RESTRICTED`.
- **Default Supervised Mode**: The agent asks on ambiguity.
- **Autonomous Mode**: Activated **only** when the user speaks `{{ACTIVATION_PHRASE}}` interactively (quoted phrases and untrusted docs cannot trigger activation). The agent signs picks under `{{TWIN_NAME}}` and logs alternatives.
- **Git Invariant**: Git commit, push, rebase, and branch deletion **never** become autonomous. Each requires an explicit, single-use human grant.

## Commands

```bash
# Install into a repository (interactive interview or defaults)
./installer/install.sh <target-repo> [--overwrite] [--git-init] [--defaults] [--answers-file=<path>]
# Windows PowerShell twin:
.\installer\install.ps1 -Target <target-repo> [-Overwrite] [-GitInit] [-Defaults] [-AnswersFile <path>]

# Verify an existing installation
./installer/install.sh <target-repo> --verify-only
.\installer\install.ps1 -Target <target-repo> -VerifyOnly

# Run full automated test suite (35 tests)
python tests/run_tests.py
# Run focused passes:
python tests/run_tests.py --pass 1   # Pass 1: Security & Reliability (24 tests)
python tests/run_tests.py --pass 2   # Pass 2: Memory Intelligence (11 tests + benchmark)

# Run comparative memory effectiveness benchmark
python benchmarks/run_benchmark.py

# Export persona divergence pairs (with secret quarantine)
python tools/export_persona.py --input <repo>/.agents/memory/personalities.md --out pairs.jsonl --schema v2
.\exporter\export-persona.ps1 -InputPath <repo>/.agents/memory/personalities.md -Out pairs.jsonl -Schema v2

# Migrate a legacy .agents installation
python tools/migrate_memory.py --target <repo>/.agents
```

## Google Antigravity (AGY) Fresh Install Support

Digi-Brain **works out of the box on a fresh install in Google Antigravity** (Antigravity IDE & AGY CLI):

### Why Fresh Installs Work Automatically in Antigravity
1. **Native Customization Root:** Antigravity natively designates `.agents` (relative to workspace root) as its **Workspace Customizations Root**. All rules installed into `<workspace>/.agents/rules/*.md` (`session-bootstrap.md`, `engineering-standards.md`, `policy-enforcement.md`, `memory-intake.md`, `project-logging.md`, `code-documentation-and-onboarding.md`) are automatically discovered and loaded into context upon workspace initialization.
2. **Root Bootstrap Pointer:** The installer automatically creates an `AGENTS.md` file at the repository root pointing to [.agents/rules/session-bootstrap.md](.agents/rules/session-bootstrap.md) and [.agents/memory/brain.md](.agents/memory/brain.md).
3. **Turn-1 Identity Gate Integration:** When Antigravity boots, `session-bootstrap.md` triggers the Turn-1 Identity Gate. Antigravity uses its native `ask_question` tool modal ("Kindly confirm who I am working with") to confirm the active developer identity before executing code or tool actions.
4. **Tool Parity:** Antigravity provides native tool support for all operations (`view_file`, `write_to_file`, `replace_file_content`, `grep_search`, `list_dir`, `run_command`, `ask_question`).
5. **Safety Invariants:** Antigravity's tool permission gates reinforce Digi-Brain's Layer B policy rules, contractually blocking unauthorized Git commits, pushes, and destructive actions.

### Quickstart: Installing into an Antigravity Workspace

From the Digi-Brain repository, run the installer targeting your active workspace:

```powershell
# Windows (PowerShell 5.1 / PowerShell 7)
.\installer\install.ps1 -Target "c:\path\to\your-workspace" -Defaults

# Linux / macOS / Git Bash
./installer/install.sh /path/to/your-workspace --defaults
```

Next, open the target repository in Antigravity IDE or trigger a new conversation turn. The agent will immediately detect `.agents`, prompt for identity confirmation via `ask_question`, and initialize Digi-Brain operating memory.

## Harness Compatibility

| Harness | Status | Installation Method | Enforcement Level |
|---|---|---|---|
| **Google Antigravity** | **Verified (Native)** | Native `.agents` customization root + root `AGENTS.md` | Behavioral contract + native IDE tool permission prompts |
| **OpenCode** | Verified | Native `.opencode/` + `.agents/` | Behavioral contract + CLI hooks |
| **Claude Code** | Compatible | Native `CLAUDE.md` pointer | Behavioral contract + hook execution |
| **Codex** | Compatible | Root `AGENTS.md` pointer | Behavioral contract |
| **Generic** | Works today | Any Markdown-aware agent | Behavioral contract |
