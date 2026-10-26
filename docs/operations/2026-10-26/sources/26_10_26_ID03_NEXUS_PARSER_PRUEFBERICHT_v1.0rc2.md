# NEXUS Parser Untersuchung und Implementierung

Status: TESTED_RELEASE_CANDIDATE, Version 1.0.0rc2. CI abgeschlossen und bestanden; unabhängige Abnahme ausstehend. Keine behauptete Produktionsfreigabe ohne diese Abnahme.

## Lieferung

- Commit: 50ef96e026efca46a51034a16e65543cf1b6f72d
- PR: https://github.com/julianzotter/AI-ENGINEERING-SYSTEM/pull/4
- 123 lokale Tests bestanden, davon 49 Parser-Tests. Typprüfung, Lint, pip check und Wheel-Build bestanden.
- Parser-Coverage: 96.57 Prozent.
- Drei reale PDFs mit 205 Seiten verarbeitet. Deutsche und englische OCR mit echtem Tesseract getestet. Die 205 Seiten wurden nicht vollständig manuell gegen Tabellen und Formeln geprüft.
- 112 Python-Dateifundstellen mit 69 unterschiedlichen Inhalts-Hashes; 12 ZIPs mit 67 Python-Mitgliedern statisch untersucht.
- Ausgegrenzte Daten-/Vendor-/Cache-Verzeichnisse und begrenzte Ordnerantworten verhindern die Behauptung eines vollständigen Drive-Dateiinventars. Die Methodenprüfung ist auf die katalogisierten Quellen begrenzt.

## Architektur

Originalbytes → native Textansicht und Seitenblöcke → optionale OCR in derselben Pipeline → exakte Chunk-Intervalle → Pydantic und Abdeckungsprüfung → atomare Artefakte und SQLite-Ledger → NEXUS DRAFT-Adapter.

Kein Solver. Keine automatische Norm-, Rechts- oder Inhaltsfreigabe. Keine WORM-Behauptung. Keine verdeckten Modell-Downloads.

## Abnahmegrenze

Software ist als reproduzierbarer Kandidat geliefert. Der konkrete CI-Run ist im PR verlinkt. Linux-/Windows-Nachweis, unabhängiger Review und Zielumgebungsabnahme müssen gegen den gelieferten Commit belegt werden. Semantische Segmentierungslogik ist getestet; Embedding-Modellqualität und Retrieval-Effektivität bleiben separate Evaluationsaufgaben.



# Parserfamilie Untersuchung und Entscheidung

## Ergebnis

Der Ausgangsstand wird als historische Parser-Variante registriert, nicht als produktionsgeprüfte Gesamtpipeline. Das neue Modul nexus_parser konsolidiert den quellengebundenen PDF- und UTF-8-Pfad in Version 1.0.0rc2. Produktivstatus und externe Inhaltsfreigabe bleiben durch RELEASE_GATE.json getrennt dokumentiert.

## Vergleich der Methoden

