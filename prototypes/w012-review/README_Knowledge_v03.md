# W012 · Lokale Evidenzsuche v0.3

`build_knowledge.py` erzeugt eine zusätzliche, lokale Suchprojektion aus der bestehenden W012-Datenbank. Alle vorhandenen Tabellen und Zeilen bleiben erhalten. Keine Cloud-Operation, kein Live-Sync, keine technische Freigabe.

## Ausführung

Im Verzeichnis `W012_Review`:

```sh
python build_knowledge.py
python build_knowledge.py --search PAR-01
python build_knowledge.py --search Gipskarton
python -m unittest -v test_knowledge.py
python build_knowledge.py --extras evidence_inputs --output snapshot_v03_final
```

Der Builder benötigt nur Python-Standardbibliotheken mit SQLite-FTS5. Der Test der tatsächlichen HTML-Suchfunktion verwendet zusätzlich das vorhandene Node-Programm, ohne zusätzliche npm-Pakete. Ein bestehendes Ausgabe-Verzeichnis wird niemals überschrieben: jeder neue Stand erhält ein neues Verzeichnis.

## Datenvertrag

- `knowledge_documents`: `id`, `title`, `body`, `url`, `status`, `source_kind`; zusätzlich `normalized_id`, `search_text`.
- 273 Basisdokumente: 88 Quellen, 62 Records, 18 Aufbauten, 105 Schichten. Aufbau-IDs tragen `ASSEMBLY:`; Schicht-IDs bestehen aus Aufbau-ID und `:L<ordinal>`.
- `body` erhält vollständige Originalzeilen und zugehörige Quellenmetadaten. Ursprüngliche Tabellen bleiben als unveränderte Projektion separat verfügbar.
- `--extras` liest rekursiv UTF-8-Dateien mit Endung `.md` oder `.json`. JSON-Listen mit den sechs Stringfeldern `id,title,body,url,status,source_kind` werden zeilenweise aufgenommen; IDs, Quellenlinks und Evidenzstatus bleiben erhalten. Weitere Metadaten werden vollständig an `body` angehängt. Doppelte normalisierte IDs werden abgelehnt. Andere JSON-/Markdown-Dateien werden vollständig als ein Dokument mit ID `EXTRA:<relativer Pfad>` und Status `UNVERIFIED` aufgenommen. JSON muss syntaktisch gültig sein. Übernommene Statuswerte sind Quellenangaben und erteilen keine technische Freigabe; die globale Freigabe bleibt `NOT_GRANTED`. Nur gewünschte Eingabedateien in den Ordner legen; keine Ausgabeordner hineinlegen.
- Die deutsche Suchnormalisierung reduziert Groß-/Kleinschreibung, `ß→ss` und kombinierende Akzentzeichen. Alle Suchbegriffe müssen als Wortpräfixe vorkommen. Exakte IDs werden zuerst ausgegeben. SQL-Parameter und zitierte alphanumerische FTS-Tokens verhindern die Interpretation eingegebener FTS-Operatoren.
- CLI liefert maximal 50, HTML maximal 100 sichtbare Treffer; HTML zeigt die gesamte Treffermenge als Zähler. Ohne Suchtext zeigt HTML alle Dokumente, CLI keine Ergebnisse.
- `snapshot_id` identifiziert kanonische Dokumente, Basisdatei-Hash, Builder-Hash und Ergänzungsdatei-Hashes. Derselbe Wert steht in `knowledge_metadata`, JSON, HTML und Manifest. Er bezeichnet diesen Suchstand, nicht die Revisionen der verlinkten Originalquellen.
- Das Manifest enthält SHA-256 für SQLite, JSON, HTML und das lokale Prüfprotokoll. Das Prüfprotokoll enthält gemessene Einzelabfragezeiten; dadurch variieren Prüfprotokoll und Manifest zwischen Läufen. SQLite, JSON und HTML sind für gleiche Inputs und gleiche SQLite-Runtime bytegleich reproduziert und getestet.

## Grenzen und Prüfungen

Getestet: vollständige Übernahme der Basistabellen; SQLite-Integrität/Fremdschlüssel; SQL/JSON/HTML-Konsistenz; gemeinsame Snapshot-ID; Datei-Hashes; exakter ID-Vorrang; Schichtmaterial-Suche; sichere Behandlung von Sonderzeichen; Python/JavaScript-Ergebnisgleichheit für Referenzabfragen; reproduzierbare Ausgabe; unveränderliche Ausgabeordner; Ergänzungsstatus.

Lokale Suchzeiten umfassen einzelne Queries mit Zeilenmaterialisierung. Sie belegen weder einen allgemeinen Geschwindigkeitsgewinn noch Download-, Cloud-, LLM- oder Synchronisationszeiten. Verlinkte Originalquellen wurden beim Build nicht neu gelesen. Vorhandene Quellenrevisionslücken bleiben sichtbar. Ein Empfänger muss Manifest/Hashes und eigene Abfragen selbst prüfen und seinen Empfang gesondert bestätigen.
