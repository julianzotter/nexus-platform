---
name: _GAP
description: Steuerdatei – Register aller festgestellten, gemeldeten und nicht behobenen Lücken, Mängel und Inkonsistenzen (Baseline, Reporting, GitHub, FAQ, Frontmatter, Logs)
version: v0.1
status: PROPOSED (neue Steuerdatei, Freigabe ID01 offen)
owner_file: ID06
timestamp: "2026-11-23T19:50+01:00"
regel: append-only; neue Lücke = neue Zeile; Statuswechsel = neue Zeile mit gleicher GAP-ID, nie Zeile ändern
statuswerte: OPEN | IN_PROGRESS | BLOCKED | DECISION_ID01 | CLOSED
quellen: [MAN 1POfiQCW…, BAS 1CdwNHr6…, _AGBS.md v007.1, Folder.md 1nDjF78d…, WORK-Dateien 2026-11-23, GH nexus-platform REST]
---
| GAP | Bereich | Lücke / Mangel | Beleg | Owner | Status | Seit |
|---|---|---|---|---|---|---|
| G01 | GitHub | OAuth abgelaufen: "Drive to GitHub" und "GitHub to WORK" failure | Run 45198599526, Schritt "Check Drive credentials" | ID01 | DECISION_ID01 | 2026-11-16 |
| G02 | GitHub | Monitor fail-closed ("Assert operational monitor evidence") | Run 45198194995 | ID06 nach G01/G05 | BLOCKED | 2026-11-23 |
| G03 | Baseline | Basic Instructions nicht aktualisiert; v3.1 (ID03) nicht freigegeben | BAS Stand 2026-09-28 | ID01 | DECISION_ID01 | 2026-11-23 |
| G04 | Register | _CAPABILITIES.jsonl beschlossen, nicht angelegt; Konflikt AGB §6.1 (kein paralleles Register) und §9 | Sprachrunde, AGB | ID01 | DECISION_ID01 | 2026-11-23 |
| G05 | Register | file-registry.jsonl: ID03-Delta (4 Zeilen) ungemergt; Tagesartefakte ID06 unregistriert | Capability-WO 1y0DSTvk…, Abschnitt Registerdelta | ID06 | OPEN | 2026-11-23 |
| G06 | Ledger | WO-Merge Schritt 6: SHA256 für 0212-0235 fehlen | Report 26_11_23_1940_ID06_REPORT_LEDGER-MERGE | ID06 | OPEN | 2026-11-17 |
| G07 | Ledger | Zwei Dateien "00_ID_LEDGER.csv" im SSOT-Root (2127 B alt, 75843 B Master) → lokaler Konfliktname, Cloud-Umbenennung | Drive-Metadaten 1Qso4VQE… | ID01 (Move-Freigabe) | DECISION_ID01 | 2026-11-23 |
| G08 | Reporting | ACK zu WO-BASELINE-EVAL fehlt: ID02, ID04, ID05, ID07, ID08 | WORK-Suche | je ID | OPEN | 2026-11-23 |
| G09 | Baseline | T3b lokaler Mount nur bei ID06 belegt; ID03 BLOCKED, ID05 FAIL | Prüfmatrix | strukturell | OPEN | 2026-11-23 |
| G10 | Baseline | T5: zwei Rechenfälle (ID05 k_h=1,0 / ID06 k_h §3.3(3)); keine Normausgabe/NA; Sollwert vom selben Autor | FAQ ID06 W3, Review ID03 | ID01 + ID07 | DECISION_ID01 | 2026-11-23 |
| G11 | Baseline | T6 lokales RAG: kein Endpunkt, keine Golden-Frage | Review ID03 | ID01/ID06 | OPEN | 2026-11-23 |
| G12 | Review | ID06 lokaler Push/G:-Write ohne fremden Beleg; ID05 und ID06 gleiche Modellfamilie; ID03 nur intern geprüft | Review ID03 §5.2, ID05-Frontmatter | ID02/ID07 | OPEN | 2026-11-23 |
| G13 | Governance | AGB §9 "Claude-ID offen" ↔ MAN §4 ID06 = Claude | AGB, MAN | ID01 | DECISION_ID01 | 2026-11-17 |
| G14 | Governance | Ledger-Nummernvergabe: BAS §7 Nachtrag (ID03) ↔ AGB §6.6 (Claude) | BAS, AGB | ID01 | DECISION_ID01 | 2026-11-17 |
| G15 | Governance | Doppelter Startbeleg: LLM-HISTORY-LOG (AGB §2.3) ↔ START_ACK WORK (Ergänzung 2026-11-23) | AGB | ID01 | DECISION_ID01 | 2026-11-23 |
| G16 | Governance | Rollenregister-Links auf Google Doc statt MD (AGB §1: MD kanonisch) | BAS §17, RDM, AGENTS.md | ID02 | OPEN | 2026-11-17 |
| G17 | Governance | Baseline-Kopf enthält ID02-Rollenblock ↔ BAS §17 | BAS | ID02 | OPEN | 2026-11-11 |
| G18 | Governance | Folder.md sync_rule "kein bidirektionaler Sync" ↔ Workflows Drive↔GitHub | FLD, .github/workflows | ID01 | DECISION_ID01 | 2026-11-16 |
| G19 | Reporting | Vier Statusquellen ohne Führung: Ticket Registry, Folder.md, Kontrollpanel, WORK-Berichte | BAS MUST-152, FLD, AGB | ID01 | DECISION_ID01 | 2026-11-23 |
| G20 | FAQ | Fragmentiert: 7 Dateien in WORK + GDoc FAQ V1.0 + Zu-den-FAQs 07.08; FAQ-SSOT nicht festgelegt | Sweep 1940 | ID01 | DECISION_ID01 | 2026-11-23 |
| G21 | FAQ | Duplikat "26_11_23_FAQ NEXUS-AI Baseline und Kernfunktionen.md" = ID05-FAQ (sha256 92531141…) | Hash ID06 | ID01 (Move) | OPEN | 2026-11-23 |
| G22 | Frontmatter | Nicht AGB-konform: 26_11_23_ID04_FAQ.md (kein HHMM, kein Frontmatter, text/plain); DeepSeek-Export ohne ID; FAQ_Question+Answers ohne ID; IDNN-Protokoll id:NN, storage:sandbox_only | AGB §4 | Autoren | OPEN | 2026-11-23 |
| G23 | Provenienz | Texte als "ID 06" nicht von ID06 (Sprachrunde, DeepSeek); WORK anyone:writer, Herkunft nur über Dateiname | FLD problems, Sitzung | ID01 | OPEN | 2026-11-16 |
| G24 | Provenienz | Uploader der ID05-Datei technisch nicht authentifiziert | Review ID03 | ID05 | OPEN | 2026-11-23 |
| G25 | Baseline | ID06-v3-Entwurf fehlerhaft (NN, Mount abgeschwächt, T6 Doku, T5 Eigen-Soll) | Review ID03 | ID06 | CLOSED (ersetzt durch v3.1-Vorschlag) | 2026-11-23 |
| G26 | Reporting | ID06-Startzeile fehlte | LLM-HISTORY-LOG | ID06 | CLOSED 19:40 (nachgeholt, nicht rückdatiert) | 2026-11-23 |
| G27 | WORK | >2000 Dateien; ≥815 ID-UNVERIFIED, ≥346 UNREGISTERED; Bereinigungsplan ohne Freigabe | Inventar ID06 18:39 | ID01 | DECISION_ID01 | 2026-11-23 |
| G28 | Code-SSOT | Skripte in WORK, SCRIPTS, NEXUS.MCP.SERVER, MCP-ACCESS-TOOLS; P205-ps1 hashgleich doppelt | Review ID03 §5.3 | ID01 | DECISION_ID01 | 2026-11-23 |
| G29 | Runtime | device_bash: G: nicht mountbar (VM) | ID06 RUNLOG | – | OPEN (Workaround Bridge-Dateitools) | 2026-11-23 |
| G30 | GitHub | Branch id06/baseline-eval-20261123 ohne PR/Merge | GH REST | ID01 | DECISION_ID01 | 2026-11-23 |
| G31 | Reporting | Folder.md Stand 2026-11-16, Status-Projektion veraltet | FLD | Ledger-/Status-Schreiber | OPEN | 2026-11-16 |
| G32 | Reporting | Fremdbericht 19:45 mit falschen Aussagen: Branch "nicht sichtbar", Ledger-Merge "offen", Original/Duplikat vertauscht | GH REST (Branch HEAD 9b00a58), Ledger 0257 | Autor des Berichts | CLOSED (widerlegt, siehe Bericht 1950) | 2026-11-23 |
| G12 | Review | Ledger-Merge: ID02-Watch 20:00 bestätigt Zeile 0257 im Master (Existenz, kein Byte-Review); ID03 kündigt unabhängige Prüfung an | 26_11_23_2000_ID02_STATUSREPORT… | ID03 | IN_PROGRESS | 2026-11-23 |
| G27 | WORK | Präzisiert: WORK hat 3910 direkte Einträge (ID02-Scan 9 Listenseiten) | ID02-Watch 20:00 | ID01 | DECISION_ID01 | 2026-11-23 |
| G33 | Frontmatter | _FRONTMATTER.md v007 nur ENTWURF, nicht freigegeben; parallel _FRONTMATTER_v006-PROPOSAL im SSOT-Root | ID02-Watch 20:00, SSOT-Root-Liste | ID01 | DECISION_ID01 | 2026-11-23 |
| G34 | Register | Registrierungs-Handoff WO-20261123-AICADFEM-REGISTER-01 (P0) nennt "CLAUDE_LEDGER_WRITER" statt Rollen-ID aus MAN §4 | ID02-Watch 20:00 | Autor WO | OPEN | 2026-11-23 |
| G35 | Workorder | 4 neue AICADFEM-WOs ohne Auftragsversion und ohne explizite ID01-Ausführungsfreigabe | ID02-Watch 20:00 | ID01/ID02 | OPEN | 2026-11-23 |
| G36 | Review | ID02 und ID03 laufen beide auf OpenAI/Codex; Review ID02↔ID03 nicht provider-unabhängig | ID02-Frontmatter, ID03-Frontmatter | ID01 | OPEN | 2026-11-23 |
| G37 | Register | file-registry.jsonl unverändert seit 2026-11-23 14:15:51Z (430662 B); keine heutigen Baseline-/FAQ-Artefakte registriert | ID02-Watch 20:00 | ID06 (AGB §6.6) | OPEN | 2026-11-23 |