| Familie | Extraktion | Segmentierung | Befund |
|---|---|---|---|
| robust_pdf_extractor | PyMuPDF, optional OCR, Seitenmarker | keine | brauchbare Vorstufe; kein Originalhash und keine Layoutvollständigkeitsprüfung |
| Engineering v5.6 klein | PDF-Blöcke, Schriftgrößenheuristik | Struktur und Zeichenlimit | OCR-Vorstufe nicht konsumiert, Kurztextverlust, Kontextfehler, schwache Quellenregex |
| Engineering v5.6 groß | mehrere Extraktoren, Hierarchie, Metadaten | Hierarchie und Regex | eigenständiger Inhalt unter gleichem Versionslabel; kein Embedding-Nachweis allein durch Namen SemanticChunker |
| Engineering v5.0 und v4 Bridges | PDF/DOCX/TXT/JSON/XLSX; teilweise Tabellen, Zellbezüge | überwiegend Absatz und Überschrift | wiederverwendbare Teilmodule; separate Excel-Fachprüfung nötig |
| text_semantic_parser | TXT/MD | Satz-Embeddings, Cosinus, Perzentil | echtes semantisches Verfahren; Kurzsatzfilter, fehlende Quellenintervalle und Modellabnahme offen |
| pdf_parser v2 bis v4 | nativer PDF-Text, optionale Randbeschneidung | PDF-Inhaltsverzeichnis | strukturelles Verfahren; gleich benannte Kopien per Hash prüfen |
| pdf-chunk-parser | PyMuPDF und Typisierungsregex | Inhaltsverzeichnis oder Zeichenfenster mit Overlap | kein Bedeutungsmodell |
| raw_batch 1 bis 3 | native Extraktion; teils OCR-Platzhalter oder zwei Engines | keine oder Zeichenstatistik | Längenvergleich beweist keinen gleichen Inhalt; OCR-Platzhalter nicht als funktionsfähige OCR akzeptieren |
| pdf_raw_extractor | pdfminer, optional Camelot, Bilder, Rendering | keine | Funktionsbaustein für Text/Tabellen/Abbildungen, keine allgemeine Verlustfreiheitsgarantie |
| universal_raw_miner und EC7 Universal | Text und Metadaten; EC7 zusätzlich pdfplumber-Tabellen und Scan-Triage | keine | Scan-Triage überspringt Quellen; keine vollautomatische OCR-Pipeline |
| Docling NORMENPARSER | DocumentConverter nach MD | keine im Wrapper | Konverter-Adapter, kein bereits integrierter semantischer Chunker |
| struct_parser und struct_layer | MD-/Tabellenzuordnung oder PDF-Strukturlayer | Regex/Überschriften | getrennte Rohtext- und Strukturansicht sinnvoll; keine verifizierte Normlogik |
| MoE und DeepMiner | Textregex und Parameter-Mining | Zeichenfenster/Parameterfunde | kein Multi-Agent- oder Bedeutungsnachweis; heuristische Einheitenkorrekturen nicht übernehmen |
| pdfcpu und OmniDocBench | Vendor-Werkzeug bzw. Benchmark-Korpus | keine NEXUS-Kernimplementierung nachgewiesen | nicht als neue eigene Parsermethode registrieren |

## Reproduzierte Ausgangsfehler

1. Im kleinen v5.6 wird der neue Überschriftenkontext vor dem Flush des alten Texts gesetzt. Alter Inhalt erhält den neuen Kontext.
2. _emit_chunk entfernt Texte unter 80 Zeichen. Dies kann kurze Anforderungen vollständig entfernen.
3. Die Normregex erkennt ÖNORM B 1995-1-1 nicht. Nichtleere Platzhalter wie EN ???? bestehen die bisherige Quellenvalidierung.
4. Der FSM-Hard-Gate lässt die Berechnung trotz leerer oder unpassender Wissensbasis weiterlaufen.
5. Phase 2 liest die PDFs erneut; OCR-Markdown aus Phase 1 bleibt ungenutzt. Importierte OCR-Module allein sind kein implementierter OCR-Pfad.
6. Batch- und Anwendungsfehler werden nicht zuverlässig in einen Abbruchstatus überführt. Die Bezeichnung ERGEBNIS ZERTIFIZIERT in der Demo ist kein Zertifikat.
7. Mindestens zwei ungleiche Implementierungen heißen v5.6. Quellenidentität muss Version plus Datei-Hash verwenden.

## Umsetzung und verbleibende Grenzen

Neu implementiert: Originalsnapshot, rohe native Textansicht, Seiten-/Block-JSON, konservative Struktursegmentierung ohne Mindestlängenfilter, exakte Fragmentintervalle, strikte Schemas, getrennte IDs/Hashes, expliziter OCR-Pfad, optionale Tabellen, semantische Vektorschnittstelle, atomare Bundles, SQLite-Registry, Hashprüfung, Fehlerexit und Windows-Starter.

Nicht behauptet: verlustfreie semantische PDF-Extraktion; korrekte Formelrekonstruktion; fachlich freigegebene Normregeln; Rechtsverbindlichkeit aus OIB-Zitaten; WORM; Modellqualität; automatische 512-Token-RAG-Indexierung; geprüfter Windows-Zielbetrieb ohne CI-Nachweis. Extrahierte Originalformulierungen müssen in ihrem gültigen Normkontext geprüft werden. Die Methode enthält keinen Tragwerks-Solver.

## Abnahme und Abschlusskriterien

Die Untersuchung der katalogisierten Parsermethoden und der Ausbau des Kernmoduls sind dokumentiert. Tests, Coverage, Typprüfung, Lint, Wheel-Build und Real-Dokumentläufe werden als tatsächliche Ausführungsnachweise geliefert. CI und Freigabeentscheidung werden gegen den konkreten Commit geführt. Solange Windows/CI oder unabhängiger Review nicht belegt sind, lautet der Softwarestatus Release Candidate. Kein Fortschrittsbericht darf diese offenen Nachweise in APPROVED umetikettieren.



