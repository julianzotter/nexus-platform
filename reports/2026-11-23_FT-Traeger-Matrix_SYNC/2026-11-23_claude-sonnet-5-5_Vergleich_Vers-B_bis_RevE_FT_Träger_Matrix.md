# Inhaltlicher Vergleich Vers-B bis RevE (und jz, RevF), August bis November 2026

Erstellt am 23.11.2026 von `claude-sonnet-5-5`. Nur gelesen; nichts neu berechnet, nichts verändert.
Verglichen wurden **gespeicherte Zellwerte** (Formelergebnisse) und **Formeltexte** aller Blätter. **Nicht** verglichen: Formate, Diagramme, Namen, Bedingte Formatierung.

## Ergebnis in drei Sätzen

1. **Vers-B, Vers-C, Vers-D, Vers-D_RC260924, Vers-DRevE und `Vers-D_jz` sind inhaltlich identisch**: 0 Formeländerungen, 0 Wertänderungen. Einziger Unterschied: Zelle `MRd!B181` (Vers-B leer, Vers-C „per side“).
2. **Der eigentliche Sprung liegt zwischen `26_08_21_…26.02` und Vers-B**: 14 neue Blätter (3OG-Rollout) und rund 24.800 neue Formeln. Danach ändert sich nichts mehr am Rechenkern.
3. **`Vers-DRevF` (heute 09:04) ist die einzige Fassung mit Änderungen**: 2.179 Formeln sind umgeschrieben, und genau für diese Zellen fehlen die gespeicherten Rechenwerte. Ob das richtig ist, zeigt erst eine Neuberechnung in Excel.

## Kette Schritt für Schritt

| Schritt | Blätter | Formeln | Werteänderungen | Befund |
|---|---|---|---|---|
| `26_08_20_…26.02` | 92 | 214.787 | Ausgangsbasis | |
| → `26_08_21_…26.02` | 92 | gleich | 73 Zellen in 5 Blättern | `#REF!`-Fehler behoben: `Übersicht` 26 Zellen (z. B. N216, P216, Q216), `EG-B` AA110/112/114/117, `2OG-G` AD110/112/114/117. `EG-G`: 33 Zellen in Zeile 107 von 3,906 auf 4,069. `_MasterIndex` O16/O20/O58/O85 neu gezählt |
| → **Vers-B** | **106** (+14) | 239.599 (+24.812) | 66 Zellen nur in `_logs` | Neu: `Guide_Rollout_26-03` und 13 Blätter `3OG-*_RO260821` (IJ, I, GH, G, F, E, CD, C, 4, 34, 3, 2, 1). `_logs` Eintrag vom 21.08.2026: „3OG-ROLLOUT gestartet“. Die 3OG-Blätter sind mit `Eingabe_RFEM_ABC` bzw. `_765` verknüpft (z. B. `R19`) |
| → **Vers-C** | 106 | gleich | 1 Zelle (`MRd!B181`) | praktisch nur neu gespeichert |
| → **Vers-D** | 106 | gleich | 0 | Inhalt gleich; nur `EG-2` im Dateiaufbau anders (Neuspeicherung) |
| → **Vers-D_RC260924** | 106 | gleich | 0 | **byte-gleich** mit Vers-D (kein einziger Dateiteil verschieden), nur anderer Name und Datum |
| → **Vers-DRevE** (22.11.) | 106 | gleich | 0 | nur Neuspeicherung |
| → **Vers-D_jz** (22.11. 20:09) | 106 | gleich | 0 | nur Neuspeicherung; 14 Blätter im Dateiaufbau anders (Verwaltungsblätter, `4OG-1`, `4OG-3`), inhaltlich gleich |
| → **Vers-DRevF** (23.11. 09:04) | 106 | gleich viele (239.599), davon **2.179 geändert** | 2.179 Werte fehlen, 33 neu, 248 Textzellen | siehe unten |

Hinweis: Dass die Dateien in Excel unterschiedlich „aussehen“ (andere Dateigrößen 6,6 bis 6,8 MB, geänderte Formate), liegt am Neuspeichern. Es sind keine Rechenänderungen.

## Detail zu RevF

