---
schema: IOD.01/1.0
run_id: 2026-10-13__NEXUS-MULTI-LLM-ORCHESTRATOR__R001
type: artifact
artifact: 03_ARTIFACTS/evaluation/NEXUS_EVAL_SYNTHESE_COUNCIL_261013.md
archived_ts: 2026-10-15T06:00:48+02:00
sha256_original: 3c997aa800feff029f6123dde160e40be61e582b0ea24e1a781d677bfee94791
---

# NEXUS-AI LLM-Evaluierung – Synthese Model Council

Stand: 13.10.2026 · Prüfgegenstand: `nexus-platform`, Branch `feat/eval-automation` (Commit `6e8f574` = `main` `78ce229` + PR #12)
Bogen: `evaluation/NEXUS_EVAL_BOGEN_v1.0.md` mit automatisch erzeugtem Kontextpaket; alle drei Modelle hatten zusätzlich Lesezugriff auf das Repo.
Modelle: Claude Fable 5.1, GPT 6.1 Sol, Gemini 3.7 Flash

## Noten

| Kriterium (Gewicht) | Claude Fable 5.1 | GPT 6.1 Sol | Gemini 3.7 Flash | Mittel | Median | Spannweite |
|---|---|---|---|---|---|---|
| K1 Funktion (30 %) | 3 | 4 | 2 | 3,0 | 3 | 2 |
| K2 Sicherheit/Governance (25 %) | 4 | 5 | 2 | 3,7 | 4 | 3 |
| K3 Architektur/Wartbarkeit (25 %) | 3 | 3 | 2 | 2,7 | 3 | 1 |
| K4 Betrieb/Nutzen (20 %) | 3 | 4 | 1 | 2,7 | 3 | 3 |
| **Gesamt (gewichtet)** | **3,2** | **4,0** (K.-o.) | **1,8** | **3,0** | | |

Konsensurteil (Median je Kriterium): K1 3 · K2 4 · K3 3 · K4 3 → **Gesamt 3,3, Befriedigend**. Hauptursache ist das Privacy-Gate.

## Where Models Agree

| Finding | Claude Fable 5.1 | GPT 6.1 Sol | Gemini 3.7 Flash | Evidence |
|---|---|---|---|---|
| Das Privacy-Gate prüft case-sensitiv; Kleinschreibung wie „vertraulich“ geht an die Cloud | ✓ | ✓ | ✓ | `core.py:16–19`: `any(m in prompt …)`, reproduziert mit Mocks |
| Model Council meldet `consensus=true` schon bei nur einer gültigen Antwort; Konsens = Textgleichheit | ✓ | ✓ | ✓ | `core.py:48–58` |
| Fallback greift nur bei `ProviderError`; Parsing-Fehler (`KeyError`, `FileNotFoundError`) brechen die Kette ab | ✓ | ✓ | | `core.py:37`, `providers.py:42–69` |
| Klare Schichtung Config/Core/Provider/CLI, Provider für Tests injizierbar | ✓ | ✓ | ✓ | `core.py:7–14`, `providers.py`, `cli.py` |
| Tests (17/17) laufen offline grün, decken aber Gate-Varianten, Quorum und Adapterverträge nicht ab | ✓ | ✓ | ✓ | `tests/test_orch.py` |
| Drive-Sync löscht nie, Keys nur aus der Umgebung, Audit nur mit Prompt-Hash | ✓ | ✓ | ✓ | `sync_nexus.ps1`, `providers.py:22–29`, `core.py:68–76` |

## Where Models Disagree

| Topic | Claude Fable 5.1 | GPT 6.1 Sol | Gemini 3.7 Flash | Why They Differ |
|---|---|---|---|---|
| Schwere der Gate-Lücke (K2) | 4: relevante Lücke ohne Gegenmaßnahme | 5: nachgewiesener Abflusspfad, löst K.-o. aus | 2: kleiner Mangel, einfach zu beheben | Unterschiedliche Lesart des Ankers „Abflusspfad“: GPT nimmt den Anker wörtlich, Gemini gewichtet den geringen Behebungsaufwand. |
| Betrieb/Nutzen (K4) | 3 | 4: Setup prüft keine Exitcodes, Nutzen nicht gemessen | 1: Installation und Doku vorbildlich | Gemini bewertet die Bedienbarkeit, GPT verlangt messbare Nutzenevidenz und robuste Skripte. |
| Funktion (K1) | 3: `gpt-5` mit Temperatur 0.0 dauerhaft defekt | 4: zusätzlich defekter OCR-Fallback | 2: Kern funktioniert, nur Retries fehlen | Claude und GPT haben tiefer in die API-Verträge geschaut, Gemini blieb bei den Testergebnissen. |
| Evaluierungsfunktion `nexus eval` | nicht als kritisch genannt | kritisch: umgeht Router und Gate ohne technische Freigabe | nicht genannt | Nur GPT hat die neue Funktion als Datenpfad mit synthetischem Testinhalt geprüft. |

## Unique Discoveries

| Model | Unique Finding | Why It Matters |
|---|---|---|
| Claude Fable 5.1 | `gpt-5` akzeptiert nur Temperatur 1; mit 0.0 kommt bei jedem Aufruf HTTP 400 `unsupported_value` | Bestätigt durch [OpenAI-Community](https://community.openai.com/t/gpt-5-models-temperature/1337957) und [NeMo-Toolkit-Issue](https://github.com/NVIDIA/NeMo-Agent-Toolkit/issues/1124): Die Routen `draft` und `review` sowie der Council verlieren GPT stillschweigend. |
| Claude Fable 5.1 | Der Auto-Sync führt frisch gezogenen Code bei der Anmeldung mit `ExecutionPolicy Bypass` aus; `COMMUNICATION/audit` steht nicht in `.gitignore` | Lieferkettenrisiko bei kompromittiertem GitHub-Zugang; das passt zur Warnung vor dem geleakten Token. |
| GPT 6.1 Sol | Der OCR-Fallback sendet Gemini nur Pfad bzw. URL als Text, nicht das Bild | Fällt Vision aus, liefert Gemini kein echtes OCR-Ergebnis. |
| GPT 6.1 Sol | `write_lesson` lässt per `**lesson` Status, ID und Zeit überschreiben | Freigabestatus `PROPOSED` ist umgehbar. |
| GPT 6.1 Sol | Die Auswertung mischt alte und neue Prüfstände desselben Modells | Verfälscht Trends zwischen Evaluierungsrunden. |
| Gemini 3.7 Flash | Keine Retries mit Backoff bei 429/5xx | Kurze Ausfälle der Anbieter lösen sofort den Fallback aus, Kosten und Qualität schwanken. |

## Comprehensive Analysis

Die Befunde mit der höchsten Sicherheit sind die, die alle drei Modelle unabhängig gefunden und zum Teil mit Mocks reproduziert haben. Das Privacy-Gate vergleicht die Marker case-sensitiv und nur im Prompt, nicht im Systemtext. Ein Dokument mit „Vertraulich:“ oder ein `--system`-Text mit „VERTRAULICH“ geht damit an Perplexity. Für ein Büro, das unter Berufsgeheimnis arbeitet, ist das die wichtigste Schwachstelle, unabhängig davon, ob man sie mit 2, 4 oder 5 benotet. Ebenso einig sind die Modelle beim Model Council. Konsens heißt dort bloß identischer Text, und schon eine einzige gültige Antwort gilt als Konsens. Das widerspricht dem Zweck „Konsens und Abweichungen ausweisen“ bei Ingenieurentscheidungen. Positiv übereinstimmend bewertet werden die schlanke Architektur ohne Fremdabhängigkeiten, die testbaren Provider, der Sync ohne Löschen und das datensparsame Audit.

Die große Streuung (Gesamt 1,8 bis 4,0) kommt fast vollständig aus der Auslegung der Notenanker, nicht aus anderen Fakten. Gemini 3.7 Flash fand dieselbe Gate-Lücke, wertete sie aber als „einfach behebbar“ und blieb nahe an der Selbstbeschreibung des Repos. Claude Fable 5.1 und GPT 6.1 Sol prüften die API-Verträge und Fehlerpfade gegen. Ihre Zusatzbefunde (Temperatur bei `gpt-5`, Abbruch der Ausweichkette bei Parsing-Fehlern, OCR-Fallback ohne Bild) sind im Code belegbar. Die Temperaturfrage ist zusätzlich extern belegt. Die strengeren Urteile sind deshalb belastbarer. Die Note 5 von GPT folgt formal korrekt dem Anker „nachweisbarer Abflusspfad“. Ob die Sicherheit 4 oder 5 bekommt, ist eine Ermessensfrage, die Maßnahme ist dieselbe.

Wertvoll sind einzelne Befunde nur eines Modells. Der GPT-Provider ist mit `gpt-5` und Temperatur 0.0 vermutlich bei jedem Aufruf defekt, ohne dass das auffällt. Der Auto-Sync führt frisch gezogenen Code aus, was zusammen mit dem gemeldeten Token-Leak ein reales Lieferkettenrisiko ist. `nexus eval` umgeht das Gate bewusst, aber nur per Kommentar abgesichert. Und Lessons können ihren Status selbst setzen.

Empfehlung: Zuerst ein kleiner Sicherheits-PR, der in wenigen Stunden mehrere Kriterien hebt.
1. Gate mit `casefold()` über Prompt und Systemtext, mit Regex-Markern und Negativtests.
2. Quorum für den Council: mindestens 2 Antworten, sonst `consensus=null`.
3. Parsing-Fehler als `ProviderError` kapseln.
4. `gpt-5` ohne Temperaturparameter aufrufen (oder ein Modell mit Temperaturunterstützung wählen).
5. `write_lesson` erzwingt `PROPOSED`.
6. `audit/` in `.gitignore`, Auto-Sync auf geprüfte Commits begrenzen.

Danach Retries mit Backoff, ein echter multimodaler OCR-Fallback und die Trennung der Prüfstände in der Auswertung. Nach diesen Punkten ist eine neue Evaluierungsrunde sinnvoll. Die Modelle erwarten dann für K1 und K2 die Note 2.
