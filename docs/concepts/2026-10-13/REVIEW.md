# Inhaltsprüfung und unabhängige Gegenprüfung

Stand 2026-10-13. Ergebnis: Konzepte dokumentarisch integrierbar; produktive Freigabe ausstehend.

## Quellen und Verfahren

[S1: SKILL.md](https://drive.google.com/file/d/1vo_0gccV1Vg-lUrGlCzmazYPqVlyeH7p/view), [S2: Human-Transcription-Markdown](https://drive.google.com/file/d/1tMW2Km2Kj_2JUfK-r54EN99PUGc3RoVI/view). Weitere Fassungen und Metadaten: [Katalog](catalog.json).

Primärprüfung: lesbarer Text aller katalogisierten Dateien. Unabhängiger Agent independent_concept_review prüfte S1 und S2 lesend und lieferte eigenständige Gegenbefunde. Das ist eine zweite Agentenprüfung, kein Nachweis eines anderen Modellherstellers und keine fachliche Freigabe durch einen Prüfingenieur. Alle sechs Gegenbefunde wurden übernommen. Keine Runtime- oder visuelle Layoutprüfung.

## Priorisierte Befunde

| ID | Priorität / Quelle | Befund und Konsequenz | Abnahmekriterium |
|---|---|---|---|
| F01 | P1, S2: How it works, mode, turnaround_time | Datei-URL und späterer Callback; live bedeutet bezahlter Auftragsmodus. Kein belegter Echtzeit-/WebRTC-/MCP-Stream. | Async-Adapter außerhalb der Live-Gesprächsschleife; eigene Streaming-Schnittstelle separat evaluieren. |
| F02 | P1, S1: Kernprinzip, Parser-Auswahl | Parser/OCR-Extrakt als alleinige Ground Truth kann Fehler konservieren. Dokumentmedian >50 Zeichen übersieht einzelne Scan-/Fehlerseiten. | Originalbytes, separate Extrakthashes, Werkzeug-/Modellversionen und Konfiguration erhalten; seitenweise Prüfergebnisse; Formeln, Tabellen und Symbole gegen Originalansicht prüfen. |
| F03 | P1, S1: Pydantic-Schema | Ein source_hash und eine page pro Chunk genügen für mehrere Blöcke/Seiten nicht. Version optional, Kapitelbeispiel ohne Normausgabe. | source_refs[] mit doc_id, Ausgabe, block_id, Hash, Seite/BBox; getrennte Quell-/Chunk-Hashes; strikte Hash-, Seiten- und BBox-Prüfung. |
| F04 | P1, S1: P3 | abort_if prüft nur new_violations. Alte ungelöste Fehler können bestehen bleiben. | Jede Revision erneut vollständig prüfen; nur valid=true UND leere Gesamtfehlerliste UND bestandene maschinelle Prüfungen zulassen. Fehler, Timeout, Schemaabweichung, Limit → Quarantäne. |
| F05 | P1, S1: P2, Datasets | Hash allein enthält keinen fachlichen Beleg; Valid-Rate auf Gold misst keine Falschfreigaben auf Negativfällen. | Verifizierte Quellblöcke an Reviewer; Negativ-/Delta-Sätze versionieren; falsche Normausgabe, Seiten, Symbole und Einheiten als Pflichtfälle prüfen. |
| F06 | P2, S2: Callbacks, Updates to downloaded files | Wiederholte Callbacks und später korrigierte Ergebnisse können gleich aussehen. Nur order_id zu deduplizieren verliert Korrekturen. | Persistente Jobzustände, authentifizierte Statusabfrage, idempotente Verarbeitung plus neue Ergebnisrevision bei verändertem Inhalt. |

Weitere Primärbefunde:

- S1/P1 erzwingt numerische Kapitelnummern. Anhänge wie A.1, Vorworte und unnummerierte Abschnitte brauchen eigene Strukturtypen. Eine Blockzuordnung muss maschinell auf Vollständigkeit geprüft werden.
- S1/Modultabelle enthält Abbildungen und Normprofilfilter; im YAML fehlen explizite entsprechende Stufen. Tabellenzellen, verbundene Zellen, Fußnoten, Formelausschnitte und Einheitenzuordnung benötigen eigene Artefakte und Tests.
- S1/Schutzregeln sind ein vorgeschlagener Umgang mit Lizenzen, kein belegter Rechtsnachweis. Öffentlich lesbar ist kein maschinenprüfbarer Nachweis eines Nutzungsrechts. Die Ein-Satz-Regel wird nicht als rechtliche Freigabe übernommen. Pro Quelle Rechtebeleg, erlaubte Zwecke und Zielgruppen erfassen; ungeklärte Exporte sperren.
- S2 enthält Anbietertext und kopierte Beispiele mit Markdown-Escapes/HTML-Entities, nicht bereits ausführbaren Adaptercode. Beispiele unverändert als Evidenz behandeln und gesonderte validierte Request-Fixtures erstellen.
- S2/auto_retranscribe kann einen zusätzlichen bezahlten Human-Auftrag auslösen. Im ersten Adapter standardmäßig deaktivieren; separate Preisprüfung und explizite Beauftragung.
- Drei API-Schlüssel allein gewährleisten keine unabhängige Prüfung. Planer und Reviewer benötigen getrennte Kontexte, einen gemeinsamen unveränderten Belegsatz und dokumentierte Konfliktauflösung.

## Fassungsabgleich

SKILL.md, DOCX, PDF und das konvertierte Google Doc enthalten dieselben zentralen Konzeptabschnitte. Eine vollständige Gleichheit ist nicht nachgewiesen.

Der PDF-Textabruf verbindet beispielsweise pdf_sha256: Hash mit class TextBlock und endet im Dataset-Satz auf retrieva. Der DOCX-Abruf enthält den vollständigen retrieval-Satz, hängt aber die Modultabelle ans Textende. Das können Export- oder Extraktionseffekte sein; ohne Seitenrendering ist die Ursache offen. Code aus diesen Extrakten nicht als ausführbar freigeben.

Die vom Nutzer anschließend erwähnte neue DOCX-Konvertierung ist noch nicht eindeutig durch eine zusätzliche Drive-ID identifiziert. Konvertierungsrichtung und führende Fassung nicht aus Dateinamen ableiten.

## Externe Plausibilisierung

- [GoTranscript API](https://gotranscript.com/api): Auftrags-/Callback-Modell; vor Adapterbau aktuellen Vertrag und produktbezogene Parameter erneut abgleichen.
- [PyMuPDF Text](https://pymupdf.readthedocs.io/en/latest/recipes-text.html): Extraktionsreihenfolge kann von der Lesereihenfolge abweichen. Ein Extrakt allein belegt keine Layouttreue.

## Noch offen

Originaldateien herunterladen und hashen, PDF-/Word-Seiten rendern, Symbole/Tabellen visuell abgleichen; kanonische Bearbeitungsfassung festlegen; Parser- und Adapterimplementierungen erstellen und gegen unabhängige Fixtures testen. Der lokale Prozessstart scheitert aktuell an einem Infrastrukturfehler, nicht an einer abgeschlossenen negativen Inhaltsprüfung.