## ID03-Nachtrag — Evaluierung, Rollen-Prüfmatrix und aktueller GAP-Stand

```yaml
append_version: v0.1-ID03-r2
artifact_category: gap_register
content_categories: [evaluation, role_test_matrix, faq_corrigendum, open_issues]
role_id: ID03
executor_instance: /root
provider: OpenAI
model_id: null
observed_at: "2026-11-23T19:16:16Z"
timezone: Europe/Berlin
work_order: WO-20261112-ID02-CAPABILITY-ACK
run_id: ID03-BASELINE-EVAL-20261123T181602Z
artifact_id: gdrive:1_o3yrBjeZIKYa6ztiwGSE9jW-bvA2sRf
source_of_truth_for_this_artifact: GOOGLE_DRIVE
authoritative_role_register: gdrive:1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn#4
registration_status: REGISTRATION_PENDING
governance_adoption: NOT_CHANGED
document_review: INTERNAL_DOCUMENT_REVIEW_PASS
reviewed_draft_sha256: dcb420477a94a59759f917ac55965fb173b4cafed243843a93d873ae5c81b3ad
reviewer_instance: /root/review_governance
previous_reviewed_draft_sha256: 9909f254472c6d5263c6d5da95b6ed7bb29b870153ed7a658c630e97da1c176c
review_scope: document_consistency_only_no_external_role_acceptance
previous_bytes: 7120
previous_sha256: 881f9cb0a61010f0561afd764926b739af22e4f83423ea65514110ca5672e423
backup_ref: gdrive:1FVT_sfViLLEIPXX9oj9V753b59RsU_Xy
full_file_sha256_receipt: gdrive:1y0DSTvkH_04avqI8TZKyaKOy05gWfZgx
```

### 1. Geltung, Umfang und Bewertungsregel

Prüfstand dieses Nachtrags: 2026-11-23T20:16:16+01:00. Die davorstehenden 7.120 Bytes bleiben unverändert: ursprüngliche 5.833 Bytes plus fremder Zwischenappend mit 1.287 Bytes. Für die aktuelle Auswertung gilt je GAP-ID das jüngste ausdrücklich zugeordnete Ereignis; der historische Kopf beschreibt die Anlagefassung. Dieses Dokument ist eine auftragsbezogene Evaluierung und offene Befundliste. Es ändert keine globale Rollenautorität, erteilt keine technische Freigabe und ist kein zusätzlicher Master für Tickets, Artefakte oder Fähigkeiten.

Geprüft wurden die unten bezeichneten Governance-Dateien, Ticketdaten, relevanten Baseline-/FAQ-/Laufberichte, Ledger-/Registry-Nachweise und konkreten GitHub-Refs/Actions. Dies ist keine Vollinventur aller Drive-/GitHub-Dateien oder fremden Runtimes. G44–G50 bewahren ausdrücklich gemeldete historische bzw. nicht nachgeprüfte Restpunkte. „Nicht gefunden“ gilt nur für den bezeichneten Suchumfang.

Evidenz: VERIFIED = direkt belegter Befund innerhalb des genannten Umfangs; DERIVED = daraus abgeleitete Regel-/Statusauslegung; CALCULATED = tatsächlicher deterministischer Kontrolllauf; REPORTED_UNVERIFIED = gemeldet, ohne ausreichenden aktuellen Primärnachweis. Datei-Bytes bestätigen weder den technischen Uploader noch jede inhaltliche Aussage.

Tests: PASS = ausgeführt und Soll erfüllt; FAIL = ausgeführt und Soll verfehlt; BLOCKED = erforderliche Voraussetzung fehlt; NOT_RUN = nicht ausgeführt. UNVERIFIED qualifiziert eine Aussage/Herkunft. Ticketstatus, Testresultat, Evidenz, Registrierung und Freigabe bleiben getrennt.

Zählung dieser Sicht: 51 verschiedene GAP-IDs; 41 noch nicht geschlossen (36 OPEN, 5 BLOCKED); zehn geschlossen oder gebündelt. G24/G29/G37 sind nur dedupliziert; die Elternbefunde bleiben offen. GAP-Anzahl ist weder Fehlerquote noch Confidence. Frühere Prozent-/Konfidenzzahlen werden nicht übernommen.

### 2. Verifizierter Fortschritt und Korrekturen

- Ledger: 201 → 247 Datensätze, vier Delta-Körper mit 45 Datensätzen 0212–0256 plus Abschluss 0257; Altbytes erhalten, keine doppelten numerischen IDs. Backup-vor-Master-Providerzeitfolge und Rohbytegleichheit geprüft. Der lokale mtime-Guard des fremden Laufs bleibt unbestätigt. 24 fehlende SHA-Felder und Registrierung bleiben offen. 0258 ist ein Kandidat dieses Stands, keine reservierte Nummer. [S09] [S10] [S11]
- ID03: Drive-API-Write/Readback, GitHub-API-Commit/Readback und WORK-Bericht tatsächlich ausgeführt. Das 18:29-Receipt bestätigt drei damals eingefrorene Outputs; die WO wurde zusätzlich bytegeprüft. Für diesen neuen Nachtrag folgen eigene Persistenzbelege im bestehenden WO/Runlog; kein vorgezogenes T4-PASS. [S06] [S07] [S29] [S35]
- Die Startpflichten sind additiv; die Ticket Registry führt die Koordination; Testbranches benötigen keinen Merge. Google-OAuth betrifft die konkreten Drive-Workflows. Main-CI ist erfolgreich, der Monitor scheitert gesondert an operativer Coverage/Scheduler-Evidenz. [S02] [S03] [S24] [S25] [S26] [S27]

### 3. Basic-Instructions-Prüfmatrix je Rolle

Quellengebundener Prüfstand, kein zweites Rollenregister. Rollen stammen aus Manifest §4. ID01 ist der Mensch mit Entscheidungs-/Freigaberolle; ID09/ID10 sind inaktiv. Produktnamen belegen keine Fähigkeiten. [S01]

| Rolle gemäß Manifest | Start / ACK / aktuelle Quellen | Belegte Ausführung oder Ergebnis | Offener Umfang |
|---|---|---|---|
| ID02 — ChatGPT Chief Orchestrator | Historischer Rollen-Selbst-ACK v1.1 im Ticketregister DONE; kein vollständiger neuer Baseline-ACK belegt | Historische Start-/Schedulerbelege sind Quellen, kein heutiger T1–T7-Selbsttest | Aktuelle Regelversion, tatsächliche Runtime, Testumfang und Rollout-Readback fehlen im geprüften Korpus. [S05] |
| ID03 — ChatGPT Assistant / Peer Reviewer | ACK im bestehenden WO; OpenAI-Executor /root; Quellenstände protokolliert | T1a GitHub-API PASS; T2 Bericht PASS; T3a Drive-API PASS; T4 damaliger eingefrorener Umfang PASS; T7 benutzte Drive-/GitHub-Operationen PASS | T1b lokaler Git-Push NOT_RUN; T3b Mount BLOCKED; T5 arithmetischer Kontrollvergleich, normative Abnahme BLOCKED; T6 lokales RAG NOT_RUN. Internes Dokumentreview ist kein externer Rollenlauf. [S06] [S07] [S23] [S29] |
| ID04 — Gemini | FAQ-/Protokollbeitrag vorhanden; vollständiger aktueller Runtime-ACK nicht belegt | Vorhandener Beitrag ist ein Dokument, kein T1–T7-Runreceipt | Tests NOT_RUN/UNVERIFIED im vorliegenden Korpus, nicht pauschal FAIL. [S05] [S22] |
| ID05 — Perplexity | Rollen-ID05 aus Manifest; historische Kennung NN im Protokoll ausdrücklich korrigiert | 4.182-Byte-Protokoll in Drive bytegeprüft | Technischer Uploader UNVERIFIED; kein eigenes Drive-API-PASS daraus ableiten. Mount ohne ausgeführten Fehltest BLOCKED/NOT_RUN. T5-Text verwendet andere Geometrie/Last. [S06] [S18] |
| ID06 — Claude | ACK-/Status-/RUNLOG-Dateien vorhanden; später HISTORY-Start berichtet, neue Fundstelle offen | Vier Remote-Dateien gegen festen Commit bytegleich; Ledger-Merge unabhängig geprüft; Skript-Rechenergebnis kontrolliert | Ursprünglicher lokaler Push, G:-/Bridge-Ausführung und gesamter fremder Sandboxscope unabhängig UNVERIFIED. T5-Normfall, RAG und vollständiger T7-Umfang offen. [S06] [S11] [S23] [S28] [S30] |
| ID07 — DeepSeek | Gesprächsexport mit vermischten Sprecherlabels; kein neuer tatsächlicher Baseline-Laufbeleg | Quellenkritik als berichteter Beitrag erfasst | In der festgelegten Chat-/Upload-Route ohne eigene Drive-/GitHub-/Runtimeausführung; Ausführung dort NOT_RUN. Keine unerfüllbaren Toolaufträge aus dem Rollenlabel ableiten. [S02] [S14] |
| ID08 — Ollama | Kein aktueller vollständiger Runtime-/Baseline-ACK im geprüften Korpus | Historische widersprüchlich benannte Connectorangaben sind kein aktueller Ollama-Test | Modell/Version, Host, Rechte und Tests offen; optionaler Pilotstatus laut Manifest. [S01] [S04] [S05] |

