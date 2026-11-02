---
name: WO-NEXUS-WAYFINDER-EXPORTLOCK-PEER-REVIEW
description: External peer review (ID03 QA, ID07 falsification) of NEXUS.* wayfinder, export hard-lock and roadmap report
version: 0.1.0
status: OPEN
timestamp: '2026-11-02T19:15:00+01:00'
agent_id: ID06
author_role: ID06_Claude_Coding_Implementierung
owner_id: ID01
target_role_ids: [ID03, ID07]
reviewer_instance: PENDING_CLAIM
review_status: NOT_RUN
ticket_id: WO-20261102-NEXUS-WAYFINDER-01-REVIEW
parent_ticket_id: WO-20261102-NEXUS-WAYFINDER-01
artifact_id: '0151'
ledger_status: UNRESERVED_PROPOSAL
artifact_registration: PENDING_REGISTRY_WRITER
priority: P1
delivery_status: PUBLISHED_NOT_ACKNOWLEDGED
human_gate: PENDING_ID01
release_status: NOT_GRANTED
canonical_folder: _developement/LLM-LOCAL-SSOT/WORK
related_artifacts: ['0149', '0150']
conflict_policy: NO_DUPLICATE_TICKETS
---
# WORK ORDER — External peer review: NEXUS wayfinder + Drive export hard-lock

## 1. Objective
Falsify or confirm (a) the NEXUS.* folder verdict + wayfinder, (b) the server-side Drive export hard-lock (Run 1 / Step 1), (c) the roadmap. Not a release.

## 2. Authority / separation
- ID01: client, sole human gate.
- ID06: author/executor; already ran an internal independent review loop (3 rounds, report §8) — **does not certify itself**.
- ID03: QA review (structure, governance, AGBS v004 compliance).
- ID07: independent falsification (code, races, bypasses). ID03 ≠ ID07 findings must be kept separate.

## 3. INPUTS (immutable identifiers; SHA-256 of raw bytes in table below the frontmatter of the delivered files)
| Artifact | Content | Location |
|---|---|---|
| 0149 | Implementation guide + roadmap + review log | WORK (Drive) + repo `WORK/REPORTS/` |
| 0150 | NEXUS.* wayfinder (generated) | WORK (Drive) + repo `docs/wayfinder/` |
| code | `tools/nexus_export_lock.py`, `tools/nexus_folder_index.py`, `tools/deliver_work.py` (2-line delta), tests | GitHub `julianzotter/nexus-platform`, branch `id06/nexus-wayfinder-export-lock` |
| data | `registry/drive-inventory/nexus_folders_inventory_2026-11-02.json` | same branch |
| governing | `_AGBS.md` v004, WORK `Folder.md`, `00_ID_LEDGER.csv` v1.8 | WORK / SSOT root |

## 4. Tasks / test plan
1. Recompute SHA-256 of 0149/0150 Drive bytes; compare with the hash list in the ID06 run-log entry 0152.
2. Re-run `python -m pytest -q tests/test_nexus_export_lock.py tests/test_nexus_folder_index.py tests/test_deliver_work.py` on the branch head; report commit SHA.
3. Regenerate the wayfinder from the inventory JSON with `tools/nexus_folder_index.py` → byte-identical? (determinism gate).
4. Spot-check ≥3 NEXUS.* folders in Drive against inventory counts (depth 1).
5. Try to bypass the lock: client-chosen name/folder/role, replay after state loss, rename/trash in Drive, concurrent requests, oversized body.
6. Governance: naming, frontmatter, no second registry, ledger numbers 0149–0152 are UNRESERVED proposals → confirm or renumber.
7. Check the verdict on ID01's claim (report §1) and the audit corrections (§2) against sources.

## 5. Expected output & acceptance
- One file per reviewer in WORK: `26_11_02_HHMM_ID03_REVIEW-WAYFINDER-EXPORTLOCK_####.md` / `..._ID07_...`.
- Findings table: `ID | Severity BLOCKER/HIGH/MEDIUM/LOW | Artifact/Locator | Expected | Observed | Proposed fix | Verification test`.
- Verdict: `PASS | FAIL | BLOCKED | INCONCLUSIVE`; `NOT_RUN` wherever no real execution happened.
- Reporting block at the end: STATUS / CHANGED / TESTS / SOURCE_STATUS / RISKS_GAPS / NEXT; begin with role ID, end with "over and out".

## 6. Explicit process, fail closed
`OPEN → (ID01 starts agent) DISPATCHED → CLAIM + ACK → RUNNING → REPORT → ID06 delta fix → re-review → ID01 HUMAN_GATE`.
Publishing in Drive is **not** delivery. `delivery_status=PUBLISHED_NOT_ACKNOWLEDGED` until a review file exists.

## 7. Status journal
- 2026-11-02 19:15 ID06: WO published. No claim, no ACK.
