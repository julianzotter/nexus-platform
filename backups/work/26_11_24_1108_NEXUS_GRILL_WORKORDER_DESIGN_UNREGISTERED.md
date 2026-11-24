---
name: "Grill-Entscheidungen und Shared Language"
version: "0.1.0"
created_at: "2026-11-24T11:08:51+01:00"
ticket_id: "WO-20261124-GRILL-DESIGN"
owner_id: "ID02"
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
objective: "Grill-Entscheidungen und Shared Language"
inputs: ["https://drive.google.com/file/d/1iv-PYO68krnFTXihSU16NzKt5fHqZBiK/view", "https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view", "https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view", "https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view", "https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view"]
constraints: ["READ_ONLY default; explicit scoped writes only; no deletion/email", "No invented ACK/role/ledger number; actual runtime and capability probe", "Fresh execution context if available; measure tokenizer and full assembled request, reserve output/tool/safety; unknown budget => no claim of fit", "No main merge, deployment or release without explicit ID01 gate"]
task: "Vorhandenes Glossar, agent-team-plan, Guide §3/6/7 prüfen; D4/D7/D9 als Entscheidungsvorschlag, echte offene Fragen markieren. Kein neuer Master."
expected_output: "Glossar-/ADR-Delta und Spec mit Test-Seams; keine Adoption."
acceptance_criteria: ["Alle 12 Knoten mit Quelle, Entscheidung/Offen, Abhängigkeit; ID01-Entscheidungen getrennt."]
dependencies: []
risks: ["Unverified runtime binding; duplicate work; existing governance conflicts; external reviewer availability"]
next_action: "ID02: Fakten selbst ermitteln, offene Entscheidungen an ID01."
---
# WO-20261124-GRILL-DESIGN — Grill-Entscheidungen und Shared Language

Owner: ID02; keine CLAIM/ACK-Aussage.

## Task
Vorhandenes Glossar, agent-team-plan, Guide §3/6/7 prüfen; D4/D7/D9 als Entscheidungsvorschlag, echte offene Fragen markieren. Kein neuer Master.

## Output
Glossar-/ADR-Delta und Spec mit Test-Seams; keine Adoption.

## Abnahme
Alle 12 Knoten mit Quelle, Entscheidung/Offen, Abhängigkeit; ID01-Entscheidungen getrennt.

## Next action
ID02: Fakten selbst ermitteln, offene Entscheidungen an ID01.

## Result contract
FINDINGS | EVIDENCE/SOURCES | ARTIFACTS | RISKS | NEXT_ACTION | QA_STATUS.