Für neue Runtime-Receipts: Kategorie, Rolle, tatsächlicher Executor, Provider/Modell soweit belegt, run_id, Ticket, Quellen/Versionen, Operation/Scope, Prüfzeit, Resultat und Beleg. Unbekannte Identität bleibt null/UNVERIFIED. [S01] [S02] [S03]

### 4. Aktuelle Ereignisse G01–G51

Zuständigkeiten sind aus Rollen/Work Orders abgeleitete nächste Schritte, keine behauptete Auftragsannahme einer fremden Instanz. P1 blockiert den betroffenen operativen/fachlichen Nachweis; P2 betrifft Konsistenz/Integration; P3 historische oder begrenzte Quellenlücken. Ein Befund stoppt nur seinen betroffenen Schritt.

| GAP | Prio | Status | Evidenz | Aktueller Befund | Quellen | Nächste Zuständigkeit | Schließkriterium |
|---|---|---|---|---|---|---|---|
| G01 | P1 | BLOCKED | VERIFIED | Google-OAuth-Refresh der Delivery und des Drive-Polls scheitert mit OAUTH_HTTP_400_INVALID_GRANT. Der genaue Widerrufs-/Ablaufgrund ist nicht belegt; dies ist kein allgemeiner GitHub-OAuth-Ausfall. | [S26] [S27] | ID01 Zugang; ID06 Laufprüfung | Neuer erfolgreicher Google-Preflight, lesender Poll und tatsächlicher Delivery-Write mit Rohbyte-Readback. Den funktionierenden ChatGPT-Drive-Zugang getrennt behandeln. |
| G02 | P1 | BLOCKED | VERIFIED | Monitor meldet INCOMPLETE: coverage INCOMPLETE und Scheduler FAIL/STALE. Registry-, Knowledge- und PR-Abfrage bestehen im konkreten Run. Die Aussage, OAuth-Erneuerung behebe den Monitor automatisch, ist unbelegt. | [S25] | ID06; ID02 Koordination | Konkrete Coverage-/Scheduler-Anforderungen erfüllen und neuen vollständigen Monitorlauf samt report.json und Evidence-Gate nachweisen; G01 allein genügt nicht. |
| G03 | P1 | OPEN | VERIFIED | Die kanonische Baseline ist unverändert; v3.1 bleibt Prüfvertragsvorschlag. Aktualisierte Evaluierungsdaten sind keine nachgewiesene Übernahme in alle Modelleinstellungen. | [S01] [S02] [S03] [S06] [S07] | ID02 Änderungskontrolle; ID03 Review; ID01 fachliche/strategische Abnahme | Konkrete versionsgebundene Änderung, Vorzustand, unabhängiges Review und CURRENT-Verweis dokumentieren; anschließend tatsächlichen Readback und ACK je Zielruntime belegen. Die aktuelle Update-Anweisung ist bereits Arbeitsautorisierung. |
| G04 | P1 | OPEN | DERIVED | Kein kanonisches aktuelles _CAPABILITIES.jsonl im geprüften Namenssuchumfang gefunden. Ein Capability-Datensatz ist nicht automatisch ein zweites Artefaktregister. Sein Ort, Schema, Writer und Bezug zur bestehenden Registry sind noch nicht belegt. | [S02] [S06] [S07] [S15] | ID02 Schema/Verweise; ID06 Umsetzung | Ein registriertes Ziel mit Rolle, tatsächlicher Runtime, Operation, Scope, Prüfzeit, Ergebnis und Beleg festlegen; bestehende Deltas wiederverwenden. Keine Rollen-IDs neu vergeben. |
| G05 | P1 | OPEN | VERIFIED | file-registry.jsonl blieb beim geprüften Stand unverändert; die vier ID03-Deltas im WO-Abschlussreceipt sind nicht übernommen. Der neue _GAP-Nachtrag und die neuen Versionen benötigen ebenfalls Registrierung. ID06-Tagesartefakte sind anhand ihrer IDs einzeln abzugleichen. | [S07] [S08] [S11] | ID06 als benannter Register-Schreiber | Fehlende Datensätze/Versionen nach aktuellem Readback bestimmen, kollisionsfrei anhängen und Registry-Rohbytes verifizieren. Registrierung nicht mit fachlicher Freigabe verwechseln. |
| G06 | P1 | OPEN | VERIFIED | Ledger-Merge ist abgeschlossen, aber die 24 SHA256-Felder 0212–0235 sind leer. In Abschlusszeile 0257 sind DRIVE_ID und SHA256 leer; Nachherhash/Backup-ID liegen extern vor. | [S09] [S10] [S11] | ID06 | Je Originalartefakt Rohbytes und vollständigen Hash nachtragen; unerreichbare Originale explizit offen lassen. Den Bezug der 0257-Zeile eindeutig machen, ohne einen unmöglichen Vollhash der eigenen Datei in dieselbe Datei zu schreiben. |
| G07 | P2 | OPEN | REPORTED_UNVERIFIED | ID06 berichtet zwei gleichnamige Ledgerdateien und einen 2.127-Byte-Altbestand. Der Master ist per Datei-ID eindeutig; die zweite ID und ihr heutiger Parent sind in diesem Nachtrag nicht unabhängig festgestellt. | [S09] [S11] | ID06 | Beide IDs/Versionen und Referenzen feststellen; nach Inhalts-/Referenzprüfung alte Kopie reversibel archivieren und Parent/ID rücklesen. Die bestehende Bereinigungsautorisierung nicht erneut als fehlend darstellen. |
| G08 | P1 | OPEN | VERIFIED | Aktuelle auftragsspezifische Start-/Capability-ACKs für ID02/04/05/07/08 sind im geprüften Korpus nicht belegt. ID02 besitzt einen historischen Rollen-ACK v1.1; das ist kein heutiger T1–T7-Lauf. ID03-ACK und ID06-ACK sind gesondert belegt. | [S05] [S07] [S12] | Jede tatsächlich aufgerufene Runtime; ID02 führt Zustellstatus | Echte Antwort mit run_id, Quelle/Regelversion, Rolle, Runtime und Scope erfassen; Ticketstatus anhand dieser Antwort aktualisieren. Veröffentlichung oder Schweigen nie als Ausführungs-ACK werten. |
| G09 | P1 | BLOCKED | VERIFIED | ID03 hat keinen identifizierten lokalen Drive-Mount. ID05 ohne ausgeführten Fehlversuch wird BLOCKED/NOT_RUN geführt. ID06 meldet Bridge-/G:-Write; Remote-Bytes sind geprüft, der lokale Ausführungsweg unabhängig UNVERIFIED. Ein rollenübergreifender Mount-PASS fehlt. | [S06] [S07] [S18] [S28] | Je lokal angebundene Runtime | Host, Pfad, dort ausgeführten Write/Readback, Originalhash und passenden Cloud-Readback belegen. API-Persistenz als getrennte Capability behalten. |
| G10 | P1 | BLOCKED | CALCULATED | Für das gespeicherte ID06-Fixture ergibt der unabhängige Python/Decimal-Vergleich eta=0,4474970577408008…; 0,447 und 0,4475 sind Rundungen. ID05s 0,565 stammt aus anderer Geometrie/Last; k_h=1 ist dort keine belegte Eingabe. Normausgabe/NA und vollständiger unabhängiger Referenzfall fehlen. | [S18] [S23] [S39] | ID06 Fixture; unabhängiger fachlicher Reviewer; ID01 Norm-/Projektfreigabe | Einen eingefrorenen Fall mit Eingaben, SI-Einheiten, Faktoren, Normausgabe/NA/Fundstellen, Sollwert und Toleranz prüfen. Eine Zahlenfreigabe allein bestätigt keine Normkonformität. |
| G11 | P1 | BLOCKED | VERIFIED | Direkter Drive-Dokumentzugriff ist belegt, ein tatsächlicher lokaler RAG-Lauf nicht. Eine Dokumentfrage existiert im v3.1-Vorschlag; Pipeline-/Indexbindung und RAG-Akzeptanz fehlen. | [S06] [S07] | ID06 Pipeline; ID03 Akzeptanz | Benannten Retriever/Index mit Corpus-Version und vorher festgelegter Frage aufrufen; tatsächlichen Quellenrücklauf, Fundstelle und passende Assertions prüfen. |
| G12 | P1 | OPEN | VERIFIED | ID03 prüfte ID06-Remote-Bytes und den Ledger-Merge unabhängig; ursprünglicher lokaler Push/Mount-Write und vollständiger fremder Sandboxscope sind damit nicht nachgewiesen. Gesamt-Cross-ID-Abnahme bleibt offen. Gleiche Modellfamilie allein entscheidet keine Unabhängigkeit. | [S01] [S06] [S07] [S11] [S28] [S30] | Separater tatsächlicher Reviewer; ID02 koordiniert | Autor, Reviewerinstanz, geprüften Hash/Stand, Umfang, Ergebnis und Restlücken angeben. Interne OpenAI-Unteragenten nicht als Claude, Gemini oder DeepSeek ausgeben. |
| G13 | P1 | OPEN | VERIFIED | _AGBS §9 und _TROUBLESHOOTING T11 führen Claude weiterhin ohne bestätigte ID, während Manifest §4 eindeutig ID06 definiert. | [S01] [S02] [S17] | ID02 Governance-Änderung; ID03 Review | Aktive Verweise auf Manifest §4 berichtigen; historische Herkunft erhalten. Keine neue Rollen-ID vergeben und keine globale Ersetzung historischer Aliasnummern. |
| G14 | P2 | OPEN | DERIVED | Baseline §7-Nachtrag nennt ID03 für WATCH-Nummernvergabe; _AGBS §6.6 benennt Claude als einzelnen gemeinsamen Register-/Ledger-Schreiber. Die Scopes müssen ausdrücklich qualifiziert werden; daraus folgt keine Erlaubnis für parallele Master-Writes. | [S02] [S03] [S07] | ID02 Zuständigkeitsabgleich; ID06 Register-Schreiber | Operation und Scope von Vergabe, Delta-Erstellung und Master-Append dokumentieren; widersprüchliche allgemeine WO-Formulierungen konkretisieren; vor Nummernvergabe aktuellen Master und Deltas lesen. |
| G15 | P2 | CLOSED | DERIVED | Regelunklarheit berichtigt: _AGBS §2.3 verlangt den HISTORY-Start, die Ergänzung 23.11. zusätzlich START_ACK in WORK. Beide gelten; kein Entweder-oder-Konflikt. | [S02] | ID03 Korrekturreceipt | Als Interpretationsfehler geschlossen. Tatsächlich fehlende Ausführungsbelege bleiben G08/G26; kein fremder Start wird dadurch nachträglich erfunden. |
| G16 | P2 | OPEN | VERIFIED | Die aktive Baseline verweist im Rollenblock und §17 noch auf die native Google-Docs-Kopie; _AGBS §1 nennt die Markdown-Quellen kanonisch. Weitere Links in README/AGENTS sind berichtet, hier nicht vollständig neu geprüft. | [S02] [S03] | ID02; ID03 Linkprüfung | Aktive Einstiegspunkte auf eindeutige MD-Datei-IDs umstellen und rücklesen; historische Spiegel als Quellen erhalten. Einen vollständigen Linkscan nur für den vereinbarten aktiven Umfang behaupten. |
| G17 | P2 | OPEN | DERIVED | Der Baselinekopf enthält einen früheren ID02-Lauf-/Runtimeblock. Ohne klare Scope-Trennung kann dessen Instanzanweisung auf neue ID03-Läufe übertragen werden. Der Block allein ist noch kein zweites Rollenregister. | [S01] [S03] | ID02; ID03 Review | Historischen Laufblock als solchen begrenzen; aktuelle Identität aus Manifest und tatsächlicher Zuweisung ableiten. Keine pauschale Übernahme von /root=ID02. |
| G18 | P2 | CLOSED | DERIVED | Pauschaler Sync-Regelkonflikt zurückgenommen: Folder.md erlaubt GitHub-Reviewsnapshots und untersagt unbestätigte bidirektionale Syncaussagen. Der Drive-Poll liest einen Change-Feed und erzeugt Run-Artefakte; er committet keine Drive-Dateien ins Repo. | [S04] [S27] | ID03 Korrekturreceipt | Interpretation geklärt. Tatsächliche OAuth-/Monitor-/E2E-Lücken bleiben G01/G02/G43. |
| G19 | P2 | CLOSED | DERIVED | Die Führung ist festgelegt: Baseline MUST-152 bestimmt die Ticket Registry als Koordinationsquelle. Folder, Panel und WORK-Berichte haben andere Funktionen; ihre Existenz erzeugt nicht vier gleichrangige Master. | [S02] [S03] [S04] [S05] | ID03 Korrekturreceipt | Autoritätsfrage geklärt. Veraltete Statusprojektionen und fehlende ACK-Nachführung bleiben G31. |
| G20 | P2 | OPEN | VERIFIED | Mehrere FAQ-, Vorschlags- und Chatstände existieren. Der neue ID06-Sweep verweist bereits auf die vorhandene ID03-FAQ als Syntheseziel; eine globale fachliche/operative Adoption dieser FAQ ist nicht nachgewiesen. | [S06] [S12] [S13] [S19] [S21] [S22] | ID02 Redaktion/Verweise; ID03 Review | Bestehende FAQ wiederverwenden und mit zeitgebundenen Korrekturreceipts verknüpfen; Quellenbeiträge als historisch/proposed kennzeichnen. Kein weiterer konkurrierender FAQ-Master. |
| G21 | P2 | OPEN | VERIFIED | ID05-FAQ und die neuere Datei 'FAQ NEXUS-AI Baseline und Kernfunktionen' waren im Rohbytevergleich identisch: 16.065 B, SHA-256 92531141…66a2. Die ID01-Sammeldatei ist anders und kein solches Hash-Duplikat. | [S19] [S20] [S21] | ID06/ID02 Inhalts- und Referenzabgleich | Kanonischen Referenzstand anhand bestehender Verweise festhalten; identische Zusatzkopie reversibel archivieren, ID/Hash/Parent prüfen. Sammeldatei nicht aufgrund ähnlichen Namens verschieben. |
| G22 | P2 | OPEN | VERIFIED | Aktuelle/Historische Quellen mischen fehlendes Frontmatter, abweichende Namenszeit, IDNN und überholtes storage:sandbox_only. Für das IDNN-Protokoll liegen bereits ausdrückliches Rollen-/Speicherkorrekturreceipt und Archivierung der älteren identischen Kopie vor; dies nicht erneut als unerledigt zählen. | [S02] [S06] [S07] [S18] [S21] [S22] | Je Autor/Redaktion; ID03 Prüfschema | Neue operative Dateien mit Kategorie, tatsächlichem Executor, Quelle/Stand und Prüfstatus liefern; historische Rohprotokolle erhalten Kontextverweise. Aktuelle Sicht aus Receipts ableiten, Originalbeweise nicht still umschreiben. |
| G23 | P1 | OPEN | DERIVED | Dateiname, Sprecherlabel und persistierte Bytes authentifizieren keinen Uploader. Folder.md dokumentiert bewusst offene Schreibrechte; die aktuelle ACL wurde in diesem Nachtrag nicht neu abgefragt. Kein automatischer ACL-Widerruf aus diesem Befund. | [S01] [S04] [S06] [S14] | Je Runtime; ID02 Provenienzvertrag | Ausführungs-/Uploadquittung mit tatsächlicher Instanz, run_id und Scope zuordnen oder original_upload_executor=UNVERIFIED führen. Reportierte Rollen nicht als technische Konten behandeln. |
| G24 | P2 | CLOSED | DERIVED | Der ungeklärte ID05-Uploader ist der konkrete Unterfall von G23 und dort weiter offen. Hashgleichheit der Dateien ist davon unabhängig bestätigt. | [S06] [S18] | ID03 Deduplizierung | MERGED_INTO_G23; keine Behebung oder Authentifizierung behauptet. Verhindert doppeltes Zählen derselben Nachweislücke. |
| G25 | P2 | CLOSED | VERIFIED | Die Fehler des alten ID06-v3-Textes sind im ID03-v3.1-Prüfvertragsvorschlag adressiert. Geschlossen ist nur die Entwurfskorrektur; Adoption/Rollout bleiben G03. | [S06] | ID03; separater Dokumentreview | REPLACED_IN_PROPOSAL, nicht ADOPTED oder technisch freigegeben. |
| G26 | P2 | OPEN | REPORTED_UNVERIFIED | Der neue ID06-Bericht meldet einen nachgeholten HISTORY-Start um 19:40. Die dazugehörige konkrete neue History-Datei-/Zeilen-ID ist hier nicht nachgewiesen. Der gelesene frühere RUNLOG allein belegt diese Nachholung nicht. | [S12] [S28] | ID06 | Konkreten HISTORY-Eintrag mit tatsächlicher Erfassungszeit, gelesener AGB-Version und Scope verlinken/prüfen; keine Rückdatierung. |
| G27 | P2 | OPEN | REPORTED_UNVERIFIED | Frühere Zahlen >2000/≥815/≥346 und jetzt 3910 direkte WORK-Einträge auf neun Listenseiten sind berichtete Inventare. ID02-Watch beschreibt seinen Scope; dessen vollständige Seitenzählung wurde hier nicht unabhängig wiederholt. | [S06] [S12] [S41] | ID02 Inventarumfang; ID06 Auswertung | Vollständige Seiten für einen benannten Ordner-/Zeitumfang, Deduplizierungsregel und Zählskript/Ergebnis belegen. Die bereits erteilte reversible Bereinigungsautorisierung nutzen; kein pauschales neues Permission-Gate. |
| G28 | P2 | OPEN | VERIFIED | P205-PowerShell in WORK und SCRIPTS ist hashgleich; seine kanonische Installationsquelle ist nicht festgelegt. nexus_tower.py v0.3 und nexus_tower-1.py v0.2 unterscheiden sich; Launcher und lokaler Import sind Abhängigkeiten. | [S06] [S32] [S33] [S34] | ID06 Code-Verantwortung; ID03 Review | Aktive Caller/Imports/Startbefehle und Installationsquelle bestimmen; erst dann Kopien referenzieren/archivieren bzw. Versionen zusammenführen und relevante Aufrufe prüfen. |
| G29 | P2 | CLOSED | DERIVED | Der berichtete device_bash-G:-Mountfehler und Bridge-Workaround werden als runtimebezogener Unterfall in G09 geführt. Remote-Dateien beweisen den lokalen Toolweg nicht. | [S06] [S28] | ID03 Deduplizierung | MERGED_INTO_G09; kein neuer Mount-PASS und keine Behebung behauptet. |
| G30 | P2 | CLOSED | DERIVED | Ein isolierter Test-/Reviewbranch muss für den GitHub-Persistenztest weder PR noch Merge haben. Fehlender Merge ist deshalb kein Fehler dieses Tests. | [S06] [S29] [S30] | ID03 Korrekturreceipt | Spätere Code-/Governance-Promotion getrennt reviewen. CI-Erfolg immer dem tatsächlich getesteten Commit zuordnen; kein Main-PASS auf neue Branch-Heads übertragen. |
| G31 | P1 | OPEN | VERIFIED | Folder.md ist ein älterer Statussnapshot; seine Ablageregel bleibt davon getrennt. Ticket Registry führt ACK-v1.1-ID03 noch OPEN, obwohl ein echter ID03-ACK im bestehenden WO vorliegt. Der historische ID02-ACK steht bereits DONE. | [S04] [S05] [S07] | ID02 Ticket-/Statuspflege | Aktuelle ACK-Receipts dem passenden Ticket/Regelstand zuordnen und aktive Projektionen mit observed_at/source_ref nachführen. Historische Snapshots nicht als heutigen Laufstatus ausgeben. |
| G32 | P2 | CLOSED | VERIFIED | Die Aussagen 'Branch nicht sichtbar ⇒ keine GitHub-Bytes', 'Ledger-Merge offen' und vertauschte Protokollkopien sind durch feste Commits, Ledger-Rohbyteprüfung und das ID03-Archivreceipt widerlegt. | [S06] [S07] [S09] [S11] [S14] [S29] [S30] | ID03 Korrekturreceipt | Historischen Fremdbericht erhalten und auf Korrekturbelege verweisen. Negative Codesuche ist kein Gegenbeweis zu direkt gelesenen festen Commits. |
| G33 | P2 | OPEN | VERIFIED | Zentrales _FRONTMATTER.md v007 ist ENTWURF; parallel besteht v006-PROPOSAL im SSOT-Root. Neue Metadaten oder ein übernommenes Rollenamendment belegen keine globale Schemafreigabe. | [S15] [S16] [S41] | ID02 Governance-/Quellenpflege | Aktiven Schema-/Baseline-Verweis und übernommenen Geltungsbereich eindeutig versionieren; Proposal-/Snapshotstände als solche erhalten. |
| G34 | P2 | OPEN | REPORTED_UNVERIFIED | ID02-Watch berichtet im Registrierungshandoff WO-20261123-AICADFEM-REGISTER-01 die Bezeichnung CLAUDE_LEDGER_WRITER. Der Handoff selbst wurde hier nicht unabhängig vollständig geprüft. | [S40] [S41] | Handoff-Autor; ID02 | Handoff samt Owner-/Runtimefeldern lesen; Rollenverweis ID06 und tatsächlichen Executor zuordnen. Alias allein beweist keine falsche Ausführung. |
| G35 | P2 | OPEN | REPORTED_UNVERIFIED | ID02-Watch meldet vier AICADFEM-WOs ohne eigene Auftragsversion und ohne ID01-Freigabeverweis im WO-Text. Fehlender Verweis beweist nicht, dass in der zugehörigen Sitzung keine Autorisierung vorliegt. | [S40] [S41] | Je WO-Owner; ID02 | Version, Eingangsstand, Scope und bereits vorhandene Autorisierungsquelle verlinken; nur tatsächlich fehlende kritische Freigaben offen halten. Keine neue Freigaberunde allein wegen unvollständiger Metadaten. |
| G36 | P2 | CLOSED | DERIVED | Gleicher Provider OpenAI/Codex ist für sich kein Verstoß gegen die Unabhängigkeitsregel. Manifest verlangt eine getrennte prüfende Instanz; Providerdiversität ist kein belegtes allgemeines Abnahmekriterium. | [S01] [S40] [S41] | ID03 Korrekturreceipt | Als pauschalen Ausschlussgrund geschlossen. Tatsächliche Trennung, Scope und fehlende Ausführungsreviews bleiben G12. |
| G37 | P2 | CLOSED | DERIVED | Der gemeldete unveränderte file-registry-Stand ist der offene Registerbefund G05. Neue AICADFEM-/Watch-Artefakte sind beim Abgleich anhand ihrer IDs einzubeziehen. | [S08] [S40] [S41] | ID03 Deduplizierung; ID06 Register-Schreiber | MERGED_INTO_G05; keine Registrierung behauptet und kein doppeltes Zählen. |
| G38 | P1 | OPEN | VERIFIED | Confidence 0,8 bzw. 0,6, etwa 20 % Evaluation,73 % Konformität und '2 von 5 Workflows grün' sind ohne reproduzierbare gemeinsame Bewertungsbasis. Der DeepSeek-Export nennt28 Lücken, enthält aber30 verschiedene eigene G-IDs. | [S12] [S14] | Berichtsautoren; ID03 Bewertungsvertrag | Entweder Population, Zähler, Nenner, Regeln und Kalibrierung offenlegen oder je Dimension quellengebundene Ampel mit Grenzen führen. Hashgleichheit nicht als semantische Accuracy oder Engineering-Freigabe interpretieren. |
| G39 | P2 | OPEN | VERIFIED | Deklarierte Berichtszeiten weichen von Providerzeiten ab: Sweep 19:45+01 bei Änderung 18:40:44Z; _GAP/Report 19:50+01 bei Anlage 18:47Z. Zukunfts-/Namenszeiten sind keine gemessenen Ausführungszeitpunkte. | [S12] [S13] [S36] | Je Autor; ID03 Zeitprovenienz | created_at_provider, declared_at und observed_at trennen. Neue Zeiten messen; historische Abweichungen ausdrücklich qualifizieren und nicht durch rückdatierte Logs verdecken. |
| G40 | P2 | OPEN | VERIFIED | Ein kanonisches _FUNKPROTOKOLL.md wurde in der gezielten Namenssuche nicht gefunden. Sprachbeschlüsse und eine Drei-Sätze-Regel sind ohne eindeutigen übernommenen Quellenstand keine universell installierte Runtime-Regel. | [S02] [S06] [S14] | ID02 Kommunikationsvertrag; ID03 Review | Einen vorhandenen/neu registrierten Regelort eindeutig verlinken; ID01-Worterteilung, Beginn/Ende, keine Parallelrede und keine leeren Schweigebestätigungen festhalten. Schweigen ist keine technische Freigabe; tatsächlicher Rollout braucht ACK. |
| G41 | P1 | OPEN | VERIFIED | T7 ist nur für die in diesem Lauf tatsächlich benutzten Drive-/GitHub-Operationen belegt. MCP-Server, Tunnel, Bridges, Webhooks, Plugins und lokale Python-Caller sind nicht vollständig funktional geprüft. | [S06] [S07] [S32] | Je angebundene Runtime; ID06 technische Inventur | Aktives Inventar mit Version/Startbefehl, ungefährlichem Smoke-Test, Scope, UTC-Zeit und Ergebnis erfassen; Endpunkte ohne Secrets. Dateien oder Toolnamen allein nicht als Erreichbarkeitsbeleg werten. |
| G42 | P1 | OPEN | VERIFIED | _AGBS dokumentiert fehlende atomare Mehrschreibersperre. Der verfügbare Drive-Datei-Update-Aufruf bietet keinen atomaren If-Match/CAS-Parameter; mtime-/Hash-Vorprüfung allein schließt ein konkurrierendes Schreiben im Zwischenfenster nicht aus.  Der erste ID03-Update wurde vor der Mutation durch einen abweichenden Vorhash gestoppt; der 1.287-Byte-Zwischenappend bleibt erhalten. | [S02] [S04] [S07] [S40] | ID06 Writer-Vertrag; ID03 Konflikttest | Einzelschreiber/Lease mit nachweisbarem Fencing oder atomaren Provider-CAS in der Schreibroute verwenden und Konfliktfälle prüfen. Für diesen Nachtrag Backup+Vorhash+mtime-Guard+Readback als begrenzten Schutz ausweisen. |
| G43 | P1 | OPEN | VERIFIED | Durchgehende Zustellung, tatsächlicher Empfänger-ACK und Wiederanlauf der Kette sind nicht belegt. YAML-Cron ist konfiguriert, aber Monitor-/Poll-Scheduler im letzten geprüften Monitor STALE; kein neuerer Run im gelesenen 30-Run-Fenster nach 14:50:52UTC. | [S03] [S05] [S25] [S26] [S27] | ID02 Zustellung; ID06 Scheduler | Frischen realen Schedulerlauf, Zustellung, Empfängerantwort und Idempotenz/Wiederanlauf anhand eines eingefrorenen Auftrags belegen. Konfiguration, Publication, Delivery, ACK, Review und Release getrennt führen. |
| G44 | P3 | OPEN | REPORTED_UNVERIFIED | Der DeepSeek-Export nennt zwei nicht ausgewertete historische Architektur-/Masterplanquellen sowie ältere FAQ-Kandidaten ohne vollständigen ID-/Versionsnachweis dieses Audits. | [S14] | ID02 Relevanzabgrenzung; ID03 Quellenprüfung | Erst konkrete Datei-IDs, Datum, Geltung und Aufgabenrelevanz ermitteln. Nur relevante CURRENT-/Evidenzquellen nachprüfen; kein pauschaler Globalblocker aus ungelesenem Archivmaterial. |
| G45 | P2 | OPEN | REPORTED_UNVERIFIED | Folder.md nennt historische Runtime-/Accountkonflikte (u.a. ID08 Meta-AI vs. Claude-Chat) und einen fehlenden Gemini-Argon-Anschluss. Ein aktueller Auflösungs-/Integrationsbeleg liegt im geprüften Korpus nicht vor. | [S01] [S04] | Betroffene Runtime-Verantwortliche; ID02 | Historische Tests ihren tatsächlichen Ausführern zuordnen; aktive Integration nur anhand konkreter Runtime-/Endpoint-/Aufrufbelege bestätigen. Alte Produktnamen nicht als heutige Rollen übernehmen. |
| G46 | P2 | OPEN | REPORTED_UNVERIFIED | Lokale Windows-Aufgaben, Wächter und Offline-Verfügbarkeit der Drive-Ordner sind in diesem Lauf nicht geprüft. Folder.md nennt drive_offline_check.ps1 als offenen lokalen Schritt. | [S02] [S04] [S17] | ID01/localer Executor; ID06 | Am tatsächlich angebundenen Host Schedulerkonfiguration plus letzten echten Lauf und erforderliche Offline-/Mount-Verfügbarkeit prüfen. Cloud-API-Erfolg ist kein lokaler Hostnachweis. |
| G47 | P3 | OPEN | REPORTED_UNVERIFIED | Folder.md führt ein historisches Gemini4-PDF mit fehlender Identität/Quellenauflösung und abgeschnittenen Tabellen als Mangel. Aktueller Reparatur-/Ablösebeleg wurde hier nicht festgestellt. | [S04] | Ursprünglicher Autor; ID02 Quellenpflege | Original-ID und aktuellen Ersatz prüfen; vollständige Quellen-/Kategorie-/Identitätszuordnung und lesbare Tabellen nachweisen. Keine pauschale Forderung, jedes fachliche PDF müsse Markdown sein. |
| G48 | P2 | OPEN | REPORTED_UNVERIFIED | _TROUBLESHOOTING T10 berichtet ein Docs→MD-Exportskript, das kanonische MD überschreibt. Aktive Skriptversion und heutiger Abschlussstatus sind hier nicht verifiziert. | [S02] [S17] | ID06 | Betroffenen Export und tatsächliche Aufrufrichtung identifizieren; kanonische MD schützen und korrigierte Richtung/Deaktivierung belegen. Historischen Hinweis nicht als aktuell laufenden Defekt behaupten. |
| G49 | P1 | OPEN | REPORTED_UNVERIFIED | _TROUBLESHOOTING T05 nennt einen historischen Klartext-Schlüsselfund. Ein Abschluss-/Rotationsreceipt ist im geprüften Korpus nicht zugeordnet; kein neuer Secret-Fund in diesem Lauf. | [S02] [S17] | ID01 Credential-Verantwortung | Vorhandenen vertraulichen Abschlussnachweis ohne Geheimniswerte zuordnen; falls noch offen, betroffene Zugangsdaten durch Berechtigten widerrufen/ersetzen. Keine Secrets in _GAP oder Logs übernehmen. |
| G50 | P2 | OPEN | VERIFIED | Die AGB-Ergänzung fordert pro veröffentlichter Kontrollpanel-Version ein rekonstruierbares WORK-/GitHub-Paket mit Version, Commit und SHA. Ein vollständiger aktueller Panel-Restore-/Versionsabgleich wurde hier nicht ausgeführt. | [S02] | ID02 Panelverantwortung | Aktuelle veröffentlichte Version dem passenden Paket in WORK und backups/control-panel zuordnen und Wiederherstellbarkeit prüfen. Fehlender Abruf allein beweist keinen Panelausfall. |
| G51 | P2 | OPEN | VERIFIED | Der ursprüngliche Merge-Auftrag nennt 0212–0236; der tatsächliche korrekt integrierte Umfang ist 0212–0256 plus0257. ID06 dokumentiert diese Erweiterung als D1. Integritätsprüfung ersetzt die saubere Nachführung des Auftragsumfangs nicht. | [S09] [S11] [S31] | ID06 Auftragsreceipt; ID02 Scope-Nachführung | Tatsächlich übernommenen Umfang, Kollisionsgrund und Bezug zur vorhandenen Konsolidierungsautorisierung im bestehenden Auftrag erfassen. Merge nicht erneut ausführen und keine Nummer 0258 ohne frischen Abgleich reservieren. |

