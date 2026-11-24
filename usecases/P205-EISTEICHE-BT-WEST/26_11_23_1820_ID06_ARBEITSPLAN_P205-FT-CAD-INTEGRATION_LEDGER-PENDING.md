---
tasks_erledigt: Bestandssuche (Workbooks, Dashboard, ezdxf-Code); Skill ft-cad-plan v0.1.0 gebaut + getestet (9/9); Arbeitsplan
tasks_offen: CAD-1…CAD-8 unten; Ledger-Registrierung (REGISTRATION_PENDING)
probleme: KEIN fehlerfreies Workbook vorhanden; RevF ungerechnet; Rowmap nur für Layout B belegt
offene_fragen: Q1 Master (RevF nach Rebuild?); Q2 Pos-Semantik je Layout L1–L3 aus Design_Guide_26-02; Q3 Planformat LV (A3 je Achse vs. A1 je Geschoss)
ergebnis_pruefstatus: SKILL = PILOT (synthetisch getestet); Pläne = VORABZUG; Freigabe nur ID01
name: ARBEITSPLAN_P205-FT-CAD-INTEGRATION
version: 1.0
timestamp: 2026-11-23T18:20+01:00
agent: ID06 Claude (claude-opus-5-5)
bezug: WO-20261123-P205-FT-CAD-01 (ID02, 17:46) · RPT_FTM_DASHBOARD-EZDXF-OPTIMIERUNG_20261123 · Vergleich Vers-B…RevE (sonnet, 23.11.)
---

# TL;DR
- **Fehlerfreies Workbook: existiert nicht.** Vers-B = C = D = RC260924 = RevE = jz (wertgleich): 288 gespeicherte Fehler + ~1.490 MRd/VRd-Bezüge auf falschen Trägertyp. RevF (23.11. 09:04): Bezüge überwiegend korrigiert (MRd 729/730, VRd 1.428/1.445 passend), aber **2.179 Zellen ohne Wert** → erst Excel-Rebuild.
- **Dashboard:** `26_11_23_FT_Traeger_Matrix_VersD-RevE_Dashboard_v1.1.html` (WORK) – Datenbasis = Vers-D-Werte (= RevE), d. h. η noch mit den falschen Bezügen.
- **CAD-Skill `ft-cad-plan` v0.1.0 gebaut:** xlsx → FTBeam-JSON → DXF (A3, Plankopf, η-Ampel ≤100/≤105/>105 %, Positionstabelle, Bemaßung cm) → PDF + PS → Readback-QA + Freigabe-Gate.
- **Strategie:** Geometrie/Pos aus RevE sofort plotten (Eingabezeilen, unabhängig von MRd/VRd), η erst nach RevF-Rebuild übernehmen → CAD läuft parallel zur Excel-Fehlerbehebung, nicht dahinter.

# 1 Bestand (Quelle · Stand · Bewertung)
| # | Artefakt | Stand | Bewertung |
|---|---|---|---|
| B1 | `26_11_22_FT_Träger_Matrix_26.02_Vers-DRevE.xlsx` | 22.11. | gerechnet, Bezugsfehler → **Quelle Geometrie/Pos (Pilot)** |
| B2 | `26_11_23_…_Vers-DRevF.xlsx` (_RECOVERY_AutoRecover…) | 23.11. | Bezüge korrigiert, ungerechnet → **Ziel-Master nach Rebuild** |
| B3 | `26_09_24_…_Vers-D_jz.xlsx` (FT_CLaude_code) | 22.11. | offen (Lock), = RevE |
| B4 | Dashboard v1.1 (WORK + ID03-Archiv) | 23.11. | 3D + Pyodide/ezdxf, Daten = Vers-D |
| B5 | `generate_ft_traeger_ezdxf.py` + `FT_ALL_224_RECOMMENDATIONS.json` (_INDEX/_FT-TRÄGER-MATRIX) | 20.08. | Zeilenmodell + 224-DB-Referenz → in Skill übernommen |
| B6 | Design Guide 26-02 = Blätter `Design_Guide_26-02` + `Guide_Rollout_26-03` in der 26.02-Linie | 21.08. | Regelwerk Pos.1–5 (R8 etc.) – bleibt in Excel |