**Was geändert wurde:** 2.175 Formeln haben dieselbe Struktur, aber **andere Zellbezüge**, 4 sind inhaltlich andere Formeln. Betroffen sind 31 Blätter, vor allem `EG-2` (757), `2OG-1` (355), `1OG-3` (197), `EG-C` (136), `2OG-2` (136), `EG-3`, `1OG-2` (je 102), `EG-6` (68).

**Beispiele (Vers-D_jz → RevF):**
- `EG-2 AT49`: `VRd!BF36` → `VRd!U36`; `AP41`: `VRd!BB28` → `VRd!T28`.
- `2OG-1 Z64`: `MRd!$L26` → `MRd!$G26`.
- `EG-C S50`: `VRd!BF37` → `VRd!BL37`.
- `2OG-2 AV45`: Kopfzeilenbezug `BB$30` → `AV$30` (eigene Spalte).

**Zwei verschiedene Arten von Änderung:**
1. **Berichtigung falscher Spaltenbezüge:** In `Vers-D_jz` zeigen 253 Formeln auf die Kopfzeile einer fremden Spalte (`1OG-2` 102, `2OG-2` 102, `2OG-1` 49), zum Beispiel `AV45` auf `BB$30`. RevF setzt diese auf die eigene Spalte. Das sieht wie eine echte Fehlerkorrektur aus. In RevF bleiben 204 Formeln mit fremdem Kopfzeilenbezug übrig.
2. **Neuzuordnung der VRd-/MRd-Spalten:** In `Vers-D_jz` laufen die VRd-Spalten je Träger fortlaufend (H→T, I→U, J→V … N→Z, O→AA). In RevF fällt das Muster ab Spalte N auf (N→T, O→U, P→V, Q→V, R→U, S→T). Das kann gewollt sein (Zuordnung nach Trägertyp), kann aber auch ein Schaden sein. **Das lässt sich aus den Formeln allein nicht entscheiden.**

**Warum die Werte fehlen:** Für exakt diese 2.179 Zellen steht kein gespeicherter Wert in der Datei. Die Formeln wurden also geschrieben, ohne dass Excel danach gerechnet hat (typisch für ein Skript oder eine Bibliothek, die Formeln einträgt). Gelesen mit einem Programm, das nur gespeicherte Werte zeigt, wirken diese Zellen leer.

## Empfehlung

- **Als Rechenstand gilt Vers-D (= RC260924 = RevE = jz).** Alle sechs sind inhaltlich gleich; `Vers-D_jz` ist die jüngste Arbeitsdatei.
- **RevF nicht ungeprüft übernehmen.** Erst in Excel vollständig neu berechnen (das ist, was dein COM-Skript macht: `CalculateFullRebuild` auf einer Kopie) und dann Werte gegen `Vers-D_jz` vergleichen. Auffällig wären Auslastungen, die sich stark ändern.
- Die Vergleichsskripte liegen im Arbeitsordner der Sitzung; ich kann den Werte-Vergleich nach der Neuberechnung in einem Schritt wiederholen.

## Nicht geprüft

- Formate, Diagramme, Definierte Namen, Bedingte Formatierung, Datenüberprüfung.
- Die Linien-A-Dateien (`kopie_DB`, ALEX-DB-TRAINING) und die älteren Fassungen vor August 2026; sie stehen in `_ANALYSE_AutoRecover_Bericht.md` und im Inventar.
- Die Formeln der `Autorecovered`-Dateien (siehe Nachtrag): Mein xlsb-Leser liest nur Werte, keine Formeltexte.

## Nachtrag: Autorecovered-Stände von Vers-D (22./23.11.)

Verglichen wurden die vier `…Vers-D_jz((Autorecovered-…)).xlsb` (22.11. 20:56, 21:19, 23.11. 02:41, 02:52) und `~ar6A6C.xar` (23.11. 10:20) mit `Vers-D_jz.xlsx`.

