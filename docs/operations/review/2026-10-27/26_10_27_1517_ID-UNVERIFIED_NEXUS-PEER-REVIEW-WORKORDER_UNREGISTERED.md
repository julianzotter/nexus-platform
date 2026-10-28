---
name: NEXUS-AI-AEC-OS-MULTI-LLM-PEER-REVIEW-WO
version: v0.4.0-review
status: REVIEW
created_at: '2026-10-27T15:17:43+01:00'
timezone: Europe/Vienna
actor_role_id: UNVERIFIED
executor_instance: ChatGPT text/document production
owner_id: ID01
artifact_id: UNREGISTERED_LEDGER_CONFLICT
human_gate: PENDING
source_of_truth: Google Drive / _developement / LLM-LOCAL-SSOT / WORK
source_policy: GOVERNANCE_REFERENCE_ONLY; NO_SILENT_ADOPTION
---
# WORK ORDER — NEXUS AI-AEC-OS Independent Cross-LLM Peer Review
**VERSION:** v0.1.0-REVIEW · **CREATED:** 2026-10-27T15:17:43+01:00 · **STATUS:** `OPEN / UNCLAIMED / NOT_DELIVERED` · **OWNER:** ID01 · **PRIORITY:** P0
**TICKET_ID:** `PROPOSED-WO-NEXUS-MANUAL-STATUS-PEER-20261027` (**noch nicht** als Ticket Registry-ID vergeben). `artifact_id=UNREGISTERED_LEDGER_CONFLICT`. Kein Fake-CLAIM/ACK/Review.

## 1. MAIN GOAL / ARBEITSPAKET
Unabhängige formale, technische, juristische, normative, informationsarchitektonische und betriebliche Prüfung der hier erzeugten vier Review-Artefakte: (A) `NEXUS ... SYSTEMSTATUS ... .md`, (B) `NEXUS ... USERMANUAL ... .md`, (C) gleichnamiges PDF, (D) `nexus_knowledge_object_schema_v0.4.0_REVIEW.json` plus synthetisches Fixture. Dazu liegende Referenzberichte, AGB v003, Manifest/Baseline, WORK `Folder.md`, Ledger/Logs/Originalnormen soweit Rechte bestehen.
**OUTCOME:** ein überprüfbarer Konsens-/Dissensreport mit einzelnem Reviewer-Mandat, echter Quellenprüfung, negativen Gegenbeispielen, codefähigen Korrekturen und ID01-Entscheidungsvorlage. Kein Mehrheitsentscheid ersetzt eine technische Primärquelle oder unabhängige Solverkontrolle.

## 2. REVIEW-PANELS (alle tatsächlich erreichbaren Rollen, Capability vorher testen)
| Rolle nach Manifest | Gewünschter Review-Fokus | Zustell-/Ausführungskriterium |
|---|---|---|
| ID02 ChatGPT | Orchestrierung, Statusmodell, E2E, Konsolidierung | tatsächliche Session/Runtime + Empfangs-ACK |
| ID03 ChatGPT Peer | Governance, Namen/IDs, State/QA, positive/negative Testmatrix | nicht Autor desselben Diffs als einziger Reviewer |
| ID04 Gemini | Quellen-/Auditkette, Sprach-/Konzeptmapping, Memory/Drive-Routing | direkter Zugriff/Test nachweisen |
| ID05 Perplexity | unabhängige Norm-/Primärquellen-/Wien-Rechtsrecherche | Normausgabe + Originalfundstelle |
| ID06 Claude | Code-/Schema-/Parser-/Regressionstest sowie Architekturfähigkeit | tatsächliche CLI/Tests/Commit-Hash |
| ID07 DeepSeek | adversariales Audit, Falsifikation, alternative Fehlerpfade | laut WO 0097 nur Text-/Chat-Übergabe, keine Git-/Drive-Rechte annehmen |
| ID08 Ollama local (optional) | Offline-/Privacy-/kleiner Kontext; Parser-Contract-Replay | nur bei belegter lokaler Runtime |
**Lieferung = nur Auftrag vorbereitet.** Keine der Rollen gilt durch Erstellung dieser Datei als tatsächlich gestartet oder informiert. Externer Empfänger muss reale `CLAIM <ticket_id> <role>` und `ACK` protokollieren. `[G02,G03,G05]`