# 2 Zielbild Integration
```
Excel Vers-DRevF (nach CalculateFullRebuild, Fixes D.1–D.6)
   │  read-only, SHA256
   ▼
ft-cad-plan.reader ──► FTBeam-JSON (je Blatt, Zellbezug je Wert)  ──► Dashboard v1.2 (Pyodide: gleiches Modul, beam_from_dict)
   ▼
dxfplan/sheetset ──► DXF (Layouts A3) ──► render ──► PDF (LV-Beilage) + PS
   ▼
qa.readback + gate ──► RUN_RESULT.json + RUNLOG.md ──► Ledger / ID01 Human Gate ──► Stempel FREIGEGEBEN
```
- Design Guide bleibt Rechenregel in Excel; CAD dokumentiert nur Ergebnisse (keine Bemessungslogik im Plot).
- Abdeckung: EG, 1OG, 2OG, 3OG (`*_RO260821`), 4OG; Achsgruppen ABC (Buchstaben) und 765 (Ziffern) – Zuordnung aus Blattnamen, **Annahme**, gegen `Eingabe_RFEM_ABC/_765` zu bestätigen.

# 3 Arbeitspakete (je 1 Token-Run)
| WP | Inhalt | Input | Gate (binär) | Owner | Dauer |
|---|---|---|---|---|---|
| CAD-1 | Pilot 4OG-2 auf RevE (Golden Slice lt. ID01) | B1 | Readback PASS, Plan visuell ok, Zahlen = Zellen | ID06 | 0,5 h |
| CAD-2 | Rowmap je Geschoss verifizieren (Dump Z1–260, Sp. A–G, EG…4OG) → ggf. `rowmap_<geschoss>.json` | B1 | Label-Treffer 12/12 je Geschoss | ID06 | 1 h |
| CAD-3 | Batch alle Blätter RevE → Vorabzug-Satz | B1 | 0 Readback-FAIL; Liste Datenbefunde | ID06 | 0,5 h |
| CAD-4 | Excel-Fixes D.1–D.6 (2OG-BC Z114, 2OG-1 BF, `?`-Platzhalter, Kopierzeilen 37/42/47, Z57/118, 4OG-D/I BD) | B2 | 0 #REF!, Fehler 288 → Rest dokumentiert | ID01/ID03 | 1 Tag |
| CAD-5 | RevF Rebuild (COM-Skript v1.2) + η-Vergleich jz↔RevF | B2 | Rebuild-Log, Δη-Liste, η>1,05 = Liste | ID01 + ID06 | 0,5 Tag |
| CAD-6 | Batch auf RevF-Master → Planfassung LV | CAD-5 | alle η ≤ 1,05 oder Ausnahme dokumentiert | ID06 | 0,5 h |
| CAD-7 | Dashboard v1.2: Datenexport RevF + Button „Plan“ (Pyodide, `beam_from_dict` → DXF/SVG) | CAD-6, B4 | Dashboard-DXF = Batch-DXF (Readback) | ID06/ID03 | 1 Tag |
| CAD-8 | LV-Beilage: Plansatz PDF + Massenauszug (Übersicht GESAMT nach Fix) + Peer Review ID02 | CAD-6 | ID01 `--approved-by` | ID01 | – |

# 4 Risiken
| # | Risiko | Gegenmaßnahme |
|---|---|---|
| R1 | Zeilen weichen je Geschoss ab | CAD-2, Label-Lookup + Readback |
| R2 | Pos-Werte in RevF ≠ RevE | CAD-5 Diff Z161–169 vor CAD-6 |
| R3 | Plan als „final“ missverstanden | Gate-Stempel automatisch, Freigabe nur ID01 |
| R4 | Konsolen/Trägerenden fehlen im Plan | eigenes WP nach Schemafestlegung (WO ID02 Canonical Schema) |

# 5 Ablage
- Skill: `ft-cad-plan_v0.1.0.zip` (WORK) + Kopie `…/05_STATIK/EXCEL/JULIAN/FT_CLaude_code` (manuell, kein Schreibzugriff in diesem Run auf Projektordner).
- Testplan: `P205_FT_4OG-2_TESTFIXTURE.pdf` (synthetische Daten, nur Layoutprüfung).

LOG 2026-11-23T18:20+01:00 | ID06 | Skill gebaut, 9/9 Tests, Arbeitsplan WORK | REGISTRATION_PENDING