- **Alle fünf Stände sind wertgleich mit `Vers-D_jz`**: 327.981 Zellen, 106 Blätter, 0 Abweichungen, auch nicht in den 2.179 Zellen, die RevF verändert hat.
- **Folge:** In den Wiederherstellungsdaten gibt es keine Zwischenstufe zwischen `jz` und RevF. Auch der jüngste Stand von 10:20, also nach RevF (09:04), enthält noch den `jz`-Inhalt. RevF ist demnach nicht in der Excel-Sitzung entstanden, die diese Wiederherstellungsdaten schreibt, sondern in einem anderen Vorgang (Skript oder Fremdprogramm), und wurde nicht in `jz` übernommen.
- **Einschränkung:** Verglichen sind gespeicherte Werte. Formeltexte der xlsb-Dateien habe ich nicht geprüft; ein Formelunterschied ohne Wertunterschied bliebe unbemerkt (gespeicherte Werte würden sich erst nach einer Neuberechnung ändern).
- **Heißt für dich:** Gehen die Arbeitsdateien `Vers-D_jz` verloren, enthalten diese fünf Wiederherstellungsstände denselben Inhalt. Die vier `Autorecovered`-Dateien sind 6,0 MB, die `jz` 6,6 MB; die Differenz liegt nach bisherigem Befund nicht in den Zellwerten.

## Nachtrag 2: Welche Fassung bezieht richtig, `jz` oder `RevF`?

**Prüfmaßstab:** Die Datenblätter `MRd` und `VRd` führen je Spalte einen Trägertyp (`BT01` bis `BT11a`) mit Gesamthöhe, Fugenhöhe und Fugenbreite (`MRd` Zeilen 9 bis 14). Jede Ergebnisspalte (z. B. `EG-F Z`) trägt ihre eigene Trägerhöhe in Zeile 17. Ein Bezug ist **richtig**, wenn die Höhe der Quellspalte in `MRd`/`VRd` zur Trägerhöhe der Ergebnisspalte passt. Dieses Kriterium steht in der Datei selbst und ist unabhängig von beiden Fassungen.

**Beispiel `EG-F Z64`:** Die Spalte ist 40 × 80 cm mit Vergussfuge 15 cm. `jz` greift auf `MRd!X` zu (BT10a: 65 cm, Fuge 0,01), `RevF` auf `MRd!W` (BT10: 80 cm, Fuge 15 / 24). `RevF` passt, `jz` nicht.

**Ergebnis über alle 2.175 umgebogenen Formeln (Trägerhöhe der Quellspalte = Höhe der Ergebnisspalte):**

| Bezug auf | `Vers-D_jz` passt | `RevF` passt |
|---|---|---|
| `MRd` (730 Formeln) | 145 | **729** |
| `VRd` (1.445 Formeln) | 544 | **1.428** |

- **`RevF` korrigiert damit überwiegend falsche Bezüge**, die in `jz` stehen: in `jz` greifen rund 1.490 von 2.175 Formeln auf einen Trägertyp mit anderer Höhe zu. In `EG-2` reicht dieses Muster mindestens bis `25_12_10` zurück (identisch in `26_02_19`, V5 und `jz`).
- **Das ist wirksam:** Bei 1.692 der Formeln liefert die neue Quellzelle einen anderen Wert (`EG-2` 726, `2OG-1` 280, `1OG-3` 197, `EG-3` 102, `EG-6` 68). Es betrifft also Rechenergebnisse (Momenten- und Querkraftwiderstände), nicht nur Optik.
- **Rest in `RevF`:** 1 `MRd`-Formel und 17 `VRd`-Formeln passen auch dort nicht (Beispiel `2OG-1 BF32`: Trägerhöhe 70, Bezug `VRd!BB` mit 77). Dazu bleiben 204 Formeln mit Kopfzeilenbezug auf eine fremde Spalte (siehe oben). Diese Reste sind zu prüfen.
- **Wichtig zur Einordnung:** Der Höhenvergleich ist ein starkes Indiz, aber kein vollständiger Nachweis. Er erkennt nur Bezüge auf einen Typ mit anderer Höhe. Zwei Typen mit gleicher Höhe (z. B. BT02 und BT10, beide 80 cm) unterscheidet er nicht. Maßgeblich bleibt die Neuberechnung in Excel und die Prüfung der Auslastungen.

