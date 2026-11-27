---
name: dropzone-ai-stack-roadmap
description: Classification of the _AUSTAUSCH-HANDY-PC dropzone (AI stack, data/tool integration, agents, MCP, GitHub sync, local hosting) + reuse check against nexus-platform + roadmap
version: 0.1.0
status: REVIEW_PENDING
timestamp: 2026-11-23T08:45:00+01:00
tasks_done: dropzone listed (Drive); 12 text/code files read in full; repo nexus-platform@e7b2bbd checked for existing building blocks; classification + roadmap written
tasks_open: ledger ID; file-registry.jsonl entry; _FRONT_LOG.md line; PDFs/DOCX/ZIPs unread; bookmarks not exported; independent review
problems: Drive connector cannot append to ledger/registry/log files; browser bookmarks not reachable; link lists inside the video notes are partly unverifiable
open_questions: ID01 - import NEXUS AEC Contracts v0.1.0 into nexus-platform (yes/no, target path)? ID01 - which of the two local gateways stays (LLM_API_KEY.py vs orchestrator/)?
result: PARTIAL - analysis and roadmap delivered; nothing executed, nothing released
actor: "ID-UNVERIFIED - Claude (claude.ai cloud session, Chrome side panel + Drive connector + GitHub); earlier reports of this runtime type used ID06, not verified against Manifest by this run"
agbs_read: "_AGBS.md v007.1 (gdrive:10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg), read 2026-11-23 08:35; Folder.md policy 0.4.0-pilot (gdrive:1nDjF78dq3l8PGpXsauzBz1bzHescDSwv, status_checked_at 2026-11-16)"
registration_status: REGISTRATION_PENDING
persistence_status: WRITTEN_UNVERIFIED
supersedes_partially: gdrive:1nWQvhIIt_0l0NuL4m6-WKCjnv12Je0ZZ (WO-CHROME-MCP-BRIDGE peer review v0.2, 2026-11-10) - see section 2
---

# ROADMAP: Dropzone -> NEXUS AI stack

## 0 TL;DR
- Strongest asset in the dropzone: `Delta-Refinement/` = **NEXUS AEC Contracts v0.1.0** (ports-and-adapters, SolverPort, 7 JSON schemas, pytest.log "96 passed"). Not found in nexus-platform@e7b2bbd -> import it first.
- Most of the "Chrome-MCP bridge" plumbing already exists in the repo: FastMCP server, `policy_context()`, Ollama routing. Build on it, do not rebuild.
- Next real value step: one self-hosted solver adapter (PyNite) behind SolverPort, exposed as an MCP tool, run by CI.
- `LLM_API_KEY.py` holds no plaintext keys (keyring/env only). Risk flag from 2026-11-10 closed.

## 1 Evidence base
| Source | Depth | Stamp |
|---|---|---|
| Dropzone folder gdrive:1jvGf8e-gKUioqeiDckgfsKJbHvLtKLAD | top level + 9 subfolders listed (first 100 child files; more exist) | 2026-11-23 |
| LLM_API_KEY.py, requirements.txt, DEEPSEEK stub, structure-aware-retrieval note, chunking-labeling.md, BestLocalCodingModels.txt, Delta-Refinement README/ARCHITECTURE/GITHUB_AGENTS/pytest.log | read in full | 2026-11-23 |
| nexus-platform main@e7b2bbd | directory + grep check, no test run | 2026-11-23 |
| PDFs (Blueprint, Cheatsheet, Beurteilung x2, MANUS, Scan, GitKraken, Microsoft Learn), COMMIT-POLLING-SYNC docx, ZIPs, Muse/Kimi notes, Wissensmanagement-DB md, signalmatrix dossier, Manifest OCR, .bat/.ps1 | NOT read (name/size only) | - |
| Browser bookmarks (Chrome/Firefox/Edge) | NOT available - no export in Drive | - |