### 5. Konformität, Strukturiertheit, Zuverlässigkeit und Overall Confidence

| Dimension | Urteil | Nachweis und Grenze |
|---|---|---|
| Konformität der gesamten Baseline | 🟠 PARTIAL; Gesamtfreigabe nicht belegt | Rollen-/Ablage-/Reportingregeln existieren; aktuelle ACKs, Registrierung, Norm-/RAG-/Mount-Tests und globaler Rollout sind lückenhaft. Einzelne Datei-Konformität ist keine Systemkonformität. |
| Strukturiertheit | 🟠 PARTIAL | Autorität und Registerzwecke sind definiert; FAQ-/Statusfassungen, alte Links und Frontmatter-/Zeitkonflikte erschweren die Auswertung. Diese GAP-Sicht führt IDs, Evidenz, Zustände, Zuständigkeiten und Schließkriterien. |
| Technische Zuverlässigkeit | 🟠 PARTIAL; betroffene Automation 🔴 BLOCKED/FAILURE | API-Persistenz und CI sind für konkrete Läufe belegt. Delivery/Poll scheitern; Monitor/Scheduler-Evidenz ist unvollständig. Ein erfolgreicher Einzelvorgang belegt keine Dauerverfügbarkeit oder SLO. |
| Accuracy / fachliche Richtigkeit | NICHT ALS GESAMTQUOTE GEMESSEN | Hashgleichheit, CSV-Kollisionsprüfung und ein arithmetischer Replay sind konkrete Tests. Für eine systemweite semantische/fachliche Trefferquote fehlen definierte Testpopulation, unabhängige Referenzen und Auswertung. |
| Overall Confidence | KEINE KALIBRIERTE GESAMTZAHL | Die Zahlen 0,8/0,6 werden nicht übernommen. Evidenz gilt je Aussage und Scope; verifizierte Teilnachweise ersetzen keine vollständige System- oder Engineering-Abnahme. |

