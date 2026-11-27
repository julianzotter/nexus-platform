---
tasks_erledigt: T1–T6 (Bestandssuche, Workbook-Befund, Skill ft-cad-plan v0.1.0, Arbeitsplan, 3 Uploads WORK, Skill im Konto)
tasks_offen: T7–T14 (Pilot echte Daten, Halb-FT/Aufbeton-Schnitt, Batch EG–4OG, Projektordner-Kopie, GitHub-PR, Ledger, RUNLOG, SQE/FAV250-Übertrag)
probleme: kein fehlerfreies Workbook; RevF ungerechnet; Rowmap nur Layout B belegt; Ledger-Schreibrecht nur designierter Writer
offene_fragen: Q1 Master RevF nach Rebuild?; Q2 Planformat LV (A3/Achse vs. A1/Geschoss); Q3 Scope FAV250/SQE (FT-Träger ja/nein)
ergebnis_pruefstatus: WRITTEN; Uploads Größen-Readback OK; fachlich VORABZUG, Freigabe ID01
name: STATUS-QUICKTASK-MATRIX+REFLIST+ROADMAP_P205-FT-CAD
version: 1.0
timestamp: 2026-11-23T18:10+01:00
agent: ID06 Claude (claude-opus-5-5, claude.ai mobile + Drive-Connector + Desktop-Bridge)
chat_start: 2026-11-23T17:55+01:00
registration_status: REGISTRATION_PENDING
---

# 0 Antwort ID01
- Chat-Datum: **23.11.2026, Start 17:55** (Europe/Vienna). Parallel-Chat (Bericht `…_1758_ID-UNVERIFIED_STATUS…`): 31.10.–23.11.
- Gesichert? **Teilweise.** Drive WORK ✅ (3 Dateien, Größe = lokal). Skill im Claude-Konto ✅. GitHub ❌, Ledger ❌ (PENDING), Projektordner-Kopie ❌, RUNLOG/Statuszettel ❌ → WO-S1…S4.

# 1 QUICK-TASK-COMPLETION-MATRIX
| # | Task | Ergebnis | Status | Beleg |
|---|---|---|---|---|
| T1 | Workbook-Lineage | 401 Dateien inventarisiert (fremd, 15:27); RevE=jz, RevF besser/ungerechnet | DONE | #05 #06 |
| T2 | „Fehlerfreies“ Workbook | existiert nicht; Wahl RevE (Geo/Pos) + RevF (η nach Rebuild) | DONE (Befund) | #06 |
| T3 | Dashboard | VersD-RevE v1.1 (Daten = Vers-D) | DONE | #07 |
| T4 | Skill ft-cad-plan v0.1.0 | 6 Module, 9/9 pytest (synthetisch) | DONE | #02 |
| T5 | Arbeitsplan CAD-1…8 | WORK | DONE | #01 |
| T6 | Testplan PDF | Layout ok, Daten synthetisch | DONE | #03 |
| T7 | Pilot 4OG-2 echte Daten | – | IN ARBEIT | – |
| T8 | Halb-FT + Aufbeton/Vergussfuge-Schnitt (MRd Z9–14) | – | OFFEN | – |
| T9 | Vorabzug-Satz EG–4OG (ABC/765) | – | OFFEN | – |
| T10 | Kopie Projektordner FT_CLaude_code | Ordner freigegeben 18:08 | OFFEN | – |
| T11 | GitHub-Sicherung (Branch + PR) | – | OFFEN | – |
| T12 | Ledger/Register | REGISTRATION_PENDING | BLOCKED (Writer) | #10 |
| T13 | RUNLOG + Statuszettel | – | OFFEN | – |
| T14 | Übertrag SQE Eibengasse / W017 FAV250 | Scope offen | OFFEN | – |

