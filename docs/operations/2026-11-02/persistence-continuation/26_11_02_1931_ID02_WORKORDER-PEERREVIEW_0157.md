---
name: WORKORDER-PEERREVIEW
version: 1.0.1
status: REVIEWED_BOUNDED
timestamp: '2026-11-02T19:31:16.452310+01:00'
agent_id: ID02
executor: OpenAI Codex
executor_instance: /root
owner: Julian Zotter
ticket_id: WO-20261102-NEXUS-PERSISTENCE-GATE
artifact_id: null
registration_status: PENDING_ACTUAL_WRITEBACK
hash_scope: body_utf8_after_closing_frontmatter_lf
hash: 4d8f2274aa92ad3cfe4c9dc88e14aa3febfb412a37af74e61cefb169c12bbe29
---
# Work Order und belegter unabhängiger Prüfrücklauf
TICKET_ID: WO-20261102-NEXUS-PERSISTENCE-GATE
CREATED_AT: 2026-11-02T19:31:16.452310+01:00
OWNER_ID: ID02 Koordination; technische Freigabe ausschließlich ID01
PRIORITY: P0
STATUS: REVIEWED_BOUNDED / LIVE_INTEGRATION_OPEN
SOURCE/SSOT_ANCHOR: AGB, Frontmatter, Manifest, Baseline und WORK gemäß verlinktem Arbeitsplan
OBJECTIVE: Verifizierte Persistenz im bestehenden Deliverypfad und kontinuierliche sichere Entwicklung.
INPUTS: nexus-platform main fb103dbe6b0bd392c8bc6adc1b5988bac9cc5735; konkrete Code-/Testdateien; AGB-v005-Diff; aktueller Voice-Verlauf.
CONSTRAINTS: keine Löschung, E-Mail, Berechtigungsänderung, Merge oder Deployment; kein erfundener externer Modellreview.
TASK: Design unabhängig falsifizieren; Negativtests; Codeprüfung; Findings korrigieren; denselben Finalstand erneut prüfen; Rücklauf mit Hashes.
EXPECTED_OUTPUT: tatsächliche Befunde, reproduzierte Fehler, Testausgaben, finaler Verdict, verbleibende Grenzen.
ACCEPTANCE_CRITERIA: reale getrennte Instanzen; Code-/Testhashbindung; File-/Registry-/Review-/Releasezustände getrennt; kein voller Erfolg bei fehlenden Nachweisen.
DEPENDENCIES: Live-Host/Drivecredentials und belegter exklusiver Writer für produktive Registrywrites; fremde Modelle nur mit tatsächlich verfügbarer Runtime.
RISKS: verteilte Konkurrenz, mutable Receipts, falsche ID-/Versionsbindung, unbelegte globale Durchsetzung.
NEXT_ACTION: finalen begrenzten Code-/Dokustand in bestehenden PR59 schreiben; echte Hostintegration separat fortführen.

## Tatsächlicher Reviewablauf
| Schritt | Tatsächlich beobachtet |
|---|---|
| Beauftragung | separate Instanzen /root/independent_design_review und /root/systems_review gestartet; aktuelle Quellen gelesen |
| Design | beide verlangen echten Ausführungsnachweis, partial states, Registrybindung und externe Single-Writer-Voraussetzung |
| Erste Tests | 18 bestehende +14 neue Tests bestanden; das allein ersetzte Review nicht |
| Befund P1 | beide erkennen den veränderlichen Receiptinhalt; systems_review reproduziert JOURNAL_SOURCE_CONFLICT beim zweiten execute-Aufruf. independent_design_review bestätigt den korrigierten Doppelrun: dynamischer registry_sha256 war zuvor im vermeintlich unveränderlichen Receipt |
| Korrektur | Delivery-only-Receipt vor Registrierungsadapter einfrieren; dynamischer Zustand bleibt im Runreport |
| Zusatzbefunde | registered_at fehlte beim Matching; finaler Registerhash bezog sich nicht zwingend auf finale Readbackbytes; HTTP403 wurde unpräzise zu UNKNOWN |
| Korrektur | timezonehaltigen ISO-Zeitpunkt prüfen; final_raw hashen; eindeutigen Berechtigungsfehler bewahren |
| Re-Review | beide Instanzen führen 17 neue +18 bestehende Tests selbst erneut aus: PASS_BOUNDED; Doppelrun mit fremdem Registerappend ohne neue Dateidublette |
| Governance | AGB-v005-Regelbody von beiden geprüft; Snapshotlink/Änderungsautorität vor Write mit realem Ergebnis korrigiert |

