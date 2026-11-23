---
tasks: erledigt = 0 | offen = 14 Schritte (S00-S13), alle NOT_RUN
probleme: G3 offen; 32 RFEM-Werte fehlen; ID03, ID04 und 6 weitere LLMs ohne Capability-Beleg
offene_fragen: S04-Entscheide ID01 (E1.1-E1.4, RevF, 105 %)
ergebnis_pruefstatus: Plan, nicht ausgefuehrt; Token-Budgets = Planwerte, nicht gemessen
timestamp: 2026-11-23T11:15+01:00
name: 26_11_23_1115_ID06_WO_P205-FT_NEXUS-WORKFLOW_v2.0_LEDGER-PENDING
description: NEXUS-AI-AEC Workflow v2.0 fuer P205 FT-Traeger - schrittweise CoT-Kette, 1 Ziel je Run, Token-Budget je Schritt, Multiagent ueber Dateien
version: 2.0
status: PROPOSED / ID01-FREIGABE OFFEN
agent_id: ID06 (laut ID01-Auftrag im Chat 23.11. 11:01)
basis: "26_11_23_1115_ID06_P205-FT_META-PEERREVIEW_MOE-SEM_LEDGER-PENDING.md"
registration_status: REGISTRATION_PENDING
engineering_release: BLOCKED
---
# WO P205 FT-Traeger - NEXUS-Workflow v2.0

## 0 Regeln (kurz)
- R1 nichts loeschen, keine E-Mails. R2 Ergebnis archivieren + berichten. R3 Statuszettel fortschreiben (AGBs 8).
- 1 Run = 1 Schritt = 1 Ausgabedatei. Kein Schritt ohne ACK-Datei. Autor ist nie Reviewer (AGBs 10).
- Status nur: NOT_RUN | RUN_OK | RUN_FAIL | BLOCKED. Kein simulierter Lauf, keine Erfolgsaussage ohne Datei + SHA-256.

## 1 Dateiname = Kollisionsschutz
- `YY_MM_DD_HHMM_ID##_THEMA.md` (Europe/Vienna). Jeder Agent schreibt nur Dateien mit eigener ID, aendert keine fremden.
- ACK: `YY_MM_DD_HHMM_ID##_ACK_S##.md`. Ergebnis: `..._ID##_P205-FT_S##_<TITEL>.md`. Review: `..._ID##_REVIEW_S##.md`.
- Schritt gilt als belegt, wenn Ergebnis- und Review-Datei verschiedener IDs existieren.

## 2 Token-Kontrolle (True-Run)
- T1 Pre-Parse: vor jedem Run Umfang zaehlen (Blaetter, Zellen, Dateigroesse). Passt es nicht ins Budget -> teilen, nicht kuerzen.
- T2 Kontext je Run: _AGBS.md + diese WO + STATUS + genau die Eingabedatei des Schritts. Keine Berichtshistorie.
- T3 Einheit: 1 Achsblatt oder 1 Befundklasse je Run.
- T4 Ausgabe: Daten als CSV/JSON-Datei, im Bericht nur Zaehler + Pfad + Hash.
- T5 Budget ueberschritten -> RUN_FAIL melden, Rest als neuer Schritt S##b.
- T6 CoT-Kette je Run: Eingabe-Hash -> Regel -> Rechnung/Scan -> Kontrolle (Summe, Einheit) -> Ergebnis -> Delta zum Vorlauf.
- T7 Budget-Summe Plan: Eingabe 247k, Ausgabe 25.5k Tokens (S10 je Achsblatt, ohne Wiederholungen).

## 3 Schritte
| ID | Schritt | Ausfuehrung | Review | Ausgabe | Tok ein k | Tok aus k | Gate | braucht | Spur |
|---|---|---|---|---|---|---|---|---|---|
| S00 | Bootstrap: _AGBS.md + diese WO + STATUS lesen, ACK-Datei schreiben | jeder Agent | - | ACK-Datei | 12 | 0.5 | - | - | alle |
| S01 | Nativer Excel-Recalc Vers-D mit v1.2-Skript ALS DATEI | ID01 lokal | ID02 | xlsx + json + errors.csv | 0 | 0 | G3 | - | A |
| S02 | Persisted-Cache-Verifier auf S01-Ausgabe; Fehler-/Luecken-Zaehlung mit 1 Definition | ID02 | ID06 | report.json + Kurzbericht | 20 | 2 | G4 | S01 | A |
| S03 | RFEM-Export 1OG-J/2OG-J: 32 Werte mit Modellrevision, Stab, x, LK | ID01 / Alex | ID06 | CSV | 0 | 0 | L01 | - | B |
| S04 | Entscheide schriftlich: E1.1 Toleranz/105 %, E1.2 alpha 4OG-2 AK, E1.3 Lage 4OG-2 BD, E1.4 Top-4, RevF verwerfen/behalten | ID01 | - | DECISION-Datei | 0 | 0 | Human Gate | - | C |
| S05 | Querschnittsliste 40 Schnittspalten (EG-F, 2OG-1) + 4 Typen ohne Katalog: b/h/h1/BT aus XLSX vs. Schalplan | ID06 (Liste) / ID01 (Entscheid) | ID02 | CSV, 1 Blatt je Run | 30 | 3 | L02-L04 | - | D |
| S06 | Pilot 4OG-2 Zell-Audit per Label-Lookup inkl. Selektor- und Nachbarspalten-Pruefung | ID06 | ID02 | Audit-CSV + Patchliste | 40 | 4 | - | S01 | A |
| S07 | Pilot-Patch in Kopie + nativer Recalc (Verfahren S01, kein LibreOffice) | ID06 Patch / ID01 Lauf | ID02 | xlsx + json | 30 | 3 | G3-Pilot | S04,S06 | A |
| S08 | Unabhaengige Handrechnung 1 Schnitt 4OG-2 (M, V, Fuge) mit OENORM EN 1992-1-1 + B 1992-1-1 | ID03 oder DeepSeek (Upload durch ID01) | ID06 | Rechenblatt MD | 15 | 3 | G5-Pilot | S07 | A |
| S09 | Pilot-Abnahme binaer (Delta S08 vs. S07 je Messgroesse) | ID01 | - | DECISION-Datei | 0 | 0 | G6-Pilot | S08 | A |
| S10 | Rollout 3OG -> 2OG -> 1OG -> EG, 1 Achsblatt je Run, Regression je Blatt | ID06 | ID02 | Patchliste + eta-/Fehler-Bilanz | 40 | 4 | - | S09,S03,S05 | A |
| S11 | Uebersicht reparieren, Mengen, LV LG16/LG07/LG36 | ID02 | ID06 | Mengen-CSV | 30 | 3 | - | S10 | A |
| S12 | DXF-/Plot-Pilot 4OG-2, dann Serie | ID06 | ID02 | DXF + A2-PDF | 30 | 3 | - | S09 | E |
| S13 | ZT-Freigabe Statik + Plaene + LV in 1 Revisionsstand | ID01 | extern | Freigabe | 0 | 0 | G6 | S11,S12 | A |

