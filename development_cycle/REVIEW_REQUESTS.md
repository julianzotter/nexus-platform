# Independent Review Requests — Claude / Gemini

Beide Reviewer erhalten CONTRACT.md, cycle.py, test_cycle.py, README.md sowie review_bundle.json. Verifiziere die Dateihashes aus dem Manifest; nenne den bundle_sha256 deiner Antwort. Prüfe denselben eingefrorenen Stand unabhängig, ohne zunächst die andere Reviewantwort zu lesen.

## Claude — Architektur und Schnittstellen

Ziel: möglichst einfacher, robuster, agiler und kreislauffähiger Entwicklungsprozess. Prüfe Rollen vs. Runtime, funktionale Schichten, Vertragsgrenzen, Fehlerbehandlung, Statusmodell, zentrale Ablage, Rekonstruktion der Deltas und unnötige Prozessschwere. Suche Brücken zu vorhandenen NEXUS-Komponenten statt Parallelarchitektur.

## Gemini — Algorithmus, Evidenz und Gegenbeispiele

Prüfe Datenverträge, deterministischen N/N-1/N-2-Vergleich, Baseline-Versionierung, Annahmen, Grenzen von Accuracy/Confidence, Hashprüfung, Abbruch/Partial Delivery und Testabdeckung. Denke vorwärts, rückwärts und lateral. Unterscheide Codebefund, tatsächlichen Test und bloße Behauptung. Keine erfundene API-/Toolausführung.

## Gemeinsames Antwortformat

bundle_sha256; actual_executor; model/version oder unknown; ausgeführte Tests oder NOT_RUN; wichtigste drei Findings mit Datei/Funktion; Gegenbeispiel; minimaler Reparaturvorschlag; messbares Abnahmekriterium; Wiederverwendung/vereinfachende Alternative; verbleibende Annahmen.

Priorität: P0 falsche Ergebnisse/Datenverlust/Vertragsbruch; P1 funktionale Lücke; P2 Vereinfachung. Fachliche Freigabe und Entwicklungsfortschritt unterscheiden. Keine Pauschalregel, die unnötig alles blockiert. Nicht pauschal APPROVED melden, wenn ein entscheidender Nachweis fehlt.

## Aufrufstatus

Vorbereitete Aufträge, noch nicht an externe Provider ausgeführt. Der vorhandene nexus-platform-Orchestrator kann später als Transportadapter dienen; Zugriff auf dessen tatsächlich laufende Instanz oder Provider-Authentifizierung ist in dieser Sitzung nicht verfügbar. Kein automatischer Versand des Repositorys an alle Cloud-Modelle.
