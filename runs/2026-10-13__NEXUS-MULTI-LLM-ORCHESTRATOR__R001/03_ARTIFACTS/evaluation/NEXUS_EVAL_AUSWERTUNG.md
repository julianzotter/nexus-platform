---
schema: IOD.01/1.0
run_id: 2026-10-13__NEXUS-MULTI-LLM-ORCHESTRATOR__R001
type: artifact
artifact: 03_ARTIFACTS/evaluation/NEXUS_EVAL_AUSWERTUNG.md
archived_ts: 2026-10-15T06:00:48+02:00
sha256_original: ac5a01e0786b1ee3aaab0988e95fce54bb80d4a1d32fbd6cb65b5698654b5821
---

# NEXUS-AI – Auswertung der Prüfberichte
Berichte: 3

## Noten je Modell
| Modell | K1 Funktion | K2 Sicherheit/Governance | K3 Architektur/Wartbarkeit | K4 Betrieb/Nutzen | Gesamt (nachgerechnet) | Gesamt (Modell) |
|---|---|---|---|---|---|---|
| Claude (Anthropic) – Council-Instanz claude_fable_5_1 | 3 | 4 | 3 | 3 | 3.2 | 3.3 |
| Gemini 3.7 Flash | 2 | 2 | 2 | 1 | 1.8 | 1.8 |
| GPT-6.1 Sol | 4 | 5 | 3 | 4 | 4.0 | 4.0 |

## Konsens je Kriterium
| Kriterium | Mittel | Median | Spannweite | Streuung | Konsens |
|---|---|---|---|---|---|
| K1 Funktion | 3.00 | 3.0 | 2–4 | 0.82 | ABWEICHUNG prüfen |
| K2 Sicherheit/Governance | 3.67 | 4.0 | 2–5 | 1.25 | ABWEICHUNG prüfen |
| K3 Architektur/Wartbarkeit | 2.67 | 3.0 | 2–3 | 0.47 | stabil |
| K4 Betrieb/Nutzen | 2.67 | 3.0 | 1–4 | 1.25 | ABWEICHUNG prüfen |

**Gesamtnote (gewichtetes Mittel aller Modelle): 3.0**

## Prüfpunkte mit Mehrheitsbefund
| ID | erfüllt | teilweise | nicht erfüllt | nicht prüfbar |
|---|---|---|---|---|
| K1.1 | 3 | 0 | 0 | 0 |
| K1.2 | 1 | 2 | 0 | 0 |
| K1.3 | 0 | 2 | 1 | 0 |
| K1.4 | 3 | 0 | 0 | 0 |
| K1.5 | 1 | 2 | 0 | 0 |
| K1.6 | 2 | 0 | 1 | 0 |
| K2.1 | 0 | 1 | 2 | 0 |
| K2.2 | 1 | 2 | 0 | 0 |
| K2.3 | 1 | 2 | 0 | 0 |
| K2.4 | 1 | 2 | 0 | 0 |
| K2.5 | 0 | 2 | 1 | 0 |
| K3.1 | 3 | 0 | 0 | 0 |
| K3.2 | 1 | 2 | 0 | 0 |
| K3.3 | 0 | 3 | 0 | 0 |
| K3.4 | 0 | 3 | 0 | 0 |
| K3.5 | 1 | 2 | 0 | 0 |
| K4.1 | 2 | 1 | 0 | 0 |
| K4.2 | 1 | 2 | 0 | 0 |
| K4.3 | 1 | 2 | 0 | 0 |
| K4.4 | 1 | 2 | 0 | 0 |
| K4.5 | 1 | 2 | 0 | 0 |