- Parallel ab sofort: Spur A (S01), B (S03), C (S04), D (S05). Spur E erst nach S09.
- S08: Ausfuehrender darf nicht der Patch-Autor aus S07 sein.

## 4 S01 exakt (behebt den Abbruch 23.11. 11:01)
- Ursache: Skript wurde in die Konsole eingefuegt. `param` fragte nach `InputXlsx`, die Folgezeilen gingen verloren, `$source` (Skriptzeile 68) blieb leer.
- v1.1 aus dem ZIP nicht verwenden (setzt Calculation vor Workbooks.Open). Datei `P205_FT_Excel_Native_Recalc_v1_2_REVIEW_CANDIDATE.ps1` liegt im FT-Ordner. Status UNTESTED.
```powershell
cd "G:\Meine Ablage\ZT-Gesellschaft\10_PROJEKTE\P205_Campus_Eisteiche_BIG\05_STATIK\EXCEL\JULIAN\FT_CLaude_code\P205_FT_PEER_REVIEW_REFINEMENT_2026-11-23_v1_1"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\P205_FT_Excel_Native_Recalc_v1_2_REVIEW_CANDIDATE.ps1" -InputXlsx "<PFAD>\Vers-D.xlsx" -OutputDirectory "C:\NEXUS\P205\native-results"
```
- `<PFAD>`: lokale Kopie der Vers-D (gdrive:1knpaqjyO33E1eZzI0PFVxzSZrTpdRJdc). Skript stoppt bei falschem SHA-256.
- Erwartet: xlsx + json + errors.csv. Laufzeitgrenze im Skript 15 min. Ergebnis-JSON nach WORK kopieren.
- Bei Fehler: Meldung in `_TROUBLESHOOTING.md` nachsehen, dann ID06 fragen (AGBs 8a).

## 5 Kontroll-Panel (Board)
| ID | Agent | belegte Faehigkeit | Status | naechster Schritt |
|---|---|---|---|---|
| ID01 | Julian (Human) | Entscheid, lokales Windows/Excel/RFEM | BELEGT | S01, S03, S04 |
| ID02 | ChatGPT Private / Codex | Python-OOXML-Audit, Drive-Write; kein Excel (Linux) | BELEGT 23.11. | Review S01, dann S02 |
| ID03 | ChatGPT Assistant / Peer Reviewer | Ordner mit Kopien 09:41; kein eigener Bericht gelesen | UNBELEGT | S00-ACK, dann S08 |
| ID04 | Gemini | kein Artefakt in den gelesenen Quellen | UNBELEGT | S00-ACK + Capability-Beleg |
| ID06 | Claude (Chat/Cowork/Code) | Drive: neue Dateien; openpyxl; GitHub-Push siehe Bericht; kein Excel | BELEGT 23.11. | S05-Liste, S06 |
| DS | DeepSeek | nur Chattext/Upload, max. 15 Textdateien (AGBs 2.6) | LAUT AGBs | S08 Variante B (Upload ID01) |
| XX | Perplexity, Kimi, Qwen, Gemma, Meta AI, Ollama | kein Beleg in den gelesenen Quellen | UNBELEGT -> Capability-Audit zuerst | kein Auftrag vor Beleg |
- Laufender Stand: Cloud-LLMs melden sich nur, wenn sie laufen. 10-30-s-Takt geht nur lokal:
```powershell
while ($true) { Clear-Host; Get-Date; Get-ChildItem "G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\WORK" -File | Sort-Object LastWriteTime -Descending | Select-Object -First 15 LastWriteTime, Name | Format-Table -AutoSize; Start-Sleep 30 }
```
- Pfad WORK auf G: = Annahme aus AGBs 5, nicht geprueft. Zeigt, welche ID zuletzt welche Datei schrieb.

## LOG
- 2026-11-23T11:15+01:00 | ID06 Claude | Workflow v2.0 angelegt, 14 Schritte NOT_RUN | PROPOSED
- Protokoll je Schritt: Ergebnisdatei in WORK + 1 Zeile RUNLOG_APPEND + STATUS_FTM_PILOT-4OG2.md.