## 2 Corrections to the 2026-11-10 peer review (v0.2)
| v0.2 statement | Corrected |
|---|---|
| `policy_context()` does not exist | exists in `mcp_bridge/ctx_router.py:53` (not in nexus_contract.py); tests in `tests/test_context_bootstrap.py` |
| WP3: register an MCP gateway | `mcp_bridge/nexus_mcp_server.py` already builds a FastMCP server `nexus-bridge` with 6 tools |
| WP7: local model routing to be built | `orchestrator/config/routing.json` v1.3.0-draft already has provider `local` (Ollama, localhost:11434, qwen2.5:7b), default_temperature 0 |
| LLM_API_KEY.py may hold plaintext keys | no: Windows Credential Manager (keyring) -> env -> HKCU env; FastAPI gateway on 127.0.0.1:8787 with bearer token |
| Two WORK folders ambiguous | canonical = gdrive:1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP (Folder.md) |

## 3 Classification (non-media items)
Legend: R = read, N = name only. Maturity: TESTED / DRAFT / NOTE / UNKNOWN.

| Category | Item | Maturity | What it is | Link |
|---|---|---|---|---|
| RULE-BASED + STATE CONTROL | Delta-Refinement/ (NEXUS AEC Contracts v0.1.0) | TESTED (96 passed, local) R | frozen typed contracts, SI canon, Decimal strings, capability profiles, MANIFEST.sha256, ADR-001..007 | https://drive.google.com/drive/folders/10HCBM8IXkR7voF_BR0m4Nw_M-5GUva4U |
| PYTHON COMPUTING in LLM frameworks | same: `SolverPort`, `ExchangePort`, `fixture_solver.py`, `result_validation.py` | TESTED, fixture only R | solver-neutral port; no real solver adapter yet | README gdrive:1GWmU3_BAA5MirDVVrWmxsW2dYrwzpvUG |
| GITHUB SYNC + ACTIONS | Delta-Refinement/GITHUB_AGENTS.md | DRAFT R | older AGENTS.md candidate (points to superseded Folder.md) | gdrive:1nqHRGeylEAmjVc6xPJBS464a6xmRUK7B |
| GITHUB SYNC + ACTIONS | 26_10_19_COMMIT-POLLING-SYNC-DRIVE-GITHUB.docx (10 MB) | UNKNOWN N | repo already has nexus-drive-poll.yml, nexus-delivery.yml, nexus-registry-append.yml | gdrive:1W59AQ0FYbcS9WTtgsy1WW6rDfEogAoTt |
| AI STACK / SELF-HOSTED | LLM_API_KEY.py + START_LLM_GATEWAY.bat + 00_UPDATE_LLM_ENV.ps1 + requirements.txt | DRAFT R (py, txt) | OpenAI-compatible local gateway, 6 cloud providers, no local provider | gdrive:1TJQQJtfCke4Pk4cwQc2IAiJi94wXq9hp |
| AI STACK / SELF-HOSTED | 26_10_25_BestLocalCodingModels.txt | NOTE R | video notes: pick model by hardware tier and task (autocomplete / agentic / long context) | gdrive:1HIIUXqTwQd1wYav4N4ZkPHDzZRvbp0Ed |
| AI STACK | 26_10_24_Kimi K3 Attention Architecture.txt; Muse Meta Model API/; MANUS-AI-TopKI+LLMs-2026.pdf | NOTE N | model/market notes | - |
| DATA INTEGRATION (RAG) | RAG Docling Agent/ (docling-agent-main.zip + folder) + structure-aware-retrieval note | NOTE R (note) | chunkless / structure-aware retrieval; hybrid: similarity picks the document, structure navigates inside it | https://drive.google.com/drive/folders/1r8Iunja7p0pHDnABl1D87TxvmS8MgoX9 |
| DATA INTEGRATION (KM standards) | 26_10_24_wissensmanagement-standards-chunking-labeling.md | DRAFT R, with own review note | ISO 30401/704/1087/25964, SKOS, PROV-O, Web Annotation, SHACL, ISO 12006/23386/23387; minimum profiles for concept, assignment, chunk | gdrive:1-3pBhS170JCsqE-FmHOtoeyWBwyz5O_N |
| DATA INTEGRATION | Wissensmanagement...Normen.../ (1 md, 22 kB); Beurteilung.Wissensdaten.ZLZT/ (DATA-MODEL-v1.0, docx); 2 Beurteilung PDFs | UNKNOWN N | knowledge-base design + quality rating | https://drive.google.com/drive/folders/1EK-v0xEmzMcYoH6CChWL6hcbtbhs9Kcr |
| MULTI-AGENT / AGENT-MANAGED | Delta-Refinement: CROSS_CHAT_HANDOFF.md, DEEPSEEK_WORK_ORDER_QA_002.md, HANDOFF_CHECK.json, agent_orchestrator_one_pager.html | DRAFT N | hand-off protocol between chat runtimes | folder link above |
| MULTI-AGENT / SYSTEM DESIGN | 2026-10-26-system-design-signalmatrix-v1.0.0/ (HTML+PDF manual, hashes, readback) | DRAFT N | signal matrix manual with ARTIFACT_HASHES + DRIVE_READBACK | https://drive.google.com/drive/folders/1Xel_Lt7MazzY6cPsC-bLpycLq2V6kHoU |
| ADK/SDK/FRAMEWORKS | AI-ENGINEERING-GUIDE/ (zip 5 MB), AI-ENGINEERING-SYSTEM-main.zip (11 MB), Microsoft Learn-Plattform.pdf | UNKNOWN N | downloaded reference repos | - |
| MCP ACCESS | 26_10_28_DEEPSEEK-GOOGLEDRIVE-MCP-GITHUB#01.txt | STUB R | one DeepSeek share link, no content | gdrive:11bqOKfUDSn5x3X8T_iDIR1E_HeEMRAcj |
| NEXUS SYSTEM DOCS | NEXUS AI System Blueprint.pdf, KNOWLEDGE-FABRIK Cheatsheet, Manifest folder (PDF + OCR md), NEXUS-A#I-NEURAL-NETWORK-ENGINEERING/ | UNKNOWN N | design documents | - |
| TOOL | CHROME-DIRLIST_HTML.html, _AUSTAUSCH-HANDY-PC.pdf, GitKraken cheat sheet | - | directory snapshot (see v0.2 review) | - |

