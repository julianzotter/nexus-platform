---
name: LESSONS-LEARNED-STATUS
version: 1.0.1
status: TESTED_REVIEWED_BOUNDED_LIVE_INTEGRATION_OPEN
timestamp: '2026-11-02T19:39:00.875989+01:00'
agent_id: ID02
executor: OpenAI Codex
executor_instance: /root
owner: Julian Zotter
ticket_id: WO-20261102-NEXUS-PERSISTENCE-GATE
artifact_id: null
registration_status: PENDING_ACTUAL_WRITEBACK
hash_scope: body_utf8_after_closing_frontmatter_lf
hash: 3103d8a68476fb77750940f95a6e85b978bd44a91d9c86787e23aac76deab2ce
---
# Lessons Learned und konsolidierter Ausführungsstatus
## Ergebnis / offene Grenzen
Dieser Fortsetzungslauf erfasst die bereitgestellte Konversation, ergänzt die Safe-Mode-Regel und UL/SU, erweitert den vorhandenen Deliverypfad, schließt zwei reale Codex-Peerreviews mit korrigierten Findings ab und führt die vorhandenen PRs fort. Kein Merge, Deployment, Fachsolver, technische Freigabe, Datei-Löschen oder E-Mail-Versand.

Die neue oberste Entwicklungspriorität gilt: Kommunikation und unabhängige sichere Entwicklung laufen weiter. Ein offener Live-/Registrierungs-/Freigabenachweis ist kein Grund, Analyse, Tests oder autorisierte WORK-Markdown-Rückläufe pauschal anzuhalten.

## Tatsächliche Ausführung und Evidenz
| Ergebnis | Tatsächlich belegter Stand | Nachweis |
|---|---|---|
| Sofortiger Safe-Mode-Vermerk | Drivewrite, Zielordner und bytegleicher SHA256-Readback geprüft | https://drive.google.com/file/d/19y0fc4s3-bVSGJKTsa8dbXWBhTEC-vyj/view ; SHA256 8d6a3a4e916c5fcf4992c5bf9e94492b983613069534dd6019d69e03d2bde580 |
| AGB v005 | gleiche führende Drive-ID; v004-Rohsnapshot erhalten; v005-Readback bytegleich | https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view ; SHA256 4c454259b40b4174d2bb773660f54fa6fbd44a30e10b7f1f3c27925adc9445ea |
| AGB-v004-Vorgänger | 4660 Rohbytes unverändert gesichert/geprüft | https://drive.google.com/file/d/1pTkf_MDOeppzP5OQwriBcGXLDvd3eaXw/view ; SHA256 1c73f672a7e9f42b52d70d89bf1e21261ad3ac1bbf26ccd814de7658e33c8046 |
| Frontmatter v005 | ENTWURF erhalten; sichere Fortführung und reale Nachweisanker ergänzt; Readback bytegleich | https://drive.google.com/file/d/1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi/view ; SHA256 8acd097743f4171c5ceabc383f1b349d9839c58ca8e04f6f3a549b10da8c5e52 |
| Glossar/UL/SU | vorhandene Datei ergänzt, ursprüngliche Kandidatenautorität erhalten; Readback bytegleich | https://drive.google.com/file/d/1MnHMlbPgKRNUlSiW7SzRk20EvLrSLEOJ/view ; SHA256 936eec1ccb8beb0286031b47088f54e257e6469aacf96df98c8aa0a889e3f885 |
| Aufgabenaufnahme | vollständige fachliche Message-Coverage 0–158 und neue Anweisungen; MVC und Roadmap | https://drive.google.com/file/d/1u_4uRHrpQRSPLOueqd7UpXZAYeV0tW2V/view |
| Reviewauftrag/-rücklauf | Version1.0.1 mit korrekter Reproduktionsprovenienz; bytegleich rückgelesen | https://drive.google.com/file/d/1c_8mdTSJLT5hlajgnwxNfPr9uMmqJXeJ/view ; SHA256 348c868786b81d892ac3f310049ec39574a8e05266d496447e72249287d97e50 |
| Steuer-/Register-/Ledger-Vorgänger | ZIP mit exakten Vorfassungen; bytegleich rückgelesen | https://drive.google.com/file/d/1fHuQyaSxvA8L9HYLXmxxCZZJk7RQf_uy/view ; SHA256 fac971fa37e4ccbcfe4920cecfdfe81a3d21b21cb4e725bd995ec66fa8500bb2 |
| Deliverygate | 18 bestehende +17 neue Python-Tests; zwei getrennte Reviewer führen dieselben Tests selbst aus: PASS_BOUNDED | https://github.com/julianzotter/nexus-platform/pull/59 ; Codecommit 6d50e5e0b4f5d07acfaa113dc771fa983a310b3e |
| Bestehender Studio-PR1 | Python13/Node6 erneut PASS, TypeScriptprüfung und Vite-Build PASS; deutsches Handbuch/Peerfix ergänzt | https://github.com/julianzotter/GEMINI-LIVE-DESKTOP-STUDIO-/pull/1 ; Fortsetzungscommit c2f996032353687697a29b6be5278823a3d67d85 |

