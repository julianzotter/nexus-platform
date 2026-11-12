# NEXUS Connector Audit and Roadmap - Run 2026-11-12
Status: PARTIAL_VERIFIED | Deployment: NOT_REQUESTED | Source policy: read-before-write
Owner: NEXUS Controller | Workstream: MCP / Data Integration / Multi-LLM

## Executive findings
- GitHub access-points/registry.json exists on main (20 catalog entries, all previously marked not_verified). Live read succeeded; registry statuses remain historical and must not be overwritten without endpoint-specific tests.
- Access Point Navigator skill and WORKORDER already exist; reuse them rather than building duplicate registries.
- Google Drive WORK canonical folder ID: 1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP.
- Latest source roadmap: 26_11_11_NEXUS-FULL-MAS-Roadmap.md (Drive ID 1Z-a6vnnhXjL_2ibYZ7nxVe7dcjt_Mv2r).
- Existing status report: 26_11_11_QUICK-STATUS-REPORTS_JULIAN-ZOTTER_ID01_NEXUS-HARNESS.md (Drive ID 1_NN1l80fm68X8Qx6p6BxSt5D3tGTDMUP).
- GitHub main repository and 5 related NEXUS repositories discovered. SharePoint connector returned OneDrive NEXUS records; SharePoint site-wide indexing remains untested. Notion NEXUS search returned zero hits, not proof of absence.
- Multiple same-named Drive blueprints/work bundles need canonical ID and hash checks.
- Existing FULL-MAS design specifies FastMCP gateway, PostgreSQL/pgvector, DAG scheduler and WORK_BUS; implementation and production readiness not verified.

## Connector test matrix
| Connector | Evidence | Verified scope | Gap |
|---|---|---|---|
| GitHub | fetch_file access-points/registry.json | authenticated read | write/CI not tested |
| Google Drive | search and fetch WORK reports | authenticated read | write/readback pending |
| Microsoft Graph | OneDrive search_drive_items | authenticated search | SharePoint site traversal and write |
| Notion | search NEXUS -> [] | search executed | workspace coverage |
| Dropbox | mounted library root detected | mount presence only | provider read/write |
| RFEM MCP | existing catalog entry | documentation only | runtime connectivity |
| IFC / DXF | existing catalog entries | documentation only | parser execution |

## Roadmap / work orders
P0 (12-15 Nov): baseline compare, access registry inventory, WORK reporting audit, GitHub CI status and delivery receipts.
P1 (16-22 Nov): scoped connector read tests, ACLs, canonical source IDs, modified-time delta sync, SHA-256 duplicate checks.
P2 (23-29 Nov): knowledge objects, provenance anchors, SQL/FTS5 vs pgvector benchmarks, graph relationships.
P3 (30 Nov-11 Dec): GPT historical inventory reconciliation, migration factory, multi-LLM Source/Ingest/Engineer/Critic/Verify agent evaluations.
P4 (from 12 Dec): RFEM read-only pilot, CI retries/dead-letter, gateway JWT/TLS checks, deployment only with explicit human approval.

## Implementation decisions
1. Extend existing access-points/registry.json; distinguish catalogued, authenticated, read_tested, write_tested, and production_approved.
2. Use Google Drive WORK for work orders/reports; GitHub for versioned code/schema/skill artifacts. Cross-link by immutable IDs and hashes.
3. PostgreSQL for persistent async queue; MCP for bounded synchronous tools; WORK_BUS for auditable file exchange. Keep SQLite FTS5 as local migration index.
4. Do not equate a connector search hit with a live MCP endpoint or production authorization.
5. Never publish raw GPT exports, credentials or confidential engineering files into public repositories.

## Open gates
G1: Compare current GitHub files and CI with FULL-MAS implementation spec.
G2: Verify Drive report write/readback and exact destination.
G3: Verify GitHub PR CI and merge status.
G4: Confirm secure GPT export archive and data access policy.
G5: RFEM/IFC/DXF live adapter tests pending.

## Source pointers
- https://github.com/julianzotter/nexus-platform/blob/main/access-points/registry.json
- https://github.com/julianzotter/nexus-platform/blob/main/access-points/WORKORDER.md
- https://drive.google.com/file/d/1Z-a6vnnhXjL_2ibYZ7nxVe7dcjt_Mv2r/view
- https://drive.google.com/file/d/1_NN1l80fm68X8Qx6p6BxSt5D3tGTDMUP/view
- https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP

Reporting: this is an audit and implementation plan, not a claim of completed runtime integration.