**Konsequenz für die Reihenfolge der Fassungen:**
- `Vers-B` bis `Vers-D_jz` rechnen in den betroffenen Blättern (`EG-2`, `2OG-1`, `1OG-3`, `EG-3`, `EG-6` u. a.) vermutlich mit falschen Querschnittsdaten. Der Fehler ist älter als diese Reihe.
- `RevF` ist **die fachlich bessere Fassung**, aber nicht gerechnet. Sie darf erst als Stand gelten, nachdem Excel sie vollständig neu gerechnet hat und die Auslastungen geprüft sind (`Übersicht`, Blätter mit hoher Änderung).
- Vor dem Übernehmen sollte ein Vergleich der Auslastungen `jz` gegen neu gerechnete `RevF` zeigen, welche Träger sich verschlechtern (Überschreitung > 1,0).


## Nachtrag 3 – Reste in RevF und Fehleranalyse (288 gespeicherte Fehler, 5 defekte Formeln)

Stand: 23.11.2026. Grundlage sind die gespeicherten Werte von `Vers-D_jz` und `Vers-DRevF`. Nichts wurde neu gerechnet.

### A. Die 18 Rest-Bezüge in RevF
Alle 18 liegen in **einer Spalte: `2OG-1` Spalte `BF`**. Die Trägerhöhe ist dort 70 cm, die Bezüge zeigen auf eine Spalte mit 77 cm:
- `BF32`, `BF37` bis `BF52` greifen auf `VRd!BB19` bis `BB39` zu.
- `BF107` greift auf `MRd!L72` zu.

Das ist wahrscheinlich ein einzelner Spaltenversatz (eine Spalte zu weit oder zu wenig) und lässt sich in einem Zug korrigieren. Welche `VRd`/`MRd`-Spalte stattdessen gemeint ist, muss die Trägerzuordnung von `2OG-1 BF` entscheiden, die ich nicht kenne.

### B. Die 5 direkt defekten Formeln (`#REF!` im Formeltext)
| Blatt | Zelle | Formel | in RevF |
|---|---|---|---|
| `2OG-BC` | Z114 | `=IF(Z19=0,"--",-#REF!)` | **weiter defekt** |
| `2OG-3` | BC110 | `=BC153*2-IF(BC15=0,0,BC108*0.5)+#REF!-IF(BC19>0.1,…)` | umgebogen |
| `2OG-3` | BC114 | `=IF(BC19=0,"--",-#REF!)` | umgebogen |
| `2OG-4` | BC110 | wie `2OG-3` BC110 | umgebogen |
| `2OG-4` | BC114 | wie `2OG-3` BC114 | umgebogen |

`RevF` repariert vier der fünf Formeln, hat aber noch keinen berechneten Wert dafür. Offen bleibt `2OG-BC Z114`. Die fehlende Referenz in `BC110`/`BC114` steht im Block „Konsole/Zusatzbewehrung“ (`G,s`, `G,s,kon`, `Asw`). Welche Zelle ursprünglich gemeint war, ist aus den Dateien nicht ableitbar. Hier sollte `Vers-A`/Linie A (`kopie_DB`) als Quelle für die frühere Formel dienen.

### C. Die 288 gespeicherten Fehler (`jz`: 288, `RevF`: 284)
Typen: `#DIV/0!` 145, `#VALUE!` 109, `#REF!` 34. Von den 288 sind 170 **Wurzelfehler** (kein Vorgänger mit Fehler), der Rest sind Folgefehler. Die Wurzelfehler fallen in sechs Ursachengruppen:

