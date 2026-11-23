# Protokoll des Chats – FT-Träger-Matrix (P205 Campus Eisteiche BIG)

Stand: 23.11.2026 · Modell: claude-sonnet-5-5 · Sitzung: Claude Code (Desktop)

> Hinweis zur Herkunft: Dieses Protokoll ist eine **Zusammenfassung** der Sitzung (Arbeitsschritte, Befunde, Dateien), keine wörtliche Mitschrift. Die vollständige Rohfassung liegt lokal als Sitzungsprotokoll unter
> `C:\Users\julia\.claude\projects\G--Meine-Ablage-ZT-Gesellschaft-10-PROJEKTE-P205-Campus-Eisteiche-BIG-05-STATIK-EXCEL-JULIAN-FT-CLaude-code--RECOVERY-AutoRecover-26-02-25-26\02d7ebbc-c254-4aa2-b84b-0387c8dca486.jsonl`.
> Neu gerechnet wurde in der gesamten Sitzung nichts; alle Zahlen stammen aus gespeicherten Werten und Formeltexten. Die Quelldateien wurden nicht verändert.

## 1. Verlauf der Aufträge

| # | Auftrag (Nutzer) | Ergebnis |
|---|---|---|
| 1 | Alle Excel-Dateien, Backups, Absturz- und Verlaufsdateien der FT_Träger_Matrix vom 25.–27.02.2026 suchen, die 12 AutoRecover-Dateien in `FT_CLaude_code\_RECOVERY_AutoRecover_26_02_25-26\` sichern, analysieren und weiter zurück suchen | 12 Dateien gesichert; Bericht `_ANALYSE_AutoRecover_Bericht.md` (Abschnitte 1–8) |
| 2 | „Ja, exportieren“ | Excel-Liste der Unterschiede Linie A / Linie B (`_DIFF_LinieA_vs_LinieB_4444_Zellen.xlsx`) |
| 3 | „ok fahre fort“ | Ausgerichteter Vergleich; Verbleib von `kopie_DB (version 2)` |
| 4 | Inventar aller FT-Träger-Matrix-Workbooks (Prompt-Vorlage) | `2026-11-23_1456_claude-sonnet-5-5_FT_Träger_Matrix-WORKBOOKS[...].md`. Das eingefügte COM-Skript (Voll-Neuberechnung + SaveCopyAs) wurde **nicht** ausgeführt. |
| 5 | Inhaltlicher Vergleich Vers-B bis RevE (Aug.–Nov. 2026) in Schritten | `2026-11-23_claude-sonnet-5-5_Vergleich_Vers-B_bis_RevE_FT_Träger_Matrix.md` |
| 6 | „Ja, vergleichen“ (autorecoverte Vers-D) | Nachtrag 1 im Vergleichsbericht |
| 7 | „prüfe anhand von anderen zuverlässigen Artefakten, was richtig ist“ | Nachtrag 2: Höhenprüfung der MRd/VRd-Bezüge |
| 8 | „Ja, Reste prüfen“ + Statusmeldung (Fehleranalyse, 288 Fehler, 5 defekte Formeln) | Nachtrag 3: Reste und Fehlerursachen |
| 9 | „Ja, Liste“ | `_Fehleranalyse_Datenluecken_Vers-D_jz.xlsx` |
| 10 | GitHub-Sync nexus-platform und Protokoll ins Google Drive | dieses Dokument; Sync siehe Abschnitt 5 |

## 2. Kernbefunde

**Linien A und B (Feb. 2026).** Linie A (`26_02_09_…_kopie_DB`, `ALEX-DB-TRAINING`) und Linie B (`26_02_11`/`26_02_19` bis V5 bis Vers-B..E) sind nach zeilenweisem Abgleich über Beschriftungen in 1.385 echten Zellen verschieden (871 Zahlen, 60 Texte, 288 Beschriftungen, 162 nur in B, 4 nur in A), dazu 187 Zeilen nur in B und 49 nur in A. `kopie_DB (version 2)` ist sehr wahrscheinlich die heutige `ALEX-DB-TRAINING` (Drive-Zeit 26.02. 06:04, Sperrdatei 07:03). Welche Linie technisch gilt, ist offen.

**Reihe Vers-B bis RevE.** 20.08. (92 Blätter) → 21.08. (73 Wertänderungen, `#REF!` behoben) → Vers-B (106 Blätter, 14 neue 3OG-Blätter, `Guide_Rollout_26-03`) → Vers-C (nur `MRd!B181`) → Vers-D = RC260924 = RevE = `Vers-D_jz` (bytegleich). Die autorecoverten Vers-D-Dateien (22./23.11.) sind wertgleich zu `jz`. `Vers-DRevF` (23.11. 09:04, nicht von mir erstellt) hat 2.179 geänderte Formeln ohne gespeicherten Wert.

