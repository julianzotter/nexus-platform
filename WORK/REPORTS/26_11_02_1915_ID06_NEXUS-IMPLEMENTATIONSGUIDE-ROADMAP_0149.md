---
name: NEXUS-IMPLEMENTATIONSGUIDE-ROADMAP
description: Verdict on the NEXUS.* folder claim, gap audit corrections, hierarchical implementation roadmap, Run 1/Step 1 Drive export hard-lock
version: 0.2.0   # 0.1.0 -> 0.2.0: delta after independent review (FAIL -> fixes)
status: ENTWURF_REVIEW_PENDING
author: ID06
reviewers_requested: [ID03, ID07]
human_gate: ID01
ticket_id: WO-20261102-NEXUS-WAYFINDER-01
artifact_no: "0149"
ledger_status: UNRESERVED_PROPOSAL   # 0149 = next free per 00_ID_LEDGER.csv v1.8 (2026-11-01T04:45Z); NOT reserved, ID06 has no ledger write path; ledger writer must confirm or renumber
registration_status: REGISTRATION_PENDING   # file-registry.jsonl append not possible via connector (no content update)
timestamp: 2026-11-02T19:15+01:00
sources: [WORK/Folder.md 11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH, WORK/_AGBS.md v004 10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg, 00_ID_LEDGER.csv 1Uvb89wWOpte3iXWKm3qrg42dEwBb7nuG, nexus-platform@fb103dbe]
---

# NEXUS — Implementation Guide + Roadmap (ID06)

## TL;DR
- Claim "NEXUS.* folders + reports are not integrated; a frontmatter wayfinder is needed" → **largely correct, two corrections** (§1).
- Inventory: **16 NEXUS.\* folders, 212 files, 0/16 with an anchor file** (Folder.md/README/_INDEX).
- Reports live in **4 places**; NEXUS.REPORTS holds only 2 links + 1 duplicated folder.
- Run 1 / Step 1 **PARTIAL**: `tools/nexus_export_lock.py` — server-side, fail-closed Drive export with byte + name readback, per-key lock, authenticated role. **19 new tests pass** (unit + FastAPI router). Real Drive E2E **NOT RUN** (no OAuth in runtime). `nexus_server.py` **not found** (repo + Drive) → integration via `build_router()` (§5).
- Lock is **bypassable until P0** (WORK `anyone: writer`).
- Peer review: independent reviewer (separate context, 3 perspectives) → v0.1 **FAIL** (1 BLOCKER, 6 MAJOR) → 2 delta rounds → **R3 PASS** (§8). External WO to ID03/ID07 in WORK: **PUBLISHED_NOT_ACKNOWLEDGED**.

## 1. Verdict on ID01 claim
| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | Reports are scattered ("Kuddelmuddel") | TRUE | 4 locations: Drive `NEXUS.REPORTS`, Drive `WORK` (ID03 status reports), repo `WORK/REPORTS`, repo `reports/` (duplicate of NEXUS.REPORTS/2026-10-13_parsing-pipeline) |
| 2 | NEXUS.* folders must be searched systematically | TRUE | 16 folders, none has an anchor; only 3 named in docs (Betriebshandbuch v0.2.0 §86, Dossier §73, Usermanual §75) |
| 3 | Without an index they are never integrated | PARTLY | Index = discoverability only. Integration per AGBS v004 §2 requires **file-registry.jsonl** entries. A second register is forbidden → wayfinder must point, not register |
| 4 | Index provided "via the frontmatter files" | CORRECTION | Per ID01 decision 2026-10-31: no new control files, bundle. → generated wayfinder (candidate) + 5-line status frontmatter per folder (R3 anchor rule), promote to `_NEXUS_WAYFINDER.md` only by ID01 |

## 2. Corrections to the "Lateral Critique & Gap Audit" (attachment)
| Audit statement | Correction |
|---|---|
| AnythingSearch.db = SSoT | Wrong for documents: Folder.md `source_of_truth: DRIVE`; GitHub = code (ID01 K-decision 2026-10-27). AnythingSearch.db = read-only search index |
| LangGraph is the state layer | Not evidenced in repo. Use a stdlib SQLite checkpointer first; LangGraph `SqliteSaver` only if LangGraph is adopted |
| Blob download bypasses SSoT | Correct → fixed by Run 1 (§5) |
| Watchdog 500 ms debounce | Correct, insufficient alone: add size+mtime stable ×2, parse-validate, keep last-good |
| Context explosion | Correct → token-budgeted loader (priority tiers, hard cap) |
| **Missing in audit** | WORK folder is `anyone: writer` (Folder.md status SECURITY_BLOCKED) → any write lock is bypassable until ID01 restricts sharing |

