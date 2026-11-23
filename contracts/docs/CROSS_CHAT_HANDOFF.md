# Cross-Chat-Handoff — projektneutral

## Auftrag und Lieferumfang

Wiederverwendbare Artefakte statt projektgebundener Beispiele erstellen.
Dieses Paket setzt den Auftrag als eigenständige Software-Referenz um. Es wurde
kein bestehendes Repository verändert, kein Commit/Push/Deploy ausgeführt und
kein CAD-/Statikprogramm angesprochen.

## Nachweisbarer Stand

Das Paket enthält ausführbare Verträge, zwei Ports, Capability-Matching,
Ergebniszuordnung, JSON-Rundlauf, Schemaexport und Fixture-Replay. Tatsächliche
Test-/Werkzeugergebnisse stehen in `qa/report.json`, `qa/pytest.xml` und den Logs.
Dieser Lieferstand ist nicht mit den zuvor als NOT_RUN gekennzeichneten
Cross-Chat-Codevorschlägen gleichzusetzen: Die Implementierung wurde konsolidiert
und teilweise bewusst anders strukturiert.

## Getroffene Implementierungsentscheidungen — DERIVED

1. Ein SI-Kanon und ein führendes Python-Typmodell; keine frei kombinierbaren Einheiten.
2. Reine, immutable Domain-Verträge mit tatsächlicher Literal-/Wertprüfung.
3. Zustandsweite konservative Capability-Prüfung; kein angenommener Lastpfad
   aus dem Fehlen direkter Stablasten.
4. Referenzzustand und Formfindungsziel sind verschiedene Verträge.
5. LF/LK werden über explizite Analysezustände mit Lastfaktoren identifiziert.
6. Rohresultate tragen explizite Schlüssel. Hüllkurven bleiben außerhalb v0.1.
7. Fixture-Replay wird als `fixture_only` gekennzeichnet und vom Bemessungsgate abgewiesen.
8. JSON-Strukturschemata sind generiert; semantische Python-Invarianten bleiben Pflicht.

## Korrekturen gegenüber eingereichten Vorschlägen

- Die Annahme „Knotenlast auf anderem Knoten → kein Stabprofil erforderlich“
  wurde verworfen. Ohne Lastpfad-/Konnektivitätsnachweis ist sie unzulässig.
- `Literal`-Annotationen wurden nicht mit Laufzeitvalidierung verwechselt.
- Ein Reaktionsmoment benötigt keine gleichzeitig angeforderte Reaktionskraft.
- Ein axialer Zug-only-Stab benötigt nicht generell einen Vorspannzustand.
- Es gibt keinen erfundenen allgemeinen Mindeststabwert von 1 mm.
- Mehrere Capability-Alternativen werden nicht still überschrieben oder vereinigt.
- Ein Schemafeld, das ein Quelldetail nicht kennt, legitimiert keinen Datenverlust.
- Norm-ID, Normausgabe und nationaler Anhang bleiben getrennt.

## Nächster sinnvoller Review

DeepSeek soll die ausgelieferten Dateien prüfen und Findings mit Dateipfad,
betroffenem Vertrag, reproduzierbarem Gegenbeispiel und erwartetem Verhalten liefern.
Keinen neuen Parallelvertrag und keine ungetestete Ersatzarchitektur erzeugen.
Besonders zu prüfen: Elementformulierungen, Total-/Initialzustandssemantik,
Schnittgrößenvorzeichen und Umfang späterer Fachverträge.

Ein reales Solver-Adapter-MVP folgt als eigener Auftrag nach Festlegung seines
Funktionsumfangs und eines unabhängigen Referenzfalls. Erforderlich sind
Lizenz-/Versions-/API-Nachweis, vollständiger Input-Readback, explizite Ablehnungen,
Konvergenz-/Gleichgewichtsprotokolle und unabhängige Ergebnisreferenzen.

## Grenzen

Die Standards-/Fachprüfung der Verträge ist nicht abgeschlossen. Numerische
Solverfähigkeiten, IFC/DXF/DWG-Mappings, Excel-Neuberechnung und normative
Bemessung sind NICHT implementiert oder nachgewiesen. Aus Software-QA folgt
keine menschliche oder behördliche technische Freigabe.
