# Exporter test fixture (fictitious owner: Ada Example - DELETE-equivalent, never real data)

## Twin divergence log (Test Twin)

| Date | Twin's pick | Owner's correction | Lesson |
|---|---|---|---|
| Date | Pick | Correction | Lesson |
|---|---|---|---|
| 2026-10-11 | Link the NOW card to the boot checklist | Create a docs brief and link that instead | Cards link to briefs, never to tooling |
| 2026-10-12 |  | Ship it today | Empty pick - must skip |
| 2026-10-13 | {placeholder pick} | {placeholder correction} | Placeholder row - must skip |
| 2026-10-14 | Use api_key abc123 for the deploy | Rotate the key via vault | Secret-bearing row - must quarantine |

Expected: written=1 skipped=2 quarantined=1 (header + separator rows ignored by the parser).
