---
name: 26_11_02_1916_ID-UNVERIFIED_NEXUS-IMPLEMENTIERUNGSGUIDE_001.md
version: 0.2.0
status: REVIEW_PENDING
timestamp: '2026-11-02T19:16:13.842814+01:00'
agent_id: null
executor: OpenAI Codex
executor_instance: /root
provider: OpenAI
model_id: null
requested_external_model: OPUS 5.5
external_model_execution: NOT_RUN
ticket_id: WO-20261102-NEXUS-DRIVE-HARDLOCK
run_id: NEXUS-DRIVE-HARDLOCK-20261102T191613+0100
artifact_id: null
canonical_target: https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP
registration_status: PENDING_AT_GENERATION
artifact_number: null
naming_deviation: ID-UNVERIFIED; suffix is bundle ordinal, not canonical ledger allocation;
  AGB v004 Drive identity applies
hash_scope: body_utf8_after_closing_frontmatter_lf
hash: f5cfb371293dd26843620c94af6a8e3c64f4f681b4ff19210f5bd605b0d12301
related_ticket: WO-20261102-NEXUS-WAYFINDER-01
---
# NEXUS AI-OS — Empfehlungsbericht und Implementierungsguide

## Entscheidung / Umfang

Run 1 ist als Codekandidat implementiert und lokal geprüft: Python-Schreibdienst,
serverseitiger Proxy und geänderter Transcript-Exporter. Kein Merge/Deployment,
keine Produktionsfreigabe. Externes OPUS-5.5-Review ist angefordert, nicht ausgeführt.
Faktische Modellverfügbarkeit ist nicht aus historischen Capabilitytabellen ableitbar.

Geprüft: AGB v004, Frontmatter v003 ENTWURF, aktuelles Manifest/Baseline, WORK/Folder,
zwei Repository-Bäume, konkreter Studio-Quellcode und Metadaten der 16 NEXUS.*-Wurzeln.
Nicht geprüft: lokales Windows-Laufwerk, laufender produktiver Prozess, AnythingSearch.db,
vollständige Inhalte aller inventarisierten Dateien, reale Drive-Credentials des Zielhosts.

## 1. Evidenzgebundene Kontrastanalyse

| Aussage / Komponente | Ergebnis | Nachweis / Bedeutung |
|---|---|---|
| Transcript nutzt nur Browserdownload | VERIFIED im geprüften Ausgangscode | TranscriptTimeline.tsx, Basis 829f5a85: Blob/createObjectURL/link.click |
| Timeline bereits vollständig fluid | WIDERLEGT im Ausgangscode | h-[500px], w-[808px] und Inlinebreite/-höhe vorhanden; im Kandidaten entfernt |
| nexus_server.py ist bestehendes Studio-Backend | WIDERLEGT im geprüften main-Baum | Tatsächlich server.ts; neuer Python-Dienst ausdrücklich separat ergänzt |
| nexus_gateway_server.py vorhanden | UNVERIFIED | Im geprüften Studio-Baum nicht vorhanden; keine Produktivdatei erfunden |
| RAG bestätigt Tragfähigkeit ohne Solver | VERIFIED im Drive-Quellartefakt | nexus_backend_server_5.0.txt: rag_query erzeugt feste Tragfähigkeits-/Erfüllungsaussagen |
| Audit-Tool schreibt tatsächlich | WIDERLEGT im selben Quellartefakt | log_audit_transcript gibt lediglich einen String zurück |
| AnythingSearch.db sei fachliche SSOT | UNVERIFIED / Autoritätskonflikt | Baseline weist Drive/Registry und _INDEX.MASTER Aufgaben zu; Index ist kein pauschaler Fachnachweis |
| Unbegrenztes Promptmerging / simulierte LangGraph-Knoten | UNVERIFIED | Entsprechender ausführbarer Compiler-/Graphcode nicht nachgewiesen |
| Fehlende Checkpoints / State Bleeding | UNVERIFIED als Systemdiagnose | Studio hält Sessionreferenz im Prozess; das belegt noch keine gesamte NEXUS-Orchestrierungsarchitektur |
| Alle NEXUS-Ordner unintegriert | UNVERIFIED | Metadatenindex beweist Auffindbarkeit; bestehende Parser-/Ingestionabdeckung ist separat zu prüfen |

