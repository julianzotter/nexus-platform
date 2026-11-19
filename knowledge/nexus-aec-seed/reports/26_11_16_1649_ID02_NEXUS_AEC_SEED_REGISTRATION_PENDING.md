---
name: NEXUS-AEC-TOP20-SEED-v1-status
version: 1.0.0
status: REVIEW_REQUIRED
timestamp: 2026-11-16T16:49:44+01:00
agent_id: ID02
role_name: ChatGPT Private / ChatGPT Chief Orchestrator
executor: OpenAI Codex
executor_instance: /root
model_id: null
ticket_id: null
run_id: 2026-11-16-ID02-NEXUS-AEC-SEED-v1
artifact_id: null
hash_scope: body_utf8_after_closing_frontmatter_lf
content_hash_sha256: 887660161c75a2662cf2a0157d690387d54eaa133d8fe81d385b5295cdfcb255
reply_to: ID01
canonical_work_folder_id: 1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP
---
# NEXUS-AEC TOP20 Seed v1 — WORK Result

## FINDINGS / STATUS
- **Previous TOP20 output**: no separately versioned Google-Drive or GitHub artifact identified in bounded prior searches; it is now preserved as `NEXUS-AEC-TOP20-2026-11-16`, not silently promoted into canonical NEXUS registry.
- **Source scope**: 20 target domains, 9 explicit source links; primary: OIB editions and state adoption, dataholz assemblies/IDS, baubook and ÖKOBAUDAT EPD, IBO circularity, EOTA ETA/EAD, TU Wien repositum, Dlubal Python gRPC API II. Sources are *discovery seeds*, not ingested datasets.
- **Code/QA**: 3 deterministic scripts (seed validation/isolated SQLite, knowledge record semantic unit QA, verified-item weekly digest), JSON schema, 3 test files; `python -m unittest discover -s tests -v` = 10/10 PASS (local offline). `python scripts/validate_seed.py --sqlite artifacts/nexus_aec_source_discovery_v1.sqlite` = 20 sources, 9 links, SQLite integrity check PASS in tests. No structural verification or RFEM live execution.
- **META_WISSEN**: existing active `Meta-Wissen Holzbau Weekly` automation ID `Automation_465069362f9c81919df70b0c1e872f43` UPDATED; Monday 08:00 Europe/Vienna unchanged. Original five news domains retained, official change-watch for OIB/material/LCA/EOTA/TU Wien/Dlubal added. Next scheduled run is not represented as already executed.

## ARTIFACTS / SAVE PROOF
- **Google Drive WORK seed JSON**: https://drive.google.com/file/d/14bpICcKiDJtg7dkWaQWrRo3VTu6Ld7yy/view ; raw-base64 byte-for-byte readback `PASS`; SHA256 `ef170ef95e52ca22c983bb3aac68ec545f640fadbae9955748fd6c2efe9b3a6d`.
- **Google Drive WORK ZIP**: https://drive.google.com/file/d/1gTxMs8CU5LApqxvVlvBhkcWADF54eN9d/view ; raw-base64 byte-for-byte readback `PASS`; SHA256 `e517b5c5b732260e42e05bb336a3f6ba791b74b4f37ced302619ecc7c9006569`. Includes source JSON, schema, Python, tests, independent SQLite index and README.
- **GitHub**: draft review PR https://github.com/julianzotter/nexus-platform/pull/87 (branch `feat/nexus-aec-seed-top20-20261116`, head `686e314199b4a2ab462737aa38afce8e6112aa51`). 9/9 files verified by exact local↔GitHub content readback, no merge to main, no production release.
- **Official links**: OIB RL7 consultation https://www.oib.or.at/kernaufgaben/oib-richtlinien1/richtlinien/oib-richtlinien-2027/ ; EOTA ETA https://www.eota.eu/etassessments ; TU Wien HBV https://repositum.tuwien.at/handle/20.500.12708/210734 ; Dlubal API https://apidocs.dlubal.com/ .

## GOVERNANCE / RISKS
- `REGISTRATION_PENDING`: file-registry and ledger assignment by designated ID03 actor not performed. No invented ledger number; filename intentionally indicates pending identity-compliance gap. `artifact_id` for this report becomes `gdrive:<new Drive ID>` after upload, to be registered externally by ID03.
- `SECURITY_GATE_OPEN`: WORK Folder.md 0.4.0-pilot reported `anyone:writer`; no change in sharing rights was authorized or performed. Recheck before release.
- `ENGINEERING_NOT_RELEASED`: licensed norms, source rights and Austrian Bundesland OIB adoption must be checked before normative claims; RL7/2027 is a draft. No real material/EPD values ingested, no physical RFEM/Windows/gRPC test, no independent peer review, no ID01 production sign-off.

## NEXT_ACTION
1. ID03: assign approved ledger ID, register all new `gdrive:<file_id>` in canonical `file-registry.jsonl`/History with collision check; confirm ACK and hash.
2. ID03/independent reviewer: evaluate PR #87 against OIB/EPD/IFC-IDS/RFEM contracts and 10 tests; conduct one licensed Golden Slice from component to source-tagged LCA and RFEM test input.
3. ID01: decide approval after security-gate repair, source-rights check and RFEM runtime check. Keep PR draft until then.

## EVIDENCE / AUTHORITY
- CURRENT Manifest (NEXUS-ROLES-v1.1): https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
- CURRENT Baseline: https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit
- AGB v006: https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view
- WORK Folder.md: https://drive.google.com/file/d/11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH/view
- Prior dataholz-IDS integration candidate: https://github.com/julianzotter/nexus-platform/blob/main/docs/integrations/2026-10-30-ids-dataholz-review-candidate.md

QA_STATUS: `LOCAL_TESTS_PASS; DRIVE_SEED_AND_ZIP_BYTES_VERIFIED; GITHUB_9_FILES_VERIFIED; AUTOMATION_UPDATE_CONFIRMED; REGISTRY_PENDING; HUMAN_RELEASE_BLOCKED`.
