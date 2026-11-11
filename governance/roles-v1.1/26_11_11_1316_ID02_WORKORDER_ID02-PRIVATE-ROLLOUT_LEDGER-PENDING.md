---
name: ID02-PRIVATE-ROLLOUT
version: 1.0.0
status: REVIEW_REQUIRED
agent_id: ID02
agent_name: ChatGPT Private
executor: OpenAI Codex
executor_instance: /root
provider: OpenAI
model_id: null
timestamp: 2026-11-11T13:16:00.928632+01:00
ticket_id: WO-20261111-ID02-PRIVATE-ROLLOUT
ledger_id: null
registration_status: PENDING
role_register_version: NEXUS-ROLES-v1.1
---
# Rollenänderung — Bekanntgabe und Work Order an ID02–ID08
## ID01-Festlegung 2026-11-11 — verbindliche Rollenbezeichnung
ChatGPT Private = ID02 — ChatGPT Private / ChatGPT Chief Orchestrator.
Maßgeblich: NEXUS-ROLES-v1.1, Manifest §4: https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
Historische Zuordnungen „ChatGPT Private = ID03“ und „ChatGPT Business = ID02“ sind für die aktuelle Benennung überholt. ID03 bleibt ChatGPT Assistant / Peer Reviewer; keine automatische Neuzuordnung anderer Instanzen.
Rollen-ID und tatsächliche Runtime getrennt dokumentieren. Für diesen autorisierten Lauf: agent_id/role_id ID02; agent_name ChatGPT Private; executor OpenAI Codex; executor_instance /root; provider OpenAI; model_id null (nicht verifiziert).
Vor neuer Rollenentscheidung aktuellen Manifeststand lesen. Kennung ID02 in neuen Berichten dieser Instanz verwenden; historische Dateien unverändert erhalten.
Publikation, Zustellung, ACK und unabhängige Prüfung getrennt erfassen. Die Bereitstellung allein belegt keine Kenntnisnahme anderer LLMs.
Änderungsautorität: ausdrückliche ID01-Anweisung im Sprachdialog 2026-11-11 zur Ergänzung, Bekanntgabe, WORK/Frontmatter/AGB-Aktualisierung, GitHub-Synchronisierung, Sicherung und Ausrollung.
Koordination: WO-20261111-ID02-PRIVATE-ROLLOUT. Geltung ausschließlich Rollenbezeichnung und deren Verteilung; keine technische Produktionsfreigabe.

## Auftrag / Abnahme
OWNER_ID: ID02; APPROVER: ID01; PRIORITY: P0.
OBJECTIVE: aktuelle Kennung eindeutig verbreiten und alte Zuordnungen als historisch abgrenzen.
INPUTS: Manifest §4 v1.1, WORK/_AGBS v005, WORK/_FRONTMATTER v005, Baseline, Ticket Registry, GitHub AGENTS.md.
TASK: aktuelle Quellen sichern, Rollenverweise aktualisieren, Bekanntgabe im bestehenden Kanal veröffentlichen, GitHub-Spiegel aktualisieren; reale Empfängerbestätigungen einholen.
EXPECTED_OUTPUT: versionierte Quellen, SHA256/Readback, vorhandenes file-registry.jsonl ergänzen, ACK-Zeilen in bestehender Ticket Registry.
ACCEPTANCE_CRITERIA: aktuelle Quellen verweisen widerspruchsfrei auf v1.1; erhaltene Rohbytes geprüft; GitHub-Commit nachgewiesen; jeder Empfänger bestätigt selbst Rollenstand und Runtime. Keine erfundenen ACKs.
DEPENDENCIES: erreichbare Runtime jedes Empfängers, unabhängige Prüfung, Ledger-Vergabe durch zuständigen Schreiber.
RISKS: alte Prompts/Chats lesen möglicherweise keinen neuen Bootstrap; veröffentlichter Auftrag aktiviert keine fremde Runtime.
NEXT_ACTION: ID03–ID08 lesen aktuelle Quellen und bestätigen im bestehenden Ticketregister; ID03 prüft die Änderungen unabhängig.
ACK-Syntax: ACK NEXUS-ROLES-v1.1 | role_id | executor_instance | provider/model_id | read_at | conflicts | evidence_url
ID02 bestätigt für /root den gelesenen v1.1-Stand in diesem Lauf. ID03–ID08: PENDING_ACTUAL_RESPONSE.
ID09/ID10 bleiben inaktiv; keine Aktivierung.
QA_STATUS: lokale Konsistenzprüfung und Provider-Readback separat im Abschlussnachweis; unabhängige Prüfung offen.
