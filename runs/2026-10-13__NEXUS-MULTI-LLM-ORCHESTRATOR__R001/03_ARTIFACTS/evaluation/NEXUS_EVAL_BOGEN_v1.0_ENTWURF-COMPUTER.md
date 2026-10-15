---
schema: IOD.01/1.0
run_id: 2026-10-13__NEXUS-MULTI-LLM-ORCHESTRATOR__R001
type: artifact
artifact: 03_ARTIFACTS/evaluation/NEXUS_EVAL_BOGEN_v1.0_ENTWURF-COMPUTER.md
archived_ts: 2026-10-15T06:00:48+02:00
sha256_original: 38c5bc2fbec9cf9d792551da061c3a3abbc3eb87ee629bdb7d8cdb61b4fa9f6a
---

# NEXUS-AI – Evaluierungsbogen v1.0

**Prüfgegenstand:** NEXUS-AI Multi-LLM System, Repository `github.com/julianzotter/nexus-platform` (Commit `3caf813`) und dessen Spiegel in Google Drive (`LLM-LOCAL-SSOT/nexus-platform`)
**Auftraggeber:** DI Julian Zotter, ZOTTERCONSULT
**Anlage:** `NEXUS_EVAL_KONTEXTPAKET_v1.0.md` (Dateibaum und Dateien im Wortlaut). Falls du direkten Zugriff auf das Repo oder Drive hast, nutze ihn zusätzlich und gib das an.
**Zweck:** Unabhängige Bewertung durch mehrere LLMs. Die Berichte werden maschinell zusammengeführt, verglichen und für Verbesserungen genutzt.

---

## 1 Auftrag an das prüfende Modell

Du bist unabhängige Prüfinstanz für ein KI-Orchestrierungssystem eines Tragwerksplanungsbüros (Eurocode/ÖNORM). Prüfe das System anhand der vier Kriterien in Abschnitt 3, vergib je Kriterium eine Note von 1 bis 5 und liefere den Prüfbericht exakt im Format von Abschnitt 5.

**Prüfregeln (verbindlich):**
1. **Nur Belege:** Jede Feststellung braucht einen Beleg im Format `Pfad:Zeile` (z. B. `orchestrator/nexus_orch/core.py:24`) oder ein wörtliches Kurzzitat. Was nicht belegbar ist, wird als `NICHT PRÜFBAR` markiert und nicht geraten.
2. **Kein Gefälligkeitsurteil:** Bewerte streng nach den Notenankern. Eine Note 1 verlangt, dass alle Anker der Note 1 erfüllt und belegt sind.
3. **Ist statt Absicht:** Bewertet wird, was implementiert und getestet ist. Konzepte und README-Ankündigungen zählen nur als „geplant“.
4. **Laufzeitnachweise:** Abschnitt B des Kontextpakets enthält vom Betreiber berichtete Testläufe. Verwende sie als Beleg mit dem Kennzeichen `[Betreiberangabe]`.
5. **Konkrete Verbesserungen:** Jede Schwäche bekommt eine umsetzbare Maßnahme (Datei, Änderung, erwarteter Effekt).
6. **Eigene Identität:** Gib Modellname, Version/Datum und Zugriffsart an (nur Kontextpaket / Repo / Drive).
7. **Sprache:** Deutsch, knapp, sachlich.

---

## 2 Systemüberblick (zur Orientierung, nicht als Beleg)

- **Orchestrator** (`orchestrator/`): Python-Paket `nexus_orch`, Befehl `nexus`. Leitet Aufgaben nach Typ an Perplexity, Claude, GPT, Gemini, Google Cloud Vision oder ein lokales Modell (Ollama, qwen2.5:7b), jeweils mit Ausweichkette, Privacy-Gate (vertrauliche Inhalte nur lokal), Model Council (Konsens/Abweichungen), Shared-Lessons-Layer und Audit-Protokoll.
- **Registry und Inventar** (`registry/`, `tools/`, `tests/`): Datei-Inventar, Duplikatprüfung, Abdeckungsstatistik.
- **Parsing-Pipeline** (`reports/2026-10-13_parsing-pipeline/`): Inventar der Drive-Bestände, OCR, TF-IDF-Index, Dashboards.
- **Konzepte und Prototypen** (`docs/concepts/`, `prototypes/`): Voice- und Normen-Parser-Konzept, VIBE-CODER-UI-Prototyp.
- **SSOT-Kette:** GitHub (Versionierung) → `sync_nexus.ps1` → Google Drive (Ablage + Benchmark-Kopie).

