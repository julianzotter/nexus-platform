---
schema: IOD.01/1.0
run_id: 2026-10-13__NEXUS-MULTI-LLM-ORCHESTRATOR__R001
type: artifact
artifact: 03_ARTIFACTS/evaluation/EVAL_gemini_3_7_flash_261013.md
archived_ts: 2026-10-15T06:00:48+02:00
sha256_original: bfacc8e576e196755947ddeeecddd963456578118733272b97720d808f7caf8b
---

# Prüfbericht NEXUS-AI v1.2.0
Prüfendes Modell: Gemini 3.7 Flash  ·  Datum: 2026-10-13  ·  Repo-Zugriff: ja

## A Ergebnis
| Kriterium | Note | Begründung (2–4 Sätze) |
|---|---|---|
| K1 Funktion | 2 | Die funktionale Kernarchitektur mit deterministischem Routing, Fallback-Ketten, Perplexity-Zitaten und isolierten Offline-Tests ist voll funktionsfähig und durch 17 Unit-Tests abgesichert (`orchestrator/tests/test_orch.py:1-102`). Das Model Council führt bei abweichenden Antworten eine fundierte Synthese durch (`core.py:61-68`), setzt jedoch bei nur einer verbleibenden Antwort einen Scheinkonsens und prüft Gleichheit rein textuell (`core.py:54-61`). |
| K2 Sicherheit/Governance | 2 | Das Sicherheitskonzept überzeugt durch strenge Trennung von Secrets via User-Environment (`setup.ps1:1-11`), Hash-basierte Audit-Logs (`core.py:73-76`) und löschfreie Sync-Strategien (`sync_nexus.ps1:25`). Allerdings ist die Erkennung der Privacy-Marker in `core.py:18` case-sensitiv implementiert, was bei kleingeschriebenen Markern ein Restrisiko für unbeabsichtigte Cloud-Weiterleitungen birgt. |
| K3 Architektur/Wartbarkeit | 2 | Die klare Schichtentrennung zwischen Konfiguration, Core-Logik, Providern und CLI sowie der Verzicht auf externe Abhängigkeiten garantieren exzellente Wartbarkeit und minimale Angriffsfläche (`providers.py:1-76`). Zur vollen Produktionsreife fehlen automatisierte HTTP-Retries mit Exponential Backoff bei API-Ratenlimits (`providers.py:7-17`) sowie standardisierte Python-Typannotationen nach PEP 484. |
| K4 Betrieb/Nutzen | 1 | Mit PowerShell-Setupskripten, dualem Sync-Mechanismus (Laufwerk G: und Rclone-Ordner-IDs), automatisierter Windows-Aufgabenplanung (`install_autosync.ps1:1-19`) und klarer Ausrichtung auf Eurocode-Statik (EN 1995/ÖNORM) bietet das System einen herausragenden Praxisnutzen für Ingenieurbüros. Fehlermeldungen enthalten durchgehend konkrete Handlungshinweise (`cli.py:27-32`). |
| **Gesamt (gewichtet)** | **1.8** | K.-o.-Regel angewendet: nein |

