# NEXUS Gemini-Chat (multimodal, Streaming)

Web-Chat mit Text- und Bildeingabe, Echtzeit-Streaming und persistentem Verlauf über die Gemini API. Prototyp, keine Freigabe.

## Starten (PowerShell)

```powershell
$env:GEMINI_API_KEY = "<Key aus Google AI Studio>"
node prototypes/gemini-chat/server.mjs
# öffnen: http://127.0.0.1:8787
```

Optional: `$env:GEMINI_MODEL` (Standard `gemini-3.8-flash`), `$env:PORT`. Node ≥ 20, keine npm-Abhängigkeiten.

## Architektur

```
Browser (index.html)  ──POST /api/sessions/{id}/chat──▶  server.mjs (127.0.0.1)  ──x-goog-api-key──▶  Gemini
   ◀──── SSE: start · delta · done · error ─────────────    hält Key + Verlauf      ◀── streamGenerateContent?alt=sse
```

- **Key nur im Serverprozess.** Der Browser erhält ihn nie; `/api/config` meldet nur `hasKey`. Server bindet an `127.0.0.1`, Seite mit Content-Security-Policy.
- **Verlauf** pro Sitzung in `.sessions/<id>.json` (gitignored), inklusive Bilder als Base64, damit Folgefragen sich auf frühere Bilder beziehen können. Ein Turn-Paar wird erst nach vollständiger Antwort gespeichert; bei Fehler oder Abbruch kommt die Nachricht zurück ins Eingabefeld.
- **Bilder**: PNG, JPEG, WebP, HEIC/HEIF; höchstens 4 pro Nachricht, je 6 MB. Große Bilder werden im Browser auf 1600 px Kantenlänge verkleinert. Anhängen per Button, Einfügen oder Drag & Drop.
- **Parameter**: Modell (Auswahl oder eigene ID), Systemanweisung, max. Ausgabe-Tokens, Temperatur. Die Temperatur wird nur auf ausdrücklichen Wunsch gesendet, weil Gemini 3.6+ und 4 sie laut Dokumentation ignorieren.
- **Ausgabe**: Markdown wird als DOM aufgebaut (kein `innerHTML`); Gedanken-Parts (`thought: true`) werden nicht angezeigt. Token-Verbrauch und Abbruchgrund stehen unter jeder Antwort. Export als Markdown oder JSON.

## Tests

```sh
node --test prototypes/gemini-chat/test/server.test.mjs
python -m unittest tests.test_gemini_chat
```

Die Tests laufen gegen einen lokalen Fake-Endpunkt im dokumentierten SSE-Format: Streaming, Ausfiltern von Gedanken, Mehrfach-Turn-Verlauf mit Bild, Persistenz über einen Neustart, 429-Fehler ohne Speicherung, fehlender Key, ungültige Sitzungs-IDs, Key-Geheimhaltung.

## Stand und Grenzen

- API-Details (Endpunkt, `inline_data`, Modell-IDs) wurden am 2026-10-21 in der Gemini-Dokumentation nachgelesen. **Ein Aufruf gegen die echte API ist nicht erfolgt**, weil kein Key vorlag.
- Google bewirbt inzwischen zusätzlich die „Interactions API“ mit serverseitigem Verlauf. Dieser Prototyp nutzt das weiterhin dokumentierte `streamGenerateContent`.
- Bilder werden inline gesendet; für große Dateien oder PDFs wäre die Files API der nächste Schritt. Sitzungsdateien sind unverschlüsselt und enthalten alle Inhalte.