# NEXUS Parser Betriebsanleitung

Version 1.0.0rc2. Wiederverwendbare lokale PDF und UTF-8 Ingestion für NEXUS. Softwarestatus: getesteter Release Candidate. Extrahierte Inhalte bleiben REVIEW_REQUIRED. Keine fachliche oder rechtliche Freigabe wird aus Extraktion, Hash oder Schema abgeleitet.

## Zweck und Systemgrenze

Der Parser ersetzt den unverbundenen Ablauf aus OCR-Markdown, erneutem PDF-Parsing und Solver-Demo. Er übernimmt Dateien in eine gemeinsame strukturierte Darstellung. Originalbytes, nativer PDF-Text und extrahierte Blöcke bleiben getrennt erhalten. PDF- und Textdaten werden niemals ausgeführt. Keine LLM-Aufrufe, Modell-Downloads, Cloud-API, Formelauswertung oder automatische VectorDB-Indexierung.

Unterstützt: lokale PDF, UTF-8 TXT und MD. Native PDF-Blöcke mit Seite, Index und Bounding Box; optional Tesseract OCR; optionale Tabellenerkennung. DOCX/XLSX/HTML sind in dieser Version kein ausführbarer Eingabevertrag. Die vorhandenen Docling- und Excel-Parser bleiben separat katalogisiert.

## Installation

Python 3.11 oder 3.12 in einer eigenen virtuellen Umgebung. Vom Repository-Verzeichnis:

```powershell
py -3.12 -m venv .venv-parser
.venv-parser\Scripts\python.exe -m pip install -r docs/parser/requirements.lock.txt
.venv-parser\Scripts\python.exe -m pip install --no-deps -e .
.venv-parser\Scripts\python.exe -m nexus_parser --doctor
```

Linux: `python3 -m venv .venv-parser`; danach `.venv-parser/bin/python` anstelle des Windows-Pfads verwenden. Tesseract ist ein separat installiertes Programm, keine durch pip bereitgestellte OCR-Engine. Für deutsche Scans müssen `deu` und `eng` verfügbar sein. Ein eigener Sprachdatenordner wird über die Tesseract-Umgebungsvariable TESSDATA_PREFIX konfiguriert. Das Programm lädt Sprachmodelle nicht selbst nach.

```powershell
.venv-parser\Scripts\python.exe -m nexus_parser --doctor --ocr --ocr-languages deu+eng
.venv-parser\Scripts\python.exe -m nexus_parser C:\NEXUS\dokumente --output C:\NEXUS\parsed --ledger C:\NEXUS\parsed\registry.sqlite --ocr --ocr-languages deu+eng --tables
```

`start_parser.bat QUELLORDNER AUSGABEORDNER` verwendet die lokale venv und bricht bei Fehler mit Exitcode 1 ab. Der Batch-Standard verarbeitet native PDFs und Text; OCR wird explizit über den Python-CLI-Aufruf aktiviert. Die Ausgabe darf kein Unterordner des Eingabeordners sein. Eingabe-Symlinks und Symlinks im Ausgabepfad werden abgewiesen.

## Datenvertrag und Ablauf

1. Dateiformat, Größenlimit und Quellenhash prüfen. Verschlüsselte oder reparaturbedürftige PDFs werden abgewiesen. Eine echte leere PDF-Seite bleibt als BLANK_PAGE erhalten; ein vollständig inhaltsloses Dokument wird abgewiesen.
2. Originalbytes unverändert kopieren. Native Textreihenfolge separat in native.txt erhalten. Extrahierte PDF-Blöcke sind geometrisch sortiert; diese Reihenfolge ist kein Nachweis semantisch korrekten Leseflusses.
3. Ohne nativen Text: OCR nur nach expliziter Aktivierung und erfolgreicher Sprachdatenprüfung. OCR-Text geht direkt in dieselben Block-, Chunk- und Validierungsfunktionen wie nativer Text ein.
4. Struktur-Chunking an erkannten nummerierten Überschriften; pro Block harte Obergrenze max_chars. Kein Mindestlängenfilter. Auch ein einzelnes Zeichen bleibt erhalten. Fragmentintervalle referenzieren exakte Zeichenpositionen innerhalb des Quellblocks.
5. Strikte Pydantic-Prüfung. Rekonstruktion aller Blocktexte aus Chunks muss exakt möglich sein, ohne Lücken oder Überlappung. Das prüft die Verarbeitung des extrahierten Texts, nicht die Vollständigkeit gegenüber dem visuellen PDF.
6. Veröffentlichung als atomar umbenanntes Bundle. Inhaltsmanifest prüft alle Bundle-Dateien. Vorhandene gleiche Run-ID wird nur nach Hashprüfung wiederverwendet. Geänderte Quelle erzeugt eine andere Run-ID.
7. Optionaler SQLite-Ledger mit Transaktion und Ereignishashkette. Extraktionsstatus bleibt REVIEW_REQUIRED. Diese lokale Datenbank ist kein WORM-Speicher und keine kryptografisch signierte Freigabeinstanz.

