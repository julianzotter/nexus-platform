# NEXUS Daten-Dashboard

Eine einzelne, eigenständige HTML-Datei: KPI-Karten, vier animierte Diagramme, Filter, sortierbare Tabelle, Dialog mit den Daten per Text oder Sprache, Datei-Import/-Export. Prototyp, keine Freigabe.

## Starten

`index.html` direkt im Browser öffnen. Kein Server, keine CDN-Abhängigkeit, keine API-Keys.

Daten neu einbetten (feste Git-Revision, deterministisch):

```sh
python prototypes/data-dashboard/build_data.py          # HEAD
python prototypes/data-dashboard/build_data.py <rev>    # bestimmte Revision
python -m unittest tests.test_data_dashboard
```

## Funktionen

| Bereich | Umsetzung |
|---|---|
| Daten | `window.DASHBOARD_DATA` zwischen `/*DATA:BEGIN*/…/*DATA:END*/`: Repository-Dateien und Commit-Historie aus `git ls-tree`, `cat-file`, `log` |
| Filter | Zeitraum-Voreinstellungen, Volltextsuche, Spaltenfilter (= ≠ enthält > ≥ < ≤), Klick auf Balken, Donut-Legende oder Tabellenzelle; alles wirkt auf alle Ansichten |
| Diagramme | Zeitverlauf (pro Tag / kumuliert, Zeitraffer), Balken, Anteile, Verteilung; requestAnimationFrame-Übergänge, Tooltips, SVG-Export |
| Dialog | Regelbasierter Parser (Deutsch/Englisch), kein KI-Modell. Analyst-Stimme antwortet, Prüfer-Stimme nennt Datenbasis und Filter. Transkript als MD, JSON, TXT, SRT |
| Sprache | Web Speech API. In Chrome/Edge wird das Mikrofon-Audio an den Erkennungsdienst des Browserherstellers gesendet; vor der ersten Nutzung erscheint ein Hinweis |
| Datei-I/O | Import CSV/TSV/JSON/JSONL per Button oder Drag & Drop mit Typ-Erkennung; „Live-Datei“ beobachtet eine lokale Datei (Chromium, File System Access API); Export CSV, JSON, Markdown-Bericht |

Beispielfragen: „Wie viele Python-Dateien?“, „Summe Zeilen im Ordner tests“, „Dateien größer als 10 kb“, „Wechsle zu Commits“, „Commits seit 2026-10-18 ohne Merge“, „Summe plus pro Autor“, „exportiere als markdown“.

## Grenzen

Importierte Daten werden nur im Browser gehalten. Der Parser versteht nur die oben genannten Muster; nicht verstandene Fragen werden als solche gemeldet, nicht geraten. Headless-Browser drosseln Animationen, deshalb können Screenshots Zwischenstände zeigen.
