---
name: control-panel-technical-review
version: 0.1.0
date: 2026-11-25
status: PROPOSED_REVIEW_PENDING
registration_status: REGISTRATION_PENDING
release_status: NO_RELEASE
review_status: NOT_RUN
scope: sanitized technical review snapshot
---
# AEC Control Panel — technical implementation review

This is a public-safe, derived technical summary, not a byte-identical copy of the internal Word report or conversation. The document authority and private source references remain in the authorized document store. No private source links, project data, GPT configurations, normative text, credentials, account identities or internal conversation transcript are included. No production deployment or technical approval is asserted.

## 1. Management summary
Reuse the existing platform and registry, rather than creating a competing master index. Integrate three user-facing layers: Knowledge Hub (source-bound search and relations), Engineering Workbench (validated solver inputs, execution, visualization and reports), Control Plane (work orders, evidence, capability, synchronization and release gates).

## 2. Architecture
Source identity and revision → metadata inventory → deterministic parsing → knowledge-object candidates → independent review → derived retrieval and graph projections → versioned service adapters → authorized application execution. Use local SSD SQLite/FTS5 with a single writer; evaluate PostgreSQL/pgvector for online retrieval. A graph projection does not require a separate graph database for the pilot. REST and MCP adapters should share the same authorized service logic. Pin solver and parser versions; use server-side access control, no generic SQL/shell endpoint or public exposure of local services.

## 3. Technical gaps
- Source refresh must be distinguished from UI refresh and show stale state on failure.
- Delivery, ACK, review, registration and human approval are independent receipts.
- Legacy code mining needs full raw-byte SHA-256, source locators, deterministic ordering, explicit error receipts and Hamming-distance comparison of SimHash candidates; no destructive deduplication.
- Source licensing and ACLs must precede indexing and export. Private data remain in approved storage.
- Engineering results require applicable norm edition, national annex, units, limits, independent reference tests and approval by the responsible human.

## 4. Proposed work packages
A. Platform and sync: extend existing issue #73 and existing sync workflows. Demonstrate three real E2E cases (delta, idempotent retry, conflict/failure), readback, stale/error signaling, denial of unauthorized access, and local runtime acceptance. Never bypass failed OAuth or soften evidence gates.

B. Knowledge and application catalog: extend the existing GPT migration project. Preserve identifiers, revisions, source manifests and original files; map reusable capabilities to versioned skills, source references, runner contracts and tests. Validate retrieval against curated queries; mark missing raw bytes, ownership and permissions explicitly. Do not activate or delete original GPTs automatically.

C. Engineering vertical slice: use a bounded timber-concrete-composite design case as the first pilot. Package SKILL.md, workflow.yaml, schemas, solver, source/formula metadata, independent benchmarks, tests, diagrams and report. Compare discrete and approximate methods only within their justified domains; define numerical tolerances before testing. Do not equate cross-method agreement with normative validity. Later extend to other domains using the same contracts.

## 5. Proposed acceptance
Three real platform E2E cases; complete pilot provenance or explicitly recorded gaps; at least 30 curated retrieval queries, proposed Recall@10 >= 0.90 and metadata/FTS p95 < 1 s on documented hardware; engineering reference cases with predeclared tolerances; authorized browser run and output readback. These are targets, not measured performance or certification. No merge or release solely on this summary.

## 6. Reusable decision protocol (condensed)
1. Recover historical infrastructure audits and reconcile inventories using stable identities, not folder numbers or names.
2. Map reusable sources, GPTs, scripts, formula libraries and benchmark candidates to existing registry contracts.
3. Prioritize a small executable vertical slice before expanding the application catalog.
4. Reuse existing control-panel, sync and local-runtime components; keep failures visible.
5. Preserve the full internal report and internal conversation summary in authorized document storage; publish only this minimized review snapshot.
6. Route work-package extensions through existing tickets, obtain real executor ACKs, independent technical reviews, correction/re-review, and final human approval.

No new canonical registry, no change to governance, no automatic deployment. This snapshot is documentation only; its presence is not evidence that a work order has been delivered, accepted or implemented.