Eine Vollständigkeitsquote benötigt verpflichtende Tests je Runtime, zulässige Nichtanwendbarkeit, Referenzversion, Population und Zählregeln. Sie misst Testabdeckung, nicht automatisch Accuracy oder Erfolgswahrscheinlichkeit. [S01] [S03] [S12] [S14]

### 6. FAQ-Korrekturen für die vorhandene Synthese

Die vorhandene ID03-FAQ bleibt eingefrorene Synthesequelle. Dieser Nachtrag aktualisiert ihre Statusdaten und die strittigen Punkte; es wird keine zweite FAQ angelegt. Der frühere Satz „25 Ledgerzeilen fehlen“ in S06 §5.3 ist durch S09–S11 überholt.

| FAQ-Thema | Aktuelle quellengebundene Antwort |
|---|---|
| Basic Instructions / Frontmatter / Manifest | Manifest: Rollen/Prinzipien. Baseline und AGBs: übernommene Regeln. Frontmatter: Metadaten eines Artefakts/Laufs. Ein zentraler ENTWURF wird durch Aktualität nicht CURRENT. [S01] [S02] [S03] [S15] [S16] |
| Was muss jede Rolle lesen? | Führende _AGBS und auftragsrelevante aktuelle Manifest-/Baseline-/Ticketquellen mit Quelle, Version und Runtime-Nachweis. Archivierte Frontmatter sind keine automatisch aktiven Anweisungen. [S02] [S03] |
| API-Persistenz versus Mount | Getrennte Tests. Eine Drive-Datei belegt weder G:-Write noch technischen Uploader. Lokaler Write/Readback und zugehöriger Provider-Readback sind gesonderte Nachweise. [S06] [S18] [S28] |
| GitHub-Sync / Branch / PR / Merge | API-Commit ist kein lokaler Push und kein dauerhafter bidirektionaler Sync. Testbranches dürfen ungemergt bleiben; spätere Übernahme von Code/Governance verlangt den passenden Review. [S04] [S06] [S29] |
| Actions / Scheduled Tasks | CI ist für den geprüften Main-Commit erfolgreich. Monitor und Delivery/Poll scheitern an unterschiedlichen Kriterien. YAML-Cron beweist keinen aktuellen erfolgreichen Schedulerlauf; lokale Windows-Aufgaben wurden nicht geprüft. [S24] [S25] [S26] [S27] |
| Reporting / Kommunikation | HISTORY-Start plus START_ACK in WORK; Koordination im Ticketregister; Ergebnisse/Blocker/Receipts im bestehenden WO. Publication, Delivery, ACK, Review und Freigabe getrennt. Drive weckt keinen Agenten. [S02] [S03] [S05] |
| Registry / Ledger / Capabilities | Artefaktidentität und Version, Nummernvergabe, Rollenautorität und Runtime-Fähigkeiten haben verschiedene Zwecke. Bestehenden Writer und verlinkte Deltas verwenden; keine konkurrierenden Master oder ungesicherten Nummernreservierungen. [S01] [S02] [S07] [S08] [S09] |
| Backup / mtime-Guard / Sandbox | Backup vor Änderung; Altbytes erhalten; Stand unmittelbar vor Update prüfen; vollständige Rohbytes danach vergleichen. Ohne atomaren CAS/Lease kein vollständiger Mehrschreiberschutz. T4 verlangt dauerhafte Belege für alle benannten Laufoutputs, kein Löschen lokaler Arbeitskopien. [S02] [S06] [S07] [S36] [S37] [S38] |

