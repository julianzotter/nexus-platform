---
name: 26_11_25_0001_ID05_WORKORDER_SYSTEMEVAL_ARCHITEKTUR_NACHTRAG_LEDGER-PENDING
version: "1.0"
status: REVIEW
timestamp: "2026-11-25T00:01:39+01:00"
timezone: Europe/Vienna
agent_id: ID05
role_id: ID05
owner_id: ID05
issuer_id: ID01
executor_instance: OpenAI Codex /root
provider: OpenAI
model_id: null
role_register_version: NEXUS-ROLES-v1.2
ticket_id: WO-20261124-ID05-SYSTEMEVAL
registration_status: REGISTRATION_PENDING
ledger_id: null
release_status: NO_RELEASE
hash_scope: body_utf8_after_closing_frontmatter_lf
hash: d1e23713eaa45875f5f656f008da57e33c09dbc2a29a231b2dd6bda97b659d8a
task_state: OPEN
participation: OPEN_CALL
review_status: REVIEW_REQUESTED
---
# Work Order · Architektur und Kontrollmechanismen

WO-20261124-ID05-SYSTEMEVAL · offener Nachtrag für ID01–ID08 · [Auftrag in WORK](https://drive.google.com/file/d/1ekmdh6AIdLuOd35jpCq3kQhLlwze6CsP/view) · [Ticket 41](https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit#gid=1465731618&range=A41:K41) · [Review-PR #129](https://github.com/julianzotter/nexus-platform/pull/129). Die drei Prüflinien dieses Nachtrags konkretisieren denselben Auftrag. ID09 und ID10 sind inaktiv. ID05 ist die vom Auftraggeber gewählte Kennung für diesen Codex-Lauf. Das Manifest führt Perplexity als regulären Akteur für ID05. Jede Antwort weist ihre tatsächliche Runtime aus.

## Was der erneute Abgleich ergibt

Vier Drive-Originale erneut roh gelesen. Die Bytes sind gegenüber der [Prüfmatrix mit SHA-256](https://drive.google.com/file/d/1wjucx0wHM8LGxVWaWuWyNncTbjODaprD/view) unverändert. GitHub steht weiterhin auf [main 3372255c0d6cbaf6f33c4ab2d893d7e3c20df961](https://github.com/julianzotter/nexus-platform/commit/3372255c0d6cbaf6f33c4ab2d893d7e3c20df961), PR #128 auf [bda587e213fd3f705b72fa0f78a8eb61eb66b1c4](https://github.com/julianzotter/nexus-platform/pull/128). Manifest und Baseline weichen zwischen den Systemen ab. AGB v007.2 und Frontmatter v008 sind im Vergleichs-PR byteidentisch. Frontmatter v008 ist ein Entwurf. Der konkrete Widerspruch aus dem neuen ID02-Bericht ist reproduziert: Die Drive-Baseline beginnt mit der Rollenentscheidung v1.2 und nennt in §17 weiterhin v1.1. [Baseline](https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view) · [Manifest §4](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view)

| Kontrollpunkt | Drive und WORK | GitHub und Ausführung | Folgerung |
|---|---|---|---|
| Quellen und Identität | Kanonische MD-Dateien und Provider-IDs, Rollenautorität im Manifest, Aufträge im Ticketregister. | Versionierte Code-/Schemasicht und Review-Snapshots an vollständigen Commit-SHAs. | Pro Artefakttyp eine führende Quelle ausweisen. Rollen-ID, Runtime, Konto und Zugriffsbeleg getrennt erfassen. |
| Zustellung und Rückmeldung | Zwei neue ID02-Berichte als Fachbeiträge gelesen. Der Governance-Bericht enthält `ticket_id: null`; im Kontrollbericht fehlt die Ticketreferenz. | Der offene PR enthält bis zur Abfrage einen Bot-Hinweis zum Review-Limit, null formale Reviews. Am ursprünglichen WORK-Auftrag null Drive-Kommentare. | Beide Beiträge sachlich berücksichtigen. Für ein ACK zu #129 fehlen eine eindeutige Zuordnung und eine bestätigte Übernahme. |
| Überwachung | ChatGPT-Aufgaben für WORK, CPLM und Critical Gates vorhanden. Im abgerufenen Inventar mit Titel NEXUS/CPLM sind 8 aktiv und 6 pausiert. | [Monitor](https://github.com/julianzotter/nexus-platform/blob/3372255c0d6cbaf6f33c4ab2d893d7e3c20df961/.github/workflows/nexus-monitor.yml) stündlich :17 UTC, bei Push auf main und manuell. [Drive-Poll](https://github.com/julianzotter/nexus-platform/blob/3372255c0d6cbaf6f33c4ab2d893d7e3c20df961/.github/workflows/nexus-drive-poll.yml) :07/:37 UTC, manuell oder bei drive_change. Poll speichert den Checkpoint und ein GitHub-Artefakt. | Soll-Intervall und tatsächliche Laufzeiten anhand mehrerer regulärer Läufe vergleichen. Einen manuellen Start gesondert kennzeichnen. |
| Writeback und Merge | Interaktiver Writeback der bisherigen drei WORK-Dateien mit Rohhash belegt. Artefaktregistereintrag offen. | [Delivery](https://github.com/julianzotter/nexus-platform/blob/3372255c0d6cbaf6f33c4ab2d893d7e3c20df961/.github/workflows/nexus-delivery.yml) nach beendetem Monitorlauf auf main oder per Dispatch, mit einer gemeinsamen Schreibgruppe. [Belegter Lauf](https://github.com/julianzotter/nexus-platform/actions/runs/45495332066) scheiterte im Credential-Check und übersprang den Schreibschritt. [CI auf bisherigem PR-Head](https://github.com/julianzotter/nexus-platform/actions/runs/45505317117) erfolgreich. | Repo-CI, Berechtigung des Runners, Rohbyte-Beleg, unabhängiges Review am aktuellen Head und ID01-Release einzeln prüfen. Branchschutz-Konfiguration nicht verifiziert. |

## Neue Feedbackquellen und Einordnung

- [ID02 Governance-Audit](https://drive.google.com/file/d/1xTguEG0f2kxiUBx-rYPIa-r-uJV_2qxm/view) · 3.217 Rohbytes, SHA-256 `46ca62e6c3d325f4e8bc8a16ab51192c044b8469bc2fc2c7c960705ae8fa5440`, identisch mit der Angabe in der übermittelten Auditkopie. Bestätigt den §17-Konflikt, den Entwurfsstatus der Vorlage und die ältere Aktivierungsklausel in AGB §12. Der Autor meldet seine Business-Runtime, eine nachträgliche Startmeldung und ausstehende unabhängige Prüfung.
- [ID02 Kontrollaudit](https://drive.google.com/file/d/1a8yhTDf1L4fKL97U_vNPoQsNlXnf2xRN/view) · 3.554 Rohbytes, SHA-256 `72b349174a6e44bdbc8436468b228ce2d16a928aa77124b47fb968a5f75b75ac`. Empfiehlt, den bestehenden Rückkanal wiederherzustellen, parallele Meldungen zu bündeln und Intervalle erst nach gemessener Liveness anzupassen. Die zwei Cron-Ausdrücke wurden am Quellcommit gegengeprüft.
- Die von ID01 beigefügte Gesprächskopie hat SHA-256 `736354df4be64ab2ca646ad54abe8e023952d743f7d54d0f17133f8b17d3943a`. Ihr erster Befund bewertet eine wiederholte Ankündigung. Der inzwischen dokumentierte Work Order, der PR und die Rohbyte-Belege schließen diese damalige Nachweislücke. Die unabhängige Abnahme ist weiter offen.

## Freier Prüfauftrag nach Ebene

| Ebene | Prüffrage und erwartetes Ergebnis | Abnahmetest |
|---|---|---|
| A · Systemlogik und Datenmodell | ID03/ID04 und weitere Interessierte prüfen einen gemeinsamen Schlüsselvertrag. Auftrag: ticket_id, owner_role, status. Lauf: run_id, ticket_id, executor_instance, model_id, observed_at. Artefakt: provider_file_id, Version, kanonische URI, Rohhash. Git-Beleg: Repository, Pfad, PR, voller Commit. Reply: Ticket, Lauf, Absender, geprüfte Revision, Befund, Quelle. Diese Felder sind ein Entwurf zur Abbildung auf vorhandene Schemata. | Eine echte Kette vom Ticket bis zum Artefakt und zurück auflösen. Eine neue Revision derselben Drive-ID muss als Änderung erkennbar sein. Eine gleichnamige Datei mit anderer ID muss getrennt bleiben. Den §17-Abgleich mit Änderungsvorschlag und Quelle liefern. |
| B · Orchestrierung und Kontrolle | ID02/ID04/ID07, reguläres ID05 und optional ID08 prüfen CLAIM → START_ACK → Ergebnis → Review. Für offene oder widersprüchliche Befunde Owner, Beleg, nächsten Prüftermin und Eskalationsziel festhalten. ID01 entscheidet bei Rollenkonflikt oder Release. | Dieselbe Antwort über Drive und GitHub nur einmal zählen, beide Fundstellen behalten. Ohne explizite Ticketreferenz als Fachbeitrag führen. Autor und unabhängige Prüfinstanz belegen. Fehlende Antwort als offen protokollieren. |
| C · Umsetzung und Synchronisation | ID06 und weitere Interessierte prüfen Poll, Monitor, Delivery, CI und Review. Vorgeschlagener Idempotenzschlüssel: Quelllauf, Artefaktversion und Ziel. Vor einem Retry den vorhandenen Beleg beziehungsweise das Journal lesen. | Drei reguläre Scheduler-Läufe je Monitor/Poller und drei reale Writebacks mit Provider-ID, SHA-256 und Registerzeile. Ein wiederholtes Ereignis darf keine doppelte Lieferung erzeugen. Nach einem Push CI und Review auf den neuen Head beziehen. [Recovery-Runbook](https://github.com/julianzotter/nexus-platform/blob/3372255c0d6cbaf6f33c4ab2d893d7e3c20df961/docs/NEXUS-SCHEDULER-RECOVERY.md) |

## Kontrollalgorithmus im lokalen Funktionstest

Den CLI-Einstieg von [assert_operational_evidence.py](https://github.com/julianzotter/nexus-platform/blob/3372255c0d6cbaf6f33c4ab2d893d7e3c20df961/tools/assert_operational_evidence.py) unverändert am angegebenen Commit mit vier synthetischen Eingaben ausgeführt. Kein Zugriff auf Produktionsdaten im Test.

| Fall | Exitcode | Rückgabe |
|---|---:|---|
| Monitorstatus INCOMPLETE | 2 | BLOCKED · MONITOR_NOT_COMPLETE |
| Poll INITIALIZED, 0 Änderungen, gültiger Initial-Checkpoint | 0 | PASS · INITIALIZED_NOT_OPERATIONAL |
| Poll OK, 1 Änderung, fehlender Checkpoint | 2 | BLOCKED · CHECKPOINT_MISSING |
| Poll OK, 1 Änderung, gültiger Folge-Checkpoint | 0 | PASS · POLL_REPORT_PASS_REQUIRES_CHECKPOINT |

Der Initialisierungsfall ist für das Reporting entscheidend: Exitcode 0 bestätigt hier einen gültigen Startzustand. Für einen Betriebsnachweis muss der Konsument zusätzlich den Rückgabegrund und einen späteren regulären Lauf mit Änderung auswerten. Für die adaptive Steuerung zunächst einen Replay-Test auf Protokolldaten vorschlagen: neue Änderung sofort einreihen, identische Ereignisse bündeln, bei vorübergehendem Fehler begrenzt verzögern und bei Authentifizierungsfehler genau einen Recovery-Fall an ID01 eskalieren. Die im ID02-Bericht genannten 15–240 Minuten dienen als Testparameter.

## Antwort und Freigabe

Teilnahme freiwillig. Im [PR #129](https://github.com/julianzotter/nexus-platform/pull/129) oder in WORK mit `CLAIM WO-20261124-ID05-SYSTEMEVAL` die Prüflinie nennen. Mit `RESULT WO-20261124-ID05-SYSTEMEVAL` Rolle, tatsächliche Runtime, Quellrevision, Test, Ergebnis und Beleg zurückmelden. Für eine Zusammenführung im Review die Quellen verlinken. Bei gleichwertigen Widersprüchen beide Befunde bis zur Entscheidung offenhalten. Die Freigabeentscheidung bleibt bei ID01. Die Rückmeldungen, Registrierungsbelege und drei operativen E2E-Nachweise sind weiterhin offen.
