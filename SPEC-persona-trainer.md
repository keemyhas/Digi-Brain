# Spec: Persona Trainer (`persona-trainer` module)

## Objective

Export an owner's recorded preferences as labeled training pairs, so a future personal AI can learn how the owner decides. Input: the twin divergence table (`personalities.md` twin section: twin's pick vs owner's correction per row) + the trait evolution log. Output: JSONL, one pair per row. This was the deferred SPEC-digi-brain open question 4 - resolved here.

## Assumptions

1. The owner used activated-twin mode enough to accumulate divergence rows (sparse tables export sparsely - no synthesis, no invention).
2. Export is lossy by design: only explicit pick-vs-correction rows qualify. Trait prose is context, not labels.
3. No PII beyond what the owner already recorded; the exporter adds a scrub pass (secret patterns) and quarantines hits.

## Schema: `digi-brain-divergence-pair-v1` (one JSON object per line)

| Field | Type | Required | Meaning |
|---|---|---|---|
| `pair_id` | string | yes | Stable: `div-<YYYYMMDD>-<NN>` from row date + order |
| `schema` | string | yes | Always `digi-brain-divergence-pair-v1` |
| `date` | string | yes | Row date (`YYYY-MM-DD`; `unknown` if absent) |
| `twin_pick` | string | yes | What the twin chose (verbatim cell) |
| `owner_correction` | string | yes | What the owner chose instead (verbatim cell) |
| `lesson` | string | no | Recorded lesson cell (omitted when empty) |
| `context` | string | no | Surrounding trait/decision reference when the row links one |

Example:

```json
{"pair_id":"div-20261011-01","schema":"digi-brain-divergence-pair-v1","date":"2026-10-11","twin_pick":"Link the NOW card to the boot checklist","owner_correction":"Create a docs brief and link that instead","lesson":"Cards link to briefs, never to tooling","context":"roadmap conventions"}
```

## Exporter behavior (`exporter/export-persona.ps1`; POSIX port deferred, see below)

1. **Locate**: `<repo>/.agents/memory/personalities.md` (flag `--input` overrides).
2. **Parse**: twin divergence table rows (`| date | pick | correction | lesson |`-shaped tables under the twin heading). Skip header/separator rows, skip rows with an empty pick or correction, skip `{...}` placeholder cells.
3. **Scrub**: drop any pair matching secret patterns (tokens, keys, connection strings); report counts.
4. **Write**: `<out>.jsonl` (default `persona-pairs.jsonl` next to input); one object per line, UTF-8, LF.
5. **Report**: rows read / pairs written / skipped (empty/placeholder) / quarantined (scrubbed).

## Commands

```text
Export:  ./export-persona.ps1 -InputPath .agents/memory/personalities.md [-Out persona-pairs.jsonl]
Validate: each line parses as JSON and carries all required fields (exporter self-checks; aborts on violation)
```

## Testing strategy

- Fixture: `exporter/test-fixture.md` (4 rows: clean pair, empty-correction skip, `{...}` placeholder skip, secret-bearing quarantine) → expect exactly 1 pair out, 2 skipped, 1 quarantined.
- Schema stability: v1 fields are append-only; new optional fields need a minor version note in this spec.

## Boundaries

- **Always:** verbatim cells (never paraphrase - the label IS the wording); scrub pass; deterministic pair_ids.
- **Ask first:** including trait prose as context (default: only when the row explicitly links it).
- **Never:** invent pairs from prose; export placeholder/example rows; transmit pairs anywhere (local file only).
- POSIX port: spec'd identically, implementation deferred until a POSIX shell is available to test it (no untested exporters ship).

## Success criteria

- [ ] Fixture test green (1/2/1 split).
- [ ] Exporter self-validates output (parse + required fields).
- [ ] Zero secrets in output on the fixture and on a real log.
- [ ] Owner review before any training use.

## Open questions

1. Weighting (correction recency/frequency) - deferred to training-time, not export format.

## Schema: `digi-brain-divergence-pair-v2` (Enhanced Scoped Format)

Adds contextual scoping to prevent project-specific corrections from becoming universal preferences:

| Field | Type | Required | Meaning |
|---|---|---|---|
| `pair_id` | string | yes | Stable identifier: `div-<YYYYMMDD>-<NN>` |
| `schema` | string | yes | `digi-brain-divergence-pair-v2` |
| `date` | string | yes | Row date (`YYYY-MM-DD` or `unknown`) |
| `twin_pick` | string | yes | What the twin chose |
| `owner_correction` | string | yes | What the owner chose instead |
| `scope` | string | yes | `project` vs `universal` vs `domain:<name>` |
| `decision_category` | string | yes | `workflow`, `architecture`, `testing`, `style` |
| `review_status` | string | yes | `verified`, `unreviewed`, `quarantined` |
| `lesson` | string | no | Extracted principle |

## Implementations & Privacy Defense

Dual implementations share this specification:
1. `tools/export_persona.py` (POSIX / Python 3 CLI)
2. `exporter/export-persona.ps1` (Windows PowerShell 5.1 CLI)

### Secret Scanning & Quarantine
- Evaluates each record against credential and private token patterns (API keys, JWTs, AWS credentials, database URIs, private keys).
- Matches are **quarantined** to `<out>.quarantine.jsonl` with row index and trigger reason.
- Quarantined records are omitted from training datasets for owner review.
- Strict local-first processing: never transmitted to external services.
