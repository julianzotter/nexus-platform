---
name: NEXUS-ID01-GOVERNANCE-DECISIONS-20261029
description: ID01 decisions Q1-Q4; implementation workorder and controlled migration
version: 0.1.0
status: APPROVED_FOR_IMPLEMENTATION_WITH_GATES
timestamp: 2026-10-29T19:23:00+01:00
agent_id: ID03
artifact_id: PENDING_LEDGER
source_status: ID01_CHAT_DECISION
canonical_source: Google Drive LLM-LOCAL-SSOT/WORK (upload/readback pending)
review_status: PENDING_INDEPENDENT_REVIEW
---
# ID01 decision and implementation workorder — NEXUS AI-OS

## Decision (ID01, 2026-10-29)
Q1=A: ID03 is Chief Orchestrator and QA coordinator. Independent review must use a different executor/reviewer runtime; no self-approval. ID02 historical references remain immutable.
Q2=A: New time-stamped Markdown files follow `YY_MM_DD_HHMM_ID##_CONTENT-TYPE_TITLE.md`, where ID## is the role identifier. Distinct artifact_id must be assigned from 00_ID_LEDGER.csv. Required YAML: name, description, version, status, timestamp. Deterministic SHA256 and hash_scope required for verifiable files. Control files retain stable-name exceptions.
Q3=C: Do not change ACLs; perform read-only permission inventory and escalate findings.
Q4=B: Phase 1: CI and workorder ACK + response mandatory. Phase 2: independent peer review and raw-byte sync readback mandatory. Existing stronger security/review gates remain binding until separately migrated and tested.

## Authority and constraints
ID01 authorized implementation on 2026-10-29. This document is a GitHub review snapshot, not a substitute for canonical Drive SSOT. No deletion, no retrospective rewrite, no ACL change. Manifest/Baseline/_AGBS v003 conflicts must be migrated through versioned successor drafts and readback. No production release without ID01 approval.

## Work packages
1. Register one canonical workorder in WORK; allocate unique ledger artifact_id; record Drive file ID, SHA256 and timestamp.
2. Prepare versioned governance changes: CURRENT Manifest roles/leadership; CURRENT Baseline routing/reporting; _AGBS filename rule; _FRONTMATTER schema; NEXUS-ROLES register; workorder template and ticket registry. Keep originals untouched and link successors.
3. Prepare schema validator: filename, role ID, unique artifact ID, YAML fields, SHA256 scope and bytes; reject missing or invented values.
4. Prepare CI and ACK gates: evidence-backed CI_PASS; explicit dispatch/ACK and response artifact; no FALSE_GREEN.
5. Independent review by ID07 or another demonstrably separate reviewer instance; preserve reviewer identity and outcome.
6. Read-only ACL audit. No permission mutations.
7. After passing gates, reconcile Drive WORK -> SSOT -> GitHub mirror; compare exact bytes/hash and log commit SHA.

## Communication matrix
ID03: orchestration and QA coordination.
ID04 Gemini: evidence/protocol/registry reconciliation.
ID05 Perplexity: external contradiction/source review if needed.
ID06 Claude: implementation and deterministic tests.
ID07 DeepSeek: independent governance/architecture review.
ID08 Ollama: optional only if runtime capability verified.
Each actual dispatch requires ticket_id, agent_id, sent_at, source_uri, ack_at, response_uri, status. Merely storing a file is not a dispatch or ACK.

## Acceptance criteria
AC01 one authoritative role register; AC02 unique ledger IDs; AC03 filename/YAML/SHA256 validator passes; AC04 CI and ACK gates pass; AC05 independent review traceable; AC06 FALSE_GREEN prevented; AC07 ACL unchanged and audit documented; AC08 historical objects intact; AC09 GitHub commit and Drive↔Repo raw-byte comparison evidenced; AC10 separate ID01 production approval.

## Evidence / gaps
CURRENT Manifest: https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
CURRENT Baseline: https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit
AGBS v003: https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view
ID Ledger: https://drive.google.com/file/d/1Uvb89wWOpte3iXWKm3qrg42dEwBb7nuG/view
WORK: https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP
Ticket registry: https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit

STATUS: IMPLEMENTATION_AUTHORIZED / GATES_PENDING
CHANGED: new GitHub review-branch workorder only
TESTS: pending
SOURCE_STATUS: sources linked; canonical Drive registration pending
RISKS_GAPS: role/name conflicts; ACL audit; missing ACK/CI/review/readback
NEXT: canonical Drive archive; ledger registration; dispatch; independent review; deterministic tests
