# Spec: Digi Brain Installer (`installer` module)

## Objective

One-command scaffold of `template/` into a foreign repo as `.agents/`, with all `{{PLACEHOLDERS}}` substituted from a single owner interview, followed by a self-verification pass. Turns adoption from "read the docs and hand-copy 38 files" into "answer ~15 prompts, get a working second brain."

**Users:** developers installing Digi Brain into their own repo (Phase 2 pilot: the owner, on a scratch repo).
**Non-goals:** harness adapters (separate module, OpenCode first), repo publishing, telemetry of any kind.

## Assumptions

1. Target is a git repo (or becomes one); installer never `git init` without a flag (`--git-init`, off by default).
2. Owner answers prompts once; answers persist to `.agents/.install.json` (git-ignored) for re-runs.
3. Two implementations share this spec: `install.ps1` (Windows/PowerShell 5.1) and `install.sh` (POSIX). Behavior identical; this spec is the contract.
4. No network access. No data leaves the machine. Ever.

## Inputs (single interview, ~15 prompts)

| Prompt | Token(s) filled | Example (fictitious) |
|---|---|---|
| Owner name, role | `{{OWNER_NAME}}`, `{{OWNER_ROLE}}` | Ada Example / Solo Developer |
| Project name | `{{PROJECT_NAME}}` | Acme Project |
| Activation phrase, twin name (or "none") | `{{ACTIVATION_PHRASE}}`, `{{TWIN_NAME}}` | "take the wheel" / Deuter |
| Safety invariants (free text, or "none yet") | `{{SAFETY_INVARIANTS}}`, `{{SAFETY_INVARIANTS_FILE}}` | see brain template |
| Stack: dirs, commands, frameworks | `{{BACKEND_DIRS}}`, `{{FRONTEND_DIRS}}`, `{{TEST_COMMAND}}`, `{{TYPE_CHECK}}`, `{{TEST_FRAMEWORK}}`, `{{TESTS_DIR}}`, `{{DATABASE}}`, `{{MIGRATIONS_DIR}}`, `{{MIGRATION_NAMING}}` | owner stack |
| Docs/api/adr locations | `{{DOCS_DIR}}`, `{{API_DOCS}}`, `{{ADR_DIR}}`, `{{FUTURE_PLANS_DIR}}` | owner layout |
| QA + personas + dev URL | `{{QA_DIR}}`, `{{FIXTURE_PREFIX}}`, `{{OWNER_PERSONAS}}`, `{{DEV_URL}}` | `.qa/`, `QA-`, "Admin, Customer", `http://localhost:<port>` |
| Auth/data policies | `{{AUTH_MIDDLEWARE}}`, `{{QUERY_PLACEHOLDER_STYLE}}`, `{{DATA_PROTECTION_STANDARD}}`, `{{SENSITIVE_RESOURCES}}`, `{{KEY_COLUMNS}}`, `{{PROTECTED_COLUMNS_POLICY}}` | owner stack |
| Optional systems | `{{DOMAIN_REVIEWER}}`, `{{WORKFLOWS_DIR}}`, `{{DOMAIN_DOCS}}`, `{{SYNC_RULE}}`, `{{CODE_GRAPH_*}}`, `{{SAFETY_MIDDLEWARE}}`, `{{COMPLIANCE_STANDARD}}`, `{{OFFLINE_STRATEGY}}`, `{{LARGE_CLIENT_FILES}}`, `{{OWNER_DOMAIN}}`, `{{TEST_SCOPE}}` | "none" deletes the slot/file |

Substitution rule: after the interview, scan `template/` for `{{[A-Z_]+}}`; every token must resolve to an answer, a default, or a documented deletion. Unresolved token = abort, never ship raw `{{…}}`.

## Behavior

1. **Preflight**: target path exists; if `<target>/.agents/` exists → show diff summary, require explicit `--overwrite` + write timestamped backup (`<target>/.agents.backup-<ts>/`). Refuse to run inside the Digi Brain source tree itself.
2. **Interview**: prompt table above (defaults offered, free text accepted, "none" where allowed).
3. **Render**: copy `template/` → `<target>/.agents/`, renaming `*.template.md` → `*.md`, substituting tokens. `SKILLS-MANIFEST.md` + owner skill mapping → `<target>/.agents/skills-map.md` (unmapped rows = `none — prose fallback`).
4. **Self-verify** (must all pass, or roll back):
   - Zero unresolved `{{…}}` tokens in output.
   - Fingerprint/secret scans clean (same patterns as `SCRUB-PROTOCOL.md` §3, pointed at output).
   - Boot checklist file written to `<target>/.agents/BOOT-CHECKLIST.md` (turn-1 gate, 3-log read, Kanban read, first log entry).
5. **Report**: files written, tokens resolved/deleted, verification results, exact next step ("open a fresh agent session in the target repo and follow BOOT-CHECKLIST.md").

## Project structure (future; not built in this spec)

```text
digi-brain/
├── SPEC-installer.md        → this file
└── installer/
    ├── install.ps1          → Windows implementation
    ├── install.sh           → POSIX implementation
    └── BOOT-CHECKLIST.template.md
```

## Commands

```text
Install:  ./install.sh <target-repo> [--overwrite] [--git-init]   (or install.ps1)
Verify:   installer self-verify runs automatically; re-run with --verify-only
Test:     cold-boot pilot on a scratch repo (procedure §Cold-boot test)
```

## Testing strategy — cold-boot test (Phase 2 Task 2-3)

1. Fresh scratch repo (e.g. `digi-brain-pilot/`), run installer with fictitious-owner answers.
2. Open a NEW agent session in the pilot repo with no owner context. Agent must: fire the turn-1 identity gate unprompted, read brain/personalities/log/kanban, and append a session log entry.
3. Activate autonomous mode with the configured phrase; confirm twin declaration + pick-flagging in the log.
4. Attempt `git commit`/`push` without orders — must refuse (or have no orders to act on).
5. Pass = all four hold with zero owner guidance. Fail = fix template or installer, re-run.

## Boundaries

- **Always:** backup before overwrite; `{{…}}`-completeness gate; scans on output; no-network invariant.
- **Ask first:** deleting or merging with a pre-existing `.agents/` (beyond backup+overwrite flag); adding new prompts to the interview.
- **Never:** install into the source tree; transmit answers anywhere; commit/push in the target repo; leave raw placeholders; proceed on red self-verify.

## Success criteria

- [ ] Both scripts implement this spec identically (behavioral diff test on fixtures).
- [ ] Cold-boot test passes on a scratch repo with zero owner guidance.
- [ ] Zero unresolved tokens + clean scans on every install (enforced, not documented).
- [ ] Owner review of installer report output before Phase 3.

## Open questions

1. `BOOT-CHECKLIST.md`: generated file in target, or section of installed `brain.md`? (Guess: generated file — keeps router clean.)
2. Minimum supported shells (sh vs bash for `install.sh`)? (Guess: bash + zsh; plain-sh compatibility deferred.)
