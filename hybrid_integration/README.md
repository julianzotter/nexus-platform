# NEXUS Hybrid ID01 — bounded integration proposal

Status: DRAFT / NO DEPLOYMENT / NO SYNC. Scope: read-only metadata gateway for an existing Source Atlas SQLite database.

## Source responsibilities
- Drive `_developement/LLM-LOCAL-SSOT`: primary knowledge and governance; human-approved originals.
- GitHub `nexus-platform`: versioned code and orchestrator; other repositories remain unchanged.
- `nexus-ai-operation-system`: parser and AEC connector candidates; `AI-ENGINEERING-SYSTEM`: notebooks.
- `skills`: skills catalog, reviewed before activation; `RFEM_Python_Client`: legacy adapter (gRPC migration review).
- `Multi-Agent-CAD`: CAD candidate; `NEXUS-AI-AEC-ENGINEERIN-KNOWLEDGE-GRAPH`: UI candidate.
- Local SQLite: disposable *derived* inventory, not canonical normative evidence.
- `_developement/MCP-ACCESS-TOOLS`: connector candidates. No credentials or automatic execution.

## Immediate use
Use Python 3.10+ with no additional packages:
```python
from hybrid_integration.hybrid_gateway import invoke
print(invoke("atlas.health", r"C:\\Temp\\ZC_ATLAS\\master_atlas.sqlite"))
print(invoke("atlas.lookup", r"C:\\Temp\\ZC_ATLAS\\master_atlas.sqlite", "Silo"))
```
Run tests from this directory with `python -m unittest -v test_hybrid_gateway.py`.
Do not point to untrusted database files. `immutable=1` requires a quiescent snapshot; never use it with a concurrently updated live WAL database.

## Contracts and human gates
- Allowed tools: `atlas.health`, `atlas.lookup` only, bounded to 100 results; no path fields in responses.
- No arbitrary SQL; parameterized lookup, wildcard escaping; no secret or file-content ingestion.
- No MCP server, voice transport, notebook authentication, CUDA install, GitHub sync, Drive writes, or RFEM commands are enabled.
- Gemini Live dual speech/translation requires separate provider auth, user consent, VAD, latency and echo tests; NotebookLM is a separate knowledge surface.
- RTX 4070 (~8 GiB VRAM as reported) driver 566.24 and CUDA toolkit 12.6; current PyTorch 2.10.0+cpu has no CUDA backend.
- Next gates: security review; Windows DB snapshot test; source provenance; GPU virtual env validation; Gemini live tests; tool-router authorization; controlled sync dry-run.
- No source earns VERIFIED/CANONICAL status solely by appearing in the index.

## Local test evidence
Five isolated offline unittest cases passed on 2026-10-15 (Linux test runtime). Windows, actual Atlas DB, RFEM, audio, GPU and cloud connector end-to-end remain untested.


## ID01 implementation update — 2026-10-15
- SQLite URL construction now uses \`Path.as_uri()\`, which percent-encodes fragments and special characters.
- Schema handshake checks \`sqlite_master\` for a real \`files\` table, and checks \`file_name\`, \`source_system\`, \`source_class\`, \`scan_status\`, \`sha256\` before any tool query. Mismatches raise \`AtlasSchemaError\`.
- PR branch updated with ten isolated regression tests; all 10 passed using temporary SQLite databases on Linux. No live CI, Windows test, Atlas DB snapshot, connected MCP server, RFEM or voice end-to-end tested.
- \`zc_scan_v2_4.py\` uploaded source defines all five columns in its \`CREATE TABLE IF NOT EXISTS files\` declaration, but that does **not** verify deployed database schema.
- Reminder: use only a transactionally consistent **inactive** copy/snapshot for immutable mode. Local \`python -m unittest -v test_hybrid_gateway.py\` runs without additional packages.
- Existing sync scripts were not invoked. No Drive mutations, merges, installations or deployments.
