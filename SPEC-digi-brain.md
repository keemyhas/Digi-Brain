# Spec: Digi Brain (Phase 1 - local plain version)

## Objective

Distill a **de-identified, portable agent-operating-memory framework** ("Digi Brain") from a private production `.agents/` corpus, so that:

1. Any developer can drop it into their repo and get a working "second brain": boot sequence, persistent memory, autonomy gates, reusable procedures.
2. It works across agent harnesses (Antigravity, Claude Code, OpenCode, Codex, others) via a harness-agnostic core + thin adapters.
3. It can optionally train a personal AI persona from the owner's recorded preferences (divergence log -> training pairs), as pioneered by the source corpus.

**Users:** solo developers / small teams who pair-program with AI agents and want continuity across sessions.
**Non-goal for Phase 1:** no git repo, no publish, no installer, no harness adapters - local skeleton + spec + scrub protocol only.

## Assumptions (correct me now or I proceed with these)

1. Source corpus stays private; Digi Brain ships zero verbatim `memory/` content (all templates/placeholders).
2. "No fingerprint" = no identity, project, anecdote, secret, or infrastructure traces **in the content** (see `SCRUB-PROTOCOL.md`); it does NOT mean anonymous publishing (repo ownership itself attributes).
3. Folder name is `digi-brain` (kebab-case; `Digi Brain` with a space breaks CLIs/URLs).
4. Markdown-only framework, no runtime code in Phase 1.
5. English-language corpus (adapters/localization deferred).

## Capability map (one request, four independently testable capabilities)

| Module id | Responsibility | Depends on | Phase |
|---|---|---|---|
| `core-template` | Generic brain router, rules, memory templates, README | - | 1 (this spec) |
| `installer` | Scaffolds `core-template` into a foreign repo, verifies boot | `core-template` | 2 |
| `auto-logging` | Harness hooks/adapters that append memory without prompting | `core-template`, `installer` | 2-3 |
| `persona-trainer` | Exports preference/divergence logs as training pairs | `core-template` | 3 |

Build order: `core-template` -> `installer` -> `auto-logging` -> `persona-trainer`. Each module gets its own spec before build.

## Tech stack

Markdown (GitHub-flavored), git (from Phase 2). No dependencies in Phase 1. Shell verification via PowerShell 5.1 / POSIX grep equivalents.

## Commands

```text
Fingerprint scan:  grep -rniE "abdul|hassan|archon|falx|synapse|vellora|synapseems" digi-brain/  (expect: zero hits)
Secret scan:       grep -rniE "password|passwd|admin123|api[_-]?key|secret|bearer |mongodb://|postgres://" digi-brain/  (expect: zero hits)
Structure check:   tree / dual directory listing of digi-brain/template
```

## Project structure (Phase 1)

```text
digi-brain/
+-- SPEC-digi-brain.md      -> this file (living spec)
+-- SCRUB-PROTOCOL.md       -> fingerprint classes, per-file disposition, verification
+-- README.md               -> public-facing front door (attribution line included)
+-- TASKS.md                -> Phase 1b/2/3 task list with acceptance + verification
+-- template/               -> the shippable skeleton (mirrors future .agents/ layout)
    +-- memory/
    |   +-- brain.md                  (generic human-brain router, placeholders only)
    |   +-- personalities.template.md
    |   +-- project-log.template.md
    |   +-- roadmap.template.md
    |   +-- decisions.template.md
    |   +-- patterns.template.md
    |   +-- bugs.template.md
    |   +-- agent-lessons.template.md
    |   +-- architecture.template.md
    |   +-- known-issues.template.md
    +-- rules/
        +-- session-bootstrap.md
        +-- memory-intake.md
        +-- engineering-standards.md
        +-- project-logging.md
        +-- code-documentation-and-onboarding.md
        +-- future-product-planning.md   (condensed port)
        +-- code-graph.md                (optional tool; merges graph + usage-log rules)
    +-- workflows/              -> 8 generic flows (feature, bug, security, qa, regression,
    |                              db-change, health, consolidation)
    +-- agents/                 -> 10 specialists (`orchestrator` lead; domain safety
    |                              reviewer defaults to Owner, overridable at install)
    +-- SKILLS-MANIFEST.md      -> gate-to-skill contract (no shipped pack; prose fallbacks)
+-- adapters/
|   +-- ADAPTER-INTERFACE.md    -> what "supports Digi Brain" means for any harness
|   +-- opencode.md             -> first adapter (dev harness) + harness constraints
+-- installer/                  -> see SPEC-installer.md (`install.ps1` + `install.sh`,
                                pilot-proven: zero tokens, banners stripped, cold-boot PASS)
```