## B Prüfpunkte
| ID | Status (erfüllt/teilweise/nicht erfüllt/nicht prüfbar) | Beleg (Datei:Zeile) | Feststellung |
|---|---|---|---|
| K1.1 | erfüllt | `orchestrator/config/routing.json:43-105`, `orchestrator/nexus_orch/core.py:16-26` | Alle 9 definierten Routen sind deterministisch auflösbar; unbekannte Tasks werfen einen definierten `KeyError` mit Auflistung aller bekannten Routen (`core.py:21`). |
| K1.2 | erfüllt | `orchestrator/nexus_orch/core.py:31-39` | Primärausfälle triggern die definierte Fallback-Kette; aufgetretene Provider-Fehler werden strukturiert gesammelt und im Resultat zurückgegeben (`core.py:34, 38`). |
| K1.3 | teilweise | `orchestrator/nexus_orch/core.py:41-70` | Konsensprüfung und Synthese via Richter-Modell funktionieren; Konsenslogik basiert jedoch rein auf exakter String-Gleichheit (`core.py:54-61`) und deklariert bei nur 1 antwortenden Provider fälschlich Konsens (`consensus=True`). |
| K1.4 | erfüllt | `orchestrator/nexus_orch/providers.py:41-42`, `orchestrator/config/routing.json:5-10`, `orchestrator/nexus_orch/evaluate.py:65-66` | Perplexity-Zitate (`citations`) werden aus der OpenAI-kompatiblen API extrahiert, durchgereicht und in Berichten formatiert; Modell (`sonar-pro`) ist frei konfigurierbar. |
| K1.5 | erfüllt | `orchestrator/tests/test_orch.py:1-102` | Alle Kernpfade (Routing, Fallback, Privacy Gate, Council, Lessons, OCR, CLI, Eval) sind durch 17 netzwerkunabhängige Mock-/Monkeypatch-Tests abgedeckt (Laufzeit < 0.5s). |
| K1.6 | erfüllt | `orchestrator/config/routing.json:3`, `orchestrator/nexus_orch/providers.py:41,45,49,58`, `orchestrator/nexus_orch/core.py:33,48` | `default_temperature=0.0` ist global definiert und wird in allen Provider-Adaptern (OpenAI-compat, Anthropic, Gemini, Ollama) explizit an die API übergeben. |
| K2.1 | teilweise | `orchestrator/nexus_orch/core.py:18`, `orchestrator/config/routing.json:83-86,107-114` | Privacy-Gate routet erkannte Marker verlässlich auf `local` ohne Cloud-Fallback (`fallback: []`); Marker-Prüfung `m in prompt` ist jedoch case-sensitiv und ignoriert kleingeschriebene Trigger. |
| K2.2 | erfüllt | `orchestrator/nexus_orch/providers.py:22-29`, `orchestrator/nexus_orch/cli.py:28`, `.gitignore:4728`, `orchestrator/sync_nexus.ps1:22` | API-Keys werden ausschließlich aus Umgebungsvariablen geladen; Fehler melden nur Variablennamen; Keys und Secrets sind in `.gitignore` sowie Sync-Ausschlüssen erfasst. |
| K2.3 | erfüllt | `orchestrator/nexus_orch/core.py:71-76`, `orchestrator/sync_nexus.ps1:21` | Tägliche JSONL-Audit-Logs speichern UTC-Zeitstempel, Route, Provider und SHA256-Prompt-Hash anstelle von Klartext; Audit-Ordner ist von externen Syncs ausgeschlossen. |
| K2.4 | erfüllt | `orchestrator/nexus_orch/core.py:86`, `orchestrator/sync_nexus.ps1:25`, `orchestrator/sync_nexus_rclone.ps1:43` | Lessons werden mit `status="PROPOSED"` erfasst; Synchronisationsskripte arbeiten destruktionsfrei (Robocopy ohne `/MIR`, Rclone per `copy` statt `sync`). |
| K2.5 | teilweise | `orchestrator/config/routing.json:5-41`, `orchestrator/nexus_orch/core.py:18`, `orchestrator/nexus_orch/evaluate.py:3-4` | Datenabflüsse an US-Cloud-Provider sind transparent über Routen gesteuert; verbleibendes Datenschutzrisiko besteht vor allem bei Umgehung des Privacy Gates durch Schreibvarianten. |
| K3.1 | erfüllt | `orchestrator/config/routing.json`, `orchestrator/nexus_orch/core.py`, `orchestrator/nexus_orch/providers.py`, `orchestrator/nexus_orch/cli.py` | Saubere Schichtentrennung: Konfiguration in JSON, Routing-/Orchestrierungslogik in `core.py`/`evaluate.py`, Provider-Schnittstellen in `providers.py`, CLI in `cli.py`. |
| K3.2 | erfüllt | `orchestrator/config/routing.json:4-42`, `orchestrator/nexus_orch/providers.py:38-70` | Neue Routen erfordern lediglich einen JSON-Eintrag; neue Provider-Typen minimalen Code in `providers.py` (Aufwand < 1h). |
| K3.3 | teilweise | `orchestrator/nexus_orch/providers.py:7-18,36` | Konsequenter Verzicht auf Fremdbibliotheken (`urllib.request`); Timeouts sind konfigurierbar, jedoch fehlen automatische Retries bei HTTP 429/503. |
| K3.4 | teilweise | `orchestrator/nexus_orch/core.py:1-98`, `orchestrator/nexus_orch/providers.py:1-76` | Schlanker, gut lesbarer Code mit dedizierter Fehlerklasse `ProviderError`; Typannotationen (PEP 484) fehlen weitgehend, vereinzelt sehr dichte Einzeiler. |
| K3.5 | erfüllt | `orchestrator/pyproject.toml:7`, `orchestrator/registry/workflow-registry.json:2-11`, `orchestrator/sync_nexus.ps1:27-28`, `orchestrator/tests/test_orch.py:45-48` | Versionierung konsistent (v1.2.0); `SYNC_STAMP.txt` stellt Git-Commit-Verfolgbarkeit im Drive-SSOT sicher; Workflow-Registry wird in Pytest validiert. |
| K4.1 | erfüllt | `orchestrator/setup.ps1:1-11`, `orchestrator/pyproject.toml:11-12`, `orchestrator/nexus_orch/cli.py:27-32` | Einfache Installation via `setup.ps1` und `pip install -e .`; CLI liefert bei fehlenden Keys oder Offline-Modellen konkrete Reparaturhinweise. |
| K4.2 | erfüllt | `orchestrator/config/routing.json:3-41`, `orchestrator/nexus_orch/core.py:73-76`, `orchestrator/nexus_orch/evaluate.py:23-27,67` | Vollständige Reproduzierbarkeit durch fixierte Modellnamen, Temperatur 0.0, SHA256-Auditierung und Commit-Kennzeichnung aller Evaluierungsberichte. |
| K4.3 | erfüllt | `orchestrator/config/routing.json:44-105`, `orchestrator/nexus_orch/core.py:41-70` | Kosten- und Latenzoptimierung durch aufgabenspezifisches Routing (Perplexity für Recherche, GPT für Entwürfe, Claude für Code/Review, lokales Ollama für Private); Council nur für Schlüsselrouten. |
| K4.4 | erfüllt | `orchestrator/config/routing.json:51-57,87-105`, `orchestrator/nexus_orch/providers.py:60-70`, `orchestrator/registry/workflow-registry.json:19-122` | Hoher Ingenieurnutzen: Normenrecherche mit Zitaten (EC5 / ÖNORM), Model-Council für Tragwerksvarianten (BSP vs. HBV) und Cloud Vision / Gemini OCR für Plan-Scans. |
| K4.5 | erfüllt | `orchestrator/registry/workflow-registry.json:1-122`, `orchestrator/sync_nexus.ps1:1-46`, `orchestrator/sync_nexus_rclone.ps1:1-54`, `orchestrator/install_autosync.ps1:1-19` | Nahtlose Integration: 17 registrierte Workflows, automatischer Drive-Sync (G: & Rclone Ordner-IDs), Scheduled Task und Shared-Lessons-Austausch (`lessons.jsonl`). |