Registry-/Ledgernachführung für diese neuen/geänderten Artefakte erfolgt nach Erstellung dieses Berichts im bestehenden Register. Dieser Text behauptet den noch nachfolgenden eigenen Registerreadback nicht vorab. Der spätere Registereintrag und finale Toolnachweis sind dafür maßgeblich. Die dokumentierte Abweichung ist die verzögerte gebündelte Nachregistrierung während sicherer Entwicklungsfortführung; keine Meldung eines bereits vollständigen Abschlusses daraus.

## Incident / Ursachenanalyse mit Evidenzgrenze
VERIFIED: Im Studio-main 829f5a85cc20cb7efdff92191106593003a70610 erzeugte handleExport ausschließlich einen Blobdownload. Timeline enthielt fixe 808×500-Abmessungen. Ein Drive-Persistenzendpoint fehlte in diesem geprüften main-Stand. Der vorhandene Monitor-Deliverycode prüfte Bytehash/Parent/Key, aber band das Ergebnis nicht an Registry, Name/MIME oder stabile Metadatenversion.

VERIFIED: AGB v004 erklärte selbst, dass die systemweite Durchsetzung und ein atomarer Mehrschreiber-Lock noch nicht implementiert seien. DERIVED: Ein Leseprompt allein erzwingt folglich keine tatsächliche Schreibausführung und kann den historischen Claim nicht absichern.

UNVERIFIED: Welche konkrete historische Datei angeblich im Voice-Modus abgelegt wurde, welcher Provideraufruf damals tatsächlich stattfand und ob ein anderer Agent sie anschließend schrieb. Der übergebene Dialog ist kein Providerlog. Deshalb keine erfundene technische Root Cause oder pauschale Aussage, jedes LLM melde zwangsläufig bei Toolfehlern Erfolg.

## Gemeinsame Lessons Learned — fallbezogene Ergänzung
Die folgenden Labels gelten nur innerhalb dieser Fallnotiz; keine neue kanonische Masterregistry.
| Fall | Beobachtung / Fehler | Verbindliche Handhabung / reproduzierbarer Nachweis |
|---|---|---|
| LL-1 | Modell-/Sessiontext wurde wie ein Speicherbeleg behandelt | Zustände trennen; keine Drivebehauptung ohne tatsächlichen Providerwrite+ID/Ziel/Name; Rohbyte-/Registerstatus separat |
| LL-2 | Prompt wurde mit technischer Durchsetzung verwechselt | vertrauenswürdiger Ausführungspfad und UI-Status; Prompt verbessert Anweisung, garantiert keine I/O-Sperre |
| LL-3 | Grüne Tests wurden vorschnell mit Vollständigkeit gleichgesetzt | beide Reviewer erkannten einen Repeat-Fehler trotz32 bestandener Tests; Negativtests und Fremdreview ergänzen |
| LL-4 | Veränderlicher Registerhash steckte in unveränderlichem Receipt | stabile Deliverybytes vor Registrierung einfrieren; Doppelrun mit fremdem Registryevent testen |
| LL-5 | Passendes Registryevent war ohne registered_at noch akzeptierbar | Pflichtzeitpunkt ISO+Zeitzone prüfen; Timestampwert bei Replay nicht künstlich neu gleichsetzen |
| LL-6 | Registryhash bezog sich nicht sicher auf final gelesene Bytes | finale Rohbytes einmal lesen, Event prüfen und genau diese Bytes hashen |
| LL-7 | Zwei ähnlich benannte Reportingordner und parallele Durchläufe | Provider-IDs/Scopes zuerst; vorhandene Wegweiser/PRs wiederverwenden; aktuelle Steuerdatei vor Write frisch abgleichen |
| LL-8 | Fail-closed wurde als globale Arbeits-/Kommunikationssperre verstanden | betroffenes Erfolgsgate sperren, unabhängige sichere Entwicklung fortsetzen; Abweichungen in timestamp+ID-WORK-MD |
| LL-9 | Falsche Aussage, Lessons-Sammlung existiere nicht | vorhandene REPORTS/LESSONS_LEARNED.md und LESSONS.jsonl sind gefunden; Lesen hier403, Inhalt/Änderbarkeit ungeprüft. Diese ergänzende Fallnotiz verlinkt sie statt sie zu ersetzen |
| LL-10 | Reviewprovenienz war zu stark formuliert | systems_review reproduzierte Repeat-Fehler; independent_design_review prüfte bereits korrigierten Doppelrun und reproduzierte andere Defekte; Bericht korrigiert, Vorgänger erhalten |
| LL-11 | 'Personal Memory gespeichert' ohne mutierendes Werkzeug | Status NOT_EXECUTED_CAPABILITY_MISSING; WORK-/Governanceregel nie als Kontoeinstellung ausgeben |

