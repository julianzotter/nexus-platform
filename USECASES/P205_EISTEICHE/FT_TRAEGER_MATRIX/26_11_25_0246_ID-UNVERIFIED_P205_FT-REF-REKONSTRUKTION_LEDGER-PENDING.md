# P205 FT-Traeger-Matrix - Rekonstruktion der 5 #REF!-Formeln

Stand: 2026-11-25 | Quelle: `26_09_24_FT_Träger_Matrix_26.02_Vers-D_jz.xlsx` (Drive-ID 1Ldc8Q1zFfBCXNvaKqJp7c0i6qmf49sMe, SHA-256 3f9d64fa…a795)
Abgleich: `26_08_20_…26.02.xlsx`, `26_08_21_…26.02.xlsx`, `26_02_09_…jz_kopie_DB.xlsx` (Linie A)
Methode: read-only, gespeicherte Werte + Formeltext. Nichts in Excel neu gerechnet, nichts veraendert.
Status aller Vorschlaege: VORSCHLAG (ID01-Pruefung + Rebuild ausstehend).

## 1. Befund

- Die 5 Defekte sind seit Linie A (Feb. 2026) unveraendert vorhanden. Keine Vorversion enthaelt die Originalformel.
- Rekonstruktion daher aus dem Spaltenmuster derselben Zeile (Belegbasis):
  - Zeile 110 `As,zusatz`: `=@153*2-IF(@15=0,0,@108*0.5)+@195-IF(@19>0.1,(@108*(@19/100+0.2)),0)` (3.572 Zellen)
  - Zeile 114 `V,c,db`: `=IF(@19=0,"--",-@194)` (3.861 Zellen)
  - `@195` = `G,s,db TONNAGE DURCHBRUCH`, `@194` = `V,db Kubatur Durchbruch`.
- Der fehlende Bezug ist also immer der Durchbruch-Block der eigenen Spalte (Zeile 194/195).

## 2. Rekonstruktionsliste

| # | Blatt!Zelle | Formel ist | Formel neu | Begruendung |
|---|---|---|---|---|
| 1 | 2OG-3!BC110 | `…+#REF!-IF(BC19>0.1,…)` | `=BC153*2-IF(BC15=0,0,BC108*0.5)+BC195-IF(BC19>0.1,(BC108*(BC19/100+0.2)),0)` | Muster Zeile 110; BC19 = 30 cm (Durchbruch in BC) |
| 2 | 2OG-3!BC114 | `=IF(BC19=0,"--",-#REF!)` | `=IF(BC19=0,"--",-BC194)` | Muster Zeile 114 |
| 3 | 2OG-4!BC110 | wie #1 | `=BC153*2-IF(BC15=0,0,BC108*0.5)+BC195-IF(BC19>0.1,(BC108*(BC19/100+0.2)),0)` | Muster Zeile 110; BC19 = 30 cm |
| 4 | 2OG-4!BC114 | wie #2 | `=IF(BC19=0,"--",-BC194)` | Muster Zeile 114 |
| 5 | 2OG-BC!Z114 | `=IF(Z19=0,"--",-#REF!)` | `=IF(Z19=0,"--",-Z194)` | Muster Zeile 114; Z19 = 0 -> Ergebnis bleibt "--" |

## 3. Pflicht-Begleitkorrekturen (sonst Doppelzaehlung / falsche Werte)

| # | Blatt!Zelle | Ist | Neu | Grund |
|---|---|---|---|---|
| A | 2OG-3!BD110 | `…+BC195-…` | `…+BD195-…` | BD (b,d = 0) zaehlt heute die Durchbruchtonnage von BC. Nach Fix #1 sonst doppelt |
| B | 2OG-3!BD114 | `-BC194` | `-BD194` | wie A |
| C | 2OG-4!BD110 | `…+BC195-…` | `…+BD195-…` | wie A |
| D | 2OG-4!BD114 | `-BC194` | `-BD194` | wie A |
| E | 2OG-3!BC188:BC194 | Eingaben `BD16/BD17/BD19/BD20/BD21` | `BC16/BC17/BC19/BC20/BC21` | Block rechnet mit Spalte BD (b,d = 0); Vergleich: 2OG-4!BC188:BC194 nutzt korrekt BC |
| F | 2OG-BC!Z110 | `…+Z194-…` (m3) | `…+Z195-…` (kg) | Einheitenfehler: Kubatur statt Tonnage addiert; heute 0, wird bei Durchbruch falsch |

