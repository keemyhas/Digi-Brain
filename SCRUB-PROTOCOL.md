# Digi Brain Scrub Protocol — how "no fingerprint" is achieved and proven

> Read this before porting ANY file from the source corpus. Scrub first, content second. When in doubt, template it out.

## 1. Fingerprint classes

| Class | What it is | Examples from source corpus (evidence, do NOT ship) | Rule |
|---|---|---|---|
| **F1 — Identity** | Names, alter egos, roles, credentials of people | Founder name(s), "Lead Architect & Founder", alter-ego code-names, persona titles | Replace with `{{OWNER_NAME}}` / `{{OWNER_ROLE}}`; activated-twin name becomes `{{TWIN_NAME}}` orDrop |
| **F2 — Project/product** | Product names, former names, domains, company refs | Product + former product names, LAN hostnames, marketing URLs, tier/edition names | Replace with `{{PROJECT_NAME}}`; drop all URLs/hostnames |
| **F3 — Anecdote** | Dated stories tying a trait to a specific incident | "following the `highlightText` modal bug…", dated session logs, per-commit history with SHAs | Never port anecdotes. Keep the *principle*, delete the *story*. History files ship as empty templates |
| **F4 — Secrets/credentials** | Passwords, tokens, connection strings, cert refs | Real finding: default test credentials sitting in a memory file (values redacted — never quote them, even as "evidence"), cert bundle paths, DB names, LAN IPs, ports | Zero-tolerance: drop, never placeholder. Secrets don't get `{{PLACEHOLDERS}}` — they get deleted |
| **F5 — Infrastructure/locale** | Vendors, gateways, locales, currency, national schemes | Payment/identity gateways, national-infra acronyms, currency symbols, city/country refs, `localhost:<port>`-style origins | Generalize ("payment gateway", "national ID provider") or drop |

## 2. Per-file disposition (source corpus: 20 memory + 8 rules + 10 workflows + 11 agents)

**Memory (20): ship as templates only — never verbatim.**

| File | Disposition | Notes |
|---|---|---|
| `brain.md` | Generalize (done: `template/memory/brain.md`) | Keep anatomy; replace clinical brainstem with generic `{{SAFETY_INVARIANTS}}` slot; tool refs genericized |
| `personalities.md` | Template only | Keep profiling *method* (archetype, decision psychology, evolution log format); drop all profiles/stories |
| `project-log.md` | Template only | Keep Asked/Decided/Why/Shipped format + append-only contract; drop all entries |
| `roadmap.md` | Template only | Keep Kanban (§0 NOW/NEXT/LATER/DONE) convention; drop all eras/tiers/dates |
| `decisions.md` | Template only | Keep ADR format; drop all ADRs (note: source ADRs also live in `docs/adr/` — out of scope) |
| `patterns.md` | Template only | Keep section scaffolding (backend/frontend/data/realtime); drop all code samples (owner rewrites for their stack) |
| `bugs.md` | Template only | Keep post-mortem format (Symptom/Root cause/Resolution/Prevention); drop all bugs |
| `agent-lessons.md` | Template only | Keep numbered-lesson format; drop all lessons incl. F4 credential blocks |
| `architecture.md` | Template only | Keep "system overview" scaffolding with stack-agnostic prompts; drop all domains/topology |
| `api-contracts.md` | Template only | Keep endpoint-table format; drop all routes |
| `clinical-workflows.md` | **Drop** (domain pack candidate) | Healthcare-specific; may return as optional `domain-packs/healthcare/` in Phase 3 |
| `database.md` | Template only | Keep headings; drop engine/schema specifics |
| `design-language.md` | Template only | Keep token-hierarchy method; drop palette/values |
| `product-knowledge.md` | **Drop** | Pure product marketing; owner writes their own |
| `security.md` | Template only | Keep threat-matrix *format*; drop all vectors/statuses (owner audits their own) |
| `testing.md` | Generalize | Keep verification-ladder idea; replace framework specifics with `{{TEST_COMMAND}}` |
| `known-issues.md` | Template only | Keep format; empty |
| `session-summaries.md` | Template only | Keep format; empty |
| `graphify-usage-log.md` | **Drop** | Tool-specific log; installer re-creates only if owner uses a code-graph tool |
| `assets/` | **Drop** | Binary/product images never transfer |

**Rules (8): generalize, keep structure.**

| File | Disposition |
|---|---|
| `session-bootstrap.md` | Generalize (done) — generic identity question, working-conditions line |
| `memory-intake.md` | Generalize (done) — generic memory map; single-tree default (dual-sync becomes optional `{{SYNC_RULE}}`) |
| `engineering-standards.md` | Generalize (done) — destructive-ops ban, test isolation, docs bar, no clinical clauses |
| `project-logging.md` | Generalize (done) — format + append-only contract |
| `code-documentation-and-onboarding.md` | ✅ Generalized (stack examples → placeholders; org doc refs → `{{DOCS_DIR}}`) |
| `future-product-planning.md` | ✅ Condensed port (principle + 5-status machine; 900-line source NOT line-ported) |
| `graphify.md`, `graphify-logging.md` | ✅ Merged into optional `code-graph.md` (tool-agnostic; logging optional) |

**Workflows (10): ✅ reviewed 2026-10-11.** Eight domain-neutral flows ported with stack specifics parameterized (`{{TYPE_CHECK}}`, `{{TEST_COMMAND}}`, `{{QA_DIR}}`, `{{FIXTURE_PREFIX}}`); project orchestrator refs → `orchestrator`; safety reviewer → owner-configured `{{DOMAIN_REVIEWER}}` slot. Domain-specific (clinical) reviewer + code-graph-specific workflow → dropped/generalized per table.

**Agents (11): ✅ reviewed 2026-10-11.** Nine domain-neutral specialists ported with scopes/commands/frameworks parameterized (`{{BACKEND_DIRS}}`, `{{TEST_FRAMEWORK}}`, `{{DEV_URL}}`, …); project-named orchestrator → `orchestrator` with safety clause generalized to the engineering standards. Domain-specific (clinical) reviewer → dropped (domain pack).

**Skills:** not ported — reference the harness's native skill system instead (source skills are installation-specific). `TASKS.md` records this decision.

## 3. Verification (must all pass before any Phase 2 step)

```text
1. Fingerprint grep → 0 hits (allowlist: "doctor" in README attribution line only):
   grep -rniE "abdul|hassan|archon|falx|synapse|vellora|synapseems|m\.d\.|ax[o0]n" digi-brain/
2. Secret grep → 0 hits, no exceptions:
   grep -rniE "password|passwd|admin123|api[_-]?key|bearer |mongodb://|postgres://|\.pem|192\.168\.|localhost:[0-9]" digi-brain/
3. Anecdote grep → 0 hits outside blocks marked `EXAMPLE — DELETE` (fictitious values only: fake names, fake SHAs): no real dates, no real SHAs, no session logs, no backticked identifiers from the source codebase.
4. Adversarial re-read: one full pass asking "could someone identify the owner, project, or locale from this?" If yes, cut more.
```

## 4. Standing cautions

- Git history is forever: never let unscrubbed content touch a repo that will go public. Phase 1 stays as loose local files for this reason.
- Anonymized anecdotes re-identify: paraphrasing a story ("a modal bug taught us…") still fingerprints via specificity. Delete, don't paraphrase.
- The README attribution ("medical doctor, part-time developer") is the *only* approved biographical claim. Nothing else about the creator ships.