## Kritische Befunde (alle Modelle)
- [Claude (Anthropic) – Council-Instanz claude_fable_5_1] Privacy Hard Gate case-sensitiv und ohne Pruefung des --system-Textes; 'Vertraulich:'/'vertraulich' gehen an Cloud (reproduziert) – orchestrator/nexus_orch/core.py:16-19 → casefold()-Vergleich ueber prompt+system, Regex-Marker in routing.json, --private-Flag, Tests
- [Claude (Anthropic) – Council-Instanz claude_fable_5_1] Provider gpt mit gpt-5 + temperature 0.0 dauerhaft defekt (HTTP 400 unsupported_value); draft degradiert still, Council ohne GPT – orchestrator/config/routing.json:20; orchestrator/nexus_orch/providers.py:41 → params/supports_temperature je Provider, gpt-5 ohne temperature oder gpt-5-chat-latest/gpt-4.1, nexus status --probe
- [Claude (Anthropic) – Council-Instanz claude_fable_5_1] Fallback nur bei ProviderError; KeyError/FileNotFoundError aus Antwort-Parsing/OCR brechen Kette ohne Audit ab (reproduziert) – orchestrator/nexus_orch/core.py:37; orchestrator/nexus_orch/providers.py:42-69 → Parsing in try/except -> ProviderError kapseln, Fehllaeufe auditieren
- [Claude (Anthropic) – Council-Instanz claude_fable_5_1] Council meldet consensus=True bei nur einem antwortenden Mitglied; Konsens = Stringgleichheit – orchestrator/nexus_orch/core.py:51-58 → Quorum in Route, consensus=None + warning bei Unterbesetzung, Judge-basierte Konsensbewertung
- [Claude (Anthropic) – Council-Instanz claude_fable_5_1] COMMUNICATION/audit nicht in .gitignore; Auto-Sync fuehrt bei Anmeldung frisch gepullten Remote-Code (pytest) mit ExecutionPolicy Bypass aus – .gitignore; orchestrator/install_autosync.ps1:13-17; orchestrator/sync_nexus.ps1:16-19 → audit/ ignorieren, Sync auf Tag/Commit pinnen, pytest im Sync optional
- [Gemini 3.7 Flash] Case-Sensitive Privacy Hard Gate ermöglicht Umgehung bei Kleinschreibung – orchestrator/nexus_orch/core.py:18 → Case-insensitive Prüfung via `m.lower() in prompt.lower()` oder Regex mit Wortgrenzen implementieren.
- [Gemini 3.7 Flash] Schein-Konsens bei Einzelausfall und naive String-Gleichheit im Model Council – orchestrator/nexus_orch/core.py:54-68 → Mindestquorum (>= 2 Antworten) für Konsens fordern; semantische Konsensprüfung im Synthese-Prompt verankern.
- [Gemini 3.7 Flash] Fehlende HTTP-Retries bei transienten Fehlern (429 Rate Limit / 503) – orchestrator/nexus_orch/providers.py:7-17 → Exponential-Backoff-Retries für transiente Statuscodes (429, 500, 502, 503, 504) in `_post()` einbauen.
- [GPT-6.1 Sol] Privacy-Gate übersieht Schreibvarianten und vertraulichen Systemkontext; Cloud-Routing offline reproduziert. – orchestrator/nexus_orch/core.py:16-19,28-33,41-48 → Vollständigen Request normalisieren und klassifizieren; explizite Privacy-Klasse, lokale Fail-closed-Prüfung und Negativtests. Aufwand M; D1.
- [GPT-6.1 Sol] Evaluierung umgeht Router und Privacy-Gate ohne technische Inhaltsfreigabe; synthetischer vertraulicher Kommentar erreicht Cloud-Mock. – orchestrator/nexus_orch/evaluate.py:3-4,36-47,60 → Nur freigegebenen Snapshot versenden; Inhalts-/Metadatenprüfung und Bestätigung von Empfängern samt Paket-Hash. Aufwand M; D1.
- [GPT-6.1 Sol] Ein Council-Mitglied erzeugt consensus=true; Quellen/Fehlergründe werden verworfen und Syntheseausfall ist ungesichert. – orchestrator/nexus_orch/core.py:48-65 → Mindestquorum, degradierter Zustand, strukturierte Evidenzprüfung, Quellen-/Fehlererhalt, Judge-Fallback und Ingenieurfreigabe. Aufwand M; D2.
- [GPT-6.1 Sol] OCR-Fallback sendet Gemini nur Textpfad/URL statt eines multimodalen Bild-Requests. – orchestrator/nexus_orch/providers.py:49-69 → Typisierten multimodalen OCR-Adapter einführen; ohne geprüfte Bildfähigkeit mit Capability-Fehler abbrechen. Aufwand M; D3.
- [GPT-6.1 Sol] Auswertung akzeptiert unvollständige Berichte und vermischt unterschiedliche Prüfstände desselben Modells; synthetisch ergibt alter Stand 1 plus aktueller Stand 5 die Gesamtnote 3.0. – evaluation/nexus_eval_auswertung.py:18-36 → Vollständiges Schema und Run-/Commit-/Prompt-Kohorte validieren; eine Stimme je Modell, getrennte Historie. Aufwand M; D4.

