---
name: W100-CIRCULAR-HOUSING-INDEX
version: 0.1.0
agent_id: ID02
ticket_id: WO-20261112-W100-CHAT-TO-KB
ledger_id: null
review_status: REVIEW_PENDING
engineering_release: NOT_GRANTED
---
# W100 Zirkulärer serieller Wohnbau — Einstieg
Tags: #Zirkularität #Bauteilkennwerte #SeriellerWohnbau #TimberLoop #AW #WTW #GD #W012 #W017
35 kondensierte Wissensobjekte plus 3 ungeprüfte Kandidaten; 31 Quellen, 23 Schichtzeilen, 14 Projektreferenzen, 8 Aufbaufamilien und 8 Bausysteme.
Keine repräsentative Häufigkeitsrangfolge. Keine Freigabe für U/Schall/Brand/GWP/LCC/Reuse; Experten-Scores sind ungeprüfte Eingangsdaten.
## Dateien / Drive SSOT
- [W100_data_v0.1.json](https://drive.google.com/file/d/1nKEZvEMYtMjLIV9xyHq4utfPM3Xxt1Ws/view?usp=drivesdk)
- [26_11_12_1931_ID02_W100-CHAT-ERGEBNISSE_LEDGER-PENDING.md](https://drive.google.com/file/d/1i6Ues0GW8QC4bDpMHcr_ByBS1ddWBGmA/view?usp=drivesdk)
- [W100_BAUSYSTEME_v0.1.md](https://drive.google.com/file/d/1z9SeGK2Mr479c5rACuS24ofRibW0qEXp/view?usp=drivesdk)
- [W100_import.sql](https://drive.google.com/file/d/1Zvblb3dwqXfQVEJMoyPgRuDR3yg69m8S/view?usp=drivesdk)
- [W100_AUFBAUFAMILIEN_v0.1.md](https://drive.google.com/file/d/1x5jYcmqc0WqAgo9zuXpQ0oy2vIZrYzgi/view?usp=drivesdk)
- [W100_MANIFEST.json](https://drive.google.com/file/d/1G33Tz53nIHhHR5uvGC-p_i8uOqPHqepp/view?usp=drivesdk)
- [W100_QA.json](https://drive.google.com/file/d/1cywk14ywdNOzqMyIYBNk4i5yOl-osCIP/view?usp=drivesdk)
- [W100_INTAKE_14_FAMILIEN_v0.1.md](https://drive.google.com/file/d/1WarPDTVBExeX07C0B_1cAPb3Oy6CyaRt/view?usp=drivesdk)
- [W012_Knowledge_v0.3_W100_20261112.sqlite](https://drive.google.com/file/d/1DtRPG0z4IdGIDuKBGLQZ3fJXdhIQZbg4/view)
- [W100_SQLITE_SNAPSHOT_20261112.sqlite](https://drive.google.com/file/d/1C_DvFXuWpqRCpshBmvXpzXe5k0XOG7rL/view?usp=drivesdk)
- [W012_Knowledge_v0.3_BEFORE_W100_20261112.sqlite](https://drive.google.com/file/d/1bqoRyIxVEgQV8qcE9kMRY_H6c62KNHat/view?usp=drivesdk)
## GitHub Review-Snapshot
[Draft PR 80](https://github.com/julianzotter/nexus-platform/pull/80)
Repository private; knowledge/W100_CIRCULAR_HOUSING/. Kein Merge oder automatischer Dauer-Sync. JSON und SQL als portable Daten; Datenbank-Binärdatei in Drive.
## SQLite / Wiederfinden
Bestehende W012_Knowledge_v0.3.sqlite wurde um w100_objects, w100_sources, w100_evidence, w100_layers sowie 38 Einträge in bestehender knowledge_documents/knowledge_fts erweitert. Alle ursprünglichen Zeilen erhalten. WORK-Datenbank ist benannter Snapshot, kein neuer globaler Master. AnythingSearch.db und eurocode.db wurden nicht identifiziert oder geändert.
```sql
SELECT id,title,status FROM w100_objects WHERE kind='families';
SELECT id,title,status FROM w100_objects WHERE kind='candidates';
SELECT * FROM w100_layers WHERE assembly_id='AS-FAV-DE' ORDER BY ordinal;
SELECT o.id,o.title,s.url,s.locator FROM w100_objects o JOIN w100_evidence e ON e.object_id=o.id JOIN w100_sources s ON s.id=e.source_id WHERE o.id='AS-FAV-DE';
SELECT id FROM knowledge_fts WHERE knowledge_fts MATCH 'W100 AND CLT' AND id LIKE 'W100:%';
```
W100_import.sql erzeugt ausschließlich den isolierten w100_* Datenbereich auch in einer anderen SQLite-Datei; bindet dort nicht automatisch vorhandene globale Suchansichten an. Zweifacher Import auf leerer SQLite getestet: 38 Objekte ohne Dubletten.
## Neue Matrix
[Original Google Doc](https://docs.google.com/document/d/1EwMAA4i9yQ8jUfF6NDOR-dyYdFT2L1Pu6ReLaiMEluQ/edit) enthält 3, nicht 14 Varianten. Externe AW-01/WTW-01/GD-03 und interne AF-* IDs sind nicht identisch. Vollständige 14er-Liste fehlt. Indikative Scores und Kennwertbereiche nicht als TimberLoop-Forschungsergebnisse deklarieren.
## Prüfnachweis
SQLite integrity_check ok; foreign_key_check leer; alte Zeilen vollständig enthalten; SQL-Replay zweimal bestanden; Rohbyte-Readback aller 11 oben verlinkten Artefakte identisch. GitHub Erststand 7/7 textgleich; Nachtrag wird separat rückgelesen.
Registry-Ereignisse werden im bestehenden file-registry.jsonl ergänzt; Registrierung bleibt von fachlichem Review getrennt. Numerische Ledger-ID offen.
