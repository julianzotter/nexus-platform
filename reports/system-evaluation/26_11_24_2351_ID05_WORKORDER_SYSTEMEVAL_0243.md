---
name: 26_11_24_2351_ID05_WORKORDER_SYSTEMEVAL_LEDGER-PENDING
version: "1.0"
status: REVIEW
timestamp: "2026-11-24T23:51:58+01:00"
timezone: Europe/Vienna
agent_id: ID05
role_id: ID05
owner_id: ID05
issuer_id: ID01
executor_instance: OpenAI Codex /root
provider: OpenAI
model_id: null
role_register_version: NEXUS-ROLES-v1.2
ticket_id: WO-20261124-ID05-SYSTEMEVAL
registration_status: REGISTRATION_PENDING
ledger_id: null
release_status: NO_RELEASE
hash_scope: body_utf8_after_closing_frontmatter_lf
hash: 6eb668e9da7396307b1c1cc5a5dd7188014cc07690aee730b6642c63cea9bbe9
task_state: OPEN
reviewer_instance: null
priority: HIGH
supervising_role: ID01
---
# Offener Aufruf an alle aktiven NEXUS-ID-Rollen

WO-20261124-ID05-SYSTEMEVAL · Auftraggeber ID01 · Koordination für diesen Auftrag ID05, ausgeführt durch OpenAI Codex /root. Im Manifest ist Perplexity der reguläre Akteur für ID05. Ein Perplexity-Lauf ist gesondert nachzuweisen. ID01 entscheidet über Änderungen. Der Aufruf hat keine vorgegebene Frist.

## Auftrag

Prüft die Unterschiede zwischen den vier Drive-Originalen und ihren GitHub-Snapshots sowie die Einhaltung der Kommunikations-, Registrierungs- und Freigaberegeln. Wählt einen Prüfpunkt frei, meldet die beanspruchte Aufgabe und führt mindestens eine eigene Prüfung am angegebenen Stand durch. Verweise auf bereits vorhandene Befunde sind willkommen. Nennt dabei die Erstquelle und den neu geprüften Stand.

| Prüfpunkt | Fragestellung | Abnahmekriterium |
|---|---|---|
| A · Regeln und Daten | Welche Fassungen von Manifest, Baseline, AGBs und Frontmatter gelten für welchen Zweck? | Vier Drive-IDs, Rohbyte-SHA-256, Git-Pfade und volle Commit-SHAs. Jede inhaltliche Differenz erhält einen Änderungsvorschlag mit Richtung, Zuständigkeit und Entscheidungsbedarf. |
| B · WORK und Register | Welche Steuerdateien und Ergebnisse lassen sich über Provider-ID, Registerzeile und Hash wiederfinden? | Quellenzeit, Zähler und Nenner angeben. Einen fehlenden oder überholten Eintrag reproduzieren. YAML, Dateiname, Ledger- und Freigabestatus gesondert prüfen. |
| C · Betrieb und Review | Tragen CI, Zustellung, ACK, unabhängiges Review und Wiederanlauf den gemeldeten Zustand? | Je Behauptung Run-/Kommentar-/Artefaktlink und Commit angeben. Für die Betriebsfreigabe drei getrennte reale E2E-Läufe mit Ziel-ID, Rücklesehash und Registerbeleg nachweisen; fehlende Nachweise einzeln ausweisen. |

## Beteiligung und Rücklauf

| Rolle | Freier Beitrag |
|---|---|
| ID01 · Julian Zotter | Über Richtungsentscheidungen, Regeländerungen und spätere Freigabe entscheiden. |
| ID02 · ChatGPT Business | Originale und Kopfstände unabhängig prüfen. Den bereits angeforderten Review zu #124/#128 kenntlich machen. |
| ID03 · ChatGPT Private | Manifest-/Baseline-Differenzen und GitHub-Task-Zuordnungen mit Erstquellen erklären. |
| ID04 · Gemini | Statusübergänge, Zeitstempel, Provenienz und Widersprüche protokollieren. |
| ID05 · Perplexity, reguläre Zuordnung | Primärquellen und Gegenbelege prüfen. Dieser Codex-Aufruf ist kein unabhängiger Rücklauf von Perplexity. |
| ID06 · Claude | Parser, Registerabgleich, Workflow-Protokolle und Abnahmetests reproduzieren. Eigene Änderungen fremdprüfen lassen. |
| ID07 · DeepSeek | Architektur, Fehlermodi und konkurrierende Befunde unabhängig bewerten. Bei fehlendem Direktzugriff Rücklauf über ID01. |
| ID08 · Ollama, optional | Datenminimierte lokale Gegenprüfung an bereitgestelltem Material. Modell, Input-Hash und Grenzen nennen. |

ID09 und ID10 sind als inaktiv verzeichnet. Eine Reaktivierung liegt bei ID01. Technische Rechte, Zustellung und Identität sind für jede Runtime einzeln zu belegen.

1. In WORK eine Startmeldung gemäß AGB §10 ablegen oder über den vorgesehenen Relay-Weg an ID01 geben. Im zugehörigen GitHub-PR oder in WORK per `CLAIM WO-20261124-ID05-SYSTEMEVAL` Rolle, Runtime, Modell-ID, Zugriffsbeleg und Prüfpunkt nennen.
2. Als `RESULT WO-20261124-ID05-SYSTEMEVAL` mit Zeit, Quell-ID/URL, Revision/SHA, Beobachtung, Auswirkung, priorisiertem Vorschlag, Abnahmetest und offenem Entscheid antworten. Eine einzelne belastbare Abweichung genügt. WORK-Dateiname gemäß AGB §4, Zeit in Europe/Vienna, Nummer nur vom Ledger-Schreiber. WORK-Link als PR-Kommentar hinterlegen, soweit Zugriff besteht.
3. ID05 konsolidiert je Quelle, Commit und Befund, verknüpft Duplikate und dokumentiert Dissens. Für einen Release Architektur-, Governance- und Systemperspektive unabhängig belegen, Korrekturen am neuen Head nachprüfen und ID01-Entscheidung dokumentieren. Zustände Publikation, Zustellung, ACK, Review, Register und Freigabe getrennt führen.

[WORK](https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP) · [Startmeldung](https://drive.google.com/file/d/12oXyYjt1TTnmrPxK1gacfmdkBWyd04WK/view) · [AGBs](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view) · [Frontmatter](https://drive.google.com/file/d/1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi/view) · [Manifest](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view) · [Baseline](https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view) · [Rollen-PR #128](https://github.com/julianzotter/nexus-platform/pull/128)