## 3. Decomposition + best algorithm per subtask
| ST | Subtask | Algorithm (deterministic) | Reuse first |
|---|---|---|---|
| ST1 | Drive inventory | BFS over `files.list q="'<id>' in parents"`, paginated; incremental via `changes.list` + startPageToken | `tools/drive_changes_poll.py` |
| ST2 | Classification | rule table name→layer (L0–L5); unknown → `UNCLASSIFIED` queue for ID01; no LLM | `tools/nexus_folder_index.py` (new) |
| ST3 | Dedupe | Drive `md5Checksum`+size (no download) → SHA-256 confirm; keep oldest, link others | `tools/detect_duplicates.py` |
| ST4 | Wayfinder | generated MD, YAML frontmatter, pinned `source_inventory_sha256`; same input → same bytes | new, tested |
| ST5 | Registry | append-only JSONL, single writer, CAS on Drive `version` before update, validation gate | `tools/artifact_registry_gate.py` |
| ST6 | Write lock | client submits JSON only; server names file; pre-generated ID + journal + SHA-256 readback; fail closed | `tools/deliver_work.py` + new lock |
| ST7 | Ledger numbers | single allocator service, monotonic counter, CAS; never infer from filenames | open (P0) |
| ST8 | Checkpointing | SQLite WAL table `run_state(run_id, step, state_json, sha256, ts)`; resume = last row with valid hash | new |
| ST9 | Parser robustness | quiet period ≥500 ms + stable size/mtime ×2 → YAML parse → schema check → atomic swap; else last-good | new |
| ST10 | Context budget | priority knapsack: AGBS > Manifest > Baseline > WO > task docs; hard cap; overflow → stored summaries (MUST-160–166) | proposal 2026-10-31 |
| ST11 | EC/FEM chain | LLM → JSON params (schema) → Python solver → ΣV=0, ΣM=0, unit check (pint) → report; LLM never computes | `areas/structural-solver-library` |
| ST12 | Review | EXEC≠REVIEW; 3 perspectives (architecture, governance, systems) per AGENTS.md rule 8; binary measured gates | WO in WORK |

## 4. Roadmap (hierarchical, gate-driven; no phase change without gate PASS)
| Phase | Layer | Runs | Content | Gate (binary, measured) |
|---|---|---|---|---|
| P0 | L0 Governance | R0 | ID01: restrict WORK `anyone:writer`; name ledger writer + allocator; decide wayfinder promotion | sharing ≠ anyone; allocator has 1 owner |
| P1 | L0/L1 I/O | R1 ◐ PARTIAL | server-side export hard-lock (this run); **depends on P0** | unit/router tests PASS ✔; real Drive E2E create + readback hash = local ✘ open |
| P1 | L1 I/O | R2 | mount `build_router()` in nexus_server.py; delete Blob path in TranscriptTimeline.tsx (POST only) | UI test: no `Blob`/`createObjectURL` in bundle |
| P2 | L2 Index | R3 | ST1–ST4 on all LLM-LOCAL-SSOT folders (recursive), per-folder status frontmatter | 100 % folders listed; anchors = folders |
| P2 | L2 Registry | R4 | ST5+ST7: registry appends for wayfinder/report/WO; dedupe ST3 | `artifact_registry_gate` PASS per artifact |
| P3 | L3 State | R5 | ST8 checkpointer + ST9 watcher | kill-test: resume after WS drop, 0 lost steps |
| P3 | L3 Context | R6 | ST10 loader | prompt tokens ≤ cap on 10 reference WOs |
| P4 | L4 Engineering | R7–R9 | ST11 for EC5 HBV γ-method, EC2 RC, cable net; golden cases | Δ vs reference ≤ 0.5 %; ΣV, ΣM residual ≤ 1e-6 |
| P5 | L5 Interface | R10 | S2S Gemini Live, ezdxf export via the same write lock | E2E protocol → Drive receipt |
| P6 | Release | R11 | 3-perspective review, delta fix, re-review, ID01 decision | ID01 signed decision record |

## 5. Run 1 / Step 1 — delivered
**Files** (git branch `id06/nexus-wayfinder-export-lock`, pushed for review; not merged):
- `tools/nexus_export_lock.py` — `ExportRequest` (role_id, theme, ticket_id, markdown, target alias) → `export_protocol()` → `ExportReceipt` only if `DELIVERY_VERIFIED`.
- `tests/test_nexus_export_lock.py` — 17 tests (incl. renamed-Drive-file rejection, CRLF flag): verified receipt; idempotent replay; lost local state → Drive name reused (no new number); trashed target → identity conflict; 8 concurrent identical requests → 1 create; readback mismatch/provider 403 → fail; client folder ID rejected; invalid inputs rejected; Vienna DST naming; HTTP status mapping; router: valid POST, 401 unauthenticated, client `role_id` ignored, 422/409 mapping.
- `tools/deliver_work.py` — find/metadata now also return `name` (2 lines, backward compatible).
- `tools/nexus_folder_index.py`, `tests/test_nexus_folder_index.py` (2 tests), inventory snapshot `registry/drive-inventory/nexus_folders_inventory_2026-11-02.json`.

