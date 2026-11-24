# Analyse der AutoRecover-Stände 25.–26.02.2026 – FT-Träger-Matrix

Erstellt: 23.11.2026. Nur gelesen, keine Datei verändert. Alle Zeiten sind Ortszeit (MEZ).
Verfahren: Jeder Stand wurde Zelle für Zelle (Wert und Formel) sowie auf Datensatz-Ebene (Auswahl, Ansicht, Formate) gegen die anderen Stände und gegen alle gespeicherten Varianten verglichen.

## 1. Kernergebnisse

1. **Die 10 großen AutoRecover-Stände gehören nicht zu `26_02_19_FT_Träger_Matrix.xlsx`**, sondern zu
   `EXCEL\26_02_09_FT_Träger_Matrix_jz_kopie_DB.xlsx`. Ihr Inhalt ist mit dieser Datei zellgleich,
   ergänzt um **zwei neue Blätter: `Design_Guide` und `Audit_U_4OG2`**.
2. **Zwischen 25.02. 06:51 und 26.02. 06:00 hat sich kein einziger Zellwert und keine Formel geändert.**
   Geändert wurden nur Navigation (aktive Zelle, Scrollposition), Spaltenbreiten in `Audit_U_4OG2`
   und die Breite des Add-in-Aufgabenbereichs (Claude-Add-in, rechts angedockt).
3. **Die 2 kleinen AutoRecover-Stände (1 MB)** gehören zu `KB-004-BETON-GPT\26_02_09_FT-TR-DB.xlsx`
   (9 Blätter inkl. `4OG-3`). Sie sind inhaltsgleich mit dem Original vom 09.02., es gab keine Änderungen.
4. **Es gibt zwei parallele Linien der Matrix**, die sich in **4.444 Zellen** unterscheiden
   (Übersicht, MRd, 4OG-IJ/I/D/C/4/3/2/1):
   - **Linie A, „DB-Kopie / Claude“:** `26_02_09_…_kopie_DB` → AutoRecover → `ALEX-DB-TRAINING` / `FT_Traeger_FIXED`
   - **Linie B, „Haupt“:** `26_02_11` = `26_02_19` → `26_02_26_FT_Träger_Matrix_jz` → `SEED-for-DESIGN-GUIDE` → `DesignGuide-V4/V5`
   Beispiel: Übersicht I9 hat in Linie A den Wert 2687,43, in Linie B 2576,67.
   Bewehrungsauswahl F165 lautet in A `4d(10;12;15;20;26)`, in B `4d(10;12;14;16;20;26)`.
5. **Inhalte, die nur in den AutoRecover-Dateien stehen:** Nur der genaue „Stand 0“ vor den Claude-Änderungen
   vom 26.02., also die DB-Kopie mit `Design_Guide` und `Audit_U_4OG2` im Originalzustand. Alles andere ist in gespeicherten Dateien enthalten:
   - `Design_Guide` ist identisch mit dem Blatt `Design_Guide` in `FT_Traeger_FIXED.xlsx`.
   - `Audit_U_4OG2` ist identisch mit `4OG2-Spalte-U-Audit_Seed` in `ALEX-DB-TRAINING`, `SEED-for-DESIGN-GUIDE` und `26_02_26_jz`.
   - `4OG-2` und `4OG-3` sind identisch mit der DB-Kopie vom 15.02.

## 2. Rekonstruierte Zeitleiste