## Dateien pro Bundle

| Datei | Inhalt |
|---|---|
| source.pdf oder source.txt oder source.md | Kopie der Originalbytes |
| native.txt | Native Textausgabe in ursprünglicher PDF-Streamreihenfolge, Seiten durch Formfeed getrennt |
| extracted.md | Seitenweise lesbare Blocktexte einschließlich OCR |
| document.json | Quellenmetadaten, Seiten, Blöcke, Tabellen, Warnungen, Chunks |
| chunks.jsonl | Einzelne quellengebundene Wissensfragmente |
| config.json und runtime.json | Verarbeitungsparameter und beobachtete Softwareversionen |
| semantic_input.json | Nur im optionalen Vektormodus; Vektoren und Modellidentität |
| hashes.json | SHA-256 aller übrigen Dateien; selbst nicht selbstreferenziell gehasht |

Die Run-ID umfasst Quellenhash, Dateiname, Konfiguration, Metadaten, Parser-Version und gegebenenfalls semantische Eingabe. object_id referenziert Quelle und Fragmentintervall; content_hash_sha256 hasht den exakten Chunk-Text. IDs und Inhaltsprüfsummen sind getrennt. Die abgeleiteten Norm-Mentions sind reine Regex-Funde, keine verifizierten Normbelege. Ausgabe, Jurisdiktion, Technikpfad und Rechtspfad können als explizite Metadaten mitgegeben werden; unbekannte Angaben bleiben null. Es werden weder NA/NAD noch Rechtsverbindlichkeit geraten.

```json
{"source_uri":null,"edition":null,"jurisdiction":"AT","language":"de","tech_path":null,"law_path":null}
```

Das JSON zeigt nur das Metadatenformat. Für produktive Quellen muss `edition` die tatsächliche Ausgabe enthalten; der Parser authentifiziert diese Angabe nicht. Aufruf: `--metadata metadata.json`.

## Semantisches Chunking

Standard ist strukturerhaltende Segmentierung. Optional kann `--semantic-vectors vectors.json` für genau eine Quelldatei genutzt werden. Es findet kein Download und keine verdeckte Embedding-Generierung statt. Der Aufrufer liefert pro Block ein lokales Satz-Embedding pro Intervall aus `sentence_spans`. Der Vertrag SemanticInput verlangt Quellenhash, model_id, Modellhash, Schwelle sowie Seiten- und Blockindizes. Fehlende, doppelte oder unbekannte Blöcke werden abgewiesen.

Die Routine vergleicht Cosinusähnlichkeiten benachbarter Satzvektoren. Bei Unterschreitung der expliziten Schwelle entsteht eine Segmentgrenze. Kurze Sätze und Whitespace werden nicht entfernt; die gleiche Intervallprüfung gilt. Semantische Grenzen überschreiten keine Quellblöcke. Algorithmus und Integration sind mit kontrollierten Vektoren getestet; Modellqualität und RAG-Retrieval wurden nicht evaluiert. Die bestehende Datei text_semantic_parser.py ist als Embedding-Prototyp wiederverwendbar, muss jedoch gegen diesen Intervallvertrag adaptiert werden.

Die Repository-Regel 512 Tokens und 20 Prozent Overlap betrifft die spätere RAG-Ansicht. Die hier ausgegebenen kanonischen Quellfragmente sind bewusst nicht überlappend und nicht als Tokenansicht deklariert. Ein Indexer muss daraus separat tokenizergebundene Ansichten erzeugen und die Fragmentverweise erhalten. Es erfolgt kein automatischer Index-Rebuild.

