---
tasks: erledigt = Zellvergleich Vers-D/RevE, Lückenanalyse G1–G18, Dashboard v1.1, Bericht | offen = GitHub-Ablage, RUNLOG.md anhängen, neuer Export (G7–G11)
probleme: GitHub-Schreibzugriff abgelehnt; RUNLOG.md nicht beschreibbar; Exporter + SQLite-DB vom 12.11. nicht im Drive
offene_fragen: E1.1–E1.4 (ID01, heute 11:15); Messgrößen-Definition G6; Ablageort Exporter/DB
ergebnis_pruefstatus: Zellvergleich VERIFIED (0 Abweichungen); Dashboard v1.1 im Browser getestet (6 Reiter, 0 Skriptfehler); Bemessung NICHT geprüft, NICHT freigegeben
name: RPT_FTM_GAP-ANALYSE_DASHBOARD-v1.1_20261123
description: P205 FT-Träger-Matrix – Lückenanalyse Dashboard 13.11. gegen Stand 23.11., Zellvergleich Vers-D/Vers-DRevE, Dashboard v1.1
version: 1.0
status: DONE (Drive) / OFFEN (GitHub)
timestamp: 2026-11-23T08:40+01:00
agent: Claude (claude.ai, Fable 5.2), Auftrag ID01 23.11.2026 08:35
---

# TL;DR
- Vers-D (22.08.) und Vers-DRevE (22.11.) sind zellidentisch. Der Datenstand des Dashboards gilt damit auch für RevE.
- 18 Lücken erfasst: 2 geschlossen, 1 teilweise geschlossen, 15 offen.
- Dashboard v1.1 liegt im WORK-Ordner: neuer Reiter „Stand 23.11.“, Kopfzeile ergänzt. Daten und Code der übrigen Reiter unverändert. v1.0 bleibt erhalten.
- GitHub nicht aktualisiert: Schreibzugriff auf nexus-platform wurde in diesem Lauf abgelehnt.

# 1 Zellvergleich Vers-D ↔ Vers-DRevE (selbst geprüft)
| Größe | Vers-D | Vers-DRevE |
|---|---|---|
| Drive-ID | 1knpaqjyO33E1eZzI0PFVxzSZrTpdRJdc | 1oVj79Li7EiYxo2SnrvgtNGzbF3tmqbiQ |
| SHA-256 | a921f515c3d56b281a47343ff5ee39c65e8cc2093fe371ef048006c4a55810f9 | af4d60389b7a89bb14995429eff3f3840948e7142133d575420d36af1240239e |
| Blätter (Reihenfolge gleich) | 106 | 106 |
| Zellen mit Inhalt | 327.999 | 327.999 |
| Formeln | 239.689 | 239.689 |
| gespeicherte Fehlerwerte | 288 | 288 |

- Abweichungen Formeln/Konstanten: **0**. Abweichungen gespeicherte Werte: **0**.
- Methode: openpyxl 3.1.5, read-only, je Datei einmal mit Formeln und einmal mit gespeicherten Werten; Vergleich je Blatt und Zelladresse.
- Nicht geprüft: Formatierung, Druckeinrichtung, bedingte Formate, Neuberechnung.
- Plausibilität: Kennzahlen decken sich mit den Dashboard-Metadaten vom 13.11. (106 / 327.999 / 239.689 / 288).