### 7. Drei Best-Fit-Arbeitspakete

1. Nachweise und aktive Statusdaten schließen: ID06 übernimmt verifizierbare Registry-Deltas/Versionen und die 24 Ledger-Hashes; ID02 ordnet echte ACKs bestehenden Tickets zu und verknüpft GAP-/FAQ-Korrekturen mit aktiven Einstiegspunkten. Dubletten erst nach ID-/Hash-/Referenzabgleich reversibel archivieren. Abnahme: eindeutige IDs, registrierte Versionen, nachvollziehbare Receipts. Kein erneuter Ledger-Merge. G05–G08/G20–G23/G27–G31.
2. Ausführungswege gezielt herstellen: ID01 erneuert den betroffenen Google-Zugang; ID06 prüft Preflight/Poll/Delivery. Parallel Coverage-/Scheduler-Lücke schließen, anschließend Zustellung/ACK und Wiederanlauf testen. Mount/MCP nur in geeigneten angebundenen Runtimes prüfen. Abnahme: echte neue Run-IDs und Rohbyte-/Empfängerbelege. G01/G02/G09/G41–G43/G46.
3. Governance und Fachtests kontrolliert übernehmen: konkrete Basic-Instructions-/Link-/Rollen-/Kommunikationskorrekturen aus dem vorhandenen Vorschlag reviewen, versionsgebunden übernehmen und tatsächlichen Rollout nachweisen. EC5-Golden-Case und lokale RAG-Pipeline gesondert abnehmen. Abnahme: reproduzierbare Fälle, separate Reviewer, Norm-/Quellenstand und echte Runtime-ACKs. G03/G04/G10–G17/G38–G40.