Duplicates seen: 2x "Developer Guide - buildingSMART Validation Service 0.8.4" (45 B link stubs); GITHUB_AGENTS.md vs repo AGENTS.md (repo is newer); WORK_AGBS_v002.md vs _AGBS v007.1 (historic). No deletion - leave or move to `_DUPLICATES_*`.

## 4 Reuse check: dropzone vs nexus-platform@e7b2bbd
| Capability | Already in repo | Gap |
|---|---|---|
| MCP server | mcp_bridge/nexus_mcp_server.py (FastMCP, 6 tools), install_mcp_bridge.ps1 | no solver / calculation tool |
| Policy pre-hook | ctx_router.policy_context(), nexus_contract.load_governance() | not passed as MCP `instructions` (not verified in code) |
| Local + cloud routing | orchestrator/ (providers.py, routing.json: perplexity, claude, gpt, gemini, local=Ollama, vision) | second gateway LLM_API_KEY.py overlaps -> decide one |
| Drive <-> GitHub | workflows nexus-drive-poll, nexus-delivery, nexus-registry-append, nexus-monitor; tools/registry_append.py | Folder.md: github_to_work_oauth BLOCKED_HTTP_400 (ID01 must renew secret) |
| Registry | registry/file-registry.jsonl, tools/validate_registry.py, schemas/file-record.schema.json | dropzone not registered |
| Solver contracts | ec5_core/, rfem_parametric/ | no SolverPort / analysis_model contracts (grep: no hit) |
| Structure-aware RAG | skills/claude-ai/knowledge-ingestion mentions docling; reports/2026-10-13_parsing-pipeline | no chunk profile as schema |