| Zeit | Ereignis | Beleg |
|---|---|---|
| 09.02. 21:48 | `26_02_09_…_kopie_DB.xlsx` angelegt | Dateisystem |
| 09.02. 22:27–23:31 | `KB-004…\26_02_09_FT-TR-DB.xlsx` angelegt und gespeichert | Dateisystem |
| 11.–12.02. | Linie B: `26_02_11_FT_Träger_Matrix.xlsx`; Benchmark-Arbeiten in `KB-004…\BENCHMARK-OG4-ACHSE2` | Dateisystem |
| 15.02. 13:49 | **Letzte Speicherung** der DB-Kopie | Dateisystem, Drive |
| **17.02. 12:28** | **DB-Kopie in Excel geöffnet**, danach **nie sauber geschlossen** (Lock-Datei `~$…kopie_DB.xlsx` steht noch) | Lock-Datei, `EXCEL (3).lnk` |
| 17.02. 12:38 | Claude-in-Excel-Sitzung „Walk me through the structure of the workbook … 4OG-2“ | `KB-004…\BENCHMARK-OG4-ACHSE2\OPEN CLAUDE walk through structure of workbook.docx` |
| 17.02.–25.02. | In dieser ungespeicherten Sitzung entstehen die Blätter `Design_Guide` (Bedienungsanleitung) und `Audit_U_4OG2` (Prüfbericht Spalte U, 4OG-2) | AutoRecover |
| 19.02. 13:45 | `26_02_09_FT-TR-DB.xlsx` geöffnet, ebenfalls nie geschlossen | Lock-Datei in KB-004 |
| 19.02. 13:55 | Linie B: `26_02_19_FT_Träger_Matrix.xlsx` angelegt | Dateisystem, Lock-Datei |
| 25.02. 06:51–19:14 | AutoRecover der DB-Kopie und von FT-TR-DB; nur Navigation (aktives Blatt erst `Audit_U_4OG2`, dann `4OG-3`) | `.xar` |
| 25.02. 19:41–21:13 | Navigation in 4OG-2, 4OG-1, Design_Guide und Audit; Spaltenbreiten im Audit-Blatt geändert | `.xar` |
| 25.02. 21:11 | Linie B: `26_02_19` gespeichert (eigenes Fenster, keine Verbindung zu den `.xar`) | Dateisystem, Drive |
| 25.02. 22:55 – 26.02. 05:46 | Drei weitere AutoRecover-Stände, alle unverändert | `.xar` |
| **26.02. 06:00** | **Letzter AutoRecover-Stand.** Danach wurde Excel offenbar beendet oder ist abgestürzt | `.xar` |
| 26.02. 06:04 | Excel-Dokumentwiederherstellung legt `26_02_09_FT-TR-DB (version 1).xlsx` an; `…_ALEX-DB-TRAINING.xlsx` wird angelegt | Drive (created 05:04Z) |
| 26.02. 06:20 | **Claude.ai-Download** `FT_Traeger_FIXED.xlsx` = Stand 06:00 + 4OG-2 X163 `2d10/20 → 2d10/10` | `KB-004…\20 EC2-DESIGNKIT…` |
| 26.02. 06:38 | Excel öffnet `FT_CLaude_code\26_02_09_FT_Träger_Matrix_jz_kopie_DB (version 2).xlsx` | Excel-Registry (zuletzt verwendet) |
| 26.02. 06:45 / 06:57 | Claude.ai-Downloads `FT_Traeger_4OG2_FIXED.xlsx` / `_1.xlsx` (zusätzlich AK163 `2d10/20 → 2d10/10`, beide identisch) | Downloads, später KB-004 |
| 26.02. 07:03 | Lock-Datei für `…kopie_DB (version 2).xlsx` | Lock-Datei |
| 26.02. 06:04–23:46 | **Claude-in-Excel, Turns 1–7** in `ALEX-DB-TRAINING`; Blätter umbenannt in `*-Seed`, neues Blatt `Claude Log Seed` | Blatt `Claude Log Seed` (siehe Abschnitt 4) |
| 26.02. 09:55–09:58 | Ordner `FT_CLaude_code` befüllt; `26_02_26_FT_Träger_Matrix_jz.xlsx` aus Linie B angelegt; `FT-TR-DB (version 0)` | Dateisystem |
| 26.02. 23:49 | `FT_CLaude_code\FT_Traeger_FIXED.xlsx`: inhaltsgleich mit dem Claude.ai-Download von 06:20, in Excel neu gespeichert | Vergleich |
| 27.02. 10:20–10:33 | `26_02_26_…_jz_SEED-for-DESIGN-GUIDE.xlsx`: Linie B plus Seed-Blätter aus Linie A | Vergleich |

