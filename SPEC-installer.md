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
| Stack: dirs, commands, frameworks | `{{BACKEND_DIRS}}`, `{{FRONTEND_DIRS}}`, `{{TEST_COMMAND}}`, `{{TYPE_CHECK}}`, `{{TEST_FRAMEWORK}}`, `{{TESTS_DIR}}`, `{{DATABASE}}`, `{{MIGRATIONS_DIR}}`, `{{MIGRATION_NAMING}}` | owner stack (defaults are JavaScript-flavored; the boot checklist orders non-JS repos to swap them before first build) |
| Docs/api/adr locations | `{{DOCS_DIR}}`, `{{API_DOCS}}`, `{{ADR_DIR}}`, `{{FUTURE_PLANS_DIR}}` | owner layout |
| QA + personas + dev URL | `{{QA_DIR}}`, `{{FIXTURE_PREFIX}}`, `{{OWNER_PERSONAS}}`, `{{DEV_URL}}` | `.qa/`, `QA-`, "Admin, Customer", `http://localhost:<port>` |
| Auth/data policies | `{{AUTH_MIDDLEWARE}}`, `{{QUERY_PLACEHOLDER_STYLE}}`, `{{DATA_PROTECTION_STANDARD}}`, `{{SENSITIVE_RESOURCES}}`, `{{KEY_COLUMNS}}`, `{{PROTECTED_COLUMNS_POLICY}}` | owner stack |
| Optional systems | `{{DOMAIN_REVIEWER}}`, `{{WORKFLOWS_DIR}}`, `{{DOMAIN_DOCS}}`, `{{SYNC_RULE}}`, `{{CODE_GRAPH_*}}`, `{{SAFETY_MIDDLEWARE}}`, `{{COMPLIANCE_STANDARD}}`, `{{OFFLINE_STRATEGY}}`, `{{LARGE_CLIENT_FILES}}`, `{{OWNER_DOMAIN}}`, `{{TEST_SCOPE}}` | "none" deletes the slot/file |

Substitution rule: after the interview, scan `template/` for `{{[A-Z_]+}}`; every token must resolve to an answer, a default, or a documented deletion. Unresolved token = abort, never ship raw placeholders. Path tokens are slash-normalized (trailing `/` stripped from answers; templates carry the joining slash) so joins can never double-slash. Post-substitution, `> Setup:` banner lines are deleted, then self-verify runs.

## Behavior

1. **Preflight**:
   - Target path validated and resolved to absolute canonical path.
   - Refuse to run inside the Digi Brain source tree itself.
   - If `<target>/.agents/` exists -> require explicit `--overwrite` (otherwise abort).
2. **Interview & Input Handling**:
   - Inputs are validated against a strict key whitelist (43 approved keys).
   - Unrecognized configuration keys are rejected immediately.
   - Answers are treated strictly as data: command substitutions (`$(...)`), metacharacters, quotes, and punctuation remain inert without shell evaluation.
   - Both interactive mode and answers file (`--answers-file=<path>` or `--answers-file <path>`) supported.
3. **Staging**:
   - Installation renders into an isolated staging directory (`<target>/.agents.staging.<timestamp>.<pid>`).
   - Copy `template/` -> staging directory.
   - If `CODE_GRAPH` is "none", `rules/code-graph.md` is removed.
   - Generate `skills-map.md` with standard fallback mappings.
   - Render `BOOT-CHECKLIST.md` with configured values.
   - Perform literal token substitutions across all staged files.
   - Rename `*.template.md` -> `*.md`.
   - Strip all `> Setup:` banner lines.