Bestehende Sammlungen (nur Metadatenidentität bestätigt):
- REPORTS/LESSONS_LEARNED.md: https://drive.google.com/file/d/1OQ0wXnlnBhtmIqbo_KI11gGpVesHYxIH/view
- REPORTS/LESSONS.jsonl: https://drive.google.com/file/d/1unUFBk95axzS6vBKga1Kv6I8IdszxuVi/view
- REPORTS: https://drive.google.com/drive/folders/1MVSe1zq-alkb3hIcclimvZvLbCIYI2NV
- NEXUS.REPORTS: https://drive.google.com/drive/folders/1mmLJyc8TpTqxPFhXASb4tmHI7515xpJn
403 wurde respektiert; kein Rechte-/Zugriffs-Workaround zum Umgehen der Sperre.

## Konvergenz / Skalierung / minimal geeignete Verfahren
1. Bereits vorhandenen rekursiven Wegweiser weiterverwenden: https://drive.google.com/file/d/14Uy-D07qGSTth8l29vfoba2m-TNzWV-U/view . Der Bericht dazu nennt16 NEXUS.*-Wurzeln/80 Listings/733 Einträge. Dies ist ein fremder korrelierter Runbericht, kein atomarer Volltext- oder Ingestionnachweis dieses Fortsetzungslaufs. Unser zusätzlicher Metadatencheck dient dem Abgleich und wird kein konkurrierender Masterindex.
2. Ein gemeinsamer kanonischer Export-/Registrycontract vor produktiver Integration. Studio-PR1 und vorhandener nexus_export_lock-Kandidat sind noch nicht als gemeinsamer Produktivpfad abgenommen. Der neue Adapter ergänzt den vorhandenen Monitor-Deliverypfad, startet keinen dritten HTTP-Dienst.
3. Nachgewiesene Writerexklusivität/persistente Wiederaufnahme vor produktiver Registrymutation. compare-before-write ist kein CAS. Solange dieser Nachweis fehlt, read-only/partielle Berichte und unabhängige Tests weiterführen.

## Noch offen — kein pauschaler Entwicklungsstopp
- Tatsächliche dauerhafte Personal-Memory-/Settings-Mutation: kein geeignetes Werkzeug verfügbar. Nicht ausgeführt; keine Kenntnisnahme aller zukünftigen Modelle behauptet.
- Realer Windows-/Drive-Hosttest, Credentials, kanonisch reservierte Nummern, Prozessneustart/Denial/Readback und sicherer Registrywriter: nicht nachgewiesen.
- Globale Migration aller Caller auf das Gate: nicht implementiert. --register ist optional; ohne Option bleibt Registrierung ausdrücklich NOT_CHECKED.
- Konsistente bun.lock/Frozen-Installation: offen; lokaler npm-Peerfix und Build sind belegt, kein vollständiger Paketlock-Abgleich.
- Externes OPUS5.5-/Claude-/DeepSeek-Review: nicht ausgeführt; vorhandener korrelierter WO bleibt offen. Reale Codex-Reviews sind abgeschlossen.
- Technische Humanfreigabe, Merge und Deployment: nicht erteilt/ausgeführt. Keine Fachbemessung durchgeführt.

FINDINGS: siehe Incident/Lessons und Grenzen.
EVIDENCE/SOURCES: aktuelle AGB/Front/Glossar, Manifest/Baseline, konkrete Commits, Reviewer-/Testausgaben und oben genannte echte Drive-IDs.
ARTIFACTS: Sofortvermerk, drei Kernrückläufe, Vorfassungsarchive und bestehende Review-PRs.
RISKS: begrenzte Runtimeintegration, nichtatomare Registrywrites, unvollständige externe Rückläufe.
QA_STATUS: TESTED_AND_REVIEWED_BOUNDED; sichere Entwicklung aktiv; keine Produktionsfreigabe.
NEXT_ACTION: kontrollierten Register-/Ledgerreadback dieses Laufs abschließen; danach den nächsten sicheren Integrationsschritt an vorhandenen Host-/Reviewnachweisen ausrichten.

## Abschlussabgleich — parallele Ledgerbelegung erkannt
Der zu Laufbeginn gelesene Stand0148 nannte next free0149. Während der Bearbeitung belegte ein anderer korrelierter Lauf0149–0154 mit anderen Drive-Dateien. Dies wurde vor unserem Ledgerwrite durch erneuten Abruf erkannt. Die fünf hier erzeugten Dateien behalten ihre Drive-IDs und Inhalte; die aktuellen Dateinamen werden mit den im aktuellen Ledger ausgewählten unbesetzten IDs0155–0159 abgeglichen. Der unveränderte neueste Ledger-Vorabstand wird als0160 gesichert; Ledger-Versionsereignis0161 nennt danach next free0162. Keine fremden Zeilen werden ersetzt oder umnummeriert.
Damit ist ein weiterer konkreter Race-Condition-Fall belegt: Lesen eines next-free-Werts ist keine atomare Reservierung. Der kontrollierte Einzellaufabgleich korrigiert diese Kollision, ersetzt aber keinen systemweiten atomaren Nummernallocator.