## 3. Navigationsverlauf in den AutoRecover-Ständen

| Stand | Aktives Blatt | Änderungen gegenüber dem vorherigen Stand |
|---|---|---|
| 25.02. 06:51 | Audit_U_4OG2 | (Ausgangsstand) |
| 25.02. 17:08 | Audit_U_4OG2 | keine |
| 25.02. 19:14 | 4OG-3 | 4OG-3: Ansicht gescrollt |
| 25.02. 19:41 | 4OG-2 | 4OG-2: Auswahl U72 → B159; 4OG-1: T68 → Y24; Design_Guide: I30 → D167; Audit: F47 → A77, Spaltenbreiten |
| 25.02. 20:50 | 4OG-3 | 4OG-3: Auswahl X8 → AK23; 4OG-2: B159 → J252 |
| 25.02. 21:13 | Design_Guide | keine (nur interne Reihenfolge) |
| 25.02. 22:55 / 23:07 / 26.02. 05:46 | Design_Guide | keine |
| 26.02. 06:00 | 4OG-2 | 4OG-2: Auswahl J252 → X8; 4OG-IJ gescrollt; Audit: A77 → A2 |

Auffällig: Um 06:00 steht die Auswahl auf **4OG-2 X8**. Genau diese Spalte X ändert Claude in Turn 1 (X163).

## 4. Claude-Protokoll (Blatt `Claude Log Seed` in `ALEX-DB-TRAINING`, alle Einträge vom 26.02.2026)

### Turn 1 (Datum 2026-02-26)
- **Anfrage:** Durchbruch-Bewehrung Pos.2 in Sheet 4OG-2, Spalte X anpassen, damit Auslastung ≤ 100%
- **Aktion:** Zelle X163 von '2d10/20' auf '2d10/10' geändert
- **Details:** Pos.2 = BÜGEL OBEN. Erforderlich: Asw,o,erf = 8.02 cm²/m. Vorher: 2d10/20 → 7.85 cm²/m → 102.1%. Nachher: 2d10/10 → 15.71 cm²/m → 51.1%. Laut Format 2d10(20;10) waren nur Abstände 20 und 10 zulässig, daher war 10 die einzige Option unter 100%.
- **Ergebnis:** Auslastung Pos.2 (X164) = 51.1% ✅. Gesamtauslastung Durchbruch (X245) = 93.2% (vorher durch Pos.2 bestimmt, jetzt maßgebend: Pos.1 = 93.2%). Alle Nachweise erfüllt.

### Turn 2 (Datum 2026-02-26)
- **Anfrage:** Sheet 4OG-3: Alle Durchbruch-Bewehrungen Pos.1-5 prüfen und anpassen, damit Auslastung ≤ 100%
- **Aktion:** 2 Zellen geändert: AK163 (2d10/20 → 2d10/10), AN165 (4d16 → 4d20)
- **Details:** 12 Durchbruch-Spalten geprüft (U, X, AA, AD, AK, AN, AR, AS, AT, AX, AZ, BD). 3 Überschreitungen gefunden: Spalte AK: Pos.2=105.9%, Druckstrebe OG=124.9% → AK163 auf '2d10/10' → Pos.2=53.0%, Druckstrebe OG=62.5%. Spalte AN: Pos.3=101.5% → AN165 auf '4d20' → Pos.3=65.0%. Alle anderen 10 Spalten waren bereits ≤100%.
- **Ergebnis:** Alle 12 Spalten jetzt ≤100%. Max. Gesamtauslastung: Spalte X = 98.5%, gefolgt von U = 94.4%, AK = 89.6%. Alle Nachweise erfüllt. ✅

