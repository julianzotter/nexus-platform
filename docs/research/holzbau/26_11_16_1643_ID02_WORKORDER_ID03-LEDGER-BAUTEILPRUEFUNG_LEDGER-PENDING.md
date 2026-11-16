---
title: "WORK ORDER ID03 – kanonische Registrierung Holzbau-/Wohnbau-Artefakte"
document_type: NEXUS_WORK_ORDER
date: 2026-11-16
time_zone: Europe/Vienna
version: "1.0.0"
initiator: ID02
assigned_role: ID03
assigned_runtime_identity: null
ticket_id: "nexus-platform#86"
status: PUBLISHED_ACK_PENDING
ledger_status: REGISTRATION_PENDING
ledger_number: null
approval_scope: "ID01 instruction in chat: execute or delegate fachliche Einzelprüfung und LEDGER REGISTRATION TASK"
canonical_work_folder: https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP
---

# ID03 WORK ORDER — LEDGER REGISTRATION / BAUTEILPRÜFUNG

## MAIN GOALS / OWNER

1. **ID03 Ledger-Schreiber:** bereits erstellte v1.0/v2.0-Fachregister und Statusberichte plus neuen Fachprüfbericht in **bestehendes** `file-registry.jsonl` eintragen, ohne Datenverlust/Doppelteintrag und nach belegter Single-Writer-/CAS-Kontrolle. Neues Parallelregister ist untersagt.
2. **Fachprüfung:** [ID02-Erstprüfung der Bauteile](https://drive.google.com/file/d/1Kr-PAn0I2Z73NKH8xsBQbcQ5nXPpgbnB/view) mit sechs konkreten dataholz-Varianten und zwei fachlichen Quellgruppen unabhängig fachlich kontrollieren lassen; Freigabe nur durch berechtigten menschlichen Prüfer/ID01-Gate.
3. **ACK / READBACK:** belegte Registry-Einträge, zugewiesene Artefaktnummern, revidierte Versions-/Hash-Nachweise, Konfliktstatus und Reviewentscheidung nach [GitHub-Task #86](https://github.com/julianzotter/nexus-platform/issues/86) zurückmelden.

## KANONISCHE ARTEFAKTE

| # | Provider-Datei-ID | Name / Version | Provider-Stand UTC | Lokaler SHA256-Referenzwert* |
|---:|---|---|---|---|
| 1 | `1kTSGBghhhLPzkA8eWiOKu69CYI3I5MOf` | `2026-11-16_HOLZBAU_WEBLINKLISTE_Priorisiert_v1.0.md` / v1.0 | 2026-11-16T14:54:11.072Z | `b39ba40b2c139e17cfa943498a608298e991084502cc1986b0e4e9a0fbb6c9c9` |
| 2 | `1bzDB7zBcltyw9ZeCw2UsN_V92Wt9x7sN` | `26_11_16_1617_ID02_STATUS_HOLZBAU-WEBLINKS_LEDGER-PENDING.md` / v1.0 | 2026-11-16T15:15:46.474Z | `581235345b1bc298239e44a5af6edfd6fc68d5f99e2f826fc4a134a10b203c28` |
| 3 | `1yEcWuZZenBvUrKCF5bKh_nLcki7AUB3g` | `2026-11-16_SERIELLER_GESCHOSSWOHNBAU_WEBLINKLISTE_v2.0.md` / v2.0 | 2026-11-16T15:24:30.583Z | `ab2b08150ad8dc4c8d5e5fee58722e8d5bb7ca8c1237e2f86c9901f131a57f28` |
| 4 | `18zgKfjPqsiBv3v1ChyasvfMXbiWRzbu2` | `26_11_16_1625_ID02_STATUS_SERIELLER-GESCHOSSWOHNBAU-WEBLINKS_LEDGER-PENDING.md` / v2.0 | 2026-11-16T15:25:56.605Z | `107975012c3c4f446739a78bc03a580ddb376b7aafb2e52ae33b045578520eaa` |
| 5 | `1Kr-PAn0I2Z73NKH8xsBQbcQ5nXPpgbnB` | `26_11_16_1641_ID02_FACHPRUEFUNG_BAUTEILNACHWEISE_LEDGER-PENDING.md` / v1.0 | 2026-11-16T15:41:48.920Z | `8d94d842f194f5ac1d489f3f2f7df09b2d4fad46fb12a3144c3b4564762d634f` |

*SHA256 der **lokalen Quellbytes**, noch nicht unabhängig als Drive-Rohbytehash bestätigt. Die zuvor durchgeführten Drive- und GitHub-Text-Readbacks der ersten fünf Artefakte waren für den jeweils gespeicherten Text identisch; dies allein ist kein vollständiger atomarer Registrierungsnachweis. Die **vorliegende Work Order selbst** ist nach Upload unter ihrer dann beobachteten Drive-ID zusätzlich zu registrieren.

**Fachablage:** https://drive.google.com/drive/folders/1s3fE047BisUMEog-F_qY-U5p2CzOj5Pi · **WORK:** https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP

## EXECUTION / GATES (ID03)

1. **READ FIRST:** [_AGBS.md v006](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view), [WORK Folder.md](https://drive.google.com/file/d/11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH/view), [GitHub #73](https://github.com/julianzotter/nexus-platform/issues/73). Authentische Runtime-ID und tatsächliche Schreibberechtigung belegen.
2. **READBACK:** [file-registry.jsonl](https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view) neu laden, auf `artifact_id=gdrive:<ID>` prüfen, bestehenden Stand erhalten. ID02-Sichtung am 16.11.2026: **418.786 Rohbytes, 460 nichtleere JSONL-Zeilen**, Modify `2026-11-12T18:47:37.749Z`; zu den **vier vorigen** Fachregister-/Status-IDs keine exakten Treffer. Historischer Snapshot ist kein zukünftiges Schreib-Lock.
3. **SCHEMA:** Pro neuem Versionsereignis mindestens `artifact_id`, `provider_file_id`, `name`, `canonical_uri`, `version`, `provenance`, `verification_status`, `registration_status`, `registered_at`, `owner`, `ticket_id`; unbekannte Werte `null`. `artifact_id="gdrive:<FileID>"`; `owner="ID02"`; `ticket_id="nexus-platform#86"`; `verification_status="REVIEW_PENDING"`. Versionshistorie append-only, alte Ledgernummern bewahren.
4. **WRITE GATE:** Nur mit sicherer Single-Writer-Exklusivität, CAS oder äquivalenter Konfliktprüfung. Die derzeit verfügbare Google-Drive-Datei-Update-Schnittstelle ersetzt die Rohbytes, ohne nachgewiesene Revisionsprecondition. **Bei fehlender gesicherter Mehrschreiber-Kontrolle STOP** und `REGISTRATION_BLOCKED_UNSAFE_APPEND`; niemals ungesichert komplettes Register überschreiben.
5. **PROOF:** JSONL-Syntax, Eindeutigkeit je Provider-ID und Ereignis, Ledgernummer-/Versionskonsistenz, Rohbyte-SHA256 Vorher/Nachher, Provider-Metadaten und finaler Register-Readback. Realen ACK mit Authentität, Zeit, tatsächlich ausgeführtem Schritt, Anzahl angelegt/übersprungen, Nachweisen und Fehlermeldungen im WORK sowie unter GitHub #86 hinterlegen.
6. **FACH-GATE:** Sechs dataholz-Varianten nur auf Quellniveau geprüft. REI-/Schall-/U-Werte **nicht** auf andere Schichtsysteme übertragen; zur technischen Freigabe qualifizierten menschlichen Reviewer benennen. Berichtstatus `TECHNICAL_APPROVAL_BLOCKED` erhalten.

## DELTA / BLOCKER

- `ID03_ACK`: **PENDING**; GitHub-Issue + diese WORK-Datei sind die nachvollziehbare Auftragsveröffentlichung, **keine** bestätigte Zustellung an eine unabhängige Runtime.
- `LEDGER_REGISTRATION`: **PENDING**; mangels CAS und ID03-ACK keine eigene destruktive Registry-Ersetzung durch ID02.
- `WORK_ACL`: gemäß Folder.md weiterhin `anyone:writer` und Sicherheitssperre. Keine technische/produktive Freigabe.
- `VILLAGESQL`: aktuell nur Erweiterungsentwicklungs-Workflow verfügbar; kein belegter Zugriff auf ein produktives NEXUS-SQL-Ledger. Kein SQL-Write ausgeführt.