---

## 3 Prüfkriterien

Notenskala (österreichisch): **1** Sehr gut · **2** Gut · **3** Befriedigend · **4** Genügend · **5** Nicht genügend

| Nr. | Kriterium | Gewicht |
|---|---|---|
| K1 | Funktion und Zuverlässigkeit | 30 % |
| K2 | Sicherheit, Datenschutz und Governance | 25 % |
| K3 | Architektur, Integration und Erweiterbarkeit | 25 % |
| K4 | Fachlicher Nutzen und Nachvollziehbarkeit für die Ingenieurpraxis | 20 % |

### K1 Funktion und Zuverlässigkeit (30 %)

Leitfrage: Tut das System, was es verspricht, und verhält es sich bei Fehlern berechenbar?

Prüffragen:
- K1.1 Routing: Wird jede Aufgabe deterministisch dem richtigen Modell zugeordnet (`routing.json`, `core.py`)? Gibt es undefinierte Aufgabentypen ohne klare Fehlermeldung?
- K1.2 Ausweichkette: Greift der Fallback korrekt, werden Fehler protokolliert und klar ausgegeben?
- K1.3 Provider-Adapter: Sind die API-Aufrufe für Perplexity, Anthropic, OpenAI, Gemini, Vision und Ollama formal korrekt (Endpunkte, Header, Antwortfelder)? Welche Annahmen sind ungeprüft (z. B. Modellnamen)?
- K1.4 Tests: Decken die Tests die Kernpfade ab (Routing, Fallback, Privacy, Council, Lessons, Fehlerausgabe)? Was fehlt (Netzwerk, Timeouts, Rate-Limits, echte Integrationstests)?
- K1.5 Pipelines und Werkzeuge: Sind `parse.py`, `ocr.py` und `tools/*.py` lauffähig, reproduzierbar und gegen Fehleingaben robust?

| Note | Anker |
|---|---|
| 1 | Alle Kernfunktionen implementiert und durch Tests belegt; Fehlerpfade abgedeckt; Integrationstest mit mindestens einem echten Anbieter belegt. |
| 2 | Kernfunktionen implementiert und getestet; einzelne Randfälle (z. B. Timeouts) ungetestet. |
| 3 | Kernfunktionen vorhanden, Tests nur mit Mocks; mehrere Fehlerpfade ungeprüft. |
| 4 | Wesentliche Funktionen lückenhaft oder nur teilweise getestet. |
| 5 | Kernfunktionen fehlen oder sind nachweislich fehlerhaft. |

### K2 Sicherheit, Datenschutz und Governance (25 %)

Leitfrage: Bleiben vertrauliche Daten und Zugangsdaten geschützt, und sind Entscheidungen nachvollziehbar und freigabepflichtig?

Prüffragen:
- K2.1 Privacy-Gate: Kann ein als `VERTRAULICH`/`CONFIDENTIAL`/`[P3]` markierter Inhalt unter irgendeinem Pfad (Fallback, Council, OCR, Synthese) zu einem Cloud-Anbieter gelangen? Ist die Marker-Erkennung robust (Groß-/Kleinschreibung, Varianten)?
- K2.2 Zugangsdaten: Wie werden API-Keys gespeichert (`setup.ps1`) und übertragen (z. B. Key in URL bei Gemini/Vision)? Werden sie aus Sync, Logs und Repo ferngehalten (`sync_nexus.ps1`, `.gitignore`)?
- K2.3 Audit: Ist das Protokoll ausreichend (Hash statt Klartext, Zeit, Modell, Route) und manipulationsarm?
- K2.4 Freigaben: Sind Push, Löschen, Veröffentlichen nur nach Bestätigung möglich? Löscht der Drive-Sync nie Daten?
- K2.5 Prototyp-Risiken: Bewerte die in `prototypes/vibe-coder-v2.3/README.md` selbst dokumentierten Risiken (Keys in localStorage, iframe ohne sandbox).

