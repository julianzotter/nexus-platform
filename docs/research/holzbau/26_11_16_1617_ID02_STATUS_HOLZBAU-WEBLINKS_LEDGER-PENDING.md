---
title: HOLZBAU-Weblinkliste — Status und Ablagenachweis
document_type: NEXUS_STATUSREPORT
date: 2026-11-16
time_zone: Europe/Vienna
version: 1.0.0
agent_id: ID02
executor: OpenAI Codex
status: FILE_VERIFIED_REGISTRATION_PENDING
review_status: REVIEW_PENDING
ledger_number: null
ticket_id: null
canonical_work_folder: https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP
---
# STATUSREPORT — HOLZBAU-WEBLINKLISTE

## FINDINGS
- **Fachliches Quellenregister v1.0 ist in Google Drive verfügbar.** 28 priorisierte Quelleneinträge, 39 eindeutige URLs; P0–P3-Klassen; Bauphysik, Holzriegel-/Holz-Hybridbau, Vorfertigung, Fassaden, Brand- und Schallschutz, DfMA.
- **Ablage Fachwissen:** `AI-ENGINEERING-KNOWLEDGEBASE/HOLZBAU/METAWISSENHOLZBAU` — https://drive.google.com/drive/folders/1s3fE047BisUMEog-F_qY-U5p2CzOj5Pi
- **Quelldokument:** `2026-11-16_HOLZBAU_WEBLINKLISTE_Priorisiert_v1.0.md` — https://drive.google.com/file/d/1kTSGBghhhLPzkA8eWiOKu69CYI3I5MOf/view
- **Inhaltsgliederung:** (1) österreichische und deutsche Regelwerke / Bauteilkataloge, (2) Planungsleitfäden und Forschung, (3) frei/registriert/abonniert/kaufpflichtig zugängliche Publikationen, (4) fachbezogene Querverweismatrix.
- **Geltungsgrenze:** Quellenauswahl und Priorisierung sind redaktionell abgeleitet. Keine statische Bemessungsfreigabe; Normen, Landesrecht, Ausgabe und nationale Anhänge im Einzelfall prüfen.

## EVIDENCE / QA
- Google Drive ID `1kTSGBghhhLPzkA8eWiOKu69CYI3I5MOf`, MIME `text/markdown`, `14452` Bytes, Parent `1s3fE047BisUMEog-F_qY-U5p2CzOj5Pi`; Google-Drive-Metadaten und Text-Readback am 16.11.2026 erfolgreich.
- Lokale Quellbytes SHA256: `b39ba40b2c139e17cfa943498a608298e991084502cc1986b0e4e9a0fbb6c9c9`; vollständiger identischer Rohbytehash des Drive-Objekts wurde **nicht** unabhängig bestätigt.
- Governance: `_AGBS.md` v006 (ID01 freigegeben, 11.11.2026), aktuelles Manifest/Baseline und WORK/`Folder.md` wurden konsultiert. `Folder.md` dokumentiert weiterhin eine kritische WORK-Berechtigungslücke (`anyone:writer`); keine Produktiv- oder Sicherheitsfreigabe.

## RISKS / OPEN
- Bestehendes `file-registry.jsonl`: fehlende bestätigte Eintragung des Fachregisters. **REGISTRATION_PENDING**, Ledgernummer mangels belegter ID03-Zuweisung nicht erfunden. Das vorliegende Berichtssuffix `LEDGER-PENDING` ist absichtlich eine gekennzeichnete temporäre Abweichung von der dreistelligen NEXUS-Artefaktnummer.
- Eine GitHub-Sicherung ist eine **Review-Kopie**, keine zweite SSOT und kein Beleg für automatischen Sync.

## NEXT_ACTION
1. ID03: Ledgernummer vergeben, append-only Registry-Eintrag des Fachregisters und dieses Berichts mit Readback bestätigen.
2. Separater Rechercheauftrag: drei verlinkte Drive-Verzeichnis-/Inventarordner und WORK auf seriellen mehrgeschossigen Wohnbau prüfen; in `v1.1` projekt- und quellenspezifisch ergänzen.
3. Bei fachlicher Anwendung: Fundstellen und PDF-Zugänge einzeln nachprüfen, keine ungeprüften Bemessungswerte übernehmen.
