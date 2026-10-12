# Code-Graph Rule (optional tool)

> Setup: if you use a code-graph / knowledge-graph tool, fill `{{CODE_GRAPH_*}}`. If not, delete this file - the brain works without it.

## Rules

- On session start, verify the tool is installed and refresh its index so it reflects the latest tree.
- For codebase/architecture questions, query the graph first when an index exists: scoped subgraphs beat raw grep dumps. Fall back to grep when they don't suffice.
- Prefer the tool's guided navigation (index/wiki) over reading raw files for orientation.
- After modifying code, refresh the index (incremental/AST-only if supported).
- Optional: log queries (query text, results, what raw reads were avoided) to `memory/code-graph-usage-log.md` to prove the tool earns its keep. Drop the log if nobody reads it.
