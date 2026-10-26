---
name: wo-nexus-kg-leitfaden-feedback
version: v0.1
status: OPEN
timestamp: 2026-10-26T12:40+01:00
agent_id: ID-06
hash: sha256:a76a9b28f6d4c55c21173a6c2f23d875f4275e2a2f6c362bbe666b731f33173f (Body vor Hash-Eintrag)
gate: PENDING
ticket_id: WO-20261026-KGLEIT-01
owner_id: ID-01
executor: ID-02, ID-03, ID-04, ID-05, ID-07, ID-08
reviewer_instance: ID-06 (Konsolidierung)
role_register_version: NEXUS-ROLES_v1.0
---

# WORK-ORDER — Feedback zu WHITE PAPER NEXUS-KG-LEITFADEN v0.1
Orchestrierung für dieses Ticket: ID-06 (durch ID-01 zugewiesen; Abweichung Register ID-02 vermerkt).

## 1 Gegenstand
- Datei: `26_10_26_12_35_ID-06_WHITEPAPER_NEXUS-KG-LEITFADEN_v0.1.md` (WORK, Drive-ID 1AhSCkG73Dnu7CArWRyrgPC9DVFBd2_it)
- Inhalt: Label-Hierarchie L0–L8 (Technik), R0–R5 (Recht), Schnittmenge `BINDING`, Pydantic-Chunk-Schema, Mapping-Layer IFC/bSDD/ISO 12006, Pipeline, Linkliste #01–#20
- Ziel: Freigabe-reife v1.0 als verbindlicher Leitfaden für alle LLM-Rollen

## 2 Statusmodell
OPEN → CLAIMED → RUNNING → DONE | BLOCKED | REVIEW_REQUIRED | FAILED

## 3 Teilaufgaben + Acceptance
| Rolle | Aufgabe | Acceptance |
|---|---|---|
| ID-02 | Struktur-Review: Hierarchie L0–L8 vollständig/überschneidungsfrei? Synthese-Vorschlag | je Ebene OK/ÄNDERN + Begründung |
| ID-03 | QA Schema §4: Pydantic-Felder, Validierungsregeln, 3 Golden-Chunks (EC2 §, EC5 §, OIB-RL) als JSON | 3 valide JSON-Beispiele |
| ID-04 | Protokoll/Evidence: Links #01–#20 prüfen (erreichbar, Primärquelle, Ausgabe) | Tabelle NR/Status/Korrektur |
| ID-05 | Recherche: ISO 12006-2/-3, bSDD, IDS Mapping-Regeln mit Primärbeleg; Widersprüche zu §5 | ≥2 Belege je Mapping-Zeile |
| ID-07 | Falsifikation: 3 Testfälle, die die Technik/Recht-Trennung brechen (z.B. OIB-NDP, Landesrecht-Abweichung, Produktnorm/ETA) | je Fall: bricht/bricht nicht + Fix |
| ID-08 | lokal: Taxonomie-JSON-Entwurf v0.1 aus §2/§3 + SQLite-Registry-DDL | Datei + DDL lauffähig |

## 4 Rücklauf
- Dateiname: `26_10_DD_HH_mm_ID-<ROLLE>_RESULT_WO-NEXUS-KG-LEITFADEN_v0.1.md`
- Ablage: WORK (1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP)
- Pflicht: CLAIM-Block (Empfangsbestätigung vor Beginn) + RESULT-Block (findings, evidence, artifacts, risks, next_action, qa_status)
- Token-Budget je Rückmeldung ≤ 1.500; Quelle Pflicht oder `unbelegt`

## 5 Fristen / Konsolidierung
- Deadline: 2026-10-28 12:00 CET
- Konsolidierung → v1.0: ID-06; Kreuz-Review: ID-03 reviewt ID-06-Konsolidat
- Freigabe ausschließlich ID-01 (REVIEWED ≠ APPROVED)

## 6 Bekannte Lücken (nicht als Finding wiederholen)
- L1 Manifest-PDF nicht extrahierbar (>10 MB) → ID-01 liefert Textfassung
- L2 Taxonomie-JSON fehlt (→ ID-08)
- L3 EN 1990 Glossar-Run offen
- L4 Links #05/#19 Unterseite unverifiziert (→ ID-04)
- L5 Mapping-Tabellen leer (→ ID-05)

## 7 Regeln
R1 keine Mails/kein Löschen · R2 archivieren + Report · R3 Statuszettel-Frontmatter · keine Produktnamen, nur Rollen-IDs

## LOG
- 2026-10-26 12:40 ID-06: WO erstellt; WORK; Ledger-ID PENDING; RUNLOG nicht fortgeschrieben