**Richtigkeit der Bezüge (Nachtrag 2).** Prüfmaßstab: Höhe der referenzierten `MRd`/`VRd`-Spalte muss zur Trägerhöhe (Zeile 17) passen. `MRd`: jz 145 passend, RevF 729 von 730. `VRd`: jz 544, RevF 1.428 von 1.445. 1.692 der 2.175 Formeln ändern den Wert. In `EG-2` reicht die alte Zuordnung bis `25_12_10` zurück. `RevF` ist fachlich besser, aber nicht gerechnet; Grenze der Prüfung: Typen gleicher Höhe (z. B. BT02/BT10, 80 cm) sind nicht unterscheidbar.

**Reste und Fehler (Nachtrag 3).**
- Alle 18 Rest-Bezüge in `RevF` liegen in `2OG-1` Spalte `BF` (Höhe 70, Bezug auf 77).
- Fünf direkt defekte Formeln (`#REF!` im Text): `2OG-BC Z114`, `2OG-3`/`2OG-4` BC110 und BC114. `RevF` biegt vier um, `2OG-BC Z114` bleibt defekt.
- 288 gespeicherte Fehler in `jz` (145 `#DIV/0!`, 109 `#VALUE!`, 34 `#REF!`), 170 davon Wurzelfehler. Ursachengruppen: Kopierzeilen 37/42/47 = 0 (ca. 85), `?`-Platzhalter in Eingaben (ca. 48), Division durch `--`-Text (ca. 14), leere Spalte `BD` in `4OG-D/I` (10), `EG-3` AE (3), `#REF!` in `Übersicht` (13, trifft die Gesamtmassen).
- Datenlücken-Liste: 81 Spalten mit V,Ed ≠ 0 und fehlenden Kopierzeilen, 172 `?`-Zellen.

## 3. Offene Punkte
1. `2OG-BC Z114` und `2OG-1 BF` (19 Zellen) korrigieren; Trägerzuordnung von `2OG-1 BF` klären.
2. `?`-Platzhalter und Kopierzeilen befüllen bzw. Formeln gegen Division durch 0 absichern.
3. Vollständige Neuberechnung von `RevF` in Excel (eigenes COM-Skript auf einer Kopie), danach Vergleich der Auslastungen `jz` gegen `RevF`. Auslastungen und die 105-%-Grenze sind bisher **ungeprüft**.
4. Entscheidung Linie A oder B bleibt beim Nutzer.

## 4. Ergebnisdateien (lokal, Ordner `FT_CLaude_code`)
- `_RECOVERY_AutoRecover_26_02_25-26\_ANALYSE_AutoRecover_Bericht.md`
- `_RECOVERY_AutoRecover_26_02_25-26\_DIFF_LinieA_vs_LinieB_4444_Zellen.xlsx`
- `2026-11-23_1456_claude-sonnet-5-5_FT_Träger_Matrix-WORKBOOKS[Versions.Artifacts.History.Milestones].md`
- `2026-11-23_claude-sonnet-5-5_Vergleich_Vers-B_bis_RevE_FT_Träger_Matrix.md`
- `_Fehleranalyse_Datenluecken_Vers-D_jz.xlsx`
- dieses Protokoll

## 5. Sync
- Google Drive: dieses Protokoll liegt im Ordner `FT_CLaude_code` auf `G:\Meine Ablage` (Drive-Synchronisation).
- GitHub: `julianzotter/nexus-platform` (privat), Ordner `reports/2026-11-23_FT-Traeger-Matrix_SYNC/`, als Pull Request, nicht direkt auf `main`.
