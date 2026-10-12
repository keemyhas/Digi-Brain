# Spec: Reporter CLI (`reporter` module) - SUPERSEDED 2026-10-11, DO NOT IMPLEMENT

> Decision: agents write Markdown directly with native file tools; enforcement lives in
> conventions + `rules/project-logging.md`, not code. The reference implementation was
> built, tested 11/11, and dual-path proven - then retired: the failure modes it guarded
> (malformed entries) never materialized in three cold-boots, while its costs (runtime
> dependency, shell-sandbox friction, cold-boot circularity) were concrete. Preserved here
> as the full design record in case export/scaffold needs ever justify a CLI.
>
> Standing rule: Python earns a place in digi-brain only for read-only tooling
> (`export --jsonl` for downstream use,answered today by `exporter/export-persona.ps1`)
> or installer scaffolding (answered today by `installer/install.ps1` + `install.sh`).
> Write access stays with the agents, not a CLI.

## Objective

A vendored single-file stdlib-only `tools/db.py` per repo that structures memory writes
(`log`, `bug`, `lesson`, `trait`, `verify`, `export`) without replacing Markdown hand-editing.
Markdown files remain the sole readable store, the boot path, and the documented fallback.
Emerged from: owner proposal (Python reporter instead of md writing) -> doubt-driven review
-> cross-model review -> reconciled verdict (augment, don't replace). All review findings
below are requirements, not suggestions.

## Assumptions

1. Python 3.6+ where available; absence is normal, never an error (probe + degrade).
   Syntax ceiling: 3.6-compatible code only (f-strings OK; no `match`, no `tomllib`, no
   version-sensitive stdlib). Runtime floor check aborts cleanly to hand-edit on violation.
   "Stdlib-only" never meant "version-invariant" - the floor + ceiling make it so.
2. One file, stdlib only, pure ASCII source (PS-5.1-class parsers and varied readers safe).
3. UTF-8 everywhere, LF line endings on write, regardless of platform.
4. Local only: no network, no exfiltration, writes sandboxed to the repo (+ configured mirrors).

## Hard requirements (from review reconciliation)

1. **True append, never rewrite.** Open files in binary append mode, single `write()` per entry.
   Read-rewrite-replace cycles are forbidden (a temp-rename scheme loses concurrent writers'
   entries on every platform - POSIX and Windows alike). Best-effort lockfile is secondary,
   not primary.
2. **Write-then-verify.** After every append, read back the tail and confirm the entry landed
   intact; on mismatch, report loudly (do not retry blindly, do not touch history).
3. **Precedence: hand-edit first.** Boot reads Markdown directly, always. CLI is writes-only,
   used only after a successful interpreter probe (`python3 --version` once per session).
   One CLI attempt: on any failure, fall back to hand-edit immediately - no retry loops,
   no environment repair spirals.
4. **Prose enters via file, not shell.** `--from <utf8-file>` is the default input mode;
   stdin only with explicit UTF-8 reconfigure AND a read timeout (EOF or timeout aborts to
   hand-edit - a hung stdin must never duplicate entries via harness retries). Scratch files
   live in system temp and are deleted on success AND failure (try/finally). Shell-quoted
   prose is forbidden.
5. **Newline discipline.** Before appending, ensure the file ends with exactly one `\n`;
   never alter existing bytes. No CRLF/LF churn: write LF always.
6. **Quarantine touches nothing historical.** Scrub failures refuse the NEW entry (report +
   let the agent fix the prose) or skip bad rows in EXPORTS (report counts). Existing
   history is never moved, stripped, or renamed by any subcommand.
7. **Mirror fan-out.** Read the repo's sync rule (written by the installer); every append
   fans out to all mirrors and verifies by hash. Single-tree default = today's behavior.
8. **`verify` warns on history, gates the new entry.** History audit is warn-only (a past
   typo must never brick logging). But every NEW entry is validated in memory BEFORE append
   and refused if structurally broken (missing required fields, bad framing). Nothing valid
   is ever blocked; garbage is never admitted.
9. **Installer shims stay.** The CLI absorbs writer/verifier/exporter logic only. Thin
   platform launchers (env check, interpreter resolution `python3`/`py -3`/`python`) remain.
10. **Minimal schema envelope, free-form bodies.** `{type, date, body...}` versioned
    (`db-v1`), additive changes only. Unknown schema versions abort to hand-edit explicitly -
    never guess. No code release required to evolve documentation prose.
11. **Path confinement.** Every file argument (`--from`, `--out`, export input, mirrors) must
    resolve inside the repo root (symlink escapes refused). "Local only" covers local
    movement too, not just network.

## Entry framing (added from cross-model review)

Every appended entry ends with a checksum line over its own bytes:

```text
## YYYY-MM-DD - <title> (commit <sha>) - <who>
- Asked: ...
- Decided: ...
- Why: ...
- Shipped: ...
- checksum: <sha256-of-the-entry-lines-above>
```

The checksum makes interleaved/concurrent writes DETECTABLE (read-back verification) and
gives boot a spot-check: entries whose checksum fails are treated as suspect - stop and ask
the owner, never operate on suspect memory. Bodies can contain anything (including `---`
and headings) because framing is positional + checksummed, never delimiter-guessed.
Machine-generated framing lines are exempt from prose-style rules; human body text stays free-form.

## Commands (contract-first sketch)

```text
db log --from <file>          append Asked/Decided/Why/Shipped entry (fields validated, body free-form)
db bug --from <file>          append post-mortem (symptom/root/resolution/prevention required)
db lesson --from <file>       append numbered lesson
db trait --from <file>        append personality trait observation
db verify                     warn-only audit: tokens resolved, files present, mirrors in sync
db export --jsonl             divergence table -> schema'd JSONL (same contract as SPEC-persona-trainer.md)
db probe                      interpreter + write-permission check; records result for the session
```

Error semantics (single format): `DB-OK: <what + where>` / `DB-FAIL: <what> | reason | next step (always: hand-edit the file directly)`.

## Project structure (not built in this spec)

```text
digi-brain/
+-- SPEC-reporter.md         -> this file
+-- reporter/
    +-- db.py                -> reference implementation (stdlib only, ASCII only)
    +-- test-fixture/        -> append-atomicity, newline, quarantine, mirror tests
```

## Testing strategy

- Fixture suite: concurrent-append simulation (no lost entries), missing-trailing-newline file, CRLF-mixed file (no churn beyond appended bytes), secret-bearing entry (refused + reported), multi-mirror fan-out with hash check, no-Python environment (clean degrade to hand-edit).
- POSIX/Windows line-ending matrix on every change.
- No POSIX-shell port problem by construction (Python is the portability layer), but no untested claims: fixture suite must pass on this machine before merge.

## Boundaries

- **Always:** spec requirements 1-10 above; every behavior in this spec ships with a fixture test.
- **Ask first:** new subcommands; new required fields; touching installer shim responsibilities.
- **Never:** rewrite history; block logging on verify failures; transmit data; require pip packages; promise harness behavior not cold-boot proven.

## Success criteria

- [ ] Fixture suite green on Windows (this machine).
- [ ] Cold-boot agent uses `db log` post-probe AND hand-edit fallback in one session each.
- [ ] Zero diff churn beyond appended bytes on all fixtures.
- [ ] Owner review before merge.

## Open questions

1. Lockfile shape (name, stale-lock timeout) - decide at implementation, fixture-proven.
2. Whether `scaffold` (installer logic in Python) ever migrates - explicitly NOT this spec; revisit after writer proves itself.