## C Kritische Befunde (max. 5, nur sicherheits- oder ergebnisrelevant)
1. **Case-Sensitive Privacy Hard Gate**: In `orchestrator/nexus_orch/core.py:18` prüft `any(m in prompt for m in p["markers"])` exakt auf Großschreibung. Kleingeschriebene Prompts (z. B. `vertraulich` oder `confidential`) passieren das Gate ungefiltert und werden an externe Cloud-APIs übertragen. Risiko: Unbeabsichtigter Abfluss sensibler Statik-, Kunden- und Projektdaten an US-Cloud-Provider. Maßnahme: Case-insensitive Prüfung via `m.lower() in prompt.lower()` und Regex-Wortgrenzen (`\b`) implementieren.
2. **Scheinkonsens bei Provider-Ausfällen im Model Council**: In `orchestrator/nexus_orch/core.py:54-61` führt `len(groups) == 1` bei Ausfall von 3 von 4 Mitgliedern zu `consensus=True`. Zudem erkennt die Normalisierung `norm(s)` nur textlich identische Antworten als Konsens. Risiko: Eine einzelne verbleibende Modellantwort wird fälschlich als Multi-Modell-Konsens bei statischen Variantenentscheidungen deklariert. Maßnahme: Mindestquorum (`len(valid) >= 2`) für Konsens vorschreiben und semantische Konsensprüfung im Synthese-Prompt verankern.
3. **Fehlende Retries bei transienten HTTP-Fehlern**: In `orchestrator/nexus_orch/providers.py:7-17` bricht `_post()` bei HTTP 429 (Rate Limit) oder HTTP 503 sofort mit `ProviderError` ab. Risiko: Vorzeitiges Scheitern von Fallback-Ketten oder Council-Abfragen bei temporären Lastspitzen externer APIs. Maßnahme: Exponential-Backoff-Retries (z. B. 3 Versuche bei Status 429, 500, 502, 503, 504) in `_post()` einbauen.

