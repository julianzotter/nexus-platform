# Nexus: Voice und Normen-Parser

Stand: 2026-10-13. Dokumentierter Integrationsentwurf, keine aktive Pipeline.

- [Quellenkatalog](catalog.json): Drive-IDs, Formate, Änderungsstände und Prüfgrenzen.
- [Inhaltsprüfung](REVIEW.md): Befunde, Gegenprüfung und Freigabekriterien.
- [Integration und Sync](INTEGRATION.md): Komponenten, Beziehungen und Umsetzungsschritte.
- [SKILL-Textsnapshot](sources/pdf-normen-parser-skill.extracted.txt): lesbarer Connector-Text; kein verifizierter Originaldatei-Export und kein installierter Skill.

Die Originale bleiben in [Google Drive](https://drive.google.com/drive/folders/1WQkvQDTlWfcHvKDrXtIYU8P4HZyYv0lA). Die gesamte Transkriptions-API-Dokumentation wird über ihre Quelle referenziert. Es wurden keine Audiodateien an Anbieter gesendet, keine Cloud-Dienste aktiviert und keine kostenpflichtigen Aufträge erstellt.

Der vorhandene [VIBE-CODER-Prototyp, PR #3](https://github.com/julianzotter/nexus-platform/pull/3), bleibt ein separater UI-Prototyp. Gemeinsame Oberfläche ist ein Ziel; daraus folgt noch keine sichere Schlüsselverwaltung, Mehragentensteuerung oder Echtzeitfunktion.

## Prüfgrenze

Textinhalte aus Markdown, DOCX, PDF und konvertiertem Google Doc wurden gelesen. Der lokale Prozessstart scheitert an der Ausführungsumgebung; daher keine visuelle DOCX/PDF-Prüfung, keine Originalbyte-Hashes und keine Ausführung der vorgeschlagenen Parser. Die nachträglich erwähnte neue Word-Konvertierung konnte keiner zusätzlichen Datei eindeutig zugeordnet werden. Keine Behauptung verlustfreier Gleichheit dieser Fassungen.

Der Konzeptkatalog ist absichtlich unter docs abgelegt. Er ersetzt nicht registry/file-registry.jsonl: dessen Validator verlangt reale Inventardaten und berechnete IDs; unbekannte Größen, Hashes und Abdeckungswerte werden nicht erfunden.
