---
name: aec-dashboard-engineering
description: Build or refine AEC engineering dashboards with parametric geometry, Three.js views, deterministic solver outputs, ULS/SLS evidence, BIM exports and RFEM connectivity. Use for NEXUS control decks, cable/beam/slab dashboards and Excel-to-web interfaces. Distinguish demonstrations from verified live results.
---
# AEC Dashboard Engineering

## Contract
Input: use case, geometry/load units, normative profile, source hashes, solver
contract, target runtime and acceptance criteria.
Output: runnable source, reproducible build, data contract, tested critical
interactions and evidence-linked status. Never invent completion percentages.

## Execute
1. Inspect repository, existing UI and governance before editing. Reuse source
   and hosting. For a new hosted website use the available Sites workflow.
   Select one executable engineering slice before expanding scope.
2. Separate UI/3D, orchestration, deterministic solver, knowledge registry and
   external adapters. Keep credentials in backend/local secret storage. Never
   expose keys in browser code or expose workstation gRPC directly to browsers.
3. Define a versioned JSON envelope using [dashboard-contract.md](references/dashboard-contract.md).
   Track project/run, input hash, model fingerprint, calculation, combination,
   solver version, normative edition/annex, units and evidence hashes.
4. Display source/time, connectivity, calculation, engineering QA and human
   acceptance independently. Show absent values as unavailable. Input changes
   invalidate old results. Keep DEMO visibly labeled; never relabel it LIVE
   through a button. Require a real current adapter receipt for live values.
5. Build responsive parameter inputs, model/loads/supports, combination selector,
   governing values, diagrams, sources and audit view. Support keyboard use,
   dispose Three.js resources and provide a useful WebGL fallback.
6. For EC checks retrieve actual clauses with edition/NAD-AT; preserve formula,
   notation and tables. Filter domain/edition before semantic ranking and cite
   chunk IDs. Similarity alone is not proof of relevance. Refuse unsupported
   normative claims. For Excel use the spreadsheet workflow: inspect formulas,
   ranges, cached-value freshness, applicability and reference benchmarks.
7. Test solver-bound inputs, stale-state invalidation, unit conversions and
   failure states. Verify IFC/DXF roundtrips retain IDs, units and topology.
   A picture is not evidence of a correct analytical model.
8. Verify desktop/mobile layouts. Commit on the authorized feature branch,
   provide review PR/tests/blockers. Do not merge or grant engineering release.

## Evidence guard
Read [source-lessons.md](references/source-lessons.md) for the supplied Colab.
A syncRFEM6 function returning a computed percentage/alert without a backend
receipt is simulation. Colab localhost checks observe the Colab machine only.