## D Top-5-Maßnahmen
| Rang | Maßnahme | Datei(en) | Kriterium | Wirkung (hoch/mittel/gering) | Aufwand (S/M/L) |
|---|---|---|---|---|---|
| 1 | Privacy Gate case-insensitiv & mit Wortgrenzen absichern | `orchestrator/nexus_orch/core.py` | K2 | hoch | S |
| 2 | Model Council Mindestquorum (>= 2) & Ausfall-Handling schärfen | `orchestrator/nexus_orch/core.py` | K1 | hoch | S |
| 3 | HTTP-Retry mit Exponential Backoff bei 429/503 implementieren | `orchestrator/nexus_orch/providers.py` | K3 | hoch | S |
| 4 | PEP 484 Typ-Annotationen & Schnittstellendokumentation ergänzen | `orchestrator/nexus_orch/core.py`, `orchestrator/nexus_orch/providers.py` | K3 | mittel | M |
| 5 | Token- und Kosten-Metadaten im Audit-Log erfassen | `orchestrator/nexus_orch/core.py`, `orchestrator/nexus_orch/providers.py` | K4 | mittel | S |

## E Stärken (max. 3)
1. **Robuste Null-Abhängigkeiten-Architektur (Stdlib-only)**: Verzicht auf externe HTTP- oder LLM-Bibliotheken ermöglicht minimale Angriffsfläche, blitzschnelle Installation und maximale Plattformunabhängigkeit.
2. **Praxisnahe Dual-Sync- & Automatisierungs-Infrastruktur**: Durchdachte Kombination aus `sync_nexus.ps1`, `sync_nexus_rclone.ps1` (ID-basiert) und `install_autosync.ps1` garantiert konsistenten Stand zwischen Git und Google Drive SSOT ohne Löschrisiko.
3. **Konsequente Datensparsamkeit im Audit-Log**: Protokollierung ausschließlich über SHA256-Prompt-Hashes und Metadaten verhindert DSGVO- und Geheimhaltungskonflikte in Logdateien.

## F Annahmen und nicht Prüfbares
1. **Live-Latenz und Quota der Cloud-Provider**: Das reale Antwortzeit- und Quota-Verhalten unter Last (Perplexity, Anthropic, OpenAI, Gemini) wurde mangels Live-API-Keys im Prüflauf nicht dynamisch gemessen.
2. **Rclone-Authentifizierung unter Windows**: Die Funktion von `sync_nexus_rclone.ps1` wurde statisch anhand des Skripts geprüft; der eigentliche OAuth-Flow für Google Drive for Desktop / Rclone erfordert Benutzerinteraktion.
3. **Lokale Ollama-Inferenz-Performance**: Die Verarbeitungsgeschwindigkeit des lokalen Modells `qwen2.5:7b` hängt von der GPU/CPU-Hardware des Endgeräts ab und ist im CI/Audit-Umfeld abstrahiert.