### Turn 3 (Datum 2026-02-26)
- **Anfrage:** 4OG-3: Optimierung Durchbruch-Bewehrung – Zeile 110 minimieren, Auslastungen möglichst nahe 100%
- **Aktion:** Spalte AK: AK163 von '2d10/10' auf '2d10/15' geändert (Abstand 15 statt 10)
- **Details:** Optimierung von Turn 2. Spalte AK: Bügelabstand von 10→15cm erhöht Auslastungen (Pos.2: 53%→79.4%, Druckstrebe OG: 62.5%→93.7%). Spart 3.2 kg/Abschnitt (AK195: 77.7→74.5, AK110: 60.5→57.3, AK112: 124.6→121.4). Spalte AN: 4d20 bleibt, da ⌀16 nicht reicht (101.5%) und kein Zwischendurchmesser existiert.
- **Ergebnis:** AK Gesamtauslastung 93.7% (maßg. Druckstrebe OG). AN Gesamtauslastung 91.8% (maßg. Druckstrebe OG). Alle Nachweise ≤100% ✅. Zeile 110 minimiert.

### Turn 4 (Datum 2026-02-26)
- **Anfrage:** 4OG-3: Spalten AR & AS optimieren – Zeile 110 minimieren, Auslastungen nahe 100%
- **Aktion:** 4 Zellen geändert: AR165 (4d14→4d10), AR169 (4d10/10→2d10/20), AS165 (4d14→4d10), AS169 (4d10/10→2d10/20)
- **Details:** AR & AS identische Geometrie (b=40,h=65,hu=20,bd=15). Pos.1/2/4 bereits minimal. Pos.3: 4d14→4d10 (AR: 34.9%→68.5%, AS: 24.0%→47.1%). Pos.5: 4d10/10→2d10/20 (AR: 22.7%→90.9%, AS: 15.6%→62.5%). Druckstrebe UK: AR 19.7%→78.9%, AS 13.6%→54.2%. As,l,min=2.4 < 3.14 ✓.
- **Ergebnis:** AR: Zeile 110: 19.85→10.25 kg (−9.6 kg), Tonnage 70.3→60.7 kg. Gesamtauslastung 90.9%. AS: Zeile 110: 19.85→10.25 kg (−9.6 kg), Tonnage 70.3→60.7 kg. Gesamtauslastung 62.5%. Alle Nachweise ≤100% ✅

### Turn 5 (Datum 2026-02-26)
- **Anfrage:** 4OG-3: Komplette Neuoptimierung aller 12 Durchbruch-Spalten. Methode: Z.210=Z.208, dann Pos.1-5, dann Z.210 korr., dann Pos.1-5 korr.
- **Aktion:** 29 Zellen geändert. Z.210: 8× auf =Z.208 (U,X,AA,AD,AN,AT,AX,AZ,BD), AK=0.765. Pos.2: X/AA/AT/AZ=2d10/15, AK/AN=2d10/10. Pos.3: U/AD/AZ/BD=4d12, AA/AT=4d16, AX=4d10. Pos.5: U/AD/AX=2d10/15, X/AA/AT/AZ/BD=2d10/10, AN=2d10/6, AK=4d10/10.
- **Details:** Korrekte Erkenntnis: Pos.5 erf. (Z.185) hängt von Struktursteifigkeit ab, NICHT von α_210. Pos.2 erf. (Z.177=Z.228) hängt von α_210 ab. Daher: Pos.1/3/4 zuerst (unabhängig), dann α + Pos.2/5 iteriert.
- **Ergebnis:** Alle 12 Spalten ≤100%: U=97.8%, X=96.9%, AA=91.5%, AD=93.3%, AK=95.6%, AN=81.9%, AR=90.9%, AS=62.5%, AT=91.5%, AX=97.0%, AZ=96.8%, BD=76.5%. ✅