## 3. PRÜFMATRIX / AKZEPTANZKRITERIEN (14 Gates)
| Gate | Prüfgegenstand | Muss-Nachweis |
|---|---|---|
| Q01 | Geltung/Hierarchie | AGB v003, Manifest-/Baseline-Konflikte lückenlos |
| Q02 | Rollen & Runtime | kanonische IDs, Provider, Authentifizierung getrennt |
| Q03 | Pfade/SSOT | Drive/GitHub/WORK/MCP/SKILLS/Index-Identitäten korrekt |
| Q04 | Dateiregel & Ledger | Namenssyntax, Exceptions, atomare IDs, History |
| Q05 | CERM/CIM/COM | 23 Core-Klassen, `IS_A` nicht mit `USES` verwechseln |
| Q06 | Ontologie/Signale | Domain, Subdomain, Glossar, de-AT/en-Mappings getrennt |
| Q07 | KO JSON Schema | schema-validate; 1 positive + ≥3 negative Fixtures, Fehlerfälle |
| Q08 | Parsing & Chunk | Tabellen, Formeln, Locator, Quell-/Normversion, Ambiguität |
| Q09 | Retrieval & RAG | ID-Lookup, Evidenzabstention, Source-Recall, Falsche Treffer |
| Q10 | Engineering Solver | Dimension, Randbedingungen, Solver-CI, unabhängiger Referenzfall |
| Q11 | Norm AT/Wien | ONR/ÖNORM/Gen2/NA, ETA/EAD-Anwendungsabgrenzung, Rechtsstand |
| Q12 | Security/ACL | credential, least privilege, injection, idempotenz, retry |
| Q13 | Runtime/State | FALSE_GREEN, Poller, Sync, ACK, Liveness, Restore |
| Q14 | Artefakt/Docs | Markdown/PDF Konsistenz, Glossar, Accessibility, Links, Version |
**Evidenzform:** `finding_id`, severity(P0/P1/P2), `claim`, Originalquelle-ID/Locator/Edition, negative evidence, vorgeschlagene minimale Korrektur, reproduzierbarer Test, `test_status`, Reviewer-Runtime, Inputhash, next action.

## 4. UNABHÄNGIGKEITS- UND KONSENSREGEL
- Jeder Reviewer erhält **denselben fixierten Inputmanifest-Hash**, prüft die Originale selbst, liefert zuerst einen **eigenen Bericht ohne Sicht auf andere Schlussfolgerungen**. Autor≠Reviewer; korrelierte Modell-/Quellenantworten nicht als unabhängige Mehrfachbeweise zählen.
- Synthese klassifiziert `CONSENSUS_VALIDATED`, `CONSENSUS_UNGROUNDED`, `DISSENT_UNRESOLVED`, `OPEN_EVIDENCE`, `FALSE_CLAIM`, `CHANGE_REQUIRED`. Fachentscheidungen nur bei nachvollziehbarer Begründung/Fundstelle. Keine Prozent-Confidence ohne Messung.
- Bei P0-Dissens: `BLOCKED`; Autor bearbeitet minimalen Diff, reproduziert dieselben Tests, unabhängiger Re-Review auf finalem Code-/Dokumenthash. Danach ID01 Human Gate.

## 5. LIEFEROBJEKTE / WORK-ROUTING
1. Reviewer-Einzelberichte mit `STATUS/CHANGED/TESTS/SOURCE_STATUS/RISKS_GAPS/NEXT/QA_STATUS/LOG` und `CLAIM/ACK`-Beleg.
2. `peer-review-matrix.json` mit `reviewer_role`, `runtime`, `artifact_hashes`, Q01–Q14, `severity`, `source_locator`, `proposed_patch`.
3. `consolidated-review.md` mit kritischen Konflikten, Test-/Korrekturanweisungen und ID01-Adoptionsvorlage.
4. `readback_manifest.json` und optional sichere GitHub-Review-PR; keine Produktiv-Änderung aus Review allein.
**Stop:** keine geeigneten Quellen/keine echten Reviewer/kein Ledger = `OPEN/BLOCKED`, niemals fingierter Konsens. **Authorisierung:** diese Datei erlaubt nur Review/Read-only und isolierte reproduzierbare Tests; produktive Konfigurations-/ACL-/Secrets-/Releaseänderungen separater ID01-Entscheid.

## 6. Quellenbezüge
- `[G01–G03]` verbindliche Regeln; `[G05]` laufende Teilaufträge; `[G07–G08]` letzter Delta- und Rolloutstand; `[G09–G10]` Usernormen-/CERM-Brief; `[N01–N07]` offizielle Norm-/Rechts-/EAD-Originale.