## Prüfung und Freigabe

```powershell
python -m pytest tests/parser -q
python -m ruff check nexus_parser tests/parser
python -m mypy nexus_parser --strict
python -m pip check
python -m nexus_parser --verify AUSGABE_BUNDLE
```

Für die Ledger-verankerte Prüfung: `verify_registered_bundle(bundle, ledger)` aus nexus_parser.review. Manipulationsnachweis setzt einen unabhängig geschützten Ledger oder extern aufbewahrten Manifesthash voraus. Wer Bundle und Ledger vollständig kontrolliert, kann beide neu schreiben. Keine WORM- oder Signaturbehauptung.

Alle RAG-Inhalte werden als untrusted_source_data markiert. Verarbeitungswarnungen sind nicht unterdrückte Freigaben. Das Paket stellt keinen Weg zur automatischen Solver-Freigabe bereit; require_approved blockiert die Übergabe extrahierter Inhalte. Ein späterer fachlich validierter Freigabedienst muss unabhängig angebunden werden.

Softwarefreigabe und Inhaltsfreigabe getrennt behandeln. Release Candidate darf in isolierten Abnahmeläufen verwendet werden. Für produktiven Windows-Betrieb muss die zugehörige CI-Matrix erfolgreich sein. Tabellen, OCR, Formeln, mehrspaltiger Lesefluss und nationale Normzuordnung verlangen quellenbezogene Abnahme. User-Anweisung autorisiert diese Entwicklung und Bereitstellung; sie ist kein erfundener Nachweis bereits absolvierter Tests.

## Betrieb und Wiederherstellung

Originale bleiben unangetastet. Bei Fehler Exitcode 1; staging-Verzeichnis wird entfernt. Bereits erfolgreich abgelegte Bundles bleiben erhalten, keine automatische Löschung. Ein vollständiges Bundle ohne Ledger-Eintrag kann durch denselben Aufruf erneut validiert und registriert werden. Bei Hashabweichung nicht überschreiben: Quelle, Runtime und betroffene Dateien prüfen. Neue Version oder Konfiguration erzeugt neue Bundles. Alte v5-Dateien bleiben als historische Quellen erhalten, werden nicht automatisch migriert oder ausgeführt.

Externe Angaben und Rechtsfragen: siehe SOURCES.md. Bekannte Grenzen und der verbindliche aktuelle Abnahmestatus: siehe RELEASE_GATE.json und REVIEW.md.

## NEXUS Plattformadapter

platform_items aus nexus_parser.platform_adapter bildet die Kernfragmente auf das gelesene nexus-platform Knowledge-Item-Schema ab. Der Aufrufer liefert die bestehende 16-stellige source_file_id aus der dortigen Registry. Keine ID wird durch Abschneiden eines Hashs erfunden. Ausgabe ausschließlich kind=note, status=DRAFT, engineering_result=false. Keine automatische norm_clause- oder VALID-Promotion. Schema-Snapshot: platform-knowledge-item.schema.json, ursprünglicher Schema-Blob ce5bc7913c123fb7042a2a036fa313e96ab4ac58.



# Quellen und Prüfumfang

Stand 26.10.2026. Dateiinhalte sind Primärnachweise der Implementierung, Kommentare und Produktivitätsbehauptungen in Altdateien kein Funktionstest.

## Interne Primärquellen

- AI-PYTHON-PARSE: https://drive.google.com/drive/folders/1nbSlOQkCQ7Yhro3RxtIXW3QLP5yj9nBc
- Ausgangspaket: https://drive.google.com/drive/folders/10U0XeqVpgyhE0Eg7MFN34bnFUmNK6q77
- Engineering-Familie: https://drive.google.com/drive/folders/1PI9oVGt77sgYowGMhu65zOQKqWyM8fJV
- text_semantic_parser.py: https://drive.google.com/file/d/1CTVFYs2u9zHWgBnLuJb4wNAC_m6iP8r2/view
- NORMENPARSER.py mit Docling: https://drive.google.com/file/d/1ADd7BtrbY4rob38ogTJyMObUCVaA_52E/view
- EC7 Universalparser: https://drive.google.com/file/d/1XAYTJoPmFoOv7VjXOdgOAPDry1BpRGpS/view
- struct_parser.py: https://drive.google.com/file/d/1WoYq4FZtlpYmikWNL4OAYIgqJ7tMzBaI/view
- Vollständige Dateinamen, Drive-IDs, SHA-256, Syntaxbefunde und Archivinhalte: method_inventory.json. Keine Gleichsetzung von Dateinamen, Größen oder Versionslabels mit Identität.
- Repository-Anweisungen: https://github.com/julianzotter/AI-ENGINEERING-SYSTEM/blob/efe5ab822d6f4fc43c43f663f018ea7c42f02bd7/AGENTS.md

