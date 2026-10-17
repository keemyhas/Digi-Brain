# Digi-Brain Hackathon Kit

Everything you need to pitch, demo, and answer judges. All numbers cited here are backed by `docs/` reports in this repository.

---

## 1. The One-Line Pitch

> Give your AI coding agent a memory it can't gaslight: Digi-Brain installs a local-first operating memory, policy, and enforcement engine into any repo — agents remember who you are, never silently break invariants, and pick every session up where the last one ended.

**Alternate (shorter):** An installable brain for AI coding agents. Local, auditable, injection-hardened, and guaranteed to survive a reboot — sessions, memory, momentum.

## 2. 30-Second Script

1. "Every developer pairing with AI hits the same wall: each session starts from zero — the agent forgets decisions, re-litigates settled choices, and can silently commit bad code." (pain)
2. "Digi-Brain installs a persistent, anatomically-organized memory plus a policy engine into your repo with one command." (solution)
3. "It's not prompt sprinkles: it's three layers — memory informs, policy constrains, enforcement blocks. Git pushes and commits can never become autonomous; every one needs a single-use human grant." (moat)
4. "It's MIT-licensed, 100% local, has a 35-test security suite and a controlled benchmark proving the gains." (credibility)

## 3. The Numbers (cite these)

| Claim | Value | Where to show it |
|---|---|---|
| Test suite | 35/35 passing, deterministic, no mocks | `python tests/run_tests.py` (live) |
| Benchmark completion vs baselines | 100% vs 80% (no memory) / 90% (minimal rules) | `docs/FINAL-SUMMARY.md` §Controlled Benchmark |
| Constraint compliance | 100% (0 unauthorized git executions) | same |
| Token overhead saved by staged retrieval | 50.6% reduction, recall 1.0 | `docs/FINAL-SUMMARY.md` / `docs/BENCHMARK-SPEC.md` |
| Installer speed fix | 1,480-process `sed -i` loop → single `awk` pass: >45s → <1s | `docs/BASELINE-REPORT.md` → `docs/FINAL-SUMMARY.md` |
| Security story | `eval`-based installer injection → eradicated, key whitelist, staging + rollback, 6-check verify | `docs/BASELINE-REPORT.md` → `docs/SECURITY-REPORT.md` |

The before/after security story is your best 60 seconds: show the judge the baseline audit (self-inflicted `eval` injection, destructive installs, weak verification), then show the hardened engine and cancel it live (abort mid-install, target untouched).

## 4. 5-Minute Live Demo

```bash
# 0. Clone (judge's machine, any OS)
git clone https://github.com/keemyhas/Digi-Brain.git && cd Digi-Brain

# 1. Install into a scratch repo — takes under 2 seconds
./installer/install.sh /tmp/demo-repo --defaults        # (Windows: .\installer\install.ps1 -Target .\demo-repo -Defaults)

# 2. Show the product — this IS the demo
cat /tmp/demo-repo/.agents/memory/brain.md               # anatomical memory router (thalamus, hippocampus...)
cat /tmp/demo-repo/.agents/rules/policy-enforcement.md   # 3-layer authority, 6-state authorization machine
cat /tmp/demo-repo/.agents/BOOT-CHECKLIST.md             # the turn-1 identity gate the agent runs on boot

# 3. Verify the install (6 checks: structure, bootstrap, safety, placeholders, fingerprints, secrets)
./installer/install.sh /tmp/demo-repo --verify-only

# 4. Prove the safety net — attempt a hostile install and watch it abort, target untouched
printf 'MALICIOUS_KEY=evil\n' > /tmp/bad.env
./installer/install.sh /tmp/demo-repo --defaults "--answers-file=/tmp/bad.env"   # rejected, whitelisted keys only

# 5. Run the 35-test security suite (68s on CI, no cloud)
python tests/run_tests.py
```

**Show, don't tell, the anatomy map** — open `.agents/memory/brain.md` and walk judges down the table: thalamus = boot, hippocampus = append-only project log, immune system = lessons from past bugs, prefrontal = roadmap + ADRs.

**The reveal moment:** in the target repo, open the agent (Antigravity / Claude Code) — it boots, checks working conditions, and CONFIRMS IDENTITY at turn 1 instead of guessing. That's the emotional beat.

## 5. FAQ (judge-proof answers)

**"Isn't this just a CLAUDE.md?"**
No — CLAUDE.md is one file of instructions; Digi-Brain is a memory operating system: anatomy-routed memory with provenance, append-only logs that can't be silently rewritten, a policy engine with authorization states, and tooling (retrieval router, task-state continuity, secret quarantining). It installs and drops CLAUDE.md and AGENTS.md as *bootstrap pointers* into its own deeper structure.

**"Does it phone home?"**
Never. 100% local-first; no telemetry, no cloud, no accounts. MIT license.

**"Which harnesses work?"**
Antigravity (native `.agents` root) and Claude Code (native `CLAUDE.md`) verified. OpenCode, Codex, and any markdown-aware agent: compatible today via root bootstrap pointers. Gemini CLI and Warp: planned (see TASKS.md).

**"What does an agent actually gain?"**
Session continuity that survives reboots (`task-state.json`), decisions with ADRs, knowledge of what's safe to do alone, graded confidence and provenance — and 50.6% fewer tokens per prompt.

**"Why is it called Digi-Brain?"**
Memory is organized anatomically — thalamus (wake-up), hippocampus (episodic facts), immune system (lessons from past bugs), prefrontal (planning). Agents instantly parse what overrides what.

**"Where's the proof?"**
35/35 tests (the repo), a 10-scenario controlled benchmark (docs/FINAL-SUMMARY.md), a baseline security audit that documents our own defects and their hardening (docs/BASELINE-REPORT.md), and a verified CI matrix on Linux + Windows across 3 Python versions.
