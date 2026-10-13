# Integrations- und Sync-Entwurf

Status: Vorschlag mit verknüpften Quellen; keine laufende Synchronisation, kein Deployment.

## Zielstruktur und Beziehungen

1. Drive bewahrt bearbeitbare Originale und Formatvarianten. Eine führende Fassung wird je Konzept explizit gewählt. Für den Parser ist SKILL.md der Vorschlag, solange keine neuere fachliche Word-Fassung bestätigt ist.
2. GitHub nexus-platform versioniert geprüfte Spezifikationen, Code, Testfälle und Reviewentscheidungen. Der Katalog verbindet Drive-Datei-ID, Revision/Änderungszeit, Originalhash, Format und Konzept-ID.
3. Nexus verwendet nur freigegebene Artefakte. Dokumente und Transkripte sind Quellenmaterial, niemals automatisch Agentenanweisungen.
4. Die vorhandene Dateiinventur bleibt getrennt: Ihr Schema und die gemessene Abdeckung werden nicht mit Konzept-IDs oder geschätzten Quellhashes überschrieben.

Beziehungsmodell: Konzept → Quellrevision → Formatvariante/abgeleitetes Artefakt → Prüfbericht → Freigabe → konsumierendes Modul.
Beziehungen erhalten Typen wie derived_from, reviewed_by, supersedes und used_by. Gleicher Titel bedeutet weder gleiche Bytes noch gleichen Inhalt.

## Drei Komponenten

| Komponente | Eingang / Ausgang | Rolle und Grenze |
|---|---|---|
| Live-Gespräch | Mikrofonereignisse → Audioantworten und vorläufiges Transkript | Gemeinsame Oberfläche; Mensch hat Vorrang, Antworten abbrechbar, nur ein KI-Sprecher gleichzeitig. Anbieteradapter separat verifizieren. |
| Transkriptionsnachbearbeitung | Freigegebene Aufnahme → Async-Auftrag → versioniertes Ergebnis | GoTranscript-Kandidat für spätere Korrektur/Benchmark. Keine Voraussetzung für flüssiges Sprechen. |
| Normen-Wissenspipeline | Originaldokument → Extrakt → geprüfte Quellenstellen/Chunks | Original und Ableitungen getrennt; Normausgabe und nationale Anhänge eindeutig; Export nur mit bestandenen Prüfungen. |

Gemeinsamer Nenner ist ein Evidence-Register. Ein Sprachturn referenziert transcript_revision und gegebenenfalls freigegebene norm_chunk_ids. Eine spätere Transkriptkorrektur überschreibt keinen alten Prüfbericht: Sie erzeugt eine neue Revision und markiert abhängige Entscheidungen als erneut prüfbedürftig.

## Sync-Vertrag, zunächst manuell

- Explizite Allowlist der Drive-IDs aus catalog.json; keine pauschale Verteilung des gesamten Drives.
- Quellmetadaten und Revision lesen, Originalbytes abrufen, SHA-256 berechnen, Metadaten erneut lesen. Bei Änderung während des Abrufs abbrechen und neu beginnen.
- Native Google Docs als explizit benannte Exportartefakte mit Exportformat/-zeit behandeln; ein Exporthash ist kein Hash einer nativen Originaldatei.
- Abgleich mit zuletzt übernommenem Quellstand und aktuellem Git-Head. Bei Änderungen auf beiden Seiten Konfliktbericht statt Überschreiben.
- Importbranch und PR enthalten Katalogdelta, geprüfte Artefakte, Transformationsprotokoll und Review. Keine direkte main-Aktualisierung.
- Fehlende Dateien als missing/unresolved markieren; keine automatische Löschung. Formatumwandlung erzeugt eine Beziehung, keinen stillen Ersatz.
- Geheimnisse, Rohaufnahmen und lizenzbeschränkte Inhalte nicht automatisch in Git übernehmen. Exportziel und Zugriffsrecht gehören zur Artefaktfreigabe.
- Unveränderter Quellstand erzeugt kein Duplikat. Verschobene/umbenannte Dateien werden über ihre ID zugeordnet.
- Automatisierung erst nach nachgewiesenem manuellen Durchlauf; Zeitplan und Ausführungsidentität sind noch nicht festgelegt.

## Umsetzung in prüfbaren Schritten

1. **Quellenbasis abschließen:** neue Word-Fassung identifizieren; Originalhashes, Formatvergleich und kanonische Fassung festhalten. Abnahme: keine ungeklärte Variantenzuordnung.
2. **Belegschema und Validator:** source_refs[], Normausgaben, Blockzuordnung, Hashprüfung, Seiten/BBox und fail-closed Freigabe. Abnahme: manipulierte Belege, alte Restfehler und falsche Ausgaben werden verworfen.
3. **Parser-Prototyp:** kleine selbst erstellte/geeignet lizenzierte Fixtures: Text, Scan, Mischdokument, Tabelle, Anhang A.1, mehrseitige Formel. Abnahme anhand unabhängiger Referenzannotation, nicht nur Zustimmung eines LLM.
4. **Voice-Prototyp:** zuerst Mensch plus eine KI, danach optional zweite KI mit getrennter Reviewrolle. Abnahme: Unterbrechen, Stummschalten, Ende, Verbindungsabbruch und keine Selbstgesprächsschleife.
5. **Async-Adapter:** zunächst lokale Callback-Fixtures und Testmodus. Abnahme: Wiederholung, Korrekturrevision, Refund/Cancel, Fehler und Wiederanlauf. Bezahlte Echtaufträge gesondert beauftragen.
6. **CI/Sync:** Prüfungen an PRs binden; fehlgeschlagene Prüfer blockieren die Freigabe. Cloud Build ist optional für spätere Google-Cloud-Builds/Deployments, kein benötigter Drive-Sync-Baustein.

GitHub Actions hat tarifabhängige Kontingente; tatsächlichen Accountstatus vor Ausführung prüfen. Cloud-Build-Abrechnung und Guthaben werden durch diesen Entwurf nicht verändert.

## Freigabeentscheidung

Planer liefert überprüfbare Anforderungen und Artefakte. Reviewer prüft unabhängig gegen denselben unveränderten Belegsatz; bei fachlichem Streit zweite Gegenposition bzw. menschliche Entscheidung. Gespeichert werden Befunde, Quellen, Tests und Entscheidungen, keine freien internen Gedankengänge. Fachliche Berechnungen erfolgen durch versionierte Python-Skripte mit Einheiten- und Testnachweisen.
