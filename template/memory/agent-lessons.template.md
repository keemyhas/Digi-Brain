# Engineering Lessons ... Durable Knowledge
<!-- APPEND-ONLY: new entries go at the bottom. Never edit past entries. Enforced by rules/project-logging.md; the reporter CLI (	ools/db.py) enforces it structurally. -->

> Setup: no placeholders. Numbered, append-only in spirit (never rewrite a lesson - supersede with a new number). Seed below with the starter set; add yours as they are earned.

### Lesson 001: Respect the blast radius

- Every fix gets a neighbor audit: if an anti-pattern bit once, search all sibling implementations before declaring done.

### Lesson 002: Never patch symptoms

- Diagnose root cause, record why it was possible, and check whether the same class exists in other domains.

### Lesson 003: No autonomous git writes

- Never `git commit` or `git push` unless the owner explicitly orders it. Prepare locally; wait for the order.

### Lesson 004: Tests must never touch live data

- Disposable fixtures/databases only, created and destroyed deterministically by the test run.

### Lesson 005: Verify in the running system

- "Implemented" means observed working in the live environment, not merely edited in source.

### Lesson 006: {Your lesson here}

- {Principle + AI interaction directive}