# 2 REFERENZLISTE (#NR, NAME, URL)
#01, Arbeitsplan, https://drive.google.com/file/d/19Xe3AcC0F90hWq9xZ41yCkoesVJzvCAj/view
#02, Skill-Zip, https://drive.google.com/file/d/1GEXWvoTqP9WYZHp45o-so01gUfrMcPHu/view
#03, Testplan PDF, https://drive.google.com/file/d/1eo1p69Dtwja_cS_K7TJ0oC506BOi7Eo3/view
#04, Inventar WB, https://drive.google.com/file/d/1bVvdVizc6XrPqs79ao2PI6B1LixcwdzL/view
#05, RevE xlsx, https://drive.google.com/file/d/1oVj79Li7EiYxo2SnrvgtNGzbF3tmqbiQ/view
#06, Vergleich B–F, https://drive.google.com/file/d/1BehSB92ErttOItiwz5upaqoBf0I2xvno/view
#07, Dashboard v1.1, https://drive.google.com/file/d/1eSOB7LU5rQKGJuCfIPevlKYjuXSecErb/view
#08, RevF xlsx, https://drive.google.com/file/d/1BPpKIENzRPrCu0qhdn34YuErKzMZ8oyy/view
#09, WO-P205-FT-CAD, https://docs.google.com/document/d/1vsVT-_kf6n_WlUyjUH0OakSJSDmxGyZ3qLGB4noQl_U/edit
#10, Register jsonl, https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view
#11, ezdxf-Altcode, https://drive.google.com/file/d/1hHEDDxnCdSaY6ciwkrHDZ3pZrzdAvlxR/view
#12, 224-DB JSON, https://drive.google.com/file/d/1uvietO5C1kGFDRffnRuvXh4QMKuiGTWN/view
#13, ec2_designkit, https://drive.google.com/file/d/1ia9fuALDC1kzzofzu4EcHp2YcUPIfOJC/view
#14, RPT ezdxf-Opt, https://drive.google.com/file/d/19Yp_2ZFHS1E5UJjODVVZ0FlmhQ6auv15/view
#15, Fehlersuche docx, https://drive.google.com/file/d/1kKEPTRzPf18fySMmA5XTV9pv_O-YxRFl/view
#16, Status 1758 (ID?), https://drive.google.com/file/d/17jKm_g0JUjOP1CNSYC07m8lMI2e2ZI0e/view
#17, WORK-Ordner, https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP

# 3 ROADMAP AI-CAD-FEM (je Stufe 1 True-Run, binäres Gate)
| Stufe | Ziel | Gate | MoE-Route |
|---|---|---|---|
| R0 | Sicherung Drive/Projektordner/GitHub/Ledger | Readback Größe+SHA = lokal | Sonnet low |
| R1 | Pilot 4OG-2 echte Mappe (RevE) | Readback PASS, Zellen = Plan | Opus mid |
| R2 | Rowmap EG–4OG + BT-Katalog (MRd Z9–14) | 12/12 Labels je Geschoss | Sonnet mid |
| R3 | Halb-FT/Aufbeton-Querschnitt + Batch-Vorabzug | 0 Readback-FAIL | Opus mid |
| R4 | Excel-Fixes D.1–D.6 + RevF-Rebuild | 0 #REF!, Δη-Liste | ID01 Excel + Opus high Review |
| R5 | LV-Planfassung aus RevF + Massen GESAMT | η ≤ 1,05 oder Ausnahme | Opus high |
| R6 | IFC/GLB aus FTBeam-JSON (WO ID02) | IfcOpenShell-Validator | Codex/ID02 |
| R7 | FEM-Slice (PyNite/RFEM), ΣV=0, ΣM=0 | Δ Reaktion < 2 % | Opus high |
| R8 | Übertrag SQE Eibengasse / W017 FAV250 | Scope ID01 | – |

# 4 WORK-ORDERS Sicherung (REVIEW_PENDING)
- **WO-S1 Projektordner-Kopie**: Skill + Pläne → `05_STATIK/EXCEL/JULIAN/FT_CLaude_code/CAD/` · Owner ID06 · Gate Readback.
- **WO-S2 GitHub**: Branch `id06/p205-ft-cad-plan`, PR mit Skill + Tests · Owner ID06 · Gate CI/pytest grün, Merge ID01.
- **WO-S3 Ledger**: Einträge für #01–#03 + dieser Bericht · Owner designierter Ledger-Writer · Gate Counter-Nr. vergeben.
- **WO-S4 RUNLOG/Statuszettel**: append-only Zeilen je Lauf · Owner ID06 · Gate Zeile vorhanden.

LOG 2026-11-23T18:10+01:00 | ID06 | Statusbericht WORK | REGISTRATION_PENDING