## 4. Erwartungswerte nach Korrektur (Golden Check fuer den Rebuild)

Nachgerechnet aus gespeicherten Eingaben. Kontrolle: 2OG-4!BC195 = 37,310 kg = gespeicherter Excel-Wert.

| Zelle | 2OG-3 BC | 2OG-4 BC |
|---|---|---|
| 195 G,s,db [kg] | 140,05 (ist 90,65, falsche Eingabespalte) | 37,31 |
| 194 V,db [m3] | 0,0144 (ist 0) | 0,0096 |
| 110 As,zusatz [kg] | 128,43 | 27,11 |
| 112 G,s [kg] | 281,25 | 115,45 |
| 117 V,c,FT [m3] | 0,6741 | 0,5412 |
| 118 [kg/m3] | 368,5 | 195,7 |
| BD112 [kg] | 169,30 (ist 259,94) | 104,82 (ist 142,13) |

Folge: Die 13 `#REF!`-Wurzeln + 21 Folgefehler in `Übersicht` (inkl. GESAMT N9/S9/T9, S473/T473) und in 2OG-3/2OG-4 Zeile 112/117/118 entfallen.
Pruefhinweis: 368,5 kg/m3 in 2OG-3 BC ist hoch (Durchbruchtraeger) und fachlich zu pruefen.

## 5. Weitere Befunde mit Einfluss auf LV-Massen

1. Systematischer Spaltenversatz Durchbruch (gleiches Muster wie Abschnitt 3, nicht `#REF!`, daher bisher unentdeckt):

| Blatt | Zelle verweist auf | Traeger mit Durchbruch |
|---|---|---|
| EG-G | P110/P114 -> Q195/Q194; Q110/Q114 -> R (leer) | Q (b,d 30) |
| EG-G | AA110/AA114 -> AD (leer) | - |
| EG-B | AB110/AB114 -> AA195/AA194 | AA (b,d 55) |
| 2OG-G | AB110/AB114 -> AD195/AD194 | AD (b,d 30) |
| 3OG-2 (+ _RO260821) | BC110/BC114 -> BB195/BB194 | BB (b,d 45) |
| 3OG-E (+ _RO260821) | Y114 -> AB194 | AB (b,d 30) |

   Wirkung: Die Durchbruchtonnage landet beim Nachbartraeger (Summe je Achse stimmt, Einzeltraeger falsch). Der Betonabzug V,c,db geht verloren, weil Zeile 117 `IF(@19=0,0,@114)` die eigene Spalte prueft. Vermutlich ist das die Folge der `#REF!`-Reparatur vom 21.08.2026 (EG-B, 2OG-G). Empfehlung: alle auf die eigene Spalte zurueckstellen.

2. `Übersicht` GESAMT: `I9:K9` und `O9:P9` = `SUM(…16:23)` erfassen nur 4OG-1, `N9`/`S9`/`T9` dagegen `16:470`. Damit ist `Q9 = N9/(O9+P9)` [kg/m3] falsch; konsistent ist `U9 = S9/T9`. Vorschlag: `O9 =SUM(O16:O470)`, `P9 =SUM(P16:P470)`.

## 6. Umsetzung

1. Auf Kopie von `Vers-D_jz` arbeiten: Zellen #1-#5, A-F, Abschnitt 5.
2. RUN-01 (CalculateFullRebuild), danach `p205_error_audit.py`.
3. Abnahme: `#REF!` = 0; Werte aus Abschnitt 4 innerhalb +-0,01 erreicht; GESAMT S9/T9 numerisch.
4. Erst danach: Kopierzeilen 37/42/47 und `?`-Platzhalter (rund 133 Wurzelfehler), siehe `reports/2026-11-23_FT-Traeger-Matrix_SYNC/`.
