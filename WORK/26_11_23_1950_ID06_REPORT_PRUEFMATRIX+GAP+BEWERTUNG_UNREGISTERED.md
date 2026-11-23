---
name: 26_11_23_1950_ID06_REPORT_PRUEFMATRIX+GAP+BEWERTUNG_UNREGISTERED
description: Prüfmatrix Basic Instructions je ID-Rolle, Verweis _GAP.md, Bewertung Konfidenz/Konformität/Struktur/Zuverlässigkeit, Next Steps
role: ID06
timestamp: "2026-11-23T19:50+01:00"
status: SNAPSHOT
quellen: [WORK + LLM-HISTORY-LOG 2026-11-23, GH REST (Branch id06 HEAD 9b00a58, Commits 49774f0/ed20716 vorhanden), Capability-WO 1y0DSTvk…, Review ID03 1w_IyHky…]
---
## 1 Prüfmatrix (PASS = Beleg mit Hash/ID; – = nicht dokumentiert)
| ID | Start-Log | ACK | T1 GH | T2 Status | T3a API | T3b Mount | T4 Sandbox | T5 EC5 | T6 RAG | T7 Konn. | Cap.-Delta | Review |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ID02 | Watch-Läufe | – | – | – | – | – | – | – | – | – | – | – |
| ID03 | ja | ja (WO) | PASS API | PASS | PASS | BLOCKED | NOT_RUN | BLOCKED | Doku PASS | Lesen PASS | file-registry-Delta | intern |
| ID04 | – | – | – | – | – | – | – | – | – | – | – | – |
| ID05 | – | – | – | – | Bytes ok, Uploader offen | FAIL | – | anderer Fall | – | GH-Lesen Selbstangabe | im Frontmatter | ID06, ID03 |
| ID06 | ja (spät) | ja | PASS | PASS | PASS | PASS | PASS | gerechnet | – | teilweise | ja | ID03 Remote-Bytes |
| ID07 | – | – | – | – | – | – | – | – | – | – | – | – |
| ID08 | – | – | – | – | – | – | – | – | – | – | – | – |

## 2 Richtigstellung Fremdbericht 19:45
| Aussage | Befund | Beleg |
|---|---|---|
| Branch id06/… nicht sichtbar | existiert, privat, HEAD 9b00a58, 15 ID06-Dateien in WORK/ | GH REST |
| Ledger-Merge 0212-0236 offen | erledigt, 0212-0256 + Zeile 0257 | Master sha256 0bdceff0… |
| 1rlPWU… = Original, 1wjxj22S… = Duplikat | byte-gleich; 1rlPWU… von ID03 nach WORK/ALT verschoben, 1wjxj22S… bleibt Referenz | sha256 b13372b3… |
| GitHub-Kopie wegen OAuth nicht belegt | OAuth betrifft nur Drive-Workflows; ID03 hat Rohbytes gegen ed20716 bestätigt | Review ID03 §5.2 |

## 3 Bewertung
| Kriterium | Wert | Basis |
|---|---|---|
| Vollständigkeit Evaluation | ≈ 20 % (11 von 56 Testzellen T1-T7 belegt) | Matrix |
| Genauigkeit belegter Fakten | hoch | ID06-Angaben per SHA-256/API geprüft; Fremdangaben teils fehlerhaft (G32) |
| Konformität Dateien heute | ≈ 73 % (16 von 22 Baseline-Dateien AGB §4-konform) | G21, G22 |
| Strukturiertheit | mittel | Frontmatter meist vorhanden; 7 FAQ-Fassungen, 4 Statusquellen |
| Zuverlässigkeit Automation | 2 von 5 Workflows grün | G01, G02 |
| Offene Lücken | 29 offen, davon 13 Entscheidung ID01; 3 geschlossen | _GAP.md |
| Gesamt-Konfidenz dieses Berichts | ≈ 0,8 (INFERENZ) | eigene Prüfungen hoch, Selbstangaben anderer IDs nicht nachgeprüft |

## 4 Best-Fit Next Steps
1. ID01: OAuth erneuern (G01) → löst G02 und GitHub↔Drive.
2. ID01: Sammelentscheid G03/G04/G10/G13-G15/G19/G20 in einer Freigabe (v3.1 + Steuerdateien + FAQ-SSOT = ID03-Review).
3. ID02: WO v3.1 an ID02, ID04, ID05, ID07 mit ACK-Pflicht verteilen (G08).
4. ID06: file-registry-Merge inkl. ID03-Delta und Tagesartefakte (G05), Ledger-SHA-Nachtrag (G06).
5. ID07: unabhängiger Review T5-Skript und Ledger-Merge (G10, G12).
6. ID01: Move-Freigabe für Duplikate und alten Ledger (G07, G21) nach WORK/ALT bzw. NEXUS.HISTORICAL.