# 2 Lückenanalyse
| # | Bereich | Lücke | Stand 23.11. | Status |
|---|---|---|---|---|
| G1 | Herkunft | LLM/Chat der Dashboard-Erzeugung nicht dokumentiert | Claude-Chat 12.11. (geteilte Kopie); Hash, Formel-/Fehlerzahl, Recalc-Wortlaut stimmen überein; Erzeugungsschritt fehlt in der Kopie | teilweise geschlossen |
| G2 | Herkunft | Kein Agent/Modell/Lauf in der HTML | Herkunftsblock in v1.1 | geschlossen |
| G3 | Herkunft | Exporter-Skript + SQLite-DB (db_sha256 79103ff2…) nicht im Drive/GitHub | nur als Downloads im Chat vom 12.11. | offen |
| G4 | Datenstand | Dashboard nennt Vers-D, aktuell ist RevE | zellidentisch, Kopf ergänzt | geschlossen |
| G5 | Datenstand | MERGED 26_05 (FIX-01…07) nicht im Drive | Fix-Satz neu anwenden | offen |
| G6 | Datenstand | Zählungen uneinheitlich: Fehlerzellen 288/140/87; η>1 227/880; Träger 224/226 | Messgröße und Blattumfang je Kennzahl festlegen | offen |
| G7 | Funktion | Keine Bewehrung im 3D-Modell (D2) | neuer Export nötig | offen |
| G8 | Funktion | η-Skala ≠ Projektskala 13.11. (D3) | nach E1.1 | offen |
| G9 | Funktion | I1–I7 nicht sichtbar (D4) | nur Zusammenfassung im neuen Reiter | offen |
| G10 | Funktion | Kein Reiter „Optimierung“ (D5) | CSV im WORK, nicht eingebunden | offen |
| G11 | Funktion | ezdxf nur eine Ansicht je Achse | Pilot B3 heute | offen |
| G12 | Bemessung | Guide-Kopf DIN/NA-D, gerechnet mit f_cd = f_ck/1,5 | ID01-Entscheid 19.11.: ÖNORM EN 1992-1-1:2015 + B 1992-1-1:2018; Kopf nicht korrigiert | offen |
| G13 | Bemessung | I1: 56 Spalten mit zu großem verknüpftem BT-Typ | E1.4; sicherheitsrelevant | offen |
| G14 | Bemessung | 32 „?“-Schnittkraftzellen (1OG-J, 2OG-J); 53 Widerstandszellen ohne Wert | RFEM-/Katalogbezug ergänzen | offen |
| G15 | Bemessung | Kein Blatt freigegeben; Schubfuge 148, Konsolen 72 offen | eigener Arbeitsgang | offen |
| G16 | Ablage | RUNLOG.md nicht fortgeschrieben | RUNLOG_APPEND-Dateien im WORK | offen |
| G17 | Ablage | Dashboard nicht im GitHub | Schreibzugriff abgelehnt | offen |
| G18 | Ablage | SQLite (AnythingSearch.db, Projekt-DB) nicht geprüft | lokal auf G:, nicht erreichbar | offen |

Quellen je Lücke stehen im Dashboard-Reiter „Stand 23.11.“ (S1–S9). G5–G15 sind aus den Berichten vom 19.–23.11. übernommen, nicht unabhängig nachgerechnet.

# 3 Dashboard v1.1
| Punkt | Inhalt |
|---|---|
| Datei | 26_11_23_FT_Traeger_Matrix_VersD-RevE_Dashboard_v1.1.html |
| SHA-256 | 1de517ecc5d001f53d4a46111a02054d5419a2c72e60d39ba92ae53c0c624276 |
| Größe | 1350473 Byte (v1.0: 1.339.073) |
| Vorgänger | 26_11_13_FT_Traeger_Matrix_VersD_Dashboard.html, Drive 11iVnKGobGw7pu-TV9IhOXOOU_vLlOohg, SHA-256 3c8ea0249525855fb06974045f8ac17d53a862813f9566ff8b97f50b4752e438 |
| Geändert | Titel „Vers-D / RevE“; Chip „v1.1 · zellidentisch mit Vers-DRevE“; Reiter „Stand 23.11.“ (Gültigkeit, Lücken G1–G18, Pilot 4OG-2, Entscheidungen E1.1–E1.4, Herkunft, Quellen) |
| Unverändert | Datenblock (byteweise geprüft), three.js, Programmcode aller bisherigen Reiter |
| Test | Chrome headless: Start, Reiter Trägerachse, Bericht, Referenzen, 3D-Modell, Stand 23.11. geöffnet; 0 Skriptfehler |
| Nicht getestet | Pyodide-Berechnung, PDF-Export, Darstellung im dunklen Modus |

# 4 Offen / nächste Schritte
1. GitHub: Dashboard v1.1 + diesen Bericht nach USECASES/P205_EISTEICHE/FT_TRAEGER_MATRIX legen (Schreibfreigabe nötig).
2. Exporter-Skript und SQLite-DB aus dem Chat vom 12.11. in den WORK-Ordner legen; erst dann sind G7–G10 umsetzbar.
3. RUNLOG.md: Einträge aus RUNLOG_APPEND_FTM_20261123.md und RUNLOG_APPEND_FTM_20261123_0840.md anhängen.
4. Nach E1.1–E1.4 und Pilot B1–B3: Dashboard neu exportieren (Skala, Befunde, Optimierung).

# LOG
- 2026-11-23T08:40+01:00 | Claude (Fable 5.2) | Zellvergleich, Lückenanalyse, Dashboard v1.1, Bericht → WORK | DONE; GitHub OFFEN
