---
name: 26_11_24_2354_ID05_STATUS_SYSTEMEVAL_FEEDBACK_LEDGER-PENDING
version: "1.0"
status: REVIEW
timestamp: "2026-11-24T23:54:13+01:00"
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
hash: 459782ea6b2762728b49479d0c348ae514e1fe273ae06b8ccf92e25b648ecedb
development_status: EVALUATE
review_status: REVIEW_REQUESTED
---
# Systemevaluierung · GitHub, Drive und konsolidierte Rückmeldungen

Stand der Erhebung 24.11.2026, 23:48–23:53 MEZ. ID05 ist die auftragsspezifische Kennung von OpenAI Codex /root. Das reguläre Manifest-Mapping ID05/Perplexity gilt weiter. [Work Order](https://drive.google.com/file/d/1ekmdh6AIdLuOd35jpCq3kQhLlwze6CsP/view) · [Ticketregister, Zeile 41](https://docs.google.com/spreadsheets/d/1o1ZCZUgsCGTDOwdbJ7EbUCKOKJng1LcJLFnrRiPjYTE/edit#gid=1465731618&range=A41:K41) · [Diskussion und Rücklauf, PR #129](https://github.com/julianzotter/nexus-platform/pull/129)

## 1. Entscheidungslage

Zwei der vier Regeldateien im Vergleichs-PR stimmen byteweise mit Drive überein. Manifest und Baseline enthalten inhaltliche Unterschiede. Die Registrierung deckt nur einen Teil von WORK ab. Code-CI, Automationszustellung, unabhängige Prüfung und menschliche Freigabe haben jeweils eigene Nachweise. Die Systemevaluierung bleibt offen.

## 2. Messung an festen Revisionen

GitHub-Basispfad `governance/current/` an [main 3372255c0d6cbaf6f33c4ab2d893d7e3c20df961](https://github.com/julianzotter/nexus-platform/tree/3372255c0d6cbaf6f33c4ab2d893d7e3c20df961/governance/current) und [PR #128 bda587e213fd3f705b72fa0f78a8eb61eb66b1c4](https://github.com/julianzotter/nexus-platform/tree/bda587e213fd3f705b72fa0f78a8eb61eb66b1c4/governance/current). Drive-Rohdaten und Git-Blobs über den jeweiligen Connector abgerufen, Base64 dekodiert, SHA-256 über die Originalbytes berechnet. 404 gilt für den geprüften Pfad am angegebenen Commit.

| Drive-Original | Drive Bytes / SHA-256 | main | #128 |
|---|---|---|---|
| [AGBs v007.2](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view) | 13851 · `4e0efb661676747f286734f17d490106ccfe6fd179ba54324dd8454fa6b71738` | 404 | identisch |
| [Frontmatter v008](https://drive.google.com/file/d/1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi/view) | 24677 · `4755b083d1d037cbd84b2a91e77bcc171cc5d5925b01bcb604652b6732e46dbe` | 404 | identisch |
| [Manifest](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view) | 8532 · `09c8786b9064c1e5f7933d7b2cd2aae50a55f3637cfb99c1b1465c077910a055` | 8931 · `78957a2d102deb1389e2f08da4586c7b57f2ad2cf14c55faa52ec75023a593a9` | wie main |
| [Baseline](https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view) | 19020 · `893bf97595b62cd3b930df78bf9b4e4de5ed162535242b8a6fa9f813cea7100e` | 20368 · `abeed5830b7f8efe132b7f060839f75bb6061bb64702856ec1d79d894e27c2b0` | wie main |

Drive führt im Manifest und in der Baseline den konkreten Nachweis für Copilot-Tasks einschließlich Rückverweis, PR und vollem SHA. GitHub ergänzt im Manifest §4 den Verweis auf die Capability-Matrix und in MUST-90 den verifizierten Ausführungsumfang. Die GitHub-Baseline enthält zugleich einen historischen Lauftext mit ID02/Private. Ein Kopieren in nur eine Richtung kann gültige Inhalte verlieren. Der Review soll einen abschnittsweisen Abgleich mit ID01-Entscheidung und einem erneuten Rohbytevergleich liefern.

AGBs §1 bestimmt die MD-Dateien im Root als Autorität für Manifest und Baseline und ordnet die gleichnamigen Google Docs dem Archiv zu. AGBs v007.2 trägt `FREIGEGEBEN_ID01`; Abschnitt 9 bezeichnet die Kennung des Claude-Reviewers als offen, während das Manifest ID06 Claude zuordnet. Die Reichweite der ID01-Freigabe und der unabhängige Review sind getrennt zu prüfen. Frontmatter v008 trägt `ENTWURF / PENDING_HUMAN_TECHNICAL_RELEASE`. Der deklarierte Body-Hash stimmt (`89a2958490e70ba46ac20ec8cbd270d92139fa35850e6656c8960e24d475c720`). Die Datei liegt unter [WORK/_ARCHIVE_STEUERDATEIEN](https://drive.google.com/drive/folders/1FaqZ2xH3nzlDI80UDa_wrGmObvT6IB52). Ein gleichnamiges Direktkind von WORK wurde nicht gefunden. [Folder.md, Pilot 0.4.0](https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view) legt Drive als Dokumentenquelle und GitHub als Review-Snapshot fest. SHA-256 Folder.md `59340dd798d19862f12049c13ffd296a2629a38426232389d87c43e5b8ffb977`.

## 3. Ordner, Register und Formalkontrolle

| Prüfung | Ergebnis und Grenze |
|---|---|
| Ordnerbestand | SSOT-Root 355 direkte Einträge. WORK über neun Seiten, nach Provider-ID dedupliziert, 4.036 direkte Einträge, davon 3.988 Dateien und 48 Ordner. Pagination während laufenden Betriebs, ohne atomaren Stichtag. REGISTRY, SCRIPTS, SKILLS, NEXUS.MCP.SERVER und MCP-ACCESS-TOOLS stichprobenweise auf Verzeichnisebene gelesen. |
| Registerabdeckung | 410 von 3.988 WORK-Dateien (10,3 %) über `provider_file_id` oder `artifact_id=gdrive:<ID>` mit mindestens einer Zeile im [kanonischen Register](https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view) verbunden. 753 Dateinamen enthalten LEDGER-PENDING. Dieser Name allein besagt nichts über die Registrierung. Keine Aussage zur Registrierungspflicht jeder historischen Datei. |
| Registerschema | 472 nichtleere Zeilen als JSON geparst. 458 enthalten alle elf Feldnamen aus AGB §6, 14 sind unvollständig, 352 tragen `verification_status=REVIEW_PENDING`. Feldpräsenz prüft keine Werte oder Freigaben. Letzte zu den geprüften IDs auffindbare Versionen sind AGB v007.1 und Frontmatter v006-ID02-ROLE-ADOPTED. Für die beiden Root-MD-IDs ergab derselbe Schlüsselvergleich keinen Treffer. |
| Frontmatter-Stichprobe | Acht gezielt ausgewählte WORK-Berichte des 24.11., siehe Belege unten. Sieben YAML-Köpfe ließen sich parsen. Einer von acht enthält alle sechs im Entwurf genannten Schlüssel `name, version, status, timestamp, agent_id, hash`. Aliasfelder getrennt gewertet. Keine Hochrechnung auf WORK. Der [WO122-Review](https://drive.google.com/file/d/1q-t1FGDnqySOwrxpwsqtuNUfIxEgtx3H/view) scheitert in Zeile 16 beim Parsen einer YAML-Liste. Der Fehler betrifft die maschinelle Auswertbarkeit seines Kopfes. |
| Zeitstempel | Der [ID06-Registerbericht](https://drive.google.com/file/d/19-CQIcMskTYyhEds0fg7myowZV8qqHHw/view) trägt im Namen 25.11., 00:15 MEZ. Provider-Anlage 2026-11-24T22:45:46.028Z. Auch bei diesem Prüflauf lagen WORK-Anlage des Auftrags und Zeitpräfix wegen des Minutenwechsels eine Minute auseinander. Anlagezeiten und deklarierte Zeiten sind separat zu erhalten (AGBs §4). |
| Panel | [Panel](https://nexus-sync-diagnose.julianzotter.chatgpt.site) Site-Version 7 über Sites als erfolgreich publiziert bestätigt, Quellcommit `f0b425203a1cbb11a2f1b51c4eeb3e69caf93605`. Im direkten WORK-Inventar identifiziertes [Archivmanifest für Site-Version 6](https://drive.google.com/file/d/1oXcLmxK_iw17_QsHtUYwd4pklNHCwGZm/view). Ein v7-Archiv-/Readbackbeleg wurde im untersuchten Bestand nicht identifiziert. |

## 4. Konsolidierte Rückmeldungen und Gegenprüfung

| Herkunft | Inhalt, Überschneidung und offener Punkt |
|---|---|
| ID06 · [Kommentar zu #122](https://github.com/julianzotter/nexus-platform/issues/122#issuecomment-7143363034) und [WORK-Review](https://drive.google.com/file/d/1q-t1FGDnqySOwrxpwsqtuNUfIxEgtx3H/view) | Ein publizierter Auftrag belegt keine Übernahme. Die WORK-ID war bekannt. Wiederanlauf braucht einen zuständigen Owner, bestätigte Zustellung und OAuth-Wiederherstellung. Kommentar und Report sind derselbe Befund. |
| ID03 · [Status Rollen/Rollout](https://drive.google.com/file/d/1sU7Gl_8WRcg50Amfim_n49p4PVP7zxnO/view) und [#125](https://github.com/julianzotter/nexus-platform/pull/125) | Vier Drive-Hashes sind reproduziert. #125 ist geschlossen, #128 offen. Der PR-Kommentar adressiert ID02 mit einem Reviewersuchen. Ein unabhängiger ID02-Business-Rücklauf zu diesem Auftrag ist in den geprüften Quellen offen. Copilot-Task-Zuordnung bleibt laut Bericht unaufgelöst. |
| ID06 · [Rollenregister](https://drive.google.com/file/d/19-CQIcMskTYyhEds0fg7myowZV8qqHHw/view) und [Systemprüfung](https://drive.google.com/file/d/1pix0uyGPu_DzhpwuYf6xfPh_0O0JzhCh/view) | Eine aus JSON erzeugte Rollenmatrix soll divergierende Handfassungen ablösen. Die drei internen Prüfperspektiven werden vom Autor als abhängig bezeichnet. Unsere Gegenprüfung ergänzt die dort noch ausstehende Baseline-Messung. #128 hat zum Stichtag keine formalen Reviews. |
| ID02 laut historischem Bericht · [Critical Gates](https://drive.google.com/file/d/1z78MpMDV__ett23O1BlOpCY3HmHi1lrW/view), ID03 · [Copilot-Audit](https://drive.google.com/file/d/1AqhLUApBtkwwuaLBQvfjq2shpe5iyggC/view) | Beide trennen funktionierende Code-CI von der operativen Kette. [CI #128](https://github.com/julianzotter/nexus-platform/actions/runs/45503862038) erfolgreich. [Delivery](https://github.com/julianzotter/nexus-platform/actions/runs/45495332066) scheiterte bei der Prüfung der Drive-Credentials, der Rohbyte-Write wurde übersprungen. [Monitor](https://github.com/julianzotter/nexus-platform/actions/runs/45495248351) scheiterte bei Zustands- und Evidenzprüfung. Die Berichte nennen OAuth `invalid_grant` und `coverage=INCOMPLETE`. Connector-Schreiben in diesem Chat ist separat nachgewiesen. |
| [Globales Peer-Review-Dossier](https://drive.google.com/file/d/11PtT7eYC9t47y_0PniTR2HceBp8XzF_Z/view) | Beanstandet Registrierungsrückstand, Reviewlücken, wiederholte Statusmeldungen ohne Zustandsänderung, uneinheitliche Rollen-/Statusfelder und schwache ACK-Evidenz. Die Registerzähler 472/458/352 sind reproduziert. Seine Schätzung über Dateinamen wurde hier durch den Join auf Provider-ID ergänzt. Thresholds oder Ausnahmen von der Registrierpflicht brauchen ID01-Entscheid. |
| [Baseline-v2.3-Evaluation](https://drive.google.com/file/d/127u1F_drQ49buie3SRwEaeL3vnrhSiZW/view) | Persönliche Instructions als „PASS mit Auflagen“, Feldlimit in der Anwendung laut Bericht ungetestet. Dieser Befund betrifft die persönlichen Einstellungen und verleiht der System-Baseline keine neue Version. |
| [Historisches Claude-Feedback zu Aufträgen](https://drive.google.com/file/d/1Ig0QDc4Ba3b7xN2hVx6MjW7rYbEsiAEb/view) und [früheres Evaluierungsfeedback](https://drive.google.com/file/d/1-pn08mPrsDa1zTEP_CidexWgBLr577f3/view) | Fordern konkrete CLAIM/RESULT-Antworten, überprüfbare Arbeitspakete und eine Trennung zwischen Quellenbefund und Architekturvorschlag. Der neue Aufruf enthält diese Elemente. Historische „ID-05 (Claude, vorläufig)“ bleibt als damalige Quellenangabe erhalten. |
| Neuer Aufruf | Beim ersten Rücklaufcheck: null Drive-Kommentare am Auftrag, null formale Reviews an #129. Ein [automatischer PR-Kommentar](https://github.com/julianzotter/nexus-platform/pull/129#issuecomment-7146748073) meldet ein Review-Limit. Unter sechs geprüften älteren Drive-Dateien waren ebenfalls keine Kommentarthreads. Inhaltliche Rückmeldungen oben stammen aus früheren Aufträgen. |

## 5. Optimierung und Abnahme

1. ID02/ID03 prüfen den Klauseldiff von Manifest und Baseline am benannten SHA. ID01 entscheidet bei Widerspruch. Zielzustand: kanonischer Drive-Text, daraus erzeugter Git-Snapshot, vier geprüfte Datei-Hashes und unabhängiger Review am finalen Commit.
2. Benannter Registerschreiber gleicht priorisiert die vier Steuerdateien und diesen Auftrag per Provider-ID, Revision und Rohhash ab. Ein lesender Validator kann ungültiges YAML, fehlende Felder und ungeklärte Rollen melden. Abnahme: eindeutiger Register-Readback, keine doppelte ID-Vergabe, dokumentierte Ausnahmen für Altbestand. Der Eintrag im Ticketregister ist vorhanden; die Artefaktregistrierung steht aus.
3. ID01 und Betriebsverantwortliche beheben die OAuth-Ursache im Actions-Kontext und messen die Drive-Abdeckung. Je drei getrennte reale Läufe mit Run-ID, Commit, Zielordner, Datei-ID, Rohhash, Registrierung und unabhängiger Gegenprüfung unter [#73](https://github.com/julianzotter/nexus-platform/issues/73) dokumentieren. Erst dann Betriebsstatus neu bewerten.

Prüfgrenze: keine Änderung an Produktionsregeln, Zugangsdaten, Rollenregister oder Freigabestatus. Die Bestellung erfasst die vorhandenen Befunde und bittet alle aktiven Rollen um echte Rückmeldungen.
