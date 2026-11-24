---
name: nexus-grill-run
description: Clarify NEXUS workorders using a grounded decision tree, shared language, bounded context and verified handoffs.
version: 0.1.0
owner: ID02
tools: read-only source tools, run_budget_guard.py, authorized WORK publication
runtime: any; verify actual provider and capabilities
status: PROPOSED
---

# NEXUS Grill Run

Scope: WO-20261124-GRILL-DESIGN and WO-20261124-GRILL-IMPLEMENT. This candidate augments `agent-team-plan`, `agent-team-orchestrator`, `model-effort-router` and `mcp_bridge/ctx_router.py`; it is not a replacement governance or registry.

1. Read current AGB, Manifest, Baseline, WORK/Folder.md, ticket and glossary. Record authority, version, actual runtime and permissions. Missing critical source blocks its dependent claim; continue safe isolated work.
2. Resolve facts from sources before asking decisions. Walk each dependent decision in topological order. Record question, options, recommendation, source, dependency, decision authority and OPEN/DECIDED status. Never substitute a recommendation for ID01 approval. Reuse the canonical glossary and propose changes as a delta.
3. Specify one vertical slice with measurable acceptance checks, dependencies, input source locators, forbidden actions and reviewer. Reuse existing tickets; avoid duplicate pipelines. Route through existing planning and effort skills.
4. Assemble a fresh minimal context: mandatory rules, scope, pinned evidence, acceptance checks and previous handoff. Use existing context router for retrieval only; its estimated count is not an exact provider request measurement. Ask the trusted provider adapter for the effective context cap and exact count of the complete serialized request (system, instructions, tools and history included). Reserve output, future tool results and positive safety margin. Run `python tools/run_budget_guard.py --request REQUEST --receipt RECEIPT`. Unknown measurement or exceeded budget: split optional context, persist handoff, restart actual execution, never truncate mandatory rules. The script only validates arithmetic and digest binding, not authenticity, provider availability or dispatch authorization. Recheck before each materially changed request.
5. Implement only the accepted slice, using deterministic tests; log actual run IDs, measured input/output tokens (unknown if unavailable), artifacts, hashes, findings and next action. Evaluate observable checks, fix only confirmed failures, repeat targeted tests plus regression suite. Stop on PASS or documented BLOCKED; no simulated independent runs.
6. Publish versioned WORK result and registration delta; obtain actual ACK, independent reviews and ID01 decision. GitHub draft PR only before release; no automatic merge, no fabricated ledger ID. A test PASS is not production approval.

Method references: https://github.com/mattpocock/skills ; NEXUS guide https://drive.google.com/file/d/1iv-PYO68krnFTXihSU16NzKt5fHqZBiK/view . Pin upstream revision before further adoption. This skill is a local adaptation, not an installed external plugin.
