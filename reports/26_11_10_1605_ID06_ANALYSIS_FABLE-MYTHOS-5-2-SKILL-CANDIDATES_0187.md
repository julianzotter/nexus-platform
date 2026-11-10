---
name: 26_11_10_1605_ID06_ANALYSIS_FABLE-MYTHOS-5-2-SKILL-CANDIDATES_0187
description: Kurzanalyse der Release-Seite Claude Fable 5.2 / Mythos 5.2 und daraus abgeleitete Skill-Kandidaten fuer NEXUS
version: 1.0.0
status: REVIEW_PENDING
timestamp: 2026-11-10T16:05:00+01:00
actor: ID06
tasks_done: Seite gelesen; 5 Kandidaten abgeleitet; Abgleich mit Skill-Liste im Konto
tasks_open: Entscheidung ID01 zu S4 und S5; Kandidaten nicht gebaut
problems: Seiteninhalt ueber Web-Fetch mit Zusammenfassungsmodell gelesen, nicht im Wortlaut geprueft
open_questions: S4 und S5 bauen? Bestehende Skills S1-S3 ins Ledger aufnehmen?
result: ANALYSE - keine Freigabe, Herstellerangaben nicht unabhaengig verifiziert
---

# Analyse Fable 5.2 / Mythos 5.2 -> Skill-Kandidaten

## Quelle
- https://www.anthropic.com/claude-fable-and-mythos-5-2, abgerufen 2026-11-10 ca. 15:36 CET.
- Alle Zahlen sind Herstellerangaben. FOUND, nicht VERIFIED.

## Fakten mit Relevanz fuer NEXUS (paraphrasiert)
| # | Aussage | Folge fuer NEXUS |
|---|---|---|
| F1 | Fable 5.2 und Mythos 5.2 sind dasselbe Basismodell; Fable hat Schutzfilter fuer Cyber und Biologie | Fuer Statik/AEC kein Unterschied relevant |
| F2 | Empfehlung: mit Opus 5.5 beginnen, nur bei Bedarf hoch- oder herunterstufen | Routing-Regel statt Standard "groesstes Modell" |
| F3 | Fable 5.2 kann als Advisor fuer kleinere Modelle oder als Orchestrator mit Delegation arbeiten | Passt zu EXEC != PEERREVIEW und Rollenregister |
| F4 | Niedrigere Effort-Stufen erreichen laut Seite bei einzelnen Benchmarks Opus-Spitzenwerte zu einem Bruchteil der Kosten | Effort je WorkOrder vorab festlegen |
| F5 | Preis 8 USD / 40 USD je Mio. Token (Input/Output); Fast Mode doppelt | Kostenrahmen je Run kalkulierbar |
| F6 | Pro- und Standard-Team-Plaetze: Fable bis 50 % des Wochenlimits | Fable-Kontingent nur fuer harte Teilaufgaben |
| F7 | BenchCAD 2.1: 83,5 gegen 65,3 (Opus 5.5) | Parametrische CAD-/STL-Erzeugung lohnt einen Test |
| F8 | Berichtete Grosslaeufe mit vielen Reviewer-Agenten (ca. 170) und bis 1000 Subagenten | Reviewer-Schwarm als Muster, im Kleinen testbar |
| F9 | Laut Seite weniger falsche Fertigmeldungen und weniger verdeckte Schlechtleistung | Definition-of-Done-Gate bleibt trotzdem noetig |
| F10 | KI-F&E-Faehigkeiten (z. B. Kernel-Optimierung) bewusst begrenzt | Fuer NEXUS ohne Belang |

## Abgeleitete Kandidaten
| # | Kandidat | Zweck | Basis | Stand im Konto (Skill-Liste 16:01 CET) |
|---|---|---|---|---|
| S1 | model-router | Modellstufe je Aufgabe waehlen | F2, F3, F6 | vorhanden als model-effort-router |
| S2 | effort-budget | Effort-Stufe vor dem Run festlegen | F4, F5 | vorhanden als model-effort-router |
| S3 | review-swarm | getrennte Reviewer-Runs mit Merge-Regel | F3, F8 | vorhanden als orchestrator-reviewer-split, agent-team-orchestrator, agent-team-plan |
| S4 | cad-param-builder | parametrische CAD/STL-Erzeugung mit Pruefschritt | F7 | nicht vorhanden |
| S5 | done-gate | DONE nur mit Artefakt + Report-Log + Statusbericht + Hash | F9 | nicht vorhanden |

Zusaetzlich im Konto vorhanden: model-release-watch, model-release-digest (Release-Seiten auswerten).

## Befunde
- #P1 --> Dubletten --> agent-team-orchestrator, agent-team-plan, orchestrator-reviewer-split ueberschneiden sich; zusammenlegen pruefen.
- #P2 --> Dubletten --> model-release-watch und model-release-digest ueberschneiden sich.
- #P3 --> Nicht registriert --> diese Konto-Skills sind im Ledger-Stand 15:40 nicht als SKILL-Zeilen belegt (nur Stichwortsuche "SKILL" im Master).

## Empfehlung
1. S1-S3 nicht neu bauen (Reuse vor Neubau).
2. S5 done-gate zuerst bauen: klein, direkt an die Drei-Ebenen-Pflicht gebunden.
3. S4 erst nach einem Messlauf an einem Golden Case (z. B. vorhandenes STL-Projekt).

## Reporting
STATUS: DONE (Analyse), OPEN (Bau)
CHANGED: diese Datei in WORK; Kopie in nexus-platform reports/
TESTS: keine
SOURCE_STATUS: 1 Primaerquelle (Herstellerseite), Zusammenfassung, nicht im Wortlaut geprueft
RISKS_GAPS: Benchmarks unverifiziert; Skill-Inhalte der Konto-Skills nicht gelesen
NEXT: ID01 entscheidet S4/S5 und Dubletten #P1/#P2
