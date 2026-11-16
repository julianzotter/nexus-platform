# NEXUS Wissensinventar und Data-Refresh

Stand 28.10.2026. Abgeleitete Review-Sicht; keine neue kanonische Master-Registry.

## Einstiegspunkte

- [Masterlisten](https://drive.google.com/drive/folders/1oWX4JbZlJkUZJWwgSA_KxuFJRemvZoxK)
- [Index, Listen und Trees](https://drive.google.com/drive/folders/1zf1aNaIFo0dJ8wQpDnJzWnvgVt2ASx66)
- [AnythingSearch](https://drive.google.com/drive/folders/1YgSdE8x2nelUcHQ_FhPAraoKPmlB-7AM)
- [März-Statusbericht](https://drive.google.com/file/d/1Ac-z2h9Q0vMakV13_V5SBrb2oLO6y1gh/view)
- [April-Roadmap Rev.2](https://docs.google.com/document/d/1HH1B927AIhTuES8W_w_AHCKaSddrYqfM/edit)
- Vorhandene Repo-Verträge: `registry/file-registry.jsonl`, `schemas/dashboard-snapshot.schema.json`, `tools/export_dashboard.py`, `prototypes/data-dashboard/README.md`.

## Rhythmus und Status

Ein wöchentlicher ChatGPT-Quellencheck wurde für Montagmorgen (Europe/Berlin, ab 02.11.2026) eingerichtet. Er recherchiert Delta-Berichte und Wegweiser; ein erfolgreicher Quellencheck beweist keinen laufenden SQLite-Hostzugriff. Der bestehende GitHub-Drive-Poller bleibt getrennt; sein dokumentierter Credential-Blocker wurde hier nicht behoben.

## Konsistente lokale SQLite-Auswertung

Die zwei vom Nutzer genannten AnythingSearch-Snapshots unterscheiden sich in Datum und Größe. Den gewünschten lokalen aktuellen Snapshot ausdrücklich auswählen; `anythingllm.db` nicht verwenden. DB nur über SQLite-Backup lesen. Matching WAL muss auf dem Host bei der Quelle verfügbar sein. Kein Kopieren einer laufenden DB ohne konsistente Sicherung.

```powershell
python anythingsearch_refresh.py --db 'C:\Users\julia\AppData\Local\AnythingSearch_2000\AnythingSearch.db' --out '.\refresh-output'
```

Das Skript liefert `files.csv` und `refresh.json`. Es prüft quick_check und das erwartete Files/Folders-Schema, bewahrt Zeitwerte unkonvertiert und kennzeichnet fehlende Parents. Bei Fehlern wird ein zuvor exportiertes CSV entfernt, damit es nicht als frisch erscheint. Ein geänderter Schemaaufbau führt zu FAILED. Quelldatenbank wird nicht verändert. Dateinamen/Pfade sind Metadaten; fachliche Richtigkeit wird nicht geprüft.

Test: temporäre SQLite-WAL-Datenbank, bestätigter Dateidatensatz, erfolgreicher Export und unveränderte Quelldatei. Kein Test gegen die reale Nutzer-DB möglich.

## Abnahme je Refresh

1. Quell-ID, Snapshotdatum, Schema und Hashscope speichern.
2. Cloud-Suche vollständig paginieren; pro Root Scope und Fehler festhalten.
3. Vergleich nur gleicher Scopes; neue/fehlende IDs als Kandidaten markieren.
4. Ausgabe validieren, Ziel zurücklesen; Laufstatus und Fehler erhalten.
5. Normen, Parser und Solver nur mit eigenem Inhalts-/Testnachweis höher einstufen.

Keine geplante Ausführung als erfolgreiche Durchführung melden. Kein Produktionsrollout, keine ACL-Änderung und kein automatischer Import von Normvolltexten.


## Delta-Erhebung 02.11.2026

- [Delta-Bericht](../docs/infrastructure-status/2026-11-02/DELTA_STATUS.md) und [Erhebung/Prüfdaten](../docs/infrastructure-status/2026-11-02/DELTA_EVIDENCE.json).
- [WORK-Fassung](https://drive.google.com/file/d/1-DJtsqscVfxVQGrs6c6i-z3BpE3o9OZc/view).
- AnythingSearch.zip ist nun erreichbar: [Archiv vom 04.10.2026](https://drive.google.com/file/d/1eVQeaxKW0gBmxyYbTN6bkCMCx5flkADR/view). quick_check ok, 2.470.605 Files-Zeilen; keine heutige Vollständigkeits- oder WAL-Garantie. Frühere NOT_ACCESSIBLE-Angabe gilt nicht mehr für dieses historische Archiv.
- Aktueller Refresh bleibt INCOMPLETE: technische manuelle Erfolge ersetzen keine erfolgreichen geplanten Zyklen mit innerem Status und Checkpoint.
- Neue Studio-v5.5-HTML enthält fest codierte Eurocode-PASS-Ausgabe; UI-Prototyp, kein Solvernachweis.
- Artefaktregistrierung BLOCKED: bestehendes Drive-Register wird beim Abruf abgeschnitten; keine Mutation aus unvollständiger Quelle. Dieser Zusatz ist eine Review-Sicht und kein kanonischer Registereintrag.


## Delta-Erhebung 09.11.2026

- [Delta-Bericht](../docs/infrastructure-status/2026-11-09/DELTA_STATUS.md) · [Prüfdaten](../docs/infrastructure-status/2026-11-09/DELTA_EVIDENCE.json) · [WORK-Fassung](https://drive.google.com/file/d/1xKPKjwq_NjzYznPfg80YaxvkLA86ZjwS/view) mit bestätigtem Rohbyte-Readback. Registrierung für diesen Rücklauf PENDING.
- Zwölf zusätzliche Dokumenttreffer im vergleichbaren Drive-Suchfenster, darunter neue Tree-Listen und Google AI-Stack v1.1. Alle 29 bisherigen Treffer weiterhin sichtbar.
- [Google AI-Stack v1.1](../docs/dashboards/google-ai-stack-serie/index.html) stimmt im gelesenen HTML-Text mit der Drive-Fassung überein. [Projektstand v1.0.3 in Drive](https://drive.google.com/drive/folders/1TamB-peHA9784LOHbBQ1MjztUDd3efdG) ist separat erfasst.
- Kein neuerer konsistenter AnythingSearch-Snapshot gefunden. Die Prüfwerte zum [Archiv vom 04.10.2026](https://drive.google.com/file/d/1eVQeaxKW0gBmxyYbTN6bkCMCx5flkADR/view) bleiben als historische Messung vom 02.11. verlinkt.
- Aktueller Refresh INCOMPLETE. Drive-Poller und WORK-Preflight melden HTTP 400, Monitor meldet INCOMPLETE. Drei CI-Tests schlagen fehl. Die Belege stehen im Delta-Bericht.
- Das [Artefaktregister](https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view) war diesmal vollständig lesbar und führt den Bericht vom 02.11. als REGISTERED.


## Delta-Erhebung 16.11.2026

- [Delta-Bericht](../docs/infrastructure-status/2026-11-16/DELTA_STATUS.md) und [Erhebungsbelege](../docs/infrastructure-status/2026-11-16/DELTA_EVIDENCE.json).
- [WORK-Fassung](https://drive.google.com/file/d/1VeuE3XVJFTWfrNvFNHHPN3r5oi26Aa9E/view), vollständig zurückgelesen: 16.343 Bytes, SHA-256 `cf7ce6f59deb0d9aacc1eabd29385940075b0108727e581dda2ea4383d111251`.
- 66 Dokumenttreffer im vergleichbaren Filter, davon 25 zusätzliche IDs gegenüber 09.11.; alle bisherigen 41 IDs weiter sichtbar. KB-/AI-Ordnernamensuche 167 Treffer. Keine globale Vollständigkeitsbehauptung.
- Neu gesichtet: Basic-Knowledge-Tree, FT-Träger-Dashboard, GWP-HTML mit zwei separaten JS-Datenteilen, Timber-Blueprint und GPT-Migrationspilot. Inhaltssichtung und Dokumentaussagen sind im Bericht getrennt.
- Refresh-Status: Runner vom 16.11. scheitern bei `oauth.token_refresh` mit `HTTP_400`; Poller und WORK-Delivery nicht betriebsfähig belegt. Neuer konsistenter AnythingSearch-Snapshot nicht gefunden; kein SQLite-Zugriff in diesem Lauf.
- Registrierung `REGISTRATION_PENDING / EXCLUSIVE_WRITER_UNVERIFIED`, Ledgernummer unzugeteilt. Kanonische Register und Berechtigungen blieben unverändert.