| Note | Anker |
|---|---|
| 1 | Kein belegbarer Pfad für Datenabfluss vertraulicher Inhalte; Keys nie im Repo, Log oder URL; Audit vollständig; Freigabepflicht technisch erzwungen. |
| 2 | Kein Datenabflusspfad; kleinere Schwächen (z. B. Key als URL-Parameter, einfache Marker-Erkennung). |
| 3 | Grundschutz vorhanden, aber mindestens eine relevante Lücke ohne Gegenmaßnahme. |
| 4 | Mehrere relevante Lücken oder Schutz nur organisatorisch. |
| 5 | Nachweisbarer Abflusspfad für vertrauliche Daten oder Keys im Repo. **K.-o.: Gesamtnote höchstens 4.** |

### K3 Architektur, Integration und Erweiterbarkeit (25 %)

Leitfrage: Ist das System sauber aufgebaut, mit den Quellen (GitHub, Drive, Perplexity) verbunden und leicht erweiterbar?

Prüffragen:
- K3.1 Modularität: Klare Trennung von Konfiguration, Adaptern, Steuerlogik und CLI? Abhängigkeiten minimal?
- K3.2 Erweiterbarkeit: Wie viel Aufwand ist ein neuer Anbieter, eine neue Route, ein neuer Workflow? Belege mit den nötigen Änderungsstellen.
- K3.3 SSOT-Kette: Ist der Weg GitHub → Drive eindeutig, reproduzierbar (SYNC_STAMP, Test-Gate) und konfliktfrei? Gibt es konkurrierende Wahrheiten (drei gleichnamige Drive-Ordner laut Parsing-Bericht)?
- K3.4 Registry-Konsistenz: Stimmen `orchestrator/registry/workflow-registry.json`, `registry/` und die tatsächlich vorhandenen Skills/Dateien überein? Sind Verweise prüfbar oder nur Platzhalter?
- K3.5 Kohärenz des Gesamtrepos: Passen Orchestrator, Inventar, Parsing-Pipeline, Konzepte und Prototyp zusammen, oder sind es unverbundene Teile?

| Note | Anker |
|---|---|
| 1 | Klare Schichten, neue Anbieter/Routen per Konfiguration plus ein Adapter; SSOT-Kette eindeutig und automatisiert; Registry vollständig referenziert. |
| 2 | Saubere Struktur; einzelne manuelle Schritte oder Platzhalter in der Registry. |
| 3 | Funktionsfähig, aber Teile unverbunden oder doppelt gepflegt. |
| 4 | Starke Kopplung oder unklare Datenflüsse. |
| 5 | Keine erkennbare Architektur; Integration nicht nachvollziehbar. |

### K4 Fachlicher Nutzen und Nachvollziehbarkeit für die Ingenieurpraxis (20 %)

Leitfrage: Unterstützt das System normgerechte, belegbare Ingenieurarbeit (Statik, Eurocode/ÖNORM) und ist es für den Betreiber bedienbar?

Prüffragen:
- K4.1 Quellenbindung: Werden Zitate (Perplexity `citations`) bis zur Ausgabe durchgereicht und gespeichert? Sind Normenaussagen prüfbar?
- K4.2 Model Council: Ist der Konsensvergleich fachlich belastbar (aktuell textuelle Gleichheit) oder nur formal? Wie würden Zahlenwerte (z. B. kmod, γM) verglichen?
- K4.3 Determinismus: Temperatur 0.0 und Reproduzierbarkeit – ausreichend für nachvollziehbare Nachweise?
- K4.4 Lessons-Learned: Ist der Shared-Lessons-Layer (Felder, Status PROPOSED) geeignet, wiederverwendbares Fachwissen zu sichern? Fehlt ein Freigabe- oder Verdichtungsprozess?
- K4.5 Bedienbarkeit: Sind Installation (`setup.ps1`, `pip install -e .`), Bedienung (`nexus`) und Dokumentation für einen Ingenieur ohne Entwicklerteam handhabbar?

| Note | Anker |
|---|---|
| 1 | Quellen durchgängig gespeichert, Council vergleicht inhaltlich inkl. Zahlenwerten, Lessons mit Freigabeprozess, Bedienung ohne Hilfe möglich. |
| 2 | Quellen und Council nutzbar, kleinere Lücken (z. B. Council nur textuell). |
| 3 | Fachlicher Nutzen erkennbar, aber Nachweisführung nur eingeschränkt belastbar. |
| 4 | Überwiegend generisches LLM-Werkzeug ohne fachliche Absicherung. |
| 5 | Kein erkennbarer fachlicher Nutzen oder irreführende Ausgaben möglich. |