Drive-Quellartefakt: https://drive.google.com/file/d/1-UVQl-jzgRzOsrV7DT22dX1AYRnivK-7/view
Das Artefakt ist kein Beleg, dass genau dieser Code produktiv läuft. Feste Engineeringwerte
und Erfüllungssätze daraus sind als technische Nachweise ungeeignet und sollen im nächsten
autorisierten Änderungslauf durch NO_SOLVER_EVIDENCE ersetzt werden. Hier keine fachlichen
Bemessungen durchgeführt und keine fremden Backendquellen überschrieben.

## 2. Vier zu korrigierende Denkfehler

1. Promptregeln sind keine I/O-Zugriffskontrolle. Deterministischer Service entscheidet
   anhand Toolantwort, Zielbindung und Readback. Die Behauptung, ein LLM melde bei jedem
   Toolfehler zwangsläufig Erfolg, ist zu absolut und wird nicht übernommen.
2. Index, Registry, Quellablage und fachliche Autorität sind unterschiedliche Rollen.
   Frontmatter verlinkt Quellen; Parser und Registry müssen die Verknüpfungen tatsächlich
   konsumieren und ihre Abdeckung belegen.
3. Upload, Byteprüfung, Registrierung, ACK, Peerreview und Humanfreigabe sind getrennte
   Zustände. Ein HTTP-200-Satz oder ein grüner Workflowlauf ersetzt diese Kette nicht.
4. Lokaler Hard-Lock schützt den eigenen Schreibpfad. Er garantiert weder exklusiven
   Drive-Zugriff anderer Akteure noch physische Datenträgerdauerhaftigkeit bei Google.

## 3. Run 1 — implementierter Vertical Slice

Quelle/Review: https://github.com/julianzotter/GEMINI-LIVE-DESKTOP-STUDIO-/pull/1 — Commit `a5e68fd970ff558837d4a3e849a4c5e88a2b136a`.

| Baustein | Implementiertes Verhalten |
|---|---|
| backend/nexus_server.py | Loopback-HTTP, Bearerprüfung, Größen-/Schemaschranken, bei fehlender Konfiguration geschlossen |
| backend/drive_writer.py | SQLite-Write-Intent mit exakten Bytes, Hash, Ziel, Dateiname und vorab erzeugter Drive-ID |
| backend/google_drive.py | Host-ADC, begrenzte I/O-/Refreshwartezeit, binärer Markdown-Upload und Rohbyte-Readback |
| protocolProxy.ts / server.ts | Ein festes Save-Ziel, Origin/Host/Loopbackprüfung, keine Zugangsdaten im Browser |
| protocolPersistence.ts | Web Locks, persistente Fingerprint→Request-ID-Zuordnung; Wiederholung mit gleicher ID |
| TranscriptTimeline.tsx | Save über Server, kein Blob-Fallback in diesem Pfad, Statusanzeige Registrierung offen, flexible Abmessungen |

Algorithmus: validieren → vorhandenen Intent suchen → ID reservieren → unveränderliche
Schreibabsicht committen → vorhandene Drive-ID abgleichen → gegebenenfalls Upload →
Metadaten und exakte Bytes lesen → HTTP 202 mit REGISTRATION_PENDING.
Unklarer Schreibausgang behält dieselbe Drive-ID. Identischer Request mit verändertem
Payload ergibt Konflikt. Kein langer SQLite-Schreibtransaction-Lock über Netzwerkanfragen.

Grenzen: Einzelhost/Einzelschreiber; kein verteilter Lock; keine Transaktionsgarantie
über Drive und kanonisches Register. Der konfigurierte Nummernpool ist nur eine
Operatorbehauptung und vor Deployment gegen das bestehende Ledger zu verifizieren.
Rollen-ID unbekannt: agent_id null, Dateinamensmarker ID-UNVERIFIED. Quellmodell unbekannt.
Browser-Storageverlust und Wiederherstellung des eigentlichen Transcripts nach Neustart
sind nicht gelöst. Bei weiterlaufendem Transcript muss der unsichere Snapshot gezielt
erneut gesendet werden. Der neue lokale Bind adressiert keine öffentliche Cloud-Installation.

Setup und Befehle stehen in `studio/docs/DRIVE-HARDLOCK.md` im Lieferpaket und PR.
API-Grundlagen: https://developers.google.com/workspace/drive/api/guides/create-file ,
https://developers.google.com/workspace/drive/api/reference/rest/v3/files/generateIds ,
https://developers.google.com/workspace/drive/api/guides/handle-errors .
Pre-generated IDs werden hier für rohe Markdown-Dateien verwendet, nicht für native Docs.

## 4. Hierarchische Implementierungsstrecke

