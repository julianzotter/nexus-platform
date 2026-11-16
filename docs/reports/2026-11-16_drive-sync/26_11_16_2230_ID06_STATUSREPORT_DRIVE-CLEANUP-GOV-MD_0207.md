---
name: drive-cleanup-gov-md
description: Manifest/Baseline converted to .md, root duplicates moved (move-only), WORK open-access decision, GitHub sync
version: 1.0
status: DONE – Drive executed + readback; GitHub PR draft (merge needs ID01)
timestamp: 2026-11-16T22:30+01:00
---
# Drive cleanup + governance .md (2026-11-16 22:30)

## 1 Governance .md (bridge unblock O3)
| File (LLM-LOCAL-SSOT) | Drive ID | Bytes | SHA256 |
|---|---|---|---|
| 00_NEXUS_MANIFEST__CURRENT__2026-09-28.md | 1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn | 7720 | cfcb2ea6088a474a6bb41654a86ed6de3e32e2b572aa57b9ce7ea6527238fdee |
| 00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28.md | 1CdwNHr6i8lMG3k8A939kiznLMw8q7J69 | 18680 | 015a635ff2745f6ae0bf61f02d3028039ea45acb86f24363db7185786d854858 |
- Content = verbatim Google-Docs export (text/markdown), no edits.
- Google Docs stay as EDIT SOURCE; description notes: re-export after every edit.
- Repo mirror: `governance/current/`.

## 2 Root duplicates → `_developement/_DUPLICATES_26_11_16` (1SKShkLj_LslasFpxejWnFHlNJIB_rFux), move-only
| Old name / location | New name | ID |
|---|---|---|
| _AGBS.md (GDoc, root, 18.10. 21:39) | _DUPLICATE_26_11_16__AGBS_gdoc_2139 | 1Ihi2Y7btkHxHS-jGkY9UiBFHO9asLJX2r2y4OfMmhvQ |
| _AGBS.md (GDoc, root, 21:36:30) | _DUPLICATE_26_11_16__AGBS_gdoc_2136b | 1kxLmSa8EOzxUMpqDwwYcy6d_3PjRz8lTzcMDb7iHrOY |
| _AGBS.md (GDoc, root, 21:36:11) | _DUPLICATE_26_11_16__AGBS_gdoc_2136a | 1cbgLSgKp9X74BPFbKFOyhP1pDznvVud9hkjt9-ULV6I |
| _AGBS.md (GDoc, root, 21:31) | _DUPLICATE_26_11_16__AGBS_gdoc_2131 | 1jlLdkrK-bqg2bsG5xTcq5WJGaUqNkUOH5n7GtCZ7fiM |
| LLM-LOCAL-SSOT (root folder) | _DUPLICATE_26_11_16__LLM-LOCAL-SSOT_root | 1hMhuuAP8FuRu6Skb_u-Am_pJ2Jas58AI |
- Canonical `_AGBS.md`: WORK (10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg). Not moved: `_AGBS.md` MD mirror 1qSv1EIp… (parent 18IIq…, unclassified).
- Note: root LLM-LOCAL-SSOT contained `INDEX_LNK_BENCHMARK` → paths pointing at My-Drive-root/LLM-LOCAL-SSOT now break; rollback = move folder back to root.

## 3 WORK access (O6) – ID01 decision 2026-11-16 22:27
- WORK stays `anyoneWithLink: writer` = intended open collaboration space for all NEXUS LLMs/workflows.
- Residual risk (accepted): anyone holding the link can edit/overwrite; mitigation = Drive revision history + this GitHub mirror + no secrets in WORK.
- `Folder.md` status SECURITY_BLOCKED is thereby outdated → update requested (ID01/ledger).

## 4 Open
- "Available offline" for LLM-LOCAL-SSOT + MCP-ACCESS-TOOLS: manual on PC; verify with `tools/windows/drive_offline_check.ps1`.
- PR merge: ID01.