## 5 Best ideas (ranked by value / effort)
1. **Contracts into the repo.** Import NEXUS AEC Contracts v0.1.0 as its own package; re-run its 96 tests in GitHub CI. Makes every later solver, MCP tool and agent hand-off checkable. Needs the 3-perspective review before any contract release (AGENTS.md rule 8).
2. **First real adapter: PyNite behind SolverPort.** Open source, pure Python, runs on your PC and in CI. Acceptance: single-span beam, UDL, M_max = q*L^2/8 and reactions within 0.1 %; sum V = 0.
3. **Solver as MCP tool.** Add `solve_analysis_model` to nexus_mcp_server.py: input validated by json_codec (unknown fields rejected), output AnalysisResults. Any MCP client (Claude, Codex, Gemini CLI, local Ollama agent) then computes instead of guessing.
4. **One gateway.** Keep orchestrator/ as router; take keyring secret handling from LLM_API_KEY.py; retire the duplicate. Local-first rule in routing.json: classification / extraction -> `local`, synthesis -> cloud.
5. **Chunk profile as schema.** Turn the minimum chunk profile from the chunking-labeling note (chunk_id, source_hash, section_path, page_anchors, content_type, review_status ...) into `schemas/chunk.schema.json` + validator; pilot on one norm section with Docling as structure parser.
6. **Dropzone scanner.** `os.scandir` + SHA-256 -> registry delta JSONL (WP1 of v0.2). Also takes bookmark exports.
7. **State control in CI.** Each of 1-6 = one PR with one binary test; nexus-monitor compares run deltas.

## 6 Roadmap
| Phase | Deliverable | Binary acceptance test | Blocker / gate |
|---|---|---|---|
| P0 (ID01, 15 min) | renew Drive OAuth secret (`tools/configure_drive_oauth.py --publish`); export bookmarks of 3 browsers as HTML into the dropzone | workflow NEXUS GitHub to WORK green; 3 files present | only ID01 can do this |
| P1 | PR: `contracts/` package from Delta-Refinement, CI job | 96 passed in CI on the PR head | ID01 decision target path |
| P2 | PR: PyNite adapter + golden case | beam case within 0.1 %; capability profile rejects an unsupported load type | P1 |
| P3 | PR: MCP tool `solve_analysis_model` + `policy_context()` as server instructions | MCP client call returns AnalysisResults; missing policy file -> BLOCKED | P2 |
| P4 | PR: gateway consolidation + routing rule local-first | `--audit` shows keys from keyring; mock-provider tests green | ID01 decision |
| P5 | PR: chunk.schema.json + Docling pilot on one EC5 section | 10 reference questions return the right clause + page anchor | licence check of norm text |
| P6 | PR: dropzone scanner + bookmark parser -> registry delta | rerun = 0 new rows | P0 for bookmarks |
| parked | WebMCP on dashboards, Gemini Nano pre-filter, RFEM adapter | - | see v0.2 review |

## 7 Links from the notes - status
Verified this month (web): Chrome Prompt API https://developer.chrome.com/docs/ai/prompt-api ; chrome-devtools-mcp https://github.com/ChromeDevTools/chrome-devtools-mcp ; Chrome GenAI policies https://support.google.com/chrome/a/answer/14443058
Named in your notes, NOT verified by this run: https://github.com/docling-project/docling-agent ; https://github.com/continuedev/continue ; FreeCAD MCP servers (neka-nat, blw) ; https://lobid.org ; https://d-nb.info/gnd/ ; dataholz.eu ; lignum.ch ; haydenschmitty/floorplan ; Graphify-Labs/graphify
Warning: the "MORE NEWS" link blocks in BestLocalCodingModels.txt and the retrieval note are LLM-generated; one block states it was built without a transcript. Treat every link there as unverified before ingesting (examples to check first: the Docling arXiv number, zenodo.org/records/10123456, structengine/eurocode-xml).

## 8 Deviations (AGBS 8)
- Filename carries LEDGER-PENDING instead of a ledger number: next free ID not determined by this run (Folder.md says 0212 as of 2026-11-16).
- Role ID not verified -> ID-UNVERIFIED.
- No raw-byte readback hash -> WRITTEN_UNVERIFIED.
- Registry, ledger and _FRONT_LOG.md not updated (connector cannot append).

LOG: artifact in WORK (this file); GitHub review snapshot under reports/ via draft PR; start line in LLM-HISTORY-LOG; report log and status sheet OPEN.
