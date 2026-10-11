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
- [ ] Task 3-2: Publish (explicit owner order GIVEN 2026-10-11; local commits `7411407` + `d09822d` ready; remote `origin` set; BLOCKED: repo `keemyhas/digi-brain` does not exist yet and agent token lacks repo-create scope - owner creates it, agent pushes)
- [ ] Task 3-3: `persona-trainer` spec (divergence log -> JSONL export schema) + reference exporter
- [ ] Task 3-4: Remaining harness adapters, one at a time (antigravity, claude-code, codex, ...)

### Checkpoint: public
- [ ] Repo live, installs clean on a foreign machine, first external pilot logged