---

## 4 Berechnung der Gesamtnote

Gesamtnote = 0,30·K1 + 0,25·K2 + 0,25·K3 + 0,20·K4, auf eine Nachkommastelle gerundet.
Regeln: K2 = 5 → Gesamtnote mindestens 4,0. Ist ein Kriterium zu mehr als der Hälfte `NICHT PRÜFBAR`, dieses Kriterium mit `null` ausweisen und die Gesamtnote über die übrigen Gewichte normieren; im Bericht vermerken.

---

## 5 Pflichtformat des Prüfberichts

Liefere genau diese Abschnitte in dieser Reihenfolge, ohne Einleitung oder Schlussformel.

~~~~markdown
# NEXUS-AI Prüfbericht – <Modellname>

## 0 Kopf
- Modell / Version: 
- Prüfdatum: 
- Zugriffsart: Kontextpaket | Repo | Drive
- Geprüfter Commit: 3caf813

## 1 Ergebnis
| Kriterium | Note | Begründung (1 Satz) |
|---|---|---|
| K1 Funktion und Zuverlässigkeit | | |
| K2 Sicherheit, Datenschutz, Governance | | |
| K3 Architektur, Integration, Erweiterbarkeit | | |
| K4 Fachlicher Nutzen, Nachvollziehbarkeit | | |
| **Gesamt (gewichtet)** | | |

## 2 Befunde je Kriterium
### K1
| ID | Prüffrage | Befund | Beleg | Bewertung (+ / o / – / n.p.) |
|---|---|---|---|---|
(K1.1 bis K1.5; analog für K2, K3, K4)

## 3 Kritische Mängel
Nummerierte Liste, max. 5, nur Mängel mit Schweregrad hoch. Je Mangel: Beschreibung, Beleg, Risiko.

## 4 Verbesserungsmaßnahmen
| Prio | Maßnahme | Datei(en) | Aufwand (S/M/L) | Erwartete Notenwirkung (Kriterium, von→nach) |
|---|---|---|---|---|
(max. 10, sortiert nach Nutzen/Aufwand)

## 5 Nicht prüfbar
Liste der Punkte, die mit dem verfügbaren Material nicht prüfbar waren, und welches Material fehlt.

## 6 Maschinenlesbare Zusammenfassung
```json
{ ... siehe Schema ... }
```
~~~~

**JSON-Schema für Abschnitt 6** (exakt diese Schlüssel, Noten als Zahl 1–5 oder `null`):

```json
{
  "eval_version": "1.0",
  "model": "",
  "model_version": "",
  "date": "YYYY-MM-DD",
  "access": "kontextpaket|repo|drive",
  "commit": "3caf813",
  "grades": { "K1": 0, "K2": 0, "K3": 0, "K4": 0 },
  "weighted_total": 0.0,
  "ko_triggered": false,
  "findings": [
    { "id": "K1.1", "rating": "+|o|-|n.p.", "summary": "", "evidence": "pfad:zeile" }
  ],
  "critical_issues": [ { "summary": "", "evidence": "", "risk": "" } ],
  "improvements": [
    { "prio": 1, "action": "", "files": [""], "effort": "S|M|L", "criterion": "K1", "grade_from": 0, "grade_to": 0 }
  ],
  "not_testable": [""]
}
```

---

## 6 Hinweise für den Versand (für den Auftraggeber)

1. Diesen Bogen und `NEXUS_EVAL_KONTEXTPAKET_v1.0.md` gemeinsam an jedes Modell senden (ChatGPT, Claude, Gemini, Perplexity, lokales Modell). Begleittext: „Führe die Prüfung gemäß Evaluierungsbogen durch. Grundlage ist das angehängte Kontextpaket.“
2. Jedes Modell in einer neuen, leeren Unterhaltung prüfen lassen, damit frühere Gespräche das Urteil nicht beeinflussen.
3. Berichte als `EVAL_<modell>_<YYMMDD>.md` in `_INDEX_LNK/BENCHMARK Multi-LLM-Orchestrierung/evaluierungen/` ablegen.
4. Auswertung: Die JSON-Blöcke aller Berichte zusammenführen; je Kriterium Mittelwert und Streuung bilden. Abweichungen von mehr als 1 Note zwischen Modellen gezielt nachprüfen. Maßnahmen, die von mehreren Modellen genannt werden, zuerst umsetzen.
