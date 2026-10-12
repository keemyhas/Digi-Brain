# Digi Brain

> Created by a medical doctor who is also a part-time developer.

**Digi Brain is a portable "second brain" for developers who pair-program with AI agents.** It gives any agent, in any repo, persistent operating memory: who you are, how you work, what was decided and why, and what is safe to do alone - so sessions pick up where the last one ended instead of starting over.

## How it works

- **Human-brain architecture** - memory is organized like a brain, so any agent knows instantly what overrides what and where truth lives:

| Region | Job | Holds |
|---|---|---|
| Thalamus | Wake-up relay | Boot sequence: identity check + working conditions |
| Brainstem | Survival reflexes (override everything) | Safety invariants, destructive-ops bans, git gates |
| Limbic system | Taste and values | Owner profile: archetype, decision style, aesthetics |
| Hippocampus | Episodic memory | Append-only log: Asked -> Decided+Why -> Shipped |
| Cerebellum | Muscle memory | Reusable procedures: how-templates, workflows |
| Temporal lobe | Facts | System layout, stack, contracts |
| Prefrontal cortex | Executive function | Roadmap (NOW/NEXT/LATER), architectural decisions |
| Occipital lobe | Vision | Verify in the running system, never trust edits alone |
| Immune system | Antibodies | Bug post-mortems + lessons that must not recur |

- **Autonomy with gates** - the agent decides nothing ambiguous by default (it asks, one question at a time, with a guess attached). When you speak the activation phrase, it switches to pick-and-flag mode: decide, log the pick plus alternatives, keep executing. Git commit/push always need your explicit order.
- **Automatic logging** - every commit and every session end appends to the log, so history is never lost.
- **Train your own persona (optional)** - the preference/divergence log doubles as labeled training data: your corrections against the agent's picks. If you ever want a personal AI that works like you, this corpus is the starting dataset.

## Harness compatibility

The core is harness-agnostic Markdown. Thin adapters map the three harness-touching behaviors (turn-1 identity prompt, working-conditions display, memory hooks):

| Harness | Status |
|---|---|
| OpenCode | Verified (cold-boot PASS, dev harness) |
| Antigravity | Draft adapter, unverified |
| Claude Code | Draft adapter, unverified |
| Codex | Draft adapter, unverified |
| Generic (any Markdown-aware agent) | Works today - core only |

## Commands

```text
# Install into a repo (interview, ~15 prompts; refuses to touch the source tree)
./installer/install.sh <target-repo> [--overwrite] [--git-init] [--verify-only] [--defaults] [--answers-file <path>]
.\installer\install.ps1 <target-repo> [-Overwrite] [-GitInit] [-VerifyOnly] [-Defaults] [-AnswersFile <path>]

# Re-check an installed repo (zero unresolved tokens, clean scans)
./installer/install.sh <target-repo> --verify-only

# Export persona training pairs from a divergence log (PowerShell; POSIX port deferred)
.\exporter\export-persona.ps1 -InputPath <personalities.md> [-Out <pairs.jsonl>]
```

Rules the commands enforce: backup-before-overwrite, no raw `{{...}}` left behind,
self-verify on every install, local only (no network, nothing leaves the machine).

## Contents

```text
template/
+-- memory/   -> brain.md router + blank templates (personalities, project-log,
|               roadmap, decisions, patterns, bugs, agent-lessons, architecture,
|               known-issues)
+-- rules/    -> session-bootstrap, memory-intake, engineering-standards,
|               project-logging, code-documentation, future-planning, code-graph
+-- workflows/ -> 8 generic flows (feature, bug, security, qa, regression,
|                 db-change, health, consolidation)
+-- agents/   -> 10 specialists (orchestrator lead + 9 reviewers/engineers)
+-- SKILLS-MANIFEST.md -> gate-to-skill contract (no shipped pack)
installer/    -> install.ps1 + install.sh + BOOT-CHECKLIST template
exporter/     -> persona-training export (JSONL) + fixture
adapters/     -> harness mappings (opencode verified; others draft)
```

## Status

Working skeleton: generic brain router, rules, memory templates, 8 workflows, 10 agents, skills manifest, harness adapter interface + OpenCode adapter, and a tested installer (`installer/`). Cold-boot verified. See `SPEC-digi-brain.md` for the spec, `SCRUB-PROTOCOL.md` for the de-identification guarantee, `TASKS.md` for what remains.

## License

MIT - see `LICENSE`.