| Stufe / Abhängigkeit | Beste geeignete Verfahren | Abnahmekriterium |
|---|---|---|
| P0.0 — technische Falschaussagen sperren | Solver-Evidence-Gate statt synthetischer rag_query-Erfüllungssätze; Toolerfolg nur mit Receipt | Kein technischer PASS ohne echten Solver-/Quellnachweis |
| P0.1 — Run 1 integrieren | Dauerhafte Write-Intent-FSM, stabile Datei-ID, Replay/Reconcile, Hash-Readback | Reale Windows-/Drive-Negativ- und Recoverytests; Gesamtbuild |
| P0.2 — Registrytransaktion | Ein authentifizierter kanonischer Writer; persistente Outbox; Versionskonflikte fail-closed; Projektionen getrennt | Keine verlorenen Append-Ereignisse bei Konkurrenz/Abbruch, vorhandenes Register bleibt führend |
| P1.1 — Discovery/Parser | BFS mit visited Provider-ID, vollständiger Pagination und Scope; unveränderlicher Scanmanifest; typisierte Parser; Quarantäne pro fehlerhafter Datei | Sichtbare Abdeckung, keine stille Auslassung, identischer Snapshot reproduziert Index |
| P1.2 — Kontextcompiler | Quellenfreeze, Schema-/Provenienzprüfung, harte Tokenbudgets, rangierte Chunk-Auswahl, explizite Pflichtanker | Budget eingehalten, Pflichtregeln nie still abgeschnitten, Quelltext bleibt untrusted data |
| P1.3 — Orchestrierung | Dependency-DAG + persistente Task-FSM; attempt_id, idempotente Toolcontracts, Deadline/Backoff, explizite ACKs | Prozessabbruch/Replay erzeugt keine doppelten irreversiblen Aktionen |
| P2.1 — Agent Interconnectivity | Capability-Registry mit echten Laufbelegen; Work Order→CLAIM→RUN→Response→ACK→Review | Ein kompletter, hashgebundener Cross-Runtime-Rücklauf |
| P2.2 — Eurocode/FEM | Schema-first Fachinputs, Normausgabe+NA+Anwendungsbereich, SI-/Dimensionsprüfung, Fachsolver, Benchmark/Regression/Konvergenz | Berechnung vollständig reproduzierbar; unabhängiges Fachreview; Human Gate |
| P2.3 — KG/RAG/Toolkatalog | ID/Locator vor Semantik; exakte Suche/BM25 zuerst, Vektoren optional; relationseigene Evidenz | Unbelegte Relation bleibt Kandidat; kein Zitieren ohne Claim-Support |

Diese Reihenfolge ist DERIVED Empfehlung aus den belegten Lücken, keine Messung einer
global optimalen Architektur. Für diesen Slice sind LangGraph, Kafka oder eine weitere
Graphdatenbank nicht notwendig. LangGraph wird erst bei nachgewiesenem Bedarf an
resumierbarer verzweigter Ablaufsteuerung ausgewählt. Deterministischer Orchestrator
und Solver bleiben Autorität für Zustandswechsel beziehungsweise Fachrechnungen.

AEC-Toolnutzung: RFEM/FEM-Adapter liefert Inputhash, Modellrevision, Solverversion,
Lastfälle/-kombinationen, Konvergenz und Ergebnisdateien. Eurocode-/eurocodepy-Bausteine
werden erst nach Ausgabe-/NA-/Anwendungsprüfung verwendet. ezdxf/CadQuery/IFC liefern
Geometry-/Austauschartefakte mit Format-/Einheitenprüfung; Geometrieprüfung ist keine
Bemessungsfreigabe. Keine dieser Fachintegrationen wurde in Run 1 ausgeführt.

## 5. Ordnerindex und Frontmatter-Einbindung

Erfasst: 16 NEXUS.*-Wurzeln, 80 Ordnerlisten,
733 Einträge. Die BFS-Warteschlange ist leer; kein Unterordner erreichte
den 100-Einträge-Fetchgrenzwert, keine gemeldeten Listingfehler. Wurzelordner wurden
zusätzlich über providergebundene Folder-Suche ohne nächsten Seitentoken abgeglichen.
Die Erfassung ist kein atomarer Cloudsnapshot und keine Zugriffs-/Volltextgarantie.
Lokale Windows-SSD und nicht-NEXUS.*-Wurzeln wurden nicht traversiert.