## Externe Primärdokumentation

- PyMuPDF Text, Lesereihenfolge und Tabellen: https://pymupdf.readthedocs.io/en/latest/recipes-text.html
- PyMuPDF Lizenz und Copyright: https://pymupdf.readthedocs.io/en/latest/about.html und dort License and Copyright
- Pydantic Strict Mode: https://docs.pydantic.dev/latest/concepts/strict_mode/
- Tesseract Sprachwahl und Kommandozeile: https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html
- Sentence Transformers lokale Modellpfade und local_files_only: https://sbert.net/docs/package_reference/sentence_transformer/model.html
- Deutsches Test-Sprachmodell: https://github.com/tesseract-ocr/tessdata_fast/blob/main/deu.traineddata
  SHA-256 der tatsächlich getesteten Bytes: 19d219bbb6672c869d20a9636c6816a81eb9a71796cb93ebe0cb1530e2cdb22d.

Die Betriebsumgebung muss die Lizenzbedingungen der Abhängigkeiten erfüllen; eine Organisationslizenz wird nicht unterstellt. Weder externe Bibliotheksdokumentation noch bestandene Parser-Tests bestätigen die Richtigkeit extrahierter Ingenieurnachweise.

## Abgrenzung der Bestandsaufnahme

118 Verzeichnisse wurden eingesehen, dabei 1701 Einträge beobachtet. Das ist keine Vollständigkeitszahl für den gesamten Drive-Ordner. Ausgabeverzeichnisse, Chat-Archive, Vektor-Datenbanken, Vendor-Bäume und Caches wurden für die Parser-Methodenprüfung begründet ausgegrenzt. Vier begrenzte Ordnerantworten mit 100 Einträgen liegen in diesen Daten-/Chat-Ausgabebereichen; deren Dateiinventar bleibt partiell. Daraus wurde keine vollständige Cloud-Registry behauptet.

Die tatsächlich eingelesenen 112 Python-Dateifundstellen ergeben 69 unterschiedliche SHA-256-Werte. Zwölf methodenbezogene ZIPs wurden ohne Codeausführung aufgelistet; 67 Python-Mitglieder wurden statisch gelesen. Syntaxprüfung ist kein Laufzeitbeweis. Alte Solver, Generatoren und Chat-Pipelines wurden nicht automatisch ausgeführt. Das neue Kernmodul wird durch eigenständige Tests geprüft.

Privater Real-Dokumenttest: B1990-1_2013.pdf, EN1990_2021.pdf und die PDF-Methodenbeschreibung, insgesamt 205 Seiten. Originale und extrahierte Normvolltexte werden nicht ins Repository übernommen. corpus_results.json enthält Identität und Messwerte, keine normativen Volltexte. Es gibt keine behauptete manuell geprüfte Ground Truth für alle Formeln und Tabellen dieser 205 Seiten.



## Integritätsnachtrag

Version rc2 verarbeitet ausschließlich eine vorab kopierte und gehashte Quelle. Ein gezielter Test zur während der Kopie geänderten Datei besteht. Die Real-Dokumenttests wurden für rc2 mit allen 205 Seiten wiederholt. Der erste CI-Lauf war in allen vier Kombinationen erfolgreich; der aktuelle rc2-Commit erhält eine eigene CI-Prüfung. Ein unabhängiger Review wurde nicht fingiert.


## Aktueller CI Nachweis

Commit 50ef96e026efca46a51034a16e65543cf1b6f72d: alle vier PR-Jobs erfolgreich, Linux und Windows jeweils mit Python 3.11 und 3.12. Run: https://github.com/julianzotter/AI-ENGINEERING-SYSTEM/actions/runs/40322175380 . Die unabhängige Code-/Zielumgebungsabnahme bleibt offen. Ein separater Push-Run hatte einen Paket-Setup-Timeout und wurde gezielt wiederholt; daraus wird kein Parser-Testfehler abgeleitet.