### Turn 6 (Datum 2026-02-26)
- **Anfrage:** Analyse & Systematik: Handlungsanweisung für Durchbruch-Bewehrung Optimierung entwickelt
- **Aktion:** Handlungsanweisung als MD-Datei exportiert + im persistenten Speicher abgelegt
- **Details:** 6-Schritte-Methodik: (1) Pos.1 sofort, (2) Pos.3+4 sofort (größter Gewichtshebel), (3) Pos.5 sofort (strukturell, nicht α-abhängig!), (4) α_210=α_208, (5) Pos.2 als Ausgleichsparameter, (6) Gegenprüfung. Kernerkenntnisse: erf5 unabhängig von α_210; G_Pos4 nutzt Pos.3-Durchmesser; Pos.3 ist größter Tonnage-Treiber.
- **Ergebnis:** Systematik dokumentiert und exportiert. Anwendbar auf alle Ergebnisblätter.

### Turn 7 (Datum 2026-02-26)
- **Anfrage:** Korrekturen zur Handlungsanweisung: Pos.2 (b=40→2d10/20|10, b=60→4d10/20|10), Pos.3/4 (4d8 bei Z.19<20 oder quadratisch), Pos.5 (4d10/20→/15→/10→/6, Abstand≤Z.21), Tonnage=Z.195
- **Aktion:** Design_Guide Sheet: STEP 10 (Zeilen 266–303) hinzugefügt. MD-Datei v2 exportiert.
- **Details:** Ergänzungen gemäß User: Pos.2 nur /20 oder /10 (kein /15). Pos.5 Reihenfolge 4d10/20→/15→/10→/6, bei kleinem UG (Z.21<20) bevorzugt 2d10/15 oder 2d10/10. Pos.3/4 mit 4d8 bei Z.19<20cm oder Z.19=Z.20. Tonnage in Z.195 ablesen, nicht Z.110.
- **Ergebnis:** Design Guide und persistenter Speicher aktualisiert. ✅


## 5. Rückwärtssuche: geprüfte Quellen

| Quelle | Ergebnis |
|---|---|
| Excel-AutoRecover `%APPDATA%\Microsoft\Excel` (alle Daten) | Vor dem 25.02. nur zwei irrelevante Dateien (2024, 0-Byte-Datei Dez. 2025). Weitere Serien gibt es vom **11.–16.03.2026** (22 Stände, Design-Guide-V4a/V5) und **heute 22./23.11.** (`Vers-D_jz`, Autorecovered), siehe Abschnitt 6 |
| Excel-Registry (zuletzt verwendet, Dokumentwiederherstellung) | Belege für `kopie_DB (version 2)` (26.02. 06:38) und die FIXED-Downloads. Die Dokumentwiederherstellung zeigt derzeit offene Wiederherstellungsdaten zu `26_09_24_…_Vers-D_jz` |
| Lock-Dateien `~$` | DB-Kopie seit 17.02. 12:28 offen; FT-TR-DB seit 19.02. 13:45; `26_02_19` seit 19.02. 13:55 |
| Windows-Verknüpfungen (Recent) | DB-Kopie am 15.02. 12:11 geöffnet; EXCEL-Ordner am 17.02. 12:28 |
| Google Drive (API) | Meist nur noch eine Version pro Datei, bei einigen zwei (siehe Abschnitt 8); Papierkorb leer. Zusätzlich gefunden: FIXED-Dateien in KB-004, `26_02_09_FT-TR-DB.xlsx` (Original) |
| Google-Drive-Cache (content_cache, 09.02.–05.03.) | Keine Excel-Dateien zwischengespeichert |
| Claude Code (`~/.claude`) | Keine Sitzungen vom Februar mehr vorhanden |
| Claude in Excel | Kein Speicher auf der Festplatte. Protokoll und Anleitung stehen **in den Mappen selbst** (`Claude Log Seed`, `Design_Guide`) sowie in `OPEN CLAUDE walk through structure of workbook.docx` |
| Sammlung `G:\Meine Ablage\AI-CODEBASE\EXCEL CLAUDE DESIGN GUIDE\EXCEL-CHRONOLOGIE-SAMMLUNG` (09.07.) | Kopien der gespeicherten Februar-/März-Stände; kein zusätzlicher Inhalt gegenüber dem Projektordner |

