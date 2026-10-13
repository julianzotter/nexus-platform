# NEXUS-AI – Evaluierungsbogen KURZ v1.0
Prüfgegenstand: `julianzotter/nexus-platform` → `orchestrator/` (Multi-LLM-Orchestrator v1.2.0, Stand 2026-10-13). Grundlage: Repo-Zugriff oder beigefügtes Kontextpaket (Langversion, Abschnitt 6).

## Auftrag
Du bist unabhängige:r Gutachter:in für LLM-Orchestrierung, Software-Architektur und Informationssicherheit im Ingenieurbüro (Statik, Eurocode/ÖNORM). Bewerte das System nach 4 Kriterien mit Noten 1–5.
Regeln: jede Feststellung mit Beleg `Datei:Zeile`, sonst als **Annahme** markieren · Unprüfbares als `nicht_pruefbar` · zu jedem Mangel eine konkrete Maßnahme mit Aufwand S/M/L · Deutsch, knapp, ohne Einleitung · Ausgabeformat exakt einhalten.

**Soll laut Doku:** Ein Befehl `nexus` routet deterministisch an Perplexity (Sonar, mit Zitaten), Claude, GPT, Gemini, Google Vision (OCR) oder lokal (Ollama), mit Fallback-Ketten. Ein Privacy-Gate (`VERTRAULICH`/`CONFIDENTIAL`/`[P3]`) erzwingt lokal, ohne Cloud-Fallback. Dazu kommen Model Council mit Konsens/Synthese, Lessons-Layer (`lessons.jsonl`, Status PROPOSED), Audit nur mit Prompt-Hash, Workflow-Registry (17 Workflows) und Drive-SSOT-Sync ohne Löschen.

## Kriterien, Gewichte, Prüfpunkte
| Kriterium | Gewicht | Prüfpunkte |
|---|---|---|
| K1 Funktion und Zuverlässigkeit | 30 % | K1.1 Routen auflösbar, unbekannte Route → definierter Fehler · K1.2 Fallback und Fehlersammlung · K1.3 Council-Logik (auch bei 1 Mitglied) · K1.4 Perplexity-Zitate, Modell konfigurierbar · K1.5 Tests decken Kernpfade ab, laufen ohne Netz · K1.6 Temperatur/Parameter je Provider gesetzt |
| K2 Sicherheit, Datenschutz, Governance | 25 % | K2.1 Privacy-Gate robust, garantiert kein Cloud-Fallback · K2.2 Keys nur aus Umgebung, nie geloggt, Sync-Ausschlüsse · K2.3 Audit nachvollziehbar und datensparsam · K2.4 Freigaben (PROPOSED, kein Löschen) · K2.5 DSGVO/Berufsgeheimnis: welche Daten zu welchem Anbieter |
| K3 Architektur und Wartbarkeit | 25 % | K3.1 Trennung Config/Core/Provider/CLI · K3.2 Aufwand neuer Provider/neue Route · K3.3 Nur Standardbibliothek: HTTP-Fehler, Timeouts, Retries · K3.4 Lesbarkeit, Typisierung, Fehlerklassen · K3.5 Konsistenz Repo ↔ Drive ↔ Registry |
| K4 Betrieb und Praxisnutzen | 20 % | K4.1 Installation Windows (`setup.ps1`, `pip install -e .`), hilfreiche Fehlermeldungen · K4.2 Reproduzierbarkeit · K4.3 Kosten/Latenz (lokal vs. Cloud, Council) · K4.4 Nutzen für Normenrecherche (EN 1995/ÖNORM B 1995), Variantenentscheid, OCR von Plänen · K4.5 Integration Drive-SSOT, Registry, Perplexity-Projekt |

## Notenskala (1 = beste)
1 Sehr gut: alles erfüllt, belegt, getestet · 2 Gut: kleine Mängel ohne Einfluss auf Sicherheit/Ergebnis · 3 Befriedigend: Kern vorhanden, mehrere Lücken · 4 Genügend: nur unter Aufsicht einsetzbar · 5 Nicht genügend: Kernanforderung fehlt oder sicherheitskritischer Mangel.
Gesamt = 0,30·K1 + 0,25·K2 + 0,25·K3 + 0,20·K4 (eine Nachkommastelle). **K.-o.:** Hat ein Kriterium die Note 5, ist die Gesamtnote nicht besser als 4,0.

## Ausgabe (exakt so)
````markdown
# Prüfbericht NEXUS-AI v1.2.0 (Kurz)
Modell: <Name, Version> · Datum: <JJJJ-MM-TT> · Repo-Zugriff: <ja/nein>

| Kriterium | Note | Begründung (max. 3 Sätze, mit Belegen) |
|---|---|---|
| K1 | | |
| K2 | | |
| K3 | | |
| K4 | | |
| Gesamt | | K.-o. angewendet: ja/nein |

Kritische Befunde (max. 3): Befund – Beleg – Maßnahme
Top-3-Maßnahmen: Maßnahme – Datei – Kriterium – Wirkung – Aufwand

```json
{"modell":"","datum":"","repo_zugriff":false,
 "noten":{"K1":0,"K2":0,"K3":0,"K4":0},"gesamt":0.0,"ko_regel":false,
 "pruefpunkte":{"K1.1":"","K1.2":"","K1.3":"","K1.4":"","K1.5":"","K1.6":"",
   "K2.1":"","K2.2":"","K2.3":"","K2.4":"","K2.5":"",
   "K3.1":"","K3.2":"","K3.3":"","K3.4":"","K3.5":"",
   "K4.1":"","K4.2":"","K4.3":"","K4.4":"","K4.5":""},
 "kritisch":[{"befund":"","datei":"","massnahme":""}],
 "massnahmen":[{"rang":1,"massnahme":"","datei":"","kriterium":"K1","wirkung":"hoch","aufwand":"S"}]}
```
````
Status-Werte: `erfuellt`, `teilweise`, `nicht_erfuellt`, `nicht_pruefbar`.
