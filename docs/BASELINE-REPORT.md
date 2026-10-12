# Digi-Brain Baseline Audit Report

Date: 2026-10-12
Host Environment: Windows 11 (PowerShell 5.1, GNU bash 5.3.9 via Git for Windows, Python 3.13.13)
Git Commit Baseline: a12b1ba (master, clean working tree)

## 1. Initial State Summary
The repository contains the initial Digi-Brain skeleton across templates, rules, specifications, draft adapters, and rudimentary installer/exporter scripts.

## 2. Baseline Test Execution
- **Existing Test Suites**: None found in repository.
- **Manual Test Fixture**: `exporter/test-fixture.md` executed with `exporter/export-persona.ps1`.
  - Execution Result: PASS (`rows=4 written=1 skipped=2 quarantined=1`).
  - Output: Single JSONL record created, but created via string concatenation.
- **Installer Baseline**:
  - `installer/install.ps1`: Executes with `-Defaults` on temporary directory.
  - `installer/install.sh`: Stalled due to 1,480-process `sed -i` nested loop on Windows/Cygwin environments.
  - Verification: `--verify-only` only checked placeholder tokens (`{{...}}`). Fails to check structure, bootstrap checklists, rules, secrets, or fingerprints.

## 3. Vulnerability and Defect Discovery
1. **Critical Injection in `install.sh`**:
   - `ask()` uses `eval` for variable assignments and answers file parsing.
   - Variable substitution uses dynamic evaluation `eval`.
   - Malicious answers files or prompt responses (e.g. `Ada; touch /tmp/pwn`) trigger arbitrary shell execution.
2. **Missing Input Whitelisting in `install.ps1`**:
   - Arbitrary lines in `--answers-file` parsed into `$AnswerMap` without key whitelist validation.
3. **Destructive Installation / Lack of Rollback**:
   - Both installers execute destructive cleanup before verifying rendered output. If verification fails, the target `.agents` is deleted or left half-rendered.
4. **Weak Verification**:
   - Verification only checks placeholder regex. It does not check required core files, safety invariants, secret heuristics, or fingerprint markers.
5. **Lack of Enforceable Authorization Model**:
   - Autonomous mode triggered solely by keyword matching. Quoted phrases in code or docs can trigger false activation.
   - No distinction between technical enforcement (Layer C), policy boundaries (Layer B), and memory content (Layer A).
6. **Unstructured Memory Without Provenance**:
   - Memory templates do not track author/source class (user vs agent vs untrusted import), confidence levels, or supersession history.
7. **No Migration Path**:
   - No utility exists to migrate or validate existing `.agents` memory trees safely.
