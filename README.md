# Digi Brain

> Created by a medical doctor who is also a part-time developer.

**Digi Brain is a portable "second brain" for developers who pair-program with AI agents.** It gives any agent, in any repo, persistent operating memory: who you are, how you work, what was decided and why, and what is safe to do alone — so sessions pick up where the last one ended instead of starting over.

## How it works

- **Human-brain architecture** — memory is organized like a brain, so any agent knows instantly what overrides what and where truth lives:

| Region | Job | Holds |
|---|---|---|
| Thalamus | Wake-up relay | Boot sequence: identity check + working conditions |
| Brainstem | Survival reflexes (override everything) | Safety invariants, destructive-ops bans, git gates |
| Limbic system | Taste and values | Owner profile: archetype, decision style, aesthetics |
| Hippocampus | Episodic memory | Append-only log: Asked → Decided+Why → Shipped |
| Cerebellum | Muscle memory | Reusable procedures: how-templates, workflows |
| Temporal lobe | Facts | System layout, stack, contracts |
| Prefrontal cortex | Executive function | Roadmap (NOW/NEXT/LATER), architectural decisions |
| Occipital lobe | Vision | Verify in the running system, never trust edits alone |
| Immune system | Antibodies | Bug post-mortems + lessons that must not recur |

- **Autonomy with gates** — the agent decides nothing ambiguous by default (it asks, one question at a time, with a guess attached). When you speak the activation phrase, it switches to pick-and-flag mode: decide, log the pick plus alternatives, keep executing. Git commit/push always need your explicit order.
- **Automatic logging** — every commit and every session end appends to the log, so history is never lost.
- **Train your own persona (optional)** — the preference/divergence log doubles as labeled training data: your corrections against the agent's picks. If you ever want a personal AI that works like you, this corpus is the starting dataset.

## Harness compatibility

The core is harness-agnostic Markdown. Thin adapters map the three harness-touching behaviors (turn-1 identity prompt, working-conditions display, memory hooks):

| Harness | Status |
|---|---|
| OpenCode | Planned first (dev harness) |
| Antigravity | Planned |
| Claude Code | Planned |
| Codex | Planned |
| Generic (any Markdown-aware agent) | Works today — core only |

## Contents (`template/`)

```text
template/
├── memory/   → brain.md router + blank templates (personalities, project-log,
│               roadmap, decisions, patterns, bugs, agent-lessons)
└── rules/    → session-bootstrap, memory-intake, engineering-standards,
                project-logging (all generic, placeholders only)
```

Agents, workflows, and skills adapters are tracked in `TASKS.md` (Phase 1b+).

## Status

Phase 1 — local skeleton. Not yet installable, not published. See `SPEC-digi-brain.md` for the spec and success criteria, `SCRUB-PROTOCOL.md` for the de-identification guarantee.