## G JSON (maschinenlesbar, keine Kommentare)
```json
{
  "modell": "Gemini 3.7 Flash",
  "datum": "2026-10-13",
  "repo_zugriff": true,
  "noten": {
    "K1": 2,
    "K2": 2,
    "K3": 2,
    "K4": 1
  },
  "gesamt": 1.8,
  "ko_regel": false,
  "pruefpunkte": {
    "K1.1": "erfuellt",
    "K1.2": "erfuellt",
    "K1.3": "teilweise",
    "K1.4": "erfuellt",
    "K1.5": "erfuellt",
    "K1.6": "erfuellt",
    "K2.1": "teilweise",
    "K2.2": "erfuellt",
    "K2.3": "erfuellt",
    "K2.4": "erfuellt",
    "K2.5": "teilweise",
    "K3.1": "erfuellt",
    "K3.2": "erfuellt",
    "K3.3": "teilweise",
    "K3.4": "teilweise",
    "K3.5": "erfuellt",
    "K4.1": "erfuellt",
    "K4.2": "erfuellt",
    "K4.3": "erfuellt",
    "K4.4": "erfuellt",
    "K4.5": "erfuellt"
  },
  "kritisch": [
    {
      "befund": "Case-Sensitive Privacy Hard Gate ermöglicht Umgehung bei Kleinschreibung",
      "datei": "orchestrator/nexus_orch/core.py:18",
      "massnahme": "Case-insensitive Prüfung via `m.lower() in prompt.lower()` oder Regex mit Wortgrenzen implementieren."
    },
    {
      "befund": "Schein-Konsens bei Einzelausfall und naive String-Gleichheit im Model Council",
      "datei": "orchestrator/nexus_orch/core.py:54-68",
      "massnahme": "Mindestquorum (>= 2 Antworten) für Konsens fordern; semantische Konsensprüfung im Synthese-Prompt verankern."
    },
    {
      "befund": "Fehlende HTTP-Retries bei transienten Fehlern (429 Rate Limit / 503)",
      "datei": "orchestrator/nexus_orch/providers.py:7-17",
      "massnahme": "Exponential-Backoff-Retries für transiente Statuscodes (429, 500, 502, 503, 504) in `_post()` einbauen."
    }
  ],
  "massnahmen": [
    {
      "rang": 1,
      "massnahme": "Privacy Gate case-insensitiv & mit Wortgrenzen absichern",
      "datei": "orchestrator/nexus_orch/core.py",
      "kriterium": "K2",
      "wirkung": "hoch",
      "aufwand": "S"
    },
    {
      "rang": 2,
      "massnahme": "Model Council Mindestquorum (>= 2) & Ausfall-Handling schärfen",
      "datei": "orchestrator/nexus_orch/core.py",
      "kriterium": "K1",
      "wirkung": "hoch",
      "aufwand": "S"
    },
    {
      "rang": 3,
      "massnahme": "HTTP-Retry mit Exponential Backoff bei 429/503 implementieren",
      "datei": "orchestrator/nexus_orch/providers.py",
      "kriterium": "K3",
      "wirkung": "hoch",
      "aufwand": "S"
    },
    {
      "rang": 4,
      "massnahme": "PEP 484 Typ-Annotationen & Schnittstellendokumentation ergänzen",
      "datei": "orchestrator/nexus_orch/core.py, providers.py",
      "kriterium": "K3",
      "wirkung": "mittel",
      "aufwand": "M"
    },
    {
      "rang": 5,
      "massnahme": "Token- und Kosten-Metadaten im Audit-Log erfassen",
      "datei": "orchestrator/nexus_orch/core.py, providers.py",
      "kriterium": "K4",
      "wirkung": "mittel",
      "aufwand": "S"
    }
  ]
}
```
