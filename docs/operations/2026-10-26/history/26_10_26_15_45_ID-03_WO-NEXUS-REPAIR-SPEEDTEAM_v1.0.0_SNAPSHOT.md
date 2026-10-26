---
name: WO-NEXUS-REPAIR-SPEEDTEAM
version: 1.0.0
status: RUNNING
timestamp: 2026-10-26T15:45:04+01:00
agent_id: ID03
executor: OpenAI Codex
runtime_instance: /root
owner_id: ID01
ticket_id: WO-20261026-NEXUS-REPAIR-01
content_hash_sha256: 2ef1674862711568bad34c5fa1c8d18fe7b5c368bb7520a063249b0e4ddb1530
hash_scope: body_utf8
canonical_location: LLM-LOCAL-SSOT/WORK
---

# Speed-Team-Rollout: Übergänge schließen

## Betriebsvertrag
TICKET_ID: WO-20261026-NEXUS-REPAIR-01
Auftraggeber/Owner: ID01. Aktiver Executor: OpenAI Codex /root, ausführende Koordination dieser ausdrücklich autorisierten Reparatur. Keine externe Rollenübernahme erfunden.
Status: RUNNING. Priorität P0. Eingaben: Reparatur-One-Pager, CURRENT Manifest/Baseline, White Paper, Parserlieferung, vorhandenes Ledger und Ticket Registry.
SSOT: LLM-LOCAL-SSOT, operativer Rücklauf: WORK. Code/Tests/Reviews: GitHub-Branch+PR. Keine neue konkurrierende Registry.

## Parallele Arbeitspakete
| Paket | Verantwortung laut Rollenregister | Aufgabe / konkretes Ergebnis | Acceptance | Startnachweis |
|---|---|---|---|---|
| R1 | ID02 Koordination | Bestand nachregistrieren, Zustände konsolidieren, zentrale Verweise | eindeutige Ledger-IDs; Hash-Readback; Ticket-Referenzen | aktiver Codex /root im Auftrag ID01; externer ID02-ACK offen |
| R2 | ID03 QA | Parser unabhängig angreifen, Regressionsfälle, Review | Befund -> reproduzierbarer Test -> Fix -> unabhängige Gegenprüfung | separate Codex-Instanz review_parser, kein externer ID07 behauptet |
| R3 | ID06 Implementierung | Parser-Integritätsbefunde und falsches Grün im Poller reparieren | Tests vor Änderung; Branch/PR; nachher Tests+Lint; eindeutiger Commit | separate Codex-Instanzen fix_integrity und repair_runtime; keine Claude-Ausführung behauptet |
| R4 | ID04 Evidenz | Provenienz, Byte-Hashes, Runlog, Ausgaben/Readbacks konsolidieren | Datei-ID+Version+SHA256+Quelle+Zeit+Status+Instanz pro Ergebnis | root führt aktuellen Bestand; externer ID04-ACK offen |
| R5 | ID05 Quellen | White-Paper-Links und Mapping-Primärquellen prüfen | genaue URL/Ausgabe/Geltungsbereich oder unbelegt | EXTERNAL_ACK_PENDING; nicht automatisch gestartet |
| R6 | ID07 unabhängige Prüfung | Code/Tests und Technik-/Recht-Trennung falsifizieren | separate Instanz, Findings mit Evidenz, keine Selbstfreigabe | externe Ausführung nicht belegt; lokale separate Review-Instanz aktiv |
| R7 | ID08 lokaler Pilot | kontrollierter Ingestion->Kandidaten->Retrieval-Slice | Wiederholung ohne Duplikate; Manipulation blockiert; Quellen-Locator | Codex pipeline_slice aktiv; kein Ollama-Lauf behauptet |
| R8 | ID01 Human Gate | Rechtehärtung sowie Software-/Inhaltsfreigabe getrennt entscheiden | tatsächliche Entscheidung und Zielbetriebsevidenz | offen; keine Freigabe aus Speed-Auftrag abgeleitet |

## Vertical Slices und Grenzen
V1: gespeicherte Lieferung -> Byte-Hash -> bestehendes ID-Ledger -> Ticket -> Wegweiser -> Readback.
V2: Rohtext -> Parserledger -> Quellenfragmente -> Kandidaten-Graph -> exakte Retrieval-Abfrage; Negativfall Manipulation und idempotenter Replay.
V3: fehlende Zugangsdaten -> BLOCKED + Fehlerexit; Doppelzustellung, Initialbestand und Wiederanlauf getrennt prüfen.
Trial-and-error nur isoliert, mit eingefrorenen Eingaben und dokumentiertem Fehler; keine stillen Produktionsänderungen.

## Bereits belegte Blocker
- WORK hat bei Live-Metadatenabfrage am 26.10.2026 weiterhin type=anyone, role=writer. P0. Der aktuelle Connector bietet keine Berechtigungsentziehung; keine Härtung behauptet. Berechtigte Zugänge vor Entfernung erhalten.
- Parser-Integritätsbefunde verhindern Freigabestatus bis Fix und Gegenprüfung.
- Save Template: Archiv und Registrierung sind getrennt von tatsächlich installierter persönlicher Vorlage; Installationsnachweis fehlt.
- Ablage weckt externe Modelle nicht. Keine externen ACK, Agentenverfügbarkeit oder Laufzeiten erfinden.

## Rücklauf / Evaluation / Verbesserung
Jedes neue Log, Statusreport und Artefakt: YY_MM_DD_HH_mm_ID-XX_<THEMA>_vX.Y.Z; UTC-Offset Europe/Vienna im Frontmatter. Maschinenfelder: run_id, ticket_id, artifact_id, agent_id, executor_instance, provider/model soweit bekannt, source_ids, inputs, outputs, hash_scope, QA/status, next_action.
Unabhängige Rückläufe bleiben einzeln erhalten. Danach Findings/Evidenz/Fixes/Testresultate/Restlücken konsolidieren. Improvement nur auf belegte Deltas beziehen, keine erfundenen Erfolgsquoten.
Kein DONE für Gesamtbetrieb vor Abnahmekriterien. Nur abgeschlossene Teilpakete separat DONE setzen; Rest REVIEW_REQUIRED/BLOCKED.

## Quellen
Reparaturplan: https://drive.google.com/file/d/1_gGFxQ0lQli-DIkbDpogaXXt25FkntTc/view
Manifest: https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
Baseline: https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit
Bestehende Ticket Registry: https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit
Vorgänger-WO KGLEIT-01: https://drive.google.com/file/d/1pFm3SEp9K8kIHdz3EO_lWXJd5ucc4VQd/view