**Hard-lock properties**
- No client-supplied name/folder/mime/role; target only from `ALLOWED_FOLDERS` (alias→ID); role + session from server-side `principal(request)` (401 otherwise).
- Per-key `flock` (single host) serializes identical exports; multi-host needs a shared lock (open).
- Name = `YY_MM_DD_HHMM_ID##_THEMA_###.md`, Europe/Vienna; number from injected allocator (contract: idempotent per key, globally monotonic); precedence Drive name > sidecar > allocation; Drive name must match pattern AND sidecar; success requires Drive name == reserved name.
- Write path = existing `deliver()`: pre-generated ID, journal, appProperties key, metadata identity check, SHA-256 readback.
- Registry record (AGBS v004 fields) validated by `artifact_registry_gate.validate_record`; status `REVIEW_PENDING`/`REGISTRATION_PENDING`.
- No delete operation exists.

**Integration in nexus_server.py** (file not available to ID06):
```python
from nexus_export_lock import build_router
app.include_router(build_router(lambda: DriveClient(get_access_token()), ledger_allocator,
                                Path('state/export'), principal=resolve_principal))  # persistent volume
```
Client: `fetch('/api/export/protocol', {method:'POST', body: JSON.stringify({...})})`; remove Blob/hidden-link code.

## 6. Tests
| Suite | Result |
|---|---|
| new: export lock (17) + folder index (2) | 19 passed, 6 subtests (fastapi 0.162 installed for router tests) |
| full `pytest tests` on branch | 178 passed, 4 failed |
| full `pytest tests` on clean HEAD fb103dbe | 159 passed, **same 4 failed** (pre-existing; shallow-clone history + catalog drift) |
| real Drive E2E of export lock | **NOT RUN** — no OAuth secrets in this runtime |

## 7. Runbook / deployment contract
- Single replica, journal + sidecar on persistent local disk (not NFS); scale-out → shared lock first.
- Trashed delivered file → every replay of same ticket+content returns `TARGET_IDENTITY_CONFLICT` (409) by design; resolve manually (restore file or new ticket).
- Renamed delivered file → `NAME_MISMATCH` (409); never adopted.
- CRLF is normalized to LF before hashing; receipt flags `line_endings_normalized`.

## 8. Peer-review log (EXEC ID06 ≠ REVIEW independent context)
| Round | Scope | Verdict | Findings | Action |
|---|---|---|---|---|
| R1 | code + tests + report v0.1 | FAIL | 1 BLOCKER (router 422 always), 6 MAJOR (race, lost-state name, self-declared role, status mapping, report overclaim, P0 bypass), 3 MINOR | all fixed / report corrected |
| R2 | delta | FAIL | 1 MAJOR new (renamed Drive file adopted), 4 MINOR | fixed + tests; runbook §7 |
| R3 | delta | **PASS** | 1 MINOR (valid-looking rename vs sidecar) | fixed + test (17th) |
| ext | ID03 (QA), ID07 (falsification) via WO 0151 | PUBLISHED_NOT_ACKNOWLEDGED | — | ID01 to start agents |

## 9. Open decisions (ID01)
1. Restrict WORK sharing (`anyone: writer`) — prerequisite for any lock.
2. Who owns the ledger allocator / file-registry.jsonl writer?
3. Promote wayfinder to `_NEXUS_WAYFINDER.md` in LLM-LOCAL-SSOT root (yes/no).
4. Report routing: one durable location (proposal: Drive `NEXUS.REPORTS`, WORK = operative originals, repo = review snapshot).
5. Provide `nexus_server.py`, `nexus_gateway_server.py`, `transcript_timeline.tsx` (not found in repo/Drive) for R2.

## Reporting
- STATUS: PARTIAL — code + tests + wayfinder done, internal review loop closed; registration, ledger reservation, real E2E, external ID03/ID07 review pending
- CHANGED: 4 new tools/tests files, inventory JSON, wayfinder, this report, WO, run-log entry
- TESTS: 19/19 new PASS; 4 pre-existing failures unchanged
- SOURCE_STATUS: Drive connector read 2026-11-02 ~19:00 CET; repo fb103dbe
- RISKS_GAPS: WORK anyone-writer (lock bypassable); ledger numbers unreserved (collision risk); no real allocator; registry record returned, not appended; journal must be on persistent storage; single-host lock; depth-1 inventory; nexus_server.py missing; open WO 0146 (ID02→ID06 review of 0142–0145) still unanswered
- NEXT: ID01 decisions §9 → R2 (mount + UI) → R3 recursive index
