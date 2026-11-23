# NEXUS-QA-002 — Unabhängiges Review und Regressionstests

Owner des Auftrags: ChatGPT Work als Gesprächsorchestrator.
Bearbeitung vorgeschlagen: DeepSeek. Ausführung durch DeepSeek ist nicht beobachtet.
Input: unverändertes Paket `NEXUS_AEC_Contracts_v0_1.zip`, Version 0.1.0;
nach Entpacken `MANIFEST.sha256` prüfen. Maßgeblicher Softwarestand ist das Paket,
nicht ein älterer Cross-Chat-Schnipsel. Auftrag umfasst keine externen Writes,
Commits, Cloud-Konfiguration oder Solverberechnung.

## Ziel

Die vorhandene Referenzimplementierung unabhängig auf falsch-positive
Capability-Zusagen, verlorene Modellmerkmale und falsch zugeordnete Ergebnisse
prüfen. Kein zweites Domain-Modell und keinen parallelen Pydantic-Kern entwerfen.

## Prioritäten

1. Gegenbeispiele als Regressionstests: nodale Lasten beanspruchen das gesamte
   aktive Modell; Eigengewicht und Initialzustände dürfen nicht verschwinden;
   gemeinsam unverträgliche Merkmale dürfen nicht aus mehreren Profilen
   zusammengesetzt werden.
2. Ergebnisintegrität: Zustands-/Objekt-/Stationsschlüssel, Rohwerte versus
   Hüllkurven, Momente/Kräfte/Einheiten, Referenzen auf Modelle und Versionen;
   partial/failed/fixture_only muss die Bemessungsweitergabe blockieren.
3. Typ-/Schema-/Architekturprüfung: strikter JSON-Decoder und Domain müssen
   falsch typisierte Werte und Zusatzfelder ablehnen; Schemasynchronität,
   Import-Linter und statische Typprüfung wiederholen.

## Abgrenzung zur zuletzt vorgeschlagenen Fokus-B-Vorlage

- ULS/SLS sind Grenzzustandsklassifikationen, keine eindeutigen LF-/LK-/Analysezustände.
- Raumkoordinaten allein identifizieren keine Stabstation oder doppelt belegte Position.
- Das Pa-Profil darf nicht nur per Description mit N/mm2 ersetzt werden.
- `frozen=True` ist keine Finite-/Strict-/Extra-Validierung.
- Ein neuer Pydantic-Domain-Kern widerspräche dem ausgelieferten Architekturvertrag.
- Ein gespeicherter Fixture-Wert ist kein numerischer Referenzwert.

## Liefergegenstände

- `review_findings.md`: je Finding ID, Schwere, Dateipfad/Fundstelle,
  reproduzierbarer Gegenfall, Erwartung und tatsächliches Verhalten.
- `tests/test_review_regressions.py`: zusätzliche, verhaltensbezogene Tests.
- `qa/review_run.json`: Paketversion/Manifestbezug, Umgebung, exakte Befehle,
  Werkzeugversionen, Exitcodes, Resultate und zugehörige Logs.
- Änderungsvorschläge separat als Diff. Keine stillschweigende Vertragsänderung.

## Abnahme

Ein Finding gilt erst als behoben, wenn ein reproduzierbarer Test den Fehler
zeigt und nach der Korrektur besteht. Bestehende Tests bleiben grün. PASS nur bei
tatsächlich beobachtetem Lauf; ohne Ausführungsumgebung NOT_RUN mit Begründung.
Der lokale Report des gelieferten Pakets ist von eigenen DeepSeek-Läufen zu trennen.

Keine numerischen Solver-, Eurocode-, Plattform- oder Projektfreigaben ableiten.
Anschließender Herstelleradapter bleibt ein eigener, engerer Integrationsauftrag.