`skills/` strategy is **decided (Phase 1b Task 1b-4): harness-native manifest** - `template/SKILLS-MANIFEST.md`
maps each gate to the skill it expects; the owner's harness provides equivalents, with prose fallbacks where missing. No shipped skill pack.

## Code/style conventions

- Placeholders use `{{DOUBLE_BRACE_UPPER}}` (e.g. `{{OWNER_NAME}}`, `{{PROJECT_NAME}}`, `{{ACTIVATION_PHRASE}}`). Never real names, even as "examples" - examples are marked `EXAMPLE - DELETE` and use obviously fake values (`Ada Example`, `Acme Project`).
- Tone: professional, precise, terse. No emojis in framework files.
- Every template file carries a one-line header stating what to replace on install.
- Router-not-duplicate: `brain.md` links, never copies, other files' content.

## Testing strategy

- **Phase 1 (now):** static scans only - identity/project-term grep = 0 hits outside the scan patterns themselves and marked fictitious examples; secret grep = 0 hits outside the scan patterns; generic domain English ("clinical" as an adjective, "medical doctor" in the README line) is allowed; structure matches section Project structure.
- **Phase 2 (later):** cold-boot test - fresh agent + pilot repo + installer, verify boot sequence completes and autonomy gates hold with no owner in the room.
- **Phase 3 (later):** harness matrix - one adapter verified at a time, never all five on day one.

## Boundaries

- **Always:** scrub before port (protocol first, content second); placeholders for all identity/project values; keep spec alive (update on every scope/decision change).
- **Ask first:** adding any source-corpus anecdote even "anonymized"; widening the Phase 1 file list; choosing the public license; choosing the publish account.
- **Never:** copy `memory/` content verbatim (history, traits, logs, credentials); commit/push anything without explicit order (standing git gate); sync `digi-brain/` into the source repo's `.agents/` trees; claim full anonymity - promise "no fingerprint in content" only; publish before the Phase 2 cold-boot gate passes.

## Success criteria (Phase 1 done = all true)

- [ ] `digi-brain/` structure matches section Project structure exactly.
- [ ] Identity/project-term grep returns 0 hits outside the scan patterns themselves, the README allowlist, and marked fictitious examples; secret grep returns 0 hits outside the scan patterns.
- [ ] `README.md` contains the attribution line verbatim: "Created by a medical doctor who is also a part-time developer."
- [ ] Every template file has placeholders, no real names/projects/URLs/credentials.
- [ ] `SCRUB-PROTOCOL.md` dispositions cover all 20 memory + 8 rules + 10 workflows + 11 agents files of the source corpus.
- [ ] `TASKS.md` lists Phase 1b/2/3 with acceptance + verification per task.
- [ ] Nothing committed, pushed, or published (local files only).

## Decided (interview-confirmed 2026-10-11 - intent explicit-yes)

1. **License: MIT** - maximum adoption; dual-license later only if a commercial split ever justifies it.
2. **Publish account: personal** - speed over neutral shell; anonymity guarantee stays content-only (account itself attributes, accepted deliberately).
3. **First adapter: OpenCode** (dev harness, zero setup, immediate dogfooding); others one at a time after.
4. **Trainer schema: deferred** to the Phase 3 `persona-trainer` spec; the divergence log preserves the raw material losslessly.

## Open questions (remaining)

- None. All four Phase-3 decisions above are locked. New questions go here as they arise.