## Eingefrorene überprüfte Codehashes
| Datei | SHA256 |
|---|---|
| tools/deliver_work.py | 2aa5216046845011e6da8c6dd5803a759078f409d73567c9f8533921448cd6e0 |
| tools/persistence_gate.py | 25c3b6c1ca7f61bf9e33bd8b2a11378f9b8a9667085e6ae55cd48b1f9d84e4f9 |
| tools/delivery_errors.py | 987ecd8cd5222e17b06bce5153dbaf5337fd182f75cdb9daf20ef45336776229 |
| tests/test_persistence_gate.py | fea6d8574fc2cb9cc3b442d1d4ac98b3922300b961ab282a3e6d693a57d26ab2 |
| AGB v005 veröffentlichte Rohbytes | 4c454259b40b4174d2bb773660f54fa6fbd44a30e10b7f1f3c27925adc9445ea |

## Testumfang
35 Python-Unittests im vorhandenen Deliverypfad und neuen Adapter, einschließlich echter lokaler HTTP-503-Wiederholung im Bestands-Test. Neue Tests verwenden FakeDrive; sie beweisen keinen Live-Google-API-Zugriff. Fälle: falsche Metadaten/Bytes/Operation, Versionsänderung, fehlende Konfiguration/Bestätigung, Read-only-Registrierung, fehlerhafte JSONL, Konflikt vor Write, unklarer Ausgang nach Registrywrite, fehlender Registrierungstimestamp, Wiederholung mit fremdem Event, echte execute-Integration und vollständige Rohbyte-Unterschiede.

Zusätzlich vorhandener Studio-PR1 a5e68fd970ff558837d4a3e849a4c5e88a2b136a in separatem lokalen Checkout: 13 Python- und 6 Node-Tests erneut ausgeführt, TypeScriptprüfung und Vite-Build bestanden. Esbuild-Bestandskonflikt wird in derselben PR-Branch korrigiert. Dieser Test ist nicht der Live-Drive-/Windows-Abnahmelauf.

## Verdict / Grenzen
PASS_BOUNDED_DEVELOPMENT. Die Ausgabe PERSISTED_VERIFIED entsteht nur im neuen optionalen --register-Pfad nach passenden Datei- und Registerreadbacks. Bestehende Aufrufer ohne diese Option liefern weiter den engen DELIVERY_VERIFIED-Zustand mit registration_status NOT_CHECKED. Keine universelle Durchsetzung oder bereits migrierte globale Caller behauptet.

Registrydefault ist read-only. --registry-write-mode exclusive-writer setzt nachgewiesene externe Exklusivität voraus; der Parameter ist kein Lock. Read-compare/replace/readback schließt nicht alle Mehrschreiberrennen. Deshalb kein Produktionseinsatz dieser Registry-Schreiboption ohne tatsächlichen Writer-/Zugriffsnachweis. Der bestehende Studiokandidat lässt Registrierung explizit offen, bis ein sicherer kanonischer Writer vorhanden ist. Beide Pfade müssen vor Produktivintegration auf einen gemeinsamen Contract konvergieren.

Kein OPUS5.5-, Claude- oder DeepSeek-Run. Der vorhandene externe Auftrag https://drive.google.com/file/d/1rGV_OdgRk4VpXsZKcQw77Ys2OqIp5WCa/view bleibt als OPEN/EXTERNAL_RUNTIME_BLOCKED erhalten. Reale Codex-Reviews sind abgeschlossen, externe Modellpluralität ist nicht behauptet. Ein späterer Code-/Testwechsel macht dieses Review für den geänderten Stand stale.

FINDINGS: konkret reproduziert und korrigiert wie oben.
EVIDENCE/SOURCES: reale Reviewerantworten dieses Chatlaufs; lokale Testausgaben; Hashmanifest; kanonische Quellen im Arbeitsplan.
ARTIFACTS: vier Code-/Testdateien, AGB v005, drei Kernrückläufe, bestehende PR59/PR1.
RISKS: Liveintegration, Registrierungsexklusivität, externe Modellruntime und Human Release offen.
QA_STATUS: PASS_BOUNDED, keine technische Freigabe.

## Präzisierung der Reviewerprovenienz (Version 1.0.1)
Die erste Fassung schrieb beiden Reviewern eine Fehlerreproduktion zu. Belegt ist: systems_review reproduzierte den Repeat-Fehler vor Korrektur; independent_design_review erkannte ihn per Codeinspektion und beobachtete beim eigenen Doppelrun bereits die korrigierte Fassung. Letzterer reproduzierte selbst fehlendes registered_at und inkonsistenten finalen Registerhash. Der Vorgänger bleibt im CONTROL-BEFORE-Archiv erhalten.