## 6. Offene Punkte

- ~~`…kopie_DB (version 2).xlsx` verschwunden~~ → geklärt in Abschnitt 8: Sie ist sehr wahrscheinlich die heutige `ALEX-DB-TRAINING`.
- Wann genau `Design_Guide` und `Audit_U_4OG2` angelegt wurden, ist nur eingrenzbar: zwischen 17.02. 12:28 und 25.02. 06:51. Ältere AutoRecover-Stände dieser Sitzung existieren nicht mehr.
- Die beiden Linien A und B wurden nie zusammengeführt. Nach Zeilenabgleich bleiben 1.385 echte Zelländerungen (Abschnitt 7). Welche Linie fachlich gültig ist, muss geprüft werden.
- Hinweis zu heute: Excel hält Wiederherstellungsdateien für `26_09_24_FT_Träger_Matrix_26.02_Vers-D_jz` (22.11. 20:56 bis 23.11. 02:52). Falls Excel seitdem abgestürzt ist: Diese Dateien liegen in `%APPDATA%\Microsoft\Excel\`.

## 7. Linie A gegen Linie B, bereinigt (Nachtrag 23.11.2026)

Datei: `_DIFF_LinieA_vs_LinieB_4444_Zellen.xlsx` in diesem Ordner. Linie A ist `26_02_09_…_kopie_DB.xlsx` (zellgleich mit AutoRecover 26.02. 06:00), Linie B ist `26_02_19_FT_Träger_Matrix.xlsx`.

- **Die 4.444 Zellen überzeichnen den Unterschied.** Der Vergleich nach Zelladresse zählt verschobene Zeilen doppelt. In allen 4OG-Blättern wurde in Linie B der **Durchbruch-Block ab Zeile ~171 umgebaut**: Tonnage und Kubatur nach oben, neue Zwischenwerte (Trägheitsmomente, Hebelarme, Schubspannungen), Querkraftaufteilung mit `α_u_gew / α_u_reg / α_o_reg / α_o_gew`, GESAMTAUSLASTUNG jetzt in Zeile 252 statt 245.
- **Nach Zuordnung der Zeilen über ihre Beschriftung** (Spalte D/E) bleiben **1.385 echte Zelländerungen**: 871 Zahlen, 60 Texte, 288 Beschriftungen, 162 Werte nur in B und 4 nur in A. Dazu kommen **187 Zeilen nur in B** (neue Rechenzeilen) und **49 nur in A**. Ohne Unterschied sind alle EG-, 1OG-, 2OG- und 3OG-Blätter, Eingabe_RFEM, VRd*, Read_me; Unterschiede gibt es nur in Übersicht, MRd und den 4OG-Blättern.
- **Fachlich relevante Beispiele (4OG-3):**
  - Pos.5 BÜGEL UNTEN (Zeile 169): A `4d10/10`, B `4d10/20`.
  - Querkraft OG im Durchbruch (V_o_db): A z. B. U = 92,5 kN, B 86,8 kN; X: A 81, B 126,7 kN. Die Querkraftaufteilung wird anders berechnet.
  - GESAMTAUSLASTUNG Durchbruch: Linie A hat **AK = 1,249** und **AN = 1,015**, also über 1,0. Linie B hat AK = 0,9996 und AN = 0,918. Genau diese Überschreitungen hat Claude am 26.02. in Linie A behoben (Protokoll Turn 2: AK163 `2d10/20→2d10/10`, AN165 `4d16→4d20`).
  - In Linie A steht in 4OG-3 T177/T185 eine Formel als Text (`(U159*(0,25+0,2*…`), eine Arbeitsnotiz.
- Blätter in der Datei: `Zusammenfassung`, `Differenzen` (alle 4.444, nach Adresse), `Abgleich_bereinigt` (1.385, mit Zeile A und Zeile B), `Zeilen_nur_A_oder_B` (236). Die Formelspalten berechnet Excel beim Öffnen.

## 8. Verbleib von `kopie_DB (version 2).xlsx` (Nachtrag 23.11.2026)

Ergebnis: Die Datei ist **sehr wahrscheinlich nicht verloren, sondern umbenannt zu `26_02_26_FT_Träger_Matrix_ALEX-DB-TRAINING.xlsx`.**

| Zeit 26.02. | Beleg | Quelle |
|---|---|---|
| 06:00 | letzter AutoRecover-Stand der DB-Kopie, danach Excel beendet/abgestürzt | AutoRecover |
| 06:03:56 | Ordner `EXCEL\FT_CLaude_code` neu angelegt | Drive `createdTime` |
| **06:04:14** | **erste Datei im neuen Ordner angelegt: heute `ALEX-DB-TRAINING`** | Drive `createdTime` (bleibt bei Umbenennung erhalten) |
| 06:04:57 | `26_02_09_FT-TR-DB (version 1).xlsx` von der Excel-Dokumentwiederherstellung gespeichert | Drive `createdTime` |
| 06:38 | Excel öffnet `FT_CLaude_code\…kopie_DB (version 2).xlsx` | Registry (zuletzt verwendet) |
| 07:03:45 | Lock-Datei `~$…kopie_DB (version 2).xlsx` im Ordner | Dateisystem |
| 23:46 | `ALEX-DB-TRAINING` zuletzt gespeichert, enthält das Claude-Protokoll vom 26.02. | Datei |

Begründung: Excel benennt wiederhergestellte Mappen „(version 1)“, „(version 2)“. Beide Mappen, die beim Absturz offen waren, wurden um 06:04 gesichert. Für die FT-TR-DB blieb der Name erhalten. In Google Drive gibt es **keine** Datei mit „kopie_DB (version 2)“ im Namen, auch nicht im Papierkorb. Die einzige Datei, die zu diesem Zeitpunkt im Ordner entstand, ist `ALEX-DB-TRAINING`. Inhaltlich ist sie die DB-Kopie (Autor Alexander Litschauer, gleiche Blätter, Linie A) plus die Claude-Änderungen vom 26.02. Einen Beweis per Dateiverlauf gibt es nicht, da Drive Umbenennungen nicht in den Metadaten zeigt.

Zusätzlich: `FT_CLaude_code\FT_Traeger_FIXED.xlsx` (5,70 MB, in Excel gespeichert 26.02. 23:49) ist inhaltlich der AutoRecover-Stand 06:00 plus nur die Änderung 4OG-2 X163 `2d10/20→2d10/10`. Er entspricht dem Claude.ai-Download von 06:20 (4,95 MB, ohne Excel-Speicherung).

### Parallelordner `_RECOVERY_DriveVersionen_26_02-03`

Seit 22.11. abends existiert neben diesem Ordner `…\FT_CLaude_code\_RECOVERY_DriveVersionen_26_02-03` mit 34 heruntergeladenen Drive-Versionen (09.02. bis 25.03.) und einem Claude-in-Excel-Verlauf (`Claude-Excel-Verlauf_Feb-Maerz-2026.md`, `…Log….csv`, 73 Runden in den Sitzungen 0 und A bis D). Er stammt nicht aus dieser Analyse. Er bestätigt sie aber: Sitzung 0 (17.02.) nennt für 4OG-2 kritische Werte X245 = 1,021 und AK245 = 1,016, und das Session-Logging war vor dem 26.02. aus.