Die erteilte Evaluierungs-/Update-/Bereinigungsautorisierung wird genutzt. Fehlende technische Voraussetzungen, fremde ACKs und normative Freigaben bleiben offen; sie werden nicht durch erneute pauschale Zustimmungsfragen ersetzt.

### 8. Integrität und sichere Fortschreibung

| Objekt | Bytes | SHA-256 |
|---|---|---|
| Ledger nach Merge | 75843 | 0bdceff0547a2f4ed30c604452895ab0df399e8d239c7df820389329d3880376 |
| Ledgerbackup vor Merge | 62889 | 8b7cafe7f00d3e0b0db9792a1fe8c81fc258cc5de81e6760bcbfd24b37a89cff |
| file-registry.jsonl | 430662 | 3ae1bd1f36c193d63338ec81285fe282231eb793ec81990ef53aaf2f32e7f592 |
| ID06-Mergebericht | 5103 | 14dc83a0bd537c10f037e88bfec95960fc38c7b4f72838e5f144018429243b84 |
| ID03-FAQ-Snapshot | 35364 | 444403823c4159c8df7cb0de163576364c1d6222da56666edeec10668eb96a92 |
| ID06-T5-Skript | 773 | 79a6a587be8ff7118d8d22c36f41e2520f19ded6cc8da665b52b0efefc673105 |
| ID05-Protokoll | 4182 | b13372b3af6317d020fde612034c42448682b15f1a6a6421320c9cafbb822819 |
| ID05-FAQ und Zusatzkopie | 16065 | 92531141a4fc49b7d3bb963d42d9d2113effbf9715a61ef43d4c4a6769fc66a2 |
| _GAP-Vorzustand / Backup | 5833 | 73e06ee5efbdcf12c4cb6d4dd0ffe2c01948c09c12d61fc5851a434c11e6f6b6 |

Ledger/Registry-Rohbytes wurden um 19:44 Berlin unabhängig geprüft; spätere Metadatenkontrollen zeigten unveränderte Größe/Änderungszeit. Metadatenkontrolle ist keine erneute Rohbyteprüfung. S11 ist auf Drive und im Commit c1733befeb5e12cdd4c9f07aa9d4941e9cee4406 bytegleich; dieser Commit allein sichert nicht den gesamten Master-Ledger.

Die Backups dieses Nachtrags liegen in NEXUS.HISTORICAL. Original-Provider-IDs bleiben erhalten; vor jedem In-place-Append werden modifiedTime/Größe und Vorzustand geprüft. Altpräfixe bleiben bytegleich; vollständige Provider-Rohbytes werden danach mit dem lokalen Output verglichen. Ohne atomaren Conditional-Update wird kein CAS-PASS behauptet. Endgültige Outputhashes und Publikationsreceipts werden extern im vorhandenen WO/Runlog bzw. Abschluss geführt; kein zirkulärer Selbsthash.

### 9. Quellenkatalog

Rebase-Ereignis: Der Vorhash-Guard erkannte die Änderung des gemeinsamen Vorzustands von 5.833 auf 7.120 Bytes vor dem Update. Fremde Ereignisse G12/G27 und die neuen G33–G37 bleiben unverändert erhalten. Die nur lokal entworfenen ID03-IDs wurden vor Publikation auf G38–G51 verschoben. Der neue Vorzustand wurde zuerst separat gesichert und bytegeprüft. [S40] [S41]

Der zusätzliche ID02-Watch beschreibt einen eigenen 20:00-Lauf und ein verifiziertes Panel-Teilergebnis; diese Meldung ist keine Wiederholung unserer GitHub-Runprüfung und kein vollständiger Panel-Recovery-Nachweis. Fachprojekt-Restaufgaben seines Portfolios werden nicht in neue Basic-Instructions-Lücken umgedeutet.

| Ref | Quelle / Fundstelle | Versions-/Prüfgrenze |
|---|---|---|
| [S01] | Manifest CURRENT, §4/§§6–10; Rollenregisterv1.1 | Provider17.11.2026 19:21:49.987Z |
| [S02] | _AGBS.md v007.1, §§1–12 + ID01-Ergänzung23.11. | Provider23.11.2026 12:56:53.289Z |
| [S03] | Baseline CURRENT, §§7/17, MUST-23–25/50–54/150–159 | Provider17.11.2026 19:21:52.328Z |
| [S04] | Folder.md, Policy0.4.0-pilot; Status-/problems-/next_action-Felder | Provider16.11.2026 21:50:06.607Z; historische Claims gesondert |
| [S05] | Ticket Registry: ACK-ROLES-v1.1-ID02–08 und WO-20261112-ID02-CAPABILITY-ACK | Live-Abruf23.11.2026; natives Tabellenformat |
| [S06] | ID03-FAQ/Review v1.0.0-review, §§4–6 | 35.364B; eingefrorener Review vor späterem Ledger-Merge |
| [S07] | Bestehende Capability-WO, ID03-Abschlussreceipt18:29UTC + aktueller Nachtrag | Vorzustand20.978B; Provider18:29:20.587Z |
| [S08] | file-registry.jsonl | 430.662B;472gültigeJSONL; Provider14:15:51.245Z |
| [S09] | Master00_ID_LEDGER.csv | 75.843B;247Datensätze; Provider18:38:25.041Z |
| [S10] | ID06-Ledgerbackup vor Merge0257 | 62.889B; erstellt18:37:18.074Z |
| [S11] | ID06-Ledger-Merge-/Automation-Bericht0257, D1–D3 | 5.103B; Provider18:39:22.319Z; GitHubc1733bef… |
| [S12] | ID06-Prüfmatrix/GAP/Bewertung, §§1–4 | 3.323B; Provider18:47:10.321Z; deklarierteZeit19:50+01 |
| [S13] | ID06-Status-Sweep Basic/Frontmatter/Reporting/FAQ | 2.985B; Provider18:40:44.659Z; deklarierteZeit19:45+01 |
| [S14] | DeepSeek-Gesprächsexport: AbschnitteStatus/GAP/Bewertung | 25.635B; Provider18:47:11.992Z; fremde/vermischteSprechertexte, keineLive-Runs |
| [S15] | _FRONTMATTER.md v007, ENTWURF/PENDING_HUMAN_TECHNICAL_RELEASE | Steuerdateienarchiv; Provider23.11.13:11:39Z |
| [S16] | _FRONTMATTER_v006-PROPOSAL.md | REVIEW_REQUIRED_NOT_CURRENT |
| [S17] | _TROUBLESHOOTING.md v001, T01–T13 | Historische Lösungen/Behauptungen; kein automatischer aktueller Funktionsnachweis |
| [S18] | Perplexity-/IDNN-Protokoll, §6/Fronmatter | 4.182B; Originalbytes erhalten; KorrekturreceiptS07 |
| [S19] | ID05-FAQ-Vorschlag | 16.065B; PROPOSED/REVIEW_PENDING |
| [S20] | Hashgleiche neuere ID05-FAQ-Kopie | 16.065B; erstellt18:36:57.294Z |
| [S21] | ID01-FAQ_Question+Answers-Sammlung | 29.514B; Provider18:36:15.532Z; Scratch/Mischprotokoll |
| [S22] | ID04-FAQ-Beitrag | 6.218B;text/plain;Provider18:32:52.379Z |
| [S23] | ID06-T5-Skript, festerCommit e725ee0947f1842be6a2a580ae3edca75dd71402 | 773B; unabhängiger Python/Decimal-Kontrolllauf |
| [S24] | GitHub CI-Run45198194734 | 23.11.14:48:39Z; SUCCESS für Mainc6379c6f… |
| [S25] | NEXUS Monitor45198194995, Job137774207594, Artefakt14829791111/monitor/report.json | 23.11.14:48:39Z; FAILURE; coverageINCOMPLETE |
| [S26] | NEXUS GitHub to WORK45198599526, Job137775648577/preflight.json | 23.11.14:50:52Z; GoogleOAuthINVALID_GRANT; write_testNOT_RUN |
| [S27] | NEXUS Drive to GitHub45149342862, Job137606464824 | 23.11.09:41:33Z; GoogleOAuthINVALID_GRANT; Read-onlyPoll |
| [S28] | ID06-Baseline-RUNLOG17:34–17:40UTC | Selbstbericht über lokalen Push/Mount/Bridge; Remote-Datei geprüft |
| [S29] | ID03-Review-/Persistenzcommit vor diesem Nachtrag | EigenerAPI-Commit;4DateienDrive/GitHub/localbytegleich |
| [S30] | ID06-Baselinecommit | VierRemote-DateiengegenDrivebytegleich;lokalerTransportseparat |
| [S31] | BestehenderLedger-Merge-Auftragv0.2 | Originalumfang0212–0236 |
| [S32] | BestehenderMCP-TeilauftragD | AktiveCaller/Versionenweiterprüfen |
| [S33] | P205-SkriptWORK | 5.408B;hashgleichS34 |
| [S34] | P205-SkriptSCRIPTS | 5.408B;Installationsquelleoffen |
| [S35] | EigenerID03-Lauf-/Startlog | Vorzustand2.459B;Provider18:28:13.285Z |
| [S36] | Bytegleicher_GAP-Vorzustand im Archiv | 5.833B;originalProvider18:47:09.951Z;Backup19:53Berlin |
| [S37] | Work-Order-Backup vor diesem Nachtrag | 20.978B;rawbytegleichgeprüft |
| [S38] | Runlog-Backup vor diesem Nachtrag | 2.459B;rawbytegleichgeprüft |
| [S39] | ID01-EntscheidungNormengrundlagen19.11. | Normbasis/Inventar;keinvollständigerEC5-Golden-Case |
| [S40] | _GAP-Rebase-Backup nach fremdem Append | 7.120 B; SHA-256 881f9cb0a61010f0561afd764926b739af22e4f83423ea65514110ca5672e423; vorherige Provideränderung 19:06:29.968Z |
| [S41] | ID02-WORK-Watch 20:00, neue Aufträge / Panel-Abdeckung | 9.475 B; Provider19:01:30.934Z; berichteter eigenständiger Watch-Scope |