| # | Ursache | Blätter / Spalten | Wurzelfehler |
|---|---|---|---|
| 1 | **Kopierzeilen 37/42/47 sind 0.** V,Ed ist gefüllt (z. B. 157,5 kN), die Widerstandszeilen `(1) Kopieren` stehen auf 0, daher teilt `Z37/(Z42*Z47)` durch 0 (Zeile 55, 233, 234). | `EG-2` (Zeile 55 in 20 Spalten, 233/234 in je 6), `EG-3` (T–X), `EG-4` (BC–BF), `2OG-I`, `2OG-F/G`, `2OG-3` (BF/BG), `1OG-F/G`, `1OG-5` | ca. 85 |
| 2 | **Platzhalter `?` in Eingaben.** In `EG-4` H–S stehen in den Zeilen 64/70/76/82/88/94 (MRd-/VRd-Formelzeilen) Fragezeichen statt Werten. Die Folgezeilen 56/66/72 werden `#VALUE!`. In `2OG-J`/`1OG-J` stehen `?` in Zeile 22/23 (Eingabe Schnittkraft), daraus werden `MAX(ABS(..))` und die Kon­solen­nachweise `#VALUE!`. | `EG-4` (36), `2OG-J` (8 Wurzeln, 29 Zellen), `1OG-J` (4 Wurzeln, 20 Zellen) | ca. 48 |
| 3 | **Text `--` in Rechenzellen.** Zeile 57 und 118 teilen durch `--`-Strings (`AV56/AV55`, `AD116+AD117`), weil die vorgelagerte Zeile bewusst `--` liefert. Die IF-Abfrage prüft die falsche Zelle. | `EG-HI`, `1OG-HI`, `2OG-C`, `EG-56`, `1OG-34`, `EG-34` | ca. 14 |
| 4 | **Leere Spalte (4OG-D/I, BD).** Zeilen 16/17/20/21 und 37/47 sind leer, `I_OG_db+I_U_db = 0`. Das ist vermutlich eine nicht belegte Reserve-Spalte, die nur ausgeblendet oder bereinigt werden muss. | `4OG-D`, `4OG-I` | 10 |
| 5 | **Division durch `z_ug_db = 0` und `V_Rd_u_db = 0`** (Zeilen 223/226/238). | `EG-3` Spalte AE | 3 |
| 6 | **`#REF!` Übersicht.** `GESAMT` (N9, S9, T9, Z473) und die Summen auf `'2OG-3'!…112` / `'2OG-4'!…112` zeigen `#REF!`, weil Zeile 112 (`G,s`) auf den defekten Zellen aus B hängt. | `Übersicht` | 13 |

Wirkung: Solange gruppe 6 (die `#REF!`-Formeln) offen ist, bleiben die Gesamtmassen in `Übersicht` (`GESAMT`) fehlerhaft. Das trifft direkt die Ableitung der Ausschreibungsmassen.

### D. Reihenfolge der Behebung (Vorschlag)
1. `2OG-BC Z114` und `2OG-1 BF` (18 Zellen) korrigieren. Das sind 19 Zellen, danach entfallen alle `#REF!`-Folgen in `Übersicht`.
2. Platzhalter `?` in `EG-4` H–S (Zeilen 64–94) und `2OG-J`/`1OG-J` (Zeile 22/23) durch RFEM-Schnittkräfte bzw. Formelzeilen ersetzen.
3. Kopierzeilen 37/42/47 in den Spalten der Gruppe 1 befüllen oder die Formel mit `IF(Z42*Z47=0,"--",…)` absichern. Das ist die größte Gruppe, aber wahrscheinlich eine Datenlücke, kein Formelfehler.
4. Zeilen 57/118: IF-Abfrage auf die tatsächlich geteilte Zelle (`AD55`, `AD116+AD117`) setzen.
5. Leere Spalte `BD` in `4OG-D/I` bereinigen.
6. Erst danach: vollständiger Neuberechnungslauf in Excel (`CalculateFullRebuild`) auf einer Kopie, dann Vergleich der Auslastungen `jz` gegen `RevF`.

### E. Grenzen
- `RevF` hat für die 2.179 geänderten Formeln keinen gespeicherten Wert. Die 284 Fehler dort sind nur die der unveränderten Formeln. Ob die Umbiegung neue Fehler erzeugt, zeigt erst die Neuberechnung.
- Die Zuordnung Ursache → Gruppe beruht auf den gespeicherten Werten der Vorgängerzellen. Die Spalten- und Blattzahlen sind gerundet („ca.").
- Die Zeile `Z37/42/47` ist nur als Datenlücke benannt, nicht als Rechenfehler. Ob die Werte aus RFEM oder aus einem Makro/Kopierlauf stammen sollten, ist offen.
