---
name: WO-NEXUS-REPAIR-SPEEDTEAM
version: 1.0.1
status: REVIEW
timestamp: '2026-10-26T16:15:05+01:00'
agent_id: ID-03
executor: OpenAI Codex
runtime_instance: /root
owner_id: ID01
ticket_id: WO-20261026-NEXUS-REPAIR-01
content_hash_sha256: 9136a8f04350e9aab02b6fba15d72de5c584eec931a9b7278bd35140a849273b
hash_scope: body_utf8_after_closing_frontmatter_lf
canonical_location: LLM-LOCAL-SSOT/WORK
execution_status: NOT_REVERIFIED
hash: Siehe hash_scope und content_hash_sha256
supersedes:
  version: 1.0.0
  drive_id: 1KeHVM_VC9nGHZTVyJd_5vBE6xBCG9KwX
  content_hash_sha256: 452c94c26016e6d20c1fbe9fc65d86878e792b3bd33ffd411eb66f06d07611d4
  snapshot_drive_id: 1RueqEUOcsGNoVXp_nMJc6CZJBbP9Ay-O
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


## Umsetzungscheckliste — Delta aus Perplexity-Review
Diese Checkliste ergänzt den unverändert erhaltenen historischen WO-Text oben. Frühere RUNNING-/Instanz-/Testaussagen sind dortige Angaben; in diesem Review nicht als laufende Ausführung bestätigt. Dokumentstatus REVIEW; Ausführung und Produktionsfreigabe separat.

### Feedback und Entscheidungen
- ÜBERNOMMEN: Frontmatter-Muster, Konsolidierung der Ticketergänzungen und klare Vorgängerreferenz. _FRONTMATTER.md ist selbst ENTWURF v001; keine globale Verbindlichkeit behaupten.
- KORRIGIERT: Perplexitys Runtime unter ID-06 ist unbelegt. Tatsächlicher Bearbeiter hier: OpenAI Codex /root; ID-03 aus bestehender Dokumentrolle fortgeführt. Perplexitys Beitrag bleibt ein übermittelter Chatvorschlag, kein selbst gelesener Laufnachweis.
- KORRIGIERT: Wortgetreu/unverändert ist im Vorschlag nicht vollständig richtig: AIM-0007 enthält PL0–PL5 als neue Ergänzung. Original bleibt in v0.3.2 erhalten; Ergänzung separat und ausdrücklich vorgeschlagen.
- KORRIGIERT: Angeblich genaue Alt-Zeitstempel und lückenlose Historie nicht nachgewiesen. Historische Angaben unverändert übernehmen; unbekannte Uhrzeiten nicht erfinden.
- NICHT ÜBERNOMMEN: Mapping 2 → IMPLEMENTED_PARTIAL oder 3 → TESTED als verbindliche Regel. Umsetzung, Tests, Validierung und Freigabe sind verschiedene Nachweise. Originalcodes 0–3 bleiben bestehen.
- NICHT ÜBERNOMMEN: behaupteter Vollfilehash 623d0c37d4cb42c81b045d5ee43d192e3302dc4943b8ab82e9e1ef68b18b1754 ohne Originalbytes; nur USER_REPORTED. Geänderte gespeicherte Ausgabe braucht eigenen Hash. Kein Selbsthash der vollständigen Datei in derselben Datei.
- NICHT ÜBERNOMMEN: Ledger-ID 0055, unbekannte Drive-ID und nicht geprüftes CSV-Schema. CURRENT + DRAFT darf keine freigegebene Gültigkeit suggerieren. Header/Enums/ID-Belegung zuerst lesen, reservieren und Konflikte prüfen. Vollständigen SHA-256 verwenden, keine 16-Zeichen-Abkürzung als Integritätsnachweis.

