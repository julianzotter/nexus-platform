---
name: ft-cad-plan
description: P205 Eisteiche FT-Träger-Matrix (xlsx) → ezdxf-DXF-Plan A3 → PDF/PostScript mit η-Ampel, Positionstabelle, Halb-FT-Querschnitt, Readback-QA und Freigabe-Gate; für LV-Hochbau-Beilagen EG–4OG.
version: 0.2.0
status: PILOT – 9/9 pytest; Vollauf Vers-DRevE 92 Blätter, 0 Readback-FAIL, 23.11.2026
timestamp: 2026-11-23T18:25+01:00
agent: ID06 Claude
---

# Wann
- Halb-FT-/FT-Träger-Pläne (Durchbruch-/Bewehrungsschema) aus der FT-Matrix: Einzelblatt, Geschoss, alle.
- Vorabzüge LV-Hochbau; Freigabe nur über Gate.

# Harte Regeln
1. Quelle read-only (openpyxl data_only). Nie in die Mappe schreiben.
2. Keine erfundene Bewehrungsgeometrie: Pos.1–5 nur Text/Tabelle; Katalogfehler (z. B. 4d23) mit (!).
3. Jede Zahl mit Zellbezug (JSON `cells`) + SHA256 der Quelle im Plankopf.
4. Gate binär: FREIGEGEBEN nur bei allen η ≤ 1,05 (GESAMTAUSLASTUNG), 0 Befunden, `--approved-by ID01`.
5. RevF/Skript-Mappen ohne Werte → η FEHLT → zuerst Excel CalculateFullRebuild.

# Ablauf
```
pip install ezdxf matplotlib openpyxl
python -m pytest -q tests
python run_ft_cad.py <MATRIX.xlsx> --sheets 4OG-2 --out OUT     # Pilot
python run_ft_cad.py <MATRIX.xlsx> --all --out OUT              # 92 Blätter ≈ 3 min
```
Output: `<sheet>_FTBeam.json`, `P205_FT_<sheet>.dxf` (Layouts `BlattN_<Achse–Achse>`), `.pdf`, `_BlattN_*.ps`, `RUN_RESULT.json`, `RUNLOG.md` (append).

# Zeilenmodell (verifiziert RevE, 92/92 Blätter)
| Feld | Quelle |
|---|---|
| Station x [m] | Z10 (Raster 1,35 m, ab Spalte G) |
| Achsen | Z12: Buchstaben (765-Blätter) bzw. Zahlen 7…1 (ABC-Blätter) |
| Konsole | Label „Konsole (1…links; 2…rechts)“ (Z15) |
| b, h, h1 (Vergussfuge) | Z16, Z17, Z18 |
| DB b,d / h,d / h,u,d | Z19 / Z20 / Z21 |
| Pos.1–5 | Labels „Pos.N“ Spalte A (Z161–169); Nachweis = Zeile +1 |
| η | Label GESAMTAUSLASTUNG (Z245/252/156); fehlt → η* = max(Pos-Nachweis) |
| BT-Katalog | MRd Z9 Name, Z11–16: b, h, h1, bi (Breite Vergussfuge), c, d_bü |

# Planinhalt je A3-Blatt
- Übersicht ganzer Träger (Annotationen im Viewport eingefroren), Detail 2 Felder (nur Felder mit DB), einheitlicher Detailmaßstab je Blatt.
- FT-Elemente getrennt an Stationen mit h = 0; Fugenlinie h − h1 (Ortbeton); Achsen + Auflager; Konsolen „K“.
- Durchbrüche, Maß h_u, Maß Achse → DB-Mitte, η-Ampel (≤100 / ≤105 / >105 %).
- Positionstabelle, Querschnitte 1:20 (Vergussfuge bi × h1 schraffiert; bi mehrdeutig → „Fuge ?“), Plankopf, Gate-Gründe.

# Grenzen
- 3OG: Blätter `3OG-x` und `3OG-x_RO260821` werden beide geplottet → ID01 wählt (Rollout = neuer).
- Keine Stablängen/Biegeformen, keine Konsolengeometrie, keine IFC (eigene WO).
- Fugenbreite bei 40/80/15 mehrdeutig (BT02/04a/10 = 24, BT21 = 32).