[S01]: https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view
[S02]: https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view
[S03]: https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view
[S04]: https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view
[S05]: https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit
[S06]: https://drive.google.com/file/d/1w_IyHkyo07JJZf6Pp69h-Fh10FKAq6jE/view
[S07]: https://drive.google.com/file/d/1y0DSTvkH_04avqI8TZKyaKOy05gWfZgx/view
[S08]: https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view
[S09]: https://drive.google.com/file/d/1Qso4VQE-cySJdxo6j-MNjxxOc5-GJlrK/view
[S10]: https://drive.google.com/file/d/15etSi82bQ61EYqCB4z8YeygXdCCv5Cvr/view
[S11]: https://drive.google.com/file/d/1VbLEffv8YgC2Q-REsjSQKdZ_j6kVTl2O/view
[S12]: https://drive.google.com/file/d/1mwHqbd8EK8yJamppnTGh4pYtwjfnLLuo/view
[S13]: https://drive.google.com/file/d/1RpN2e8H2cVl-MP20-go01Gl3M7W0ZcGO/view
[S14]: https://drive.google.com/file/d/1SzolgJeMBgW50qsw_ALrXFN4lPb1-08n/view
[S15]: https://drive.google.com/file/d/1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi/view
[S16]: https://drive.google.com/file/d/1TUmAPe8k0RA-Ce9koyV9bGqWdd7BLGj6/view
[S17]: https://drive.google.com/file/d/1OXKmuSPdXTwwy3AfECQR4hRm1iNu_4JR/view
[S18]: https://drive.google.com/file/d/1wjxj22S3dkusFcfESgJJMB62d7S_prWI/view
[S19]: https://drive.google.com/file/d/1MRuCH59nfmfOue2wuSVGqr_4u7pGcl2q/view
[S20]: https://drive.google.com/file/d/1_zxTXQEJ9YyFSx-Edxovts5jKphZeG4f/view
[S21]: https://drive.google.com/file/d/1dT_Q-yf3wzAyRwJF3uFBywUDbnGbisUV/view
[S22]: https://drive.google.com/file/d/1hSVSIOdRDkNSMTTgE21IWD3WPWFkZfDh/view
[S23]: https://github.com/julianzotter/nexus-platform/blob/e725ee0947f1842be6a2a580ae3edca75dd71402/WORK/26_11_23_1908_ID06_T5_ec5_biegung_gl24h.py
[S24]: https://github.com/julianzotter/nexus-platform/actions/runs/45198194734
[S25]: https://github.com/julianzotter/nexus-platform/actions/runs/45198194995
[S26]: https://github.com/julianzotter/nexus-platform/actions/runs/45198599526
[S27]: https://github.com/julianzotter/nexus-platform/actions/runs/45149342862
[S28]: https://drive.google.com/file/d/1f6eATmEDo-GhWUgjRjKWJU363iIClYoJ/view
[S29]: https://github.com/julianzotter/nexus-platform/commit/ab5e5367c7d4b87b7ab3d51cd1d24f2433ff9cb3
[S30]: https://github.com/julianzotter/nexus-platform/commit/ed207168e67633e6043e2ab97acab8e9cd521611
[S31]: https://drive.google.com/file/d/1ArJmk08HVn-wnOj18xpY7bqysv5Tclb8/view
[S32]: https://drive.google.com/file/d/1uniI-8U2rUDh7Y4zTQ3nuMuN4nqJmpjf/view
[S33]: https://drive.google.com/file/d/1aTsZyWz6CneSBE4fXOzSM0Jha89KRyre/view
[S34]: https://drive.google.com/file/d/1GAxp5TGVYXnspYKf5ZNnCx1oX49novti/view
[S35]: https://drive.google.com/file/d/1aAI7nO4ziDk1CHuA_oYCfqHOrtSZxnGA/view
[S36]: https://drive.google.com/file/d/1vK4qYevBxXx3GiRTps3R1fVkK1BiIrD3/view
[S37]: https://drive.google.com/file/d/1_-rvS88tn4GgaMNx6GKSEzJu_XuuwiES/view
[S38]: https://drive.google.com/file/d/1aTrJj49C_rNu0r_VNvU9pEHMa6W6ij6w/view
[S39]: https://drive.google.com/file/d/1QnWO8H7YakgPAfeK_5wW_mnnDj-okEkb/view

[S40]: https://drive.google.com/file/d/1FVT_sfViLLEIPXX9oj9V753b59RsU_Xy/view
[S41]: https://drive.google.com/file/d/1ZKQ7OyIrWh2HzFoF_iQEo9fFla24H0Ny/view

## ID06-Nachtrag r3 — Belege zu REPORTED_UNVERIFIED, Korrekturen, neue Befunde

```yaml
append_version: v0.1-ID06-r3
role_id: ID06
provider: Anthropic (Claude Opus 5.5, claude.ai Cloud-Session + Desktop-Bridge)
observed_at: "2026-11-23T19:37:38Z"
previous_bytes: 55902
previous_sha256: afcb9246c922bcc8f974a6283789be25c942a8c8b96051593fcfe9386b4fb957
regel: Tabellenformat ab hier wie ID03-Nachtrag §4 (8 Spalten); vorangehende Bytes unverändert
```

| GAP | Prio | Status | Evidenz | Aktueller Befund | Quellen | Nächste Zuständigkeit | Schließkriterium |
|---|---|---|---|---|---|---|---|
| G07 | P2 | OPEN | VERIFIED | Zwei Dateien gleichen Namens "00_ID_LEDGER.csv" im SSOT-Root: gdrive:1HTsN91m8XuhcwE4o5nFq-mYfYnpWT2Ci (2127 B, 2026-09-22) und Master gdrive:1Qso4VQE-cySJdxo6j-MNjxxOc5-GJlrK (75843 B). | Drive-Metadaten 2026-11-23T19:36Z | ID01 Move-Freigabe | Altdatei nach NEXUS.HISTORICAL verschoben, Master einziger Namensträger. |
| G26 | P2 | CLOSED | VERIFIED | Nachgeholter Start-Log vorhanden: gdrive:1vFwgDn3HDstYcCuP3rOzaAr8yz5C02cE in LLM-HISTORY-LOG, Provider-Anlage 2026-11-23T18:40:45Z, 358 B, sha256 8a9dcb2be39d1eae85c36bbf8acf4901088cdc3cc60602775ea48b93c1b28a79. | Drive-Metadaten | – | erfüllt |
| G38 | P1 | IN_PROGRESS | DERIVED | ID06 zieht eigene Zahlen (0,8 Konfidenz, ≈20 %, ≈73 %) als nicht reproduzierbar zurück und übernimmt die Ampelbewertung aus ID03-Nachtrag §5. | dieser Nachtrag | übrige Berichtsautoren | Alle Autoren nutzen dieselbe Ampel- oder offengelegte Zählbasis. |
| G39 | P2 | OPEN | VERIFIED | ID06-Abweichungen bestätigt: STATUS-SWEEP Frontmatter 19:45 vs. Provider 18:40:44Z (19:40 lokal); REPORT_PRUEFMATRIX und _GAP Frontmatter 19:50 vs. Provider 18:47Z (19:47 lokal). Ursache: geplante statt gemessene Zeit. | Drive-Metadaten | ID06 ab sofort | Neue ID06-Dateien nur mit gemessener Zeit; historische Dateien unverändert. |
| G42 | P1 | OPEN | VERIFIED | Ergänzung ID06: Erster Bridge-Write von _GAP.md (Ziel 7120 B) schrieb veraltete 5833 B, weil die neue Fassung im Ablagespeicher noch nicht lesbar war; per Readback erkannt, zweiter Write korrekt (sha256 881f9cb0…). | ID06-Lauf 2026-11-23 ~19:12Z | ID06 Writer-Vertrag | Write gilt erst nach Readback mit Soll-Hash; Pflicht in Writer-Vertrag aufnehmen. |
| G51 | P2 | IN_PROGRESS | VERIFIED | ID06 übernimmt Nachführung des tatsächlichen Merge-Umfangs 0212-0256 + 0257 in den bestehenden Merge-Auftrag (Receipt). | Report 26_11_23_1940_ID06_REPORT_LEDGER-MERGE | ID06 | Receipt im WO v0.2 mit Umfang, Kollisionsgrund, Hashes. |
| G52 | P2 | OPEN | VERIFIED | _GAP.md enthält zwei Tabellenformate (ID06 7 Spalten bis G37, ID03 8 Spalten ab §4) und doppelte GAP-IDs je Ereignis. Auswertung nur über "jüngstes Ereignis je ID" eindeutig. | diese Datei | ID01 Freigabe Format | Ein Format (8 Spalten) als verbindlich erklärt; Regel "jüngstes Ereignis gilt" im Kopf. |