## Maßnahmen-Backlog (nach Nennungen, dann Rang)
| Maßnahme | Datei | Kriterium | Wirkung | Aufwand | Modell | Rang |
|---|---|---|---|---|---|---|
| Privacy-Gate: casefold, Regex-Marker, prompt+system, --private-Flag, Tests | orchestrator/nexus_orch/core.py; orchestrator/config/routing.json; orchestrator/nexus_orch/cli.py; orchestrator/tests/test_orch.py | K2 | hoch | S | Claude (Anthropic) – Council-Instanz claude_fable_5_1 | 1 |
| Privacy Gate case-insensitiv & mit Wortgrenzen absichern | orchestrator/nexus_orch/core.py | K2 | hoch | S | Gemini 3.7 Flash | 1 |
| D1: Datenschutzgrenze über alle Eingabekanäle schließen; Eval-Snapshot/Freigabe, Error-Redaction und gemeinsame Git-/Sync-Ausschlüsse. | orchestrator/nexus_orch/core.py:16-19,28-33; orchestrator/nexus_orch/evaluate.py:36-60; orchestrator/nexus_orch/providers.py:12-17; orchestrator/nexus_orch/cli.py; .gitignore:152-160,222-225; orchestrator/sync_nexus.ps1:21-22; orchestrator/sync_nexus_rclone.ps1:31-34; orchestrator/tests/test_orch.py | K2 | hoch | M | GPT-6.1 Sol | 1 |
| Antwort-Parsing in ProviderError kapseln; Fehllaeufe auditieren; Audit um user/host/model/members/judge/latency/usage erweitern | orchestrator/nexus_orch/providers.py; orchestrator/nexus_orch/core.py | K1 | hoch | S | Claude (Anthropic) – Council-Instanz claude_fable_5_1 | 2 |
| Model Council Mindestquorum (>= 2) & Ausfall-Handling schärfen | orchestrator/nexus_orch/core.py | K1 | hoch | S | Gemini 3.7 Flash | 2 |
| D2: Council-Quorum, belegte Konsens-/Dissensprüfung, Fehler-/Quellenerhalt, abgesicherte Synthese und fachliche Freigabe. | orchestrator/nexus_orch/core.py:44-67; orchestrator/config/routing.json:87-98; orchestrator/tests/test_orch.py:30-37; orchestrator/README.md | K1 | hoch | M | GPT-6.1 Sol | 2 |
| Provider-Parameter je Modell (params, supports_temperature, max_completion_tokens); gpt-5 korrigieren; nexus status --probe | orchestrator/config/routing.json; orchestrator/nexus_orch/providers.py; orchestrator/nexus_orch/cli.py | K1 | hoch | S | Claude (Anthropic) – Council-Instanz claude_fable_5_1 | 3 |
| HTTP-Retry mit Exponential Backoff bei 429/503 implementieren | orchestrator/nexus_orch/providers.py | K3 | hoch | S | Gemini 3.7 Flash | 3 |
| D3: Typisierte Adapterverträge und Capability-/Schemavalidierung, Fehlernormalisierung, transiente Retries sowie echter multimodaler OCR-Pfad. | orchestrator/nexus_orch/providers.py:7-70; orchestrator/nexus_orch/core.py:28-39; orchestrator/config/routing.json; orchestrator/tests/test_orch.py | K1/K3 | hoch | M | GPT-6.1 Sol | 3 |
| Council: Quorum, consensus=None bei Unterbesetzung, Judge-basierte strukturierte Synthese (Konsens/Abweichungen/Empfehlung/Normbezug) | orchestrator/nexus_orch/core.py; orchestrator/config/routing.json; orchestrator/tests/test_orch.py | K1 | mittel | M | Claude (Anthropic) – Council-Instanz claude_fable_5_1 | 4 |
| PEP 484 Typ-Annotationen & Schnittstellendokumentation ergänzen | orchestrator/nexus_orch/core.py, providers.py | K3 | mittel | M | Gemini 3.7 Flash | 4 |
| D4: Immutable Evaluierungskohorte mit vollständigem Schema; Attempt-Audit, erzwungene Lessons-Metadaten/Review und Datei-Hashmanifest für SSOT. | orchestrator/nexus_orch/core.py:71-98; orchestrator/nexus_orch/evaluate.py:49-85; evaluation/nexus_eval_auswertung.py:18-36; orchestrator/sync_nexus.ps1:24-28; orchestrator/sync_nexus_rclone.ps1:47-51; orchestrator/tests/test_orch.py | K2/K3/K4 | hoch | M | GPT-6.1 Sol | 4 |
| Retries/Backoff 429/5xx, Token-/Kostenlog, Lessons-Review-Befehl, audit/ in .gitignore, Sync auf Tag pinnen | orchestrator/nexus_orch/providers.py; orchestrator/nexus_orch/core.py; orchestrator/nexus_orch/cli.py; .gitignore; orchestrator/sync_nexus.ps1; orchestrator/sync_nexus_rclone.ps1 | K3 | mittel | M | Claude (Anthropic) – Council-Instanz claude_fable_5_1 | 5 |
| Token- und Kosten-Metadaten im Audit-Log erfassen | orchestrator/nexus_orch/core.py, providers.py | K4 | mittel | S | Gemini 3.7 Flash | 5 |
| D5: Fail-fast Windows-Setup/Sync, Paketressourcen und Smokechecks, Readiness/Budget-/Latenzmessung sowie Transferdokumentation und fachlicher AEC-Goldsatz. | orchestrator/setup.ps1:2-11; orchestrator/sync_nexus.ps1:15-19; orchestrator/sync_nexus_rclone.ps1:18-19,47-51; orchestrator/pyproject.toml:14-15; orchestrator/nexus_orch/core.py; orchestrator/nexus_orch/providers.py; orchestrator/nexus_orch/cli.py; orchestrator/README.md; orchestrator/tests/ | K4 | hoch | L | GPT-6.1 Sol | 5 |