`_NEXUS_WAYFINDER.md` ist eine generierte Navigationssicht dieses Runs, kein neuer
unabhängig gepflegter Master. JSON-Manifest liegt im Paket. Der neue Navigationsverweis
in `_FRONTMATTER.md` soll den Wegweiser direkt erreichbar machen; AGBs bleiben unverändert.
Vorhandene Registry/_INDEX.MASTER bleiben autoritativ. Der Import der Manifestzeilen in
die bestehende Ingestion ist eine gesonderte, noch nicht nachgewiesene Stufe.

## 6. Peerreview und QA

Drei separate Codex-Instanzen prüften zuerst den Plan, verlangten Korrekturen und prüften
anschließend den finalen Code und dieselben 15 Dateihashes. Perspektiven: Software,
AI-Governance, Systeme. Ergebnis: PASS im begrenzten Kandidatenumfang mit Releasegates.
Alle führten 13 Python- und 6 Node-Tests erneut aus: PASS. Reviewertexte liegen unverändert
im Paket. Gleiche Modellfamilie, keine externe Modellpluralität oder OPUS-Ausführung behauptet.

Geprüfte Fehler: fehlende Berechtigung, falsche Metadaten/Zielordner/Bytes, Requestkonflikt,
Abbruch vor/nach Upload, Wiederholung nach Service-Neustart, paralleler Zugriff, Journalfehler,
Originabweichung, nicht eingerichteter Writer, falsche Receipts, fehlender Browserstorage.
Gesamtapp `npm run lint`/`npm run build`, Browserlayouttest, Windows-/Live-Drive-E2E,
Registertransaktion und OPUS-Review: NOT_RUN/BLOCKED. Tests mit FakeDrive beweisen
keinen echten Providerzugriff. Ein späterer Code-/Testwechsel macht das Review stale.

## 7. Quellen und nächste Entscheidung

- Führende AGB v004: https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view
- Frontmatter v003 ENTWURF, Änderungsziel Navigation: https://drive.google.com/file/d/1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi/view
- Manifest: https://docs.google.com/document/d/1o5ywhvaz0_fDn10diIy4ZIhSyQsL3C_3qODNNM5IGVg/edit
- Baseline: https://docs.google.com/document/d/1Ig0YFqbWji6B5-oOFcxuVpHb5GEBk0HlbJVz51rf9ho/edit
- WORK/Folder: https://drive.google.com/file/d/11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH/view
- Bestehendes Register: https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view
- Geprüfter Code: https://github.com/julianzotter/GEMINI-LIVE-DESKTOP-STUDIO-/pull/1, Commit `a5e68fd970ff558837d4a3e849a4c5e88a2b136a`

Keine Entscheidung zur Produktionsfreigabe erforderlich, solange die offenen E2E-/Review-
Gates fehlen. Nächster überprüfbarer Schritt: tatsächliche OPUS-Instanz meldet Modell-/Runtime-
Receipt und ACK, prüft den Freeze und liefert hashgebundene Findings. Danach Deltakorrektur,
erneutes Review und ausschließlich ID01 entscheidet über Merge/Deployment.

## Korrelierter paralleler Rücklauf — vor Abschluss frisch entdeckt

Ein anderer laufender NEXUS-Auftrag hat parallel bereits einen [Guide](https://drive.google.com/file/d/1YU3_S39wwLV1ilnin4ie8Smgedgc7-3C/view)
und einen [Depth-1-Wegweiser](https://drive.google.com/file/d/1e8LetZRMUC_bxkbDAwfjmRcxBTEvoTia/view) unter Ticket
WO-20261102-NEXUS-WAYFINDER-01 veröffentlicht. Dessen Angaben zu 212 Dateien
und unserem rekursiven Inventar mit 733 Einträgen haben unterschiedliche Zähl-/Tiefenscopes.
Keine dieser Zahlen ist ein systemweiter Volltext-/Ingestionnachweis. Fremde Test- und
Reviewangaben werden als berichtete Angaben behandelt, hier nicht erneut zertifiziert.

Der Parallelguide nennt `tools/nexus_export_lock.py` im Branch
`julianzotter/nexus-platform:id06/nexus-wayfinder-export-lock`. Vor Merge sind beide
Kandidaten gegeneinander zu prüfen und ein gemeinsamer kanonischer Schreibpfad
festzulegen; kein ungeprüftes zweites produktives Gateway. Unser Kandidat ergänzt
insbesondere die tatsächlich gefundene Studio-UI/Express-Anbindung. Diese Navigation
ist eine zusätzliche rekursive Run-Projektion und übernimmt keine Masterautorität.
Externer Reviewauftrag muss diese Konvergenz explizit beurteilen.
