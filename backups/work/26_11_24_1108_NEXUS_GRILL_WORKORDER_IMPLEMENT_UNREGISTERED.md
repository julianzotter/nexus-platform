---
name: "Grill-/Context-Skill und deterministischer Run-Guard"
version: "0.1.0"
created_at: "2026-11-24T11:08:51+01:00"
ticket_id: "WO-20261124-GRILL-IMPLEMENT"
owner_id: "ID06"
agent_id: null
executor_instance: null
provider: null
model_id: null
reviewer_instance: null
capability_check: "NOT_RUN"
role_register_version: "NEXUS-ROLES-v1.1"
priority: "P1"
status: "OPEN"
development_status: "PROPOSED"
evidence_status: "UNVERIFIED"
eval_status: "NOT_RUN"
registration_status: "REGISTRATION_PENDING"
delivery_status: "NOT_ACKNOWLEDGED"
artifact_id: null
source_ssot_anchor: "https://drive.google.com/file/d/1iv-PYO68krnFTXihSU16NzKt5fHqZBiK/view"
objective: "Grill-/Context-Skill und deterministischer Run-Guard"
inputs: ["https://drive.google.com/file/d/1iv-PYO68krnFTXihSU16NzKt5fHqZBiK/view", "https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view", "https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view", "https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view", "https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view"]
constraints: ["READ_ONLY default; explicit scoped writes only; no deletion/email", "No invented ACK/role/ledger number; actual runtime and capability probe", "Fresh execution context if available; measure tokenizer and full assembled request, reserve output/tool/safety; unknown budget => no claim of fit", "No main merge, deployment or release without explicit ID01 gate"]
task: "Vorhandene skills/agent-team-plan, agent-team-orchestrator, mcp_bridge/ctx_router.py, tools/registry_append.py und Tests prüfen. Kleiner isolierter Slice: Grill-Skill/Handoff und Budgetguard nur bei nachgewiesener Lücke."
expected_output: "Versionierte Skill-/Script-Deltas, Tests, Runlog, Hash, GitHub Branch."
acceptance_criteria: ["TDD: Budgetgrenze, fehlende Tokenmessung, negative Fälle, unveränderter Baseline-Scope; keine fingierten Agentenruns."]
dependencies: ["WO-20261124-GRILL-DESIGN"]
risks: ["Unverified runtime binding; duplicate work; existing governance conflicts; external reviewer availability"]
next_action: "ID06: Ist-Check, dann genau einen kleinen Slice implementieren und testen."
---
# WO-20261124-GRILL-IMPLEMENT — Grill-/Context-Skill und deterministischer Run-Guard

Owner: ID06; keine CLAIM/ACK-Aussage.

## Task
Vorhandene skills/agent-team-plan, agent-team-orchestrator, mcp_bridge/ctx_router.py, tools/registry_append.py und Tests prüfen. Kleiner isolierter Slice: Grill-Skill/Handoff und Budgetguard nur bei nachgewiesener Lücke.

## Output
Versionierte Skill-/Script-Deltas, Tests, Runlog, Hash, GitHub Branch.

## Abnahme
TDD: Budgetgrenze, fehlende Tokenmessung, negative Fälle, unveränderter Baseline-Scope; keine fingierten Agentenruns.

## Next action
ID06: Ist-Check, dann genau einen kleinen Slice implementieren und testen.

## Result contract
FINDINGS | EVIDENCE/SOURCES | ARTIFACTS | RISKS | NEXT_ACTION | QA_STATUS.