### A — Dokument-, Identitäts- und Änderungsnachweis
- [x] A01 Aktuelle AIM v0.3.1 und WO v1.0.0 gelesen; _FRONTMATTER.md v001 und WORK-Policy geprüft.
- [x] A02 Perplexity-Behauptungen klassifiziert; keine neue AIM-ID oder bestehende Fortschrittsänderung aus redaktioneller Arbeit.
- [x] A03 Lokaler Vergleich: neun eindeutige Haupttickets; ursprüngliche Inhaltsabsätze, Links, Statuswerte und Dispositionen der v0.3.1 erhalten; Ergänzungen explizit markiert; YAML geprüft.
- [x] A04 Vorgängerbytes als Snapshot in WORK sichern; neue Inhalte speichern; Rohbytes zurücklesen und vollständigen SHA-256 vergleichen. PASS: vollständige Vorgänger- und Ausgabebytes nach Speicherung zurückgelesen und SHA-256 verglichen; Einzelhashes im zugehörigen RUNLOG. Für jede weitere Änderung erneut prüfen.
- [ ] A05 Bestehendes ID-Ledger eindeutig identifizieren, CSV-Header/Statuswerte und letzte IDs prüfen; ID unter Konfliktschutz vergeben; append-only Eintrag mit Datei-ID, Version, vollständigem Bytehash und Vorgänger; danach Readback. Aktuelle Suche nach ID_LEDGER liefert keinen Treffer; keine Abwesenheit behauptet.
- [ ] A06 Ticket-Registry, bestehender Wegweiser und Runlog mit tatsächlich gespeicherten Artefakten konsistent verknüpfen; keine konkurrierende Registry.
- [ ] A07 Globale Adoption des Frontmatter-/Statusschemas und ggf. Mapping der lokalen Codes separat prüfen und dokumentieren. UNKNOWN statt rückdatierter Historie.
- [ ] A08 Paralleles Schreiben: authentifizierte Writer, Claim/Lease oder CAS; Konflikt als Fehler, keine stille Überschreibung. Dieses Update nutzt Frischlese-Vergleich, keinen atomaren CAS-Nachweis.

### B — Kommunikations- und Auftragsbetrieb (weiterhin offen)
- [ ] B01 WORK-Zugriffe frisch prüfen; legitime Writer sichern; Rechtehärtung und Negativtest durchführen. Alte anyone:writer-Befunde sind Quellenbefunde, kein neuer Live-Rechtetest.
- [ ] B02 Capability-Rückläufe WO-REG-CAP-001 einholen, tatsächliche Runtime/Account-Identität und ACK nachweisen; Ablage ist keine Zustellung.
- [ ] B03 Intervalle 1/10/30/60 Minuten und 00/06/12/18 Europe/Vienna pro Runtime testen; Minutenmodus nur expliziter WO mit Scope, Ablauf und Stop-Nachweis; Wochenwartung terminieren.
- [ ] B04 Ein Auftrag vollständig: Erkennung → Claim → Bearbeitung → Prüfung → Ablage → Byte-Readback → ACK → Abschluss. Gleiche ticket_id; Doppelzustellung, Ausfall, fehlende Credentials, Schreibfehler und Wiederanlauf testen.

### C — Parser, Wissensgraph und Abnahme (weiterhin offen)
- [ ] C01 Aktuellen PR-/Commitstand lesen; Parser-Integritätsbefunde schließen; Regression, unabhängige Gegenprüfung und realer Zielbetrieb nachweisen. Frühere Testzahlen sind versionsgebunden.
- [ ] C02 White-Paper-Fassungen konsolidieren; Technik-Hauptachse, Recht-Nebenpfad, Deutsch als Hauptsprache und englisches Mapping in ein datiert angenommenes Domänenprofil überführen; Normausgaben, Geltung und Quellen prüfen.
- [ ] C03 Ingestion → Registry → Quelle/Seite → Chunk → Kandidatenobjekt → Graph/Vektor-Retrieval testen; Replay ohne Dubletten, Manipulation blockiert, fehlende Evidenz führt zur Enthaltung.
- [ ] C04 Save-Template-Installation getrennt von ZIP-Ablage und Methodenregistrierung nachweisen.
- [ ] C05 Unabhängige Abnahme und ID01-Freigabe für Betrieb, Inhalte und Engineering getrennt dokumentieren. Redaktionelle Konsolidierung ist keine Produktionsfreigabe.

### Quellen
- Perplexity: vollständiger Vorschlag im aktuellen ID01-Chat; keine separate MD und keine Originalbytes des behaupteten Hashes vorgelegt.
- Frontmatter: https://drive.google.com/file/d/1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi/view (v001, ENTWURF).
- AIM: https://drive.google.com/file/d/1y7jmHlyxq7Ja2xA2FM6MJapOjIkIMlqZ/view (gelesene Basis 0.3.1).
- WORK-Policy: https://drive.google.com/file/d/11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH/view (0.4.0-pilot; ältere Befunde).
- Evaluierungsbogen: https://drive.google.com/file/d/1PN9FKKPtujQMfTMFZTh4GsX-sSGHV8TR/view.
- White Paper AEC: https://drive.google.com/file/d/16apTjdDsVy-cEK_A6552FJVgnZv8DHnQ/view.
- Quellen-Linkliste: https://drive.google.com/file/d/135k1DB7KIC9xMaoFBBBEHl6GuObsd2OH/view.

## Historie v1.0.1
2026-10-26T16:15:05+01:00: OpenAI Codex /root ergänzt auf ID01-Auftrag die Umsetzungscheckliste nach Prüfung des Perplexity-Chatvorschlags. Historischer WO-Body erhalten; keine früheren Ausführungsbehauptungen erneut bestätigt.
