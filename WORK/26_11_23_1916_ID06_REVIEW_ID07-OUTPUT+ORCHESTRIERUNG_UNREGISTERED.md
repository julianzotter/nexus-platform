---
name: 26_11_23_1916_ID06_REVIEW_ID07-OUTPUT+ORCHESTRIERUNG_UNREGISTERED
description: Review ID06 der DeepSeek-Ausgabe (ID07) vom 2026-11-23 19:16 und Orchestrierungsregeln für ID07
version: v1.0
status: REVIEW_DONE / FREIGABE_ID01_OFFEN
timestamp: "2026-11-23T19:16+01:00"
agent: ID06 (Claude)
geprueft: 26_11_23_1916_ID07_RAW-OUTPUT_DEEPSEEK_UEBERGABE-ID01_UNREGISTERED.txt (sha256 3dde7afb…06a4)
quellen: [Manifest §4 NEXUS-ROLES-v1.1 (gdrive:1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn), _AGBS.md v007.1 §2.6]
---
## Befunde
| # | Befund | Beleg |
|---|---|---|
| F1 | DeepSeek spricht als "ID 06"; laut Manifest §4 ist DeepSeek ID07 | Rohausgabe Z.1, Z.57 |
| F2 | Denkschritte und Entwurf doppelt im Output | Rohausgabe Z.47-55 |
| F3 | Schreibt sich fremde Aussagen und Dateien zu ("Meine Dateien tragen ID06") | Z.31, Z.80 |
| F4 | Vermutete WORK-Datei "Perplexity=ID07" existiert nicht | Drive-Suche WORK, geändert ab 18:00 Uhr, Stichwort Perplexity: kein Treffer |
| F5 | Nebenbefund: zwei byte-identische Perplexity-Protokolle in WORK | sha256 b13372b3… für 1909_IDNN_PROTOKOLL und ID-PERPLEXITY_BASELINE-INSTRUCTION-EVALUATION |
| F6 | Positiv: ehrliche Grenzangabe (kein Drive-Zugriff), Manifest als Autorität anerkannt | Z.33-35 |

## Orchestrierungsregeln ID07 (Vorschlag, Freigabe ID01)
1. Identitätskopf in jedem Prompt: "Du bist ID07 DeepSeek, unabhängiger Auditor. Du bist nicht ID06."
2. Eingabepaket als Upload (max. 15 Textdateien, AGBs §2.6): _AGBS.md, Manifest §4, das zu prüfende Artefakt.
3. Auftragsart: nur Audit, Falsifikation, Lückenanalyse von fremden Artefakten. Nie Autor und Prüfer desselben Ergebnisses.
4. Output-Vertrag (Manifest §6): FINDINGS | EVIDENCE (Datei + Zeile aus dem Paket) | RISKS | NEXT_ACTION. Unbelegtes = "nicht belegt".
5. Nur Endantwort, keine Denkschritte, kein Entwurf.
6. Archivierung durch ID01 oder ID06 als YY_MM_DD_HHMM_ID07_…; Ausführung bleibt NOT_RUN.