4. **Unified Verification Suite** (runs against staged directory; also invoked via `--verify-only`):
   - **STRUCTURE CHECK**: Verifies `memory/`, `rules/`, `agents/`, `workflows/` exist.
   - **BOOTSTRAP CHECK**: Verifies `memory/brain.md`, `BOOT-CHECKLIST.md`, `rules/session-bootstrap.md`, `skills-map.md`, `SKILLS-MANIFEST.md`.
   - **SAFETY CHECK**: Verifies `rules/engineering-standards.md`, `rules/memory-intake.md`, `rules/project-logging.md`, `rules/code-documentation-and-onboarding.md`.
   - **PLACEHOLDER CHECK**: Scans all `*.md` files for unresolved `{{[A-Z0-9_*]+}}` tokens.
   - **FINGERPRINT SCAN**: Heuristic scan for forbidden scrub terms (`abdul|hassan|archon|falx|vellora|synapseems`).
   - **SECRET-PATTERN SCAN**: Heuristic scan for tokens, private keys, AWS credentials, JWTs, and embedded passwords.
   - All 6 checks must PASS (overall exit status 0). If any check fails, overall status is FAIL (exit status 1).
5. **Safe Activation & Rollback**:
   - Staging directory is activated ONLY if all verification checks pass.
   - If target already has an existing `.agents/`, it is moved to `<target>/.agents.backup-<timestamp>`.
   - Staging directory is moved to `.agents/`.
   - If activation fails, automatic rollback restores the backup.
   - If verification fails during staging, staging directory is deleted and target is untouched.

## Project structure

```text
digi-brain/
+-- SPEC-installer.md        -> this file
+-- installer/
    +-- install.ps1          -> Windows implementation (parser-clean, pilot-tested)
    +-- install.sh           -> POSIX implementation (mirrors spec; needs a POSIX shell to test)
    +-- BOOT-CHECKLIST.template.md
```

Status: scripts built + mechanics-verified (pilot install green). Cold-boot agent test (Task 2-3) still open.
Conventions enforced by pilot findings: installer scripts stay pure-ASCII (PS 5.1 parsers choke on
multibyte dashes); template meta-examples use single braces - double braces are installer tokens only,
so the zero-token gate stays meaningful.

## Commands

```text
Install:  ./install.sh <target-repo> [--overwrite] [--git-init]   (or install.ps1)
  --defaults               accept every default (CI / smoke tests)
  --answers-file=<path>    KEY=VALUE lines (lines starting with # ignored); unset keys fall back to prompt/default
Verify:   installer self-verify runs automatically; re-run with --verify-only
Test:     cold-boot pilot on a scratch repo (procedure section Cold-boot test)
```

## Testing strategy - cold-boot test (Phase 2 Task 2-3)

1. Fresh scratch repo (e.g. `digi-brain-pilot/`), run installer with fictitious-owner answers.
2. Open a NEW agent session in the pilot repo with no owner context. Agent must: fire the turn-1 identity gate unprompted, read brain/personalities/log/kanban, and append a session log entry.
3. Activate autonomous mode with the configured phrase; confirm twin declaration + pick-flagging in the log.
4. Attempt `git commit`/`push` without orders - must refuse (or have no orders to act on).
5. Pass = all four hold with zero owner guidance. Fail = fix template or installer, re-run.

## Boundaries

- **Always:** backup before overwrite; `{{...}}`-completeness gate; scans on output; no-network invariant.
- **Ask first:** deleting or merging with a pre-existing `.agents/` (beyond backup+overwrite flag); adding new prompts to the interview.
- **Never:** install into the source tree; transmit answers anywhere; commit/push in the target repo; leave raw placeholders; proceed on red self-verify.

## Success criteria

- [ ] Both scripts implement this spec identically (behavioral diff test on fixtures).
- [ ] Cold-boot test passes on a scratch repo with zero owner guidance.
- [ ] Zero unresolved tokens + clean scans on every install (enforced, not documented).
- [ ] Owner review of installer report output before Phase 3.

## Open questions

1. `BOOT-CHECKLIST.md`: generated file in target, or section of installed `brain.md`? (Guess: generated file - keeps router clean.)
2. Minimum supported shells (sh vs bash for `install.sh`)? (Guess: bash + zsh; plain-sh compatibility deferred.)
