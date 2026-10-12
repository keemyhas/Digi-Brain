# Digi Brain Task List (Phase 1b -> 2 -> 3)

> Convention per planning skill: acceptance + verification + dependencies + files per task. Checkpoints gate phases. Human reviews each checkpoint.

## Phase 1b: Finish the skeleton (local, no repo)

- [x] Task 1b-1: Port remaining rules
  - Acceptance: all 8 source rules have a dispositioned generic counterpart; zero F1-F5 hits
  - Verify: fingerprint + secret greps clean
  - Files: `digi-brain/template/rules/*`
- [x] Task 1b-2: Per-file review + port of the domain-neutral workflows
  - Acceptance: each ported workflow re-read line-by-line; dispositions logged in `SCRUB-PROTOCOL.md`
  - Verify: greps clean; each file states its trigger clearly
  - Files: `digi-brain/template/workflows/*`
- [x] Task 1b-3: Per-file review + port of the domain-neutral agents
  - Acceptance: no project refs; each agent states role, inputs, outputs, done-criteria
  - Verify: greps clean
  - Files: `digi-brain/template/agents/*`
- [x] Task 1b-4: Skills strategy - decided: harness-native manifest (`template/SKILLS-MANIFEST.md`), no shipped pack
  - Acceptance: decision recorded in `SPEC-digi-brain.md`; no action without it
  - Files: `digi-brain/SPEC-digi-brain.md`

### Checkpoint: skeleton complete
- [ ] Structure matches spec; greps clean; owner reviews + approves

## Phase 2: Installer + cold-boot proof (private repo)

- [x] Task 2-1: `git init` digi-brain (private), first commit (commit `7411407`, 39 files, no remote)
- [x] Task 2-2: Write installer spec (`SPEC-installer.md`): scaffold script, placeholder substitution, boot verification
- [x] Task 2-2b: Build `installer/install.ps1` + `install.sh` + `BOOT-CHECKLIST.template.md`; mechanics-tested via pilot install to temp (zero unresolved tokens, substitution + code-graph-deletion proven; `--defaults`/`--answers-file` added after NonInteractive finding)
- [x] Task 2-3: Pilot install on a scratch repo; cold-boot test with no owner in the room
  - Ran THREE fresh-context agent boots (pilot/pilot5/pilot6): run 1 found 13 defects (4 boot-blockers), run 2 retest found 2 blockers + 10 minors, run 3 verdict PASS - "boots without improvisation".
  - Fixed along the way: installer rename no-op, doubled-key substitution corruption, 2-arg DATABASE call, NonInteractive support (--defaults/--answers-file), token/banner hygiene, ASCII-only, stack-swap note, naming glossary.
  - Acceptance: turn-1 gate fires, log appends, autonomy gates hold - PROVEN (pilot5/pilot6 logs).
- [x] Task 2-4: First harness adapter (opencode) + adapter interface doc (`adapters/ADAPTER-INTERFACE.md` + `adapters/opencode.md`)

### Checkpoint: installable + proven
- [ ] Cold-boot passes; owner reviews; publish decision (license + account) recorded

## Phase 3: Public + persona (publish only after Phase 2 gate)

- [x] Task 3-1: Secret sweep + adversarial re-read of the entire repo (sweep clean; full `install.ps1` re-read; usage-line fix)
- [x] Task 3-2: Publish - LIVE at `https://github.com/keemyhas/Digi-Brain` (commits `7411407` + `d09822d` + `f97cfda`, branch `master`, MIT LICENSE). Note: repo created as `Digi-Brain`; remote set to canonical URL.
- [x] Task 3-3: `persona-trainer` spec (divergence log -> JSONL export schema) + reference exporter
  - Shipped: `SPEC-persona-trainer.md` (schema `digi-brain-divergence-pair-v1`), `exporter/export-persona.ps1` (parser-clean, fixture test green at exact 1/2/1 split, self-validating), `exporter/test-fixture.md`. POSIX port deferred (no shell to test). Found + fixed: `$Input` automatic-variable collision.
- [x] Task 3-4: Remaining harness adapters - shipped as DRAFT-unverified (`adapters/antigravity.md`, `claude-code.md`, `codex.md`, each with verification-debt checklist). Rule: banners come off only after a cold-boot pass on that harness.

## Phase 4 (new): Reporter CLI (optional writer; augment, don't replace)
- [x] Task 4-1: Doubt cycle on the reporter proposal (fresh-context adversarial review -> reconcile; verdict: augment-don't-replace).
- [x] Task 4-2: Cross-model review offered (CLIs absent on this machine - surfaced, not skipped); owner pasted packet externally; findings reconciled (atomic-append, quarantine scope, shim retention, mirror fan-out, precedence rule).
- [x] Task 4-3: `SPEC-reporter.md` (10 hard requirements, command contract, fixture plan). Implementation (`reporter/db.py`) NOT started - needs explicit order. Amended post-cross-model review: true-append formalism, stdin timeout, split verify (warn history / gate new), checksum framing + boot spot-check, 3.6 syntax ceiling + floor check.
- [x] Task 4-4 (SUPERSEDED by owner decision 2026-10-11): `reporter/db.py` was implemented,
  tested 11/11, dual-path proven - then retired and deleted. Rationale: convention over code;
  agents write Markdown directly, `rules/project-logging.md` enforces; Python reserved for
  read-only export/scaffold needs only. Design preserved in `SPEC-reporter.md` (superseded).

## Post-public: autonomous graduation (owner request 2026-10-12)

- [x] Activation command + graduation readiness gate (rain.md section 6a, BOOT-CHECKLIST autonomy check, README graduation note). Owner-absent work unlocks only on: real profile, 10+ log entries incl. a correction, live roadmap, one proven cold-boot.
