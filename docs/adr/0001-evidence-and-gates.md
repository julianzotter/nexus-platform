# ADR 0001: Evidence-first records and human gates

Status: Accepted (proposed by implementation, pending ID-01 review)

## Decision
- Metrics are only measured by tools, never pre-filled; unmeasurable values are `null` with status `INCOMPLETE`.
- Files are written atomically (`.tmp` then replace).
- Work happens on feature branches via PR; agents never merge. ID-01 is the gate.
- The NEXUS-AI-AEC knowledge graph is the system of record for knowledge; this repo holds the registry and evidence, linked by stable IDs.
- Engineering calculations are done by deterministic solvers, not LLMs; norm items track edition and national annex.

## Deferred (need real data first)
Norms register, solvers, skill/agent fabric, self-improvement loop, orchestration. The improvement loop starts only once baseline runs exist; changes are kept only if scores improve, bounded by an iteration limit, rollback and a human gate for solvers/norms.
