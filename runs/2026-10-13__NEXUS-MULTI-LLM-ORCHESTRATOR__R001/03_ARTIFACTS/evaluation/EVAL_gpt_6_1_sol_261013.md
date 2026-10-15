---
schema: IOD.01/1.0
run_id: 2026-10-13__NEXUS-MULTI-LLM-ORCHESTRATOR__R001
type: artifact
artifact: 03_ARTIFACTS/evaluation/EVAL_gpt_6_1_sol_261013.md
archived_ts: 2026-10-15T06:00:48+02:00
sha256_original: 22e1b0a7c0ecd40c74561c694204200a0ad40f3e1bb0c620a50fdec276bb6951
---

# Prüfbericht NEXUS-AI v1.2.0
Prüfendes Modell: GPT-6.1 Sol  ·  Datum: 2026-10-13  ·  Repo-Zugriff: ja, read-only

## A Ergebnis
| Kriterium | Note | Begründung (2–4 Sätze) |
|---|---|---|
| K1 Funktion | 4 | Routing und regulärer Fallback sind vorhanden; die vorgegebenen 17 Tests bestehen offline ([core.py:16–39](/tmp/n/np/orchestrator/nexus_orch/core.py), [Prüflog:3–5](/home/user/workspace/nexus_gpt_6_1_test_run.txt)). Ein einziges erfolgreiches Council-Mitglied erzeugt jedoch `consensus=true`, und Adapter-Schemafehler umgehen den Fallback ([core.py:48–65](/tmp/n/np/orchestrator/nexus_orch/core.py), [providers.py:42–69](/tmp/n/np/orchestrator/nexus_orch/providers.py)). Der OCR-Fallback übergibt Gemini nur einen Textpfad beziehungsweise eine URL, kein Bild; damit bestehen wesentliche ergebnisrelevante Einschränkungen ([providers.py:49–53](/tmp/n/np/orchestrator/nexus_orch/providers.py)). |
| K2 Sicherheit/Governance | 5 | Das Hard Gate ist sicherheitskritisch umgehbar: Groß-/Kleinschreibung wird nicht normalisiert, der Systemkontext wird nicht geprüft ([core.py:16–19,28–33,41–48](/tmp/n/np/orchestrator/nexus_orch/core.py)). Die neue Evaluierungsfunktion umgeht den Router ausdrücklich, ohne die angenommene Unvertraulichkeit der gelesenen Inhalte technisch abzusichern ([evaluate.py:3–4,36–47,49–60](/tmp/n/np/orchestrator/nexus_orch/evaluate.py)). Audit und Lessons besitzen zusätzlich Governance-Lücken; der Note-5-Anker wird durch den nachgewiesenen Gate-Mangel erfüllt ([core.py:71–98](/tmp/n/np/orchestrator/nexus_orch/core.py)). |
| K3 Architektur/Wartbarkeit | 3 | JSON, Orchestrierung, Adapter und CLI sind übersichtlich getrennt; Provider lassen sich für Tests injizieren ([core.py:7–14](/tmp/n/np/orchestrator/nexus_orch/core.py), [providers.py:19–70](/tmp/n/np/orchestrator/nexus_orch/providers.py), [cli.py:6–54](/tmp/n/np/orchestrator/nexus_orch/cli.py)). Nacharbeit benötigen insbesondere typisierte Adapterverträge, vollständige Fehlernormalisierung und belastbare Paket-/Konfigurationsgrenzen; Konfiguration und Registry werden außerhalb des einzigen paketierten Python-Pakets gesucht ([providers.py:35–69](/tmp/n/np/orchestrator/nexus_orch/providers.py), [core.py:5–8](/tmp/n/np/orchestrator/nexus_orch/core.py), [pyproject.toml:14–15](/tmp/n/np/orchestrator/pyproject.toml)). |
| K4 Betrieb/Nutzen | 4 | Editable-Installation und Windows-Sync sind dokumentiert, aber Setup prüft native Exitcodes nicht und die Sync-Skripte kontrollieren nicht jeden Teil ihrer Git-/Stamp-Sequenz ([README.md:18–40](/tmp/n/np/orchestrator/README.md), [setup.ps1:2–11](/tmp/n/np/orchestrator/setup.ps1), [sync_nexus.ps1:15–19](/tmp/n/np/orchestrator/sync_nexus.ps1), [sync_nexus_rclone.ps1:47–51](/tmp/n/np/orchestrator/sync_nexus_rclone.ps1)). Audit und Evaluierung reichen für belastbare Reproduzierbarkeit nicht aus; ältere und aktuelle Berichte werden ohne Kohortenfilter zusammengerechnet ([core.py:71–76](/tmp/n/np/orchestrator/nexus_orch/core.py), [nexus_eval_auswertung.py:18–36](/tmp/n/np/evaluation/nexus_eval_auswertung.py)). Fachliche Anwendungen sind Beispiele, keine gemessene Nutzenevidenz; der fehlerhafte Bild-Fallback beschränkt den Planeinsatz zusätzlich ([README.md:27–30](/tmp/n/np/orchestrator/README.md), [providers.py:49–69](/tmp/n/np/orchestrator/nexus_orch/providers.py)). |
| **Gesamt (gewichtet)** | **4,0** | K.-o.-Regel angewendet: ja. Gewichtetes Mittel: 0,30 × 4 + 0,25 × 5 + 0,25 × 3 + 0,20 × 4 = 4,0; max(4,0; 4,0) = 4,0. |

## B Prüfpunkte
| ID | Status (erfüllt/teilweise/nicht erfüllt/nicht prüfbar) | Beleg (Datei:Zeile) | Feststellung |
|---|---|---|---|
| K1.1 | erfüllt | [orchestrator/config/routing.json:43–105](/tmp/n/np/orchestrator/config/routing.json); [orchestrator/nexus_orch/core.py:16–26](/tmp/n/np/orchestrator/nexus_orch/core.py); [orchestrator/tests/test_orch.py:26–28,45–48](/tmp/n/np/orchestrator/tests/test_orch.py) | Alle neun konfigurierten Routen verweisen auf vorhandene Provider; unbekannte unmarkierte Aufgaben ergeben einen definierten `KeyError`. |
| K1.2 | teilweise | [orchestrator/nexus_orch/core.py:28–39](/tmp/n/np/orchestrator/nexus_orch/core.py); [orchestrator/nexus_orch/providers.py:42–69](/tmp/n/np/orchestrator/nexus_orch/providers.py); [offline_probe_results.json:41–48](/home/user/workspace/nexus_gpt_6_1_probe_artifacts/offline_probe_results.json) | `ProviderError` wird gesammelt und löst Fallback aus. Schemafehler (`KeyError`) und fehlende OCR-Dateien (`FileNotFoundError`) brechen dagegen ohne Fallback ab; Adapterfehler normalisieren und explizit fatal/retryfähig klassifizieren → D3. |
| K1.3 | nicht erfüllt | [orchestrator/nexus_orch/core.py:44–67](/tmp/n/np/orchestrator/nexus_orch/core.py); [offline_probe_results.json:22–40](/home/user/workspace/nexus_gpt_6_1_probe_artifacts/offline_probe_results.json) | Ein gültiges Mitglied wird als Konsens ausgegeben; Fehlergründe und Zitate gehen verloren, Syntheseausfall wird nicht abgefangen. Textgleichheit nach Kleinschreibung/Whitespace ist kein fachlicher Konsensnachweis; Quorum, Evidenz und degradierten Zustand einführen → D2. |
| K1.4 | erfüllt | [orchestrator/config/routing.json:5–9](/tmp/n/np/orchestrator/config/routing.json); [orchestrator/nexus_orch/providers.py:38–42](/tmp/n/np/orchestrator/nexus_orch/providers.py); [orchestrator/nexus_orch/core.py:33–34](/tmp/n/np/orchestrator/nexus_orch/core.py) | Modellname ist konfigurierbar; der Einzelaufruf erhält die `citations` unverändert. Die separate Council-Lücke ist K1.3 zugeordnet; reale Zitierqualität ist nicht_pruefbar. |
| K1.5 | teilweise | [orchestrator/tests/test_orch.py:5–102](/tmp/n/np/orchestrator/tests/test_orch.py); [nexus_gpt_6_1_test_run.txt:3–11](/home/user/workspace/nexus_gpt_6_1_test_run.txt) | 17/17 Tests bestehen ohne Netz; Routing, Fallback, exakter Marker, Council und Lessons sind abgedeckt. Varianten/Systemkontext, Council-Quorum, Adapterverträge und Governance-Negativfälle fehlen im bestehenden Testsatz; reproduzierte Zusatzfälle übernehmen → D1–D4. |
| K1.6 | erfüllt | [orchestrator/nexus_orch/core.py:33,48,65](/tmp/n/np/orchestrator/nexus_orch/core.py); [orchestrator/nexus_orch/providers.py:41,45,49,57–58,65](/tmp/n/np/orchestrator/nexus_orch/providers.py) | Alle Textadapter setzen Temperatur tatsächlich; Ollama setzt zusätzlich `num_ctx`, OCR einen festen Feature-Typ. API-Akzeptanz der Parameter und bitgleiche Wiederholbarkeit sind nicht_pruefbar, nicht durch T=0 bewiesen. |
| K2.1 | nicht erfüllt | [orchestrator/nexus_orch/core.py:16–19,28–33,41–48](/tmp/n/np/orchestrator/nexus_orch/core.py); [orchestrator/config/routing.json:83–85](/tmp/n/np/orchestrator/config/routing.json); [offline_probe_results.json:2–20](/home/user/workspace/nexus_gpt_6_1_probe_artifacts/offline_probe_results.json) | Exakte Marker führen zur lokalen Route ohne Fallback. `vertraulich`, `Confidential`, `[p3]` sowie `VERTRAULICH` ausschließlich im Systemkontext gehen im Mocknachweis an Perplexity; alle Eingabekanäle normalisieren und lokal fail-closed erzwingen → D1. |
| K2.2 | teilweise | [orchestrator/nexus_orch/providers.py:12–17,22–29,40,52,64](/tmp/n/np/orchestrator/nexus_orch/providers.py); [.gitignore:152–160,222–225](/tmp/n/np/.gitignore); [orchestrator/sync_nexus.ps1:21–22](/tmp/n/np/orchestrator/sync_nexus.ps1); [orchestrator/sync_nexus_rclone.ps1:31–34](/tmp/n/np/orchestrator/sync_nexus_rclone.ps1) | Keys kommen aus Umgebung; Audit speichert keinen Prompt. HTTP-Fehlertexte werden unbereinigt weitergereicht, `.gitignore` deckt die Sync-Muster `*.key/*.pem/*.secret` nicht ab und Sync behandelt nur die exakte `.env`; Redaction und gemeinsame Ausschlussregeln ergänzen → D1. Tatsächlicher Secret-Bestand wurde ausdrücklich nicht untersucht. |
| K2.3 | teilweise | [orchestrator/nexus_orch/core.py:35–39,48–50,68–76](/tmp/n/np/orchestrator/nexus_orch/core.py); [offline_probe_results.json:31–35](/home/user/workspace/nexus_gpt_6_1_probe_artifacts/offline_probe_results.json) | UTC-Zeit, Prompt-Hash und Route sind vorhanden. Akteur, Modell-/Konfigurationsstand, Systemkontext-Hash, erfolglose Versuche und Council-Mitglieder fehlen; datensparsames Attempt-Audit ergänzen → D4. |
| K2.4 | teilweise | [orchestrator/nexus_orch/core.py:80–98](/tmp/n/np/orchestrator/nexus_orch/core.py); [orchestrator/nexus_orch/cli.py:12–14,33–36](/tmp/n/np/orchestrator/nexus_orch/cli.py); [orchestrator/sync_nexus.ps1:25](/tmp/n/np/orchestrator/sync_nexus.ps1); [orchestrator/sync_nexus_rclone.ps1:43](/tmp/n/np/orchestrator/sync_nexus_rclone.ps1); [offline_probe_results.json:63–67](/home/user/workspace/nexus_gpt_6_1_probe_artifacts/offline_probe_results.json) | Sync löscht keine Zielinhalte; CLI schreibt normalerweise `PROPOSED`. Die Bibliotheksfunktion lässt durch abschließendes `**lesson` Status, ID und Zeit überschreiben; ein Review-Übergang und Statusfilter fehlen. Reservierte Metadaten erzwingen und Review mit Akteur implementieren → D4. |
| K2.5 | nicht erfüllt | [orchestrator/nexus_orch/providers.py:38–69](/tmp/n/np/orchestrator/nexus_orch/providers.py); [orchestrator/nexus_orch/evaluate.py:3–4,33–41,60](/tmp/n/np/orchestrator/nexus_orch/evaluate.py); [orchestrator/README.md:61–74](/tmp/n/np/orchestrator/README.md) | Technischer Datenfluss ist ablesbar: Text/System an gewählte Cloud-Anbieter, Bildbytes oder Bild-URI an Vision, Evaluierungspaket samt Dateinamen an Cloud-Modelle. Eine überprüfbare Transfer-/Freigabematrix und Restrisikobewertung fehlen im vorgelegten Betriebsumfang; dokumentieren und Gate-Ausnahme absichern → D1/D5. AVV, Region, Aufbewahrung und tatsächliche DSGVO-Konformität: nicht_pruefbar. |
| K3.1 | erfüllt | [orchestrator/config/routing.json:1–116](/tmp/n/np/orchestrator/config/routing.json); [orchestrator/nexus_orch/core.py:7–14](/tmp/n/np/orchestrator/nexus_orch/core.py); [orchestrator/nexus_orch/providers.py:19–70](/tmp/n/np/orchestrator/nexus_orch/providers.py); [orchestrator/nexus_orch/cli.py:6–54](/tmp/n/np/orchestrator/nexus_orch/cli.py) | Konfiguration, Kernlogik, Adapter und CLI sind getrennt; Provider und Ablagewurzel sind injizierbar. |
| K3.2 | teilweise | [orchestrator/config/routing.json:4–106](/tmp/n/np/orchestrator/config/routing.json); [orchestrator/nexus_orch/providers.py:37–70](/tmp/n/np/orchestrator/nexus_orch/providers.py); [orchestrator/nexus_orch/evaluate.py:21](/tmp/n/np/orchestrator/nexus_orch/evaluate.py); [orchestrator/nexus_orch/cli.py:22–23](/tmp/n/np/orchestrator/nexus_orch/cli.py) | Bestehenden Adapter nutzen: eine Konfigurationsdatei; neue Route plus Workflow: Routing, Registry, Test. Neuer API-Typ zusätzlich `providers.py`, Evaluierungsmitglied zusätzlich `CLOUD`; typisierten Adaptervertrag und Validierung ergänzen → D3. Aufwand S für Route, M für neuen API-Typ: Prüfschätzung. |
| K3.3 | teilweise | [orchestrator/nexus_orch/providers.py:2,7–17,35–36](/tmp/n/np/orchestrator/nexus_orch/providers.py); [orchestrator/pyproject.toml:1–3](/tmp/n/np/orchestrator/pyproject.toml); [orchestrator/setup.ps1:2](/tmp/n/np/orchestrator/setup.ps1) | Laufzeit nutzt Standardbibliothek, Build benötigt setuptools und Tests pytest. Timeout und HTTP-Fehlerhilfe existieren; Retry/Backoff und Response-Schemavalidierung fehlen, Dekodierungsfehler entstehen außerhalb `_post`. Begrenzte Retries für transiente Fehler und vollständigen Fehlervertrag ergänzen → D3. |
| K3.4 | teilweise | [orchestrator/nexus_orch/core.py:1–98](/tmp/n/np/orchestrator/nexus_orch/core.py); [orchestrator/nexus_orch/providers.py:4–5,35–69](/tmp/n/np/orchestrator/nexus_orch/providers.py); [orchestrator/nexus_orch/evaluate.py:49–71](/tmp/n/np/orchestrator/nexus_orch/evaluate.py) | Kurze, lesbare Funktionen und eigene Fehlerklasse sind vorhanden. Öffentliche Schnittstellen sind untypisiert, Antworten unvalidierte Dicts; `evaluate.run` verändert Provider-Konfiguration dauerhaft. Typen/Schemata einführen und Evaluierungsparameter ohne Zustandsmutation übergeben → D3/D4. |
| K3.5 | teilweise | [orchestrator/sync_nexus.ps1:16–28,32–38](/tmp/n/np/orchestrator/sync_nexus.ps1); [orchestrator/sync_nexus_rclone.ps1:18–19,43–51](/tmp/n/np/orchestrator/sync_nexus_rclone.ps1); [orchestrator/registry/workflow-registry.json:2–10](/tmp/n/np/orchestrator/registry/workflow-registry.json); [orchestrator/tests/test_orch.py:45–48](/tmp/n/np/orchestrator/tests/test_orch.py) | Git-Stand, Zielstempel und Registry-Routenprüfung existieren. Nur `pull`, nicht separat `checkout`, wird auf Fehler geprüft; `rclone rcat` bleibt ungeprüft und alte Zieldateien bleiben unter neuem Stempel erhalten. Exitcodes/Branch prüfen, Dateihashmanifest und Altbestandkennzeichnung ergänzen → D4/D5; tatsächlicher Drive-Abgleich: nicht_pruefbar. |
| K4.1 | teilweise | [orchestrator/README.md:18–34](/tmp/n/np/orchestrator/README.md); [orchestrator/setup.ps1:2–11](/tmp/n/np/orchestrator/setup.ps1); [orchestrator/nexus_orch/cli.py:25–32](/tmp/n/np/orchestrator/nexus_orch/cli.py); [orchestrator/nexus_orch/providers.py:30–34](/tmp/n/np/orchestrator/nexus_orch/providers.py) | Editable-Installation und nützliche Key-/Ollama-Hinweise sind vorhanden. Setup ist CWD-abhängig, kontrolliert weder pip- noch Testexitcode; `status` prüft Keys, nicht Erreichbarkeit. Skriptwurzel, Fail-fast und getrennte Readiness-Prüfung einführen → D5; Windows-Ausführung: nicht_pruefbar. |
| K4.2 | teilweise | [orchestrator/pyproject.toml:2,7,9,14–15](/tmp/n/np/orchestrator/pyproject.toml); [orchestrator/config/routing.json:8–39](/tmp/n/np/orchestrator/config/routing.json); [orchestrator/nexus_orch/core.py:71–76](/tmp/n/np/orchestrator/nexus_orch/core.py); [orchestrator/nexus_orch/evaluate.py:40,63–69](/tmp/n/np/orchestrator/nexus_orch/evaluate.py); [evaluation/nexus_eval_auswertung.py:18–36](/tmp/n/np/evaluation/nexus_eval_auswertung.py) | Version/Modellnamen sind vorhanden, aber Audit ohne Konfigurationshash; Evaluierung liest den Arbeitsbaum und kennzeichnet nur HEAD, überschreibt Tagesberichte und aggregiert Altstände. Run-ID, Prompt-/Konfigurationshash, Dirty-Status, eindeutige Kohorte und gepackte Ressourcen ergänzen → D4/D5. |
| K4.3 | teilweise | [orchestrator/config/routing.json:29–34,87–98](/tmp/n/np/orchestrator/config/routing.json); [orchestrator/nexus_orch/core.py:46–65](/tmp/n/np/orchestrator/nexus_orch/core.py); [orchestrator/nexus_orch/providers.py:35–36](/tmp/n/np/orchestrator/nexus_orch/providers.py) | Lokale Route existiert; Engineering-Council tätigt seriell bis zu vier Erstaufrufe plus Synthese. Tokenverbrauch, Kosten, Laufzeit und Gesamtbudget werden nicht erfasst; Instrumentierung, Budget/Deadline und kontrollierte Parallelität ergänzen → D5. Reale Kosten/Latenzen: nicht_pruefbar. |
| K4.4 | teilweise | [orchestrator/README.md:27–30](/tmp/n/np/orchestrator/README.md); [orchestrator/nexus_orch/providers.py:49–69](/tmp/n/np/orchestrator/nexus_orch/providers.py); [orchestrator/tests/test_orch.py:30–37,50–57](/tmp/n/np/orchestrator/tests/test_orch.py); [offline_probe_results.json:49–61](/home/user/workspace/nexus_gpt_6_1_probe_artifacts/offline_probe_results.json) | Normen-/Varianten-/OCR-Routen sind angelegt, aber Tests nutzen Mocktexte statt Normausgaben oder Plan-Ground-Truth. Gemini-Fallback und lokaler Textadapter erhalten kein Bild. Multimodale Fähigkeit explizit prüfen oder OCR mit definiertem Fehler sperren → D3; fachlichen Goldsatz samt menschlicher Freigabe ergänzen → D5; messbarer AEC-Nutzen: nicht_pruefbar. |
| K4.5 | teilweise | [orchestrator/registry/workflow-registry.json:3–10,19–122](/tmp/n/np/orchestrator/registry/workflow-registry.json); [orchestrator/nexus_orch/cli.py:49–50](/tmp/n/np/orchestrator/nexus_orch/cli.py); [orchestrator/config/sync_targets.json:8–14](/tmp/n/np/orchestrator/config/sync_targets.json) | 17 Workflow-Einträge, SSOT-/Projektverweise und Sync-Ziele sind vorhanden. CLI zeigt Registry nur an, führt keine Workflows aus; tatsächliche Drive-/Perplexity-Verknüpfung ist nicht_pruefbar. Inventar klar von ausführbarer Integration unterscheiden und End-to-End-Smokecheck dokumentieren → D5. |

## C Kritische Befunde (max. 5, nur sicherheits- oder ergebnisrelevant)
1. **Hard Gate übersieht Schreibvarianten und Systemkontext.** Beleg: [orchestrator/nexus_orch/core.py:16–19,28–33,41–48](/tmp/n/np/orchestrator/nexus_orch/core.py); offline reproduziert mit `vertraulich`, `Confidential`, `[p3]` und einem markierten Systemtext ([offline_probe_results.json:6–20](/home/user/workspace/nexus_gpt_6_1_probe_artifacts/offline_probe_results.json)). Risiko: vertrauliche Inhalte können einen Cloud-Aufruf erreichen. Maßnahme: gemeinsame Klassifizierung des vollständigen Requests, Unicode-/Case-Normalisierung, explizite Privacy-Metadaten und fail-closed lokale Providerprüfung; `core.py`, `cli.py`, Tests, Aufwand M, D1.
2. **Evaluierung vertraut einer ungesicherten Inhaltsannahme.** Beleg: dokumentierte Gate-Ausnahme und direkter Adapteraufruf in [orchestrator/nexus_orch/evaluate.py:3–4,36–47,60](/tmp/n/np/orchestrator/nexus_orch/evaluate.py); synthetischer vertraulicher Kommentar erreicht den Cloud-Mock ([offline_probe_results.json:68–70](/home/user/workspace/nexus_gpt_6_1_probe_artifacts/offline_probe_results.json)). Risiko: versehentlich eingefügte Projektinformationen oder sensible lokale Dateinamen gelangen ins Evaluierungspaket; **keine tatsächliche Exfiltration behauptet**. Maßnahme: veröffentlichungsfähigen Snapshot, Inhalts-/Metadatenfreigabe und Bestätigung für exakte Empfänger samt Paket-Hash verlangen; nicht bloß alle Marker sperren, weil der Bogen selbst legitime Markerbeispiele enthält; `evaluate.py`, Tests, Aufwand M, D1.
3. **Council bestätigt Einzelmeinung als Konsens und verliert Evidenz.** Beleg: [orchestrator/nexus_orch/core.py:48–65](/tmp/n/np/orchestrator/nexus_orch/core.py), Ein-Mitglied-Nachweis und Syntheseabbruch in [offline_probe_results.json:22–40](/home/user/workspace/nexus_gpt_6_1_probe_artifacts/offline_probe_results.json). Risiko: scheinbare unabhängige Absicherung bei Tragwerksentscheidungen; Quellen sind im Council nicht mehr separat verfügbar. Maßnahme: Mindestquorum ≥2, `degraded/insufficient_quorum`, strukturierte belegte Aussagen statt Textgleichheit, Fehler-/Zitaterhalt, Judge-Fallback und verpflichtende fachliche Freigabe; `core.py`, Tests, Aufwand M, D2.
4. **OCR-Fallback ist kein Bild-Fallback.** Beleg: Vision liest Bildbytes, Gemini/Ollama verwenden ausschließlich Text in [orchestrator/nexus_orch/providers.py:49–69](/tmp/n/np/orchestrator/nexus_orch/providers.py); der tatsächliche Gemini-Request enthält nur `parts[].text` ([offline_probe_results.json:49–61](/home/user/workspace/nexus_gpt_6_1_probe_artifacts/offline_probe_results.json)). Risiko: scheinbar erfolgreicher Text über ein nicht verarbeitetes Bild statt belegbarer Plantranskription. Maßnahme: typisierter OCR-Request mit Bildbytes/URI und multimodalem Adapter; lokale OCR-Fähigkeit separat prüfen, andernfalls klarer Capability-Fehler; `providers.py`, `core.py`, Tests, Aufwand M, D3.
5. **Automatische Auswertung vermischt Prüfstände und akzeptiert unvollständige Berichte.** Beleg: nur Notenbereich wird geprüft; Datum, Commit, Modell-Duplikate und 21 Statusfelder werden nicht validiert ([evaluation/nexus_eval_auswertung.py:18–36](/tmp/n/np/evaluation/nexus_eval_auswertung.py)). Zwei Berichte desselben Modells von unterschiedlichen Tagen, jeweils mit nur einem Prüfpunkt, werden fehlerfrei gemeinsam angenommen; alter Stand Note 1 plus aktueller Stand Note 5 ergibt 3,0 ([offline_probe_results.json:72–79](/home/user/workspace/nexus_gpt_6_1_probe_artifacts/offline_probe_results.json)). Risiko: aktuelle kritische Mängel werden durch historische Bewertungen verdeckt. Maßnahme: vollständiges JSON-Schema, Run-/Commit-/Prompt-Kohorte und eine Stimme je Modell erzwingen; frühere Berichte getrennt historisieren; `evaluate.py`, `nexus_eval_auswertung.py`, Tests, Aufwand M, D4.

## D Top-5-Maßnahmen
| Rang | Maßnahme | Datei(en) | Kriterium | Wirkung (hoch/mittel/gering) | Aufwand (S/M/L) |
|---|---|---|---|---|---|
| 1 | **D1 – Datenschutzgrenze schließen:** gesamte Eingabe normalisieren/klassifizieren, explizite Privacy-Klasse und lokale Destination fail-closed; Eval nur mit freigegebenem Snapshot/Empfängern/Paket-Hash. Fehlertexte redigieren; gemeinsame Git-/Sync-Ausschlüsse einschließlich Env-Varianten. Negativtests für Schreibvarianten, Systemkontext und Eval ergänzen. Belege: B K2.1/K2.2/K2.5 und C1/C2. | `orchestrator/nexus_orch/{core,cli,evaluate,providers}.py`; `.gitignore`; beide Sync-Skripte; `orchestrator/tests/test_orch.py` | K2 | hoch | M |
| 2 | **D2 – Council ehrlich degradieren:** Quorum, strukturierte Konsens-/Dissensprüfung, Quellen/Modell-/Fehlererhalt, abgesicherte Synthese und Ingenieurfreigabe; Ein-Mitglied-, Ausfall- und Gegenbelegtests. Belege: B K1.3 und C3. | `orchestrator/nexus_orch/core.py`; `orchestrator/config/routing.json`; `orchestrator/tests/test_orch.py`; `orchestrator/README.md` | K1 | hoch | M |
| 3 | **D3 – Adapterverträge härten:** typisierte Requests/Responses, Capability- und Konfigurationsvalidierung; Schema-/Dateifehler in definierte Fehlerklassen übersetzen, leere Resultate nicht als Erfolg behandeln; begrenzte transiente Retries/Backoff. OCR multimodal umsetzen oder sauber sperren; Request-/Fehlerfixtures für alle Adapter. Belege: B K1.2/K1.5/K3.2–K3.4/K4.4 und C4. | `orchestrator/nexus_orch/{providers,core}.py`; `orchestrator/config/routing.json`; `orchestrator/tests/test_orch.py` | K1/K3 | hoch | M |
| 4 | **D4 – Beleg-/Freigabekette absichern:** immutable Run-ID, Commit/Dirty-/Prompt-/Konfigurationshash und vollständiges Berichts-Schema; Aggregation je Kohorte/Modell. Audit je Versuch mit Akteur, Modell und Fehlerklasse ohne Klartext; Lessons-Metadaten erzwingen, Review-Übergang/Statusfilter implementieren. Eval-Konfigurationsmutation beseitigen; Sync-Dateimanifest und Altbestandkennzeichnung ergänzen. Belege: B K2.3/K2.4/K3.4/K3.5/K4.2 und C5. | `orchestrator/nexus_orch/{core,evaluate}.py`; `evaluation/nexus_eval_auswertung.py`; beide Sync-Skripte; `orchestrator/tests/test_orch.py` | K2/K3/K4 | hoch | M |
| 5 | **D5 – Betrieb abnahmefähig machen:** Setup an `$PSScriptRoot` binden, alle nativen Exitcodes/Branch und Sync-Stamp prüfen; Paketressourcen explizit ausliefern, Editable-/Wheel-/Windows-Smokechecks. Readiness separat, Token-/Latenz-/Budgetmessung und Deadline; Transfers/Restrisiken dokumentieren. AEC-Goldsatz mit Normausgabe, Plan-Ground-Truth, Fehlerquote und menschlicher Freigabe; Registry-Inventar von ausführbaren Integrationen abgrenzen. Belege: B K2.5/K3.5/K4.1–K4.5. | `orchestrator/{setup,sync_nexus,sync_nexus_rclone}.ps1`; `orchestrator/pyproject.toml`; `orchestrator/nexus_orch/{core,providers,cli}.py`; `orchestrator/README.md`; `orchestrator/tests/` | K4 | hoch | L |

## E Stärken (max. 3)
1. Kleine, nachvollziehbare Architektur mit konfigurierten Providerketten und injizierbaren Testprovidern ([orchestrator/nexus_orch/core.py:7–26](/tmp/n/np/orchestrator/nexus_orch/core.py)).
2. Reale Offline-Tests für reguläre Kernpfade: 17 bestanden; Testfälle enthalten auch Privacy ohne Cloud-Fallback und HTTP-Fehlerhilfe ([Prüflog:3–5](/home/user/workspace/nexus_gpt_6_1_test_run.txt), [orchestrator/tests/test_orch.py:19–24,67–85](/tmp/n/np/orchestrator/tests/test_orch.py)).
3. Datensparsamer Audit-Grundansatz und nichtlöschende Zielkopien; keine automatische Prompt-Klartextablage im Audit ([orchestrator/nexus_orch/core.py:71–76](/tmp/n/np/orchestrator/nexus_orch/core.py), [orchestrator/sync_nexus.ps1:25](/tmp/n/np/orchestrator/sync_nexus.ps1), [orchestrator/sync_nexus_rclone.ps1:43](/tmp/n/np/orchestrator/sync_nexus_rclone.ps1)).

## F Annahmen und nicht Prüfbares
- Prüfumfang: vollständiger Evaluierungsbogen einschließlich Abschnitt 6 gelesen; tatsächlicher Repo-Stand `6e8f57417e3d086c3118ee3b2a62a07637b5957c` geprüft, nicht ein behaupteter produktiver Main-Stand ([eval_prompt.md:1–128](/home/user/workspace/eval_prompt.md), [Prüflog:1–2](/home/user/workspace/nexus_gpt_6_1_test_run.txt)).
- Vorgeschriebener Testbefehl ausgeführt: `cd /tmp/n/np/orchestrator && python -m pytest -q tests`; 17 Tests bestanden in 0,29 s unter Python 3.14.3. Testcaches danach entfernt; Repo-Status blieb leer ([Prüflog:3–8](/home/user/workspace/nexus_gpt_6_1_test_run.txt)).
- Zusatznachweise verwenden ausschließlich synthetische Daten, Mockprovider und ersetzte HTTP-Aufrufe; sie belegen Kontrollfluss/Payloads, **keine echten Cloud-Transfers** ([nexus_gpt_6_1_offline_probes.py:21–154](/home/user/workspace/nexus_gpt_6_1_offline_probes.py), [offline_probe_results.json:1–81](/home/user/workspace/nexus_gpt_6_1_probe_artifacts/offline_probe_results.json)).
- **nicht_pruefbar:** aktuelle API-Modellverfügbarkeit/-Parameterakzeptanz, reale Zitate, OCR-Qualität, Windows-/PowerShell-Ausführung, geplante Aufgaben, Drive-/Projektzustand, Vertrags-/Regions-/Retention-Einstellungen sowie tatsächliche Kosten, Latenzen und fachlicher AEC-Nutzen; keine Live-Aufrufe oder externe Zustandsprüfung durchgeführt ([Prüflog:9–11](/home/user/workspace/nexus_gpt_6_1_test_run.txt)). Die entsprechenden Punkte sind bei belegbarer Teilfunktion als „teilweise“ und nicht insgesamt als „nicht prüfbar“ bewertet.
- **Annahme/Prüfschätzung:** S = kleine isolierte Änderung, M = mehrere zusammenhängende Änderungen mit Negativtests, L = Betriebs-/fachliche Abnahme über mehrere Komponenten; keine gemessenen Projektaufwände.
- Die dokumentierte Privacy-Ausnahme für Evaluierung ist bewusst vorgesehen, aber keine nachgewiesene Inhaltsfreigabe; das Urteil behauptet weder vorhandene Geheimnisse im Repo noch tatsächlichen DSGVO-Verstoß ([orchestrator/README.md:73](/tmp/n/np/orchestrator/README.md), [orchestrator/nexus_orch/evaluate.py:3–4,36–60](/tmp/n/np/orchestrator/nexus_orch/evaluate.py)). Keys wurden nicht gesucht.

## G JSON (maschinenlesbar, keine Kommentare)
```json
{
  "modell": "GPT-6.1 Sol",
  "datum": "2026-10-13",
  "repo_zugriff": true,
  "noten": {"K1": 4, "K2": 5, "K3": 3, "K4": 4},
  "gesamt": 4.0,
  "ko_regel": true,
  "pruefpunkte": {
    "K1.1": "erfuellt",
    "K1.2": "teilweise",
    "K1.3": "nicht_erfuellt",
    "K1.4": "erfuellt",
    "K1.5": "teilweise",
    "K1.6": "erfuellt",
    "K2.1": "nicht_erfuellt",
    "K2.2": "teilweise",
    "K2.3": "teilweise",
    "K2.4": "teilweise",
    "K2.5": "nicht_erfuellt",
    "K3.1": "erfuellt",
    "K3.2": "teilweise",
    "K3.3": "teilweise",
    "K3.4": "teilweise",
    "K3.5": "teilweise",
    "K4.1": "teilweise",
    "K4.2": "teilweise",
    "K4.3": "teilweise",
    "K4.4": "teilweise",
    "K4.5": "teilweise"
  },
  "kritisch": [
    {
      "befund": "Privacy-Gate übersieht Schreibvarianten und vertraulichen Systemkontext; Cloud-Routing offline reproduziert.",
      "datei": "orchestrator/nexus_orch/core.py:16-19,28-33,41-48",
      "massnahme": "Vollständigen Request normalisieren und klassifizieren; explizite Privacy-Klasse, lokale Fail-closed-Prüfung und Negativtests. Aufwand M; D1."
    },
    {
      "befund": "Evaluierung umgeht Router und Privacy-Gate ohne technische Inhaltsfreigabe; synthetischer vertraulicher Kommentar erreicht Cloud-Mock.",
      "datei": "orchestrator/nexus_orch/evaluate.py:3-4,36-47,60",
      "massnahme": "Nur freigegebenen Snapshot versenden; Inhalts-/Metadatenprüfung und Bestätigung von Empfängern samt Paket-Hash. Aufwand M; D1."
    },
    {
      "befund": "Ein Council-Mitglied erzeugt consensus=true; Quellen/Fehlergründe werden verworfen und Syntheseausfall ist ungesichert.",
      "datei": "orchestrator/nexus_orch/core.py:48-65",
      "massnahme": "Mindestquorum, degradierter Zustand, strukturierte Evidenzprüfung, Quellen-/Fehlererhalt, Judge-Fallback und Ingenieurfreigabe. Aufwand M; D2."
    },
    {
      "befund": "OCR-Fallback sendet Gemini nur Textpfad/URL statt eines multimodalen Bild-Requests.",
      "datei": "orchestrator/nexus_orch/providers.py:49-69",
      "massnahme": "Typisierten multimodalen OCR-Adapter einführen; ohne geprüfte Bildfähigkeit mit Capability-Fehler abbrechen. Aufwand M; D3."
    },
    {
      "befund": "Auswertung akzeptiert unvollständige Berichte und vermischt unterschiedliche Prüfstände desselben Modells; synthetisch ergibt alter Stand 1 plus aktueller Stand 5 die Gesamtnote 3.0.",
      "datei": "evaluation/nexus_eval_auswertung.py:18-36",
      "massnahme": "Vollständiges Schema und Run-/Commit-/Prompt-Kohorte validieren; eine Stimme je Modell, getrennte Historie. Aufwand M; D4."
    }
  ],
  "massnahmen": [
    {
      "rang": 1,
      "massnahme": "D1: Datenschutzgrenze über alle Eingabekanäle schließen; Eval-Snapshot/Freigabe, Error-Redaction und gemeinsame Git-/Sync-Ausschlüsse.",
      "datei": "orchestrator/nexus_orch/core.py:16-19,28-33; orchestrator/nexus_orch/evaluate.py:36-60; orchestrator/nexus_orch/providers.py:12-17; orchestrator/nexus_orch/cli.py; .gitignore:152-160,222-225; orchestrator/sync_nexus.ps1:21-22; orchestrator/sync_nexus_rclone.ps1:31-34; orchestrator/tests/test_orch.py",
      "kriterium": "K2",
      "wirkung": "hoch",
      "aufwand": "M"
    },
    {
      "rang": 2,
      "massnahme": "D2: Council-Quorum, belegte Konsens-/Dissensprüfung, Fehler-/Quellenerhalt, abgesicherte Synthese und fachliche Freigabe.",
      "datei": "orchestrator/nexus_orch/core.py:44-67; orchestrator/config/routing.json:87-98; orchestrator/tests/test_orch.py:30-37; orchestrator/README.md",
      "kriterium": "K1",
      "wirkung": "hoch",
      "aufwand": "M"
    },
    {
      "rang": 3,
      "massnahme": "D3: Typisierte Adapterverträge und Capability-/Schemavalidierung, Fehlernormalisierung, transiente Retries sowie echter multimodaler OCR-Pfad.",
      "datei": "orchestrator/nexus_orch/providers.py:7-70; orchestrator/nexus_orch/core.py:28-39; orchestrator/config/routing.json; orchestrator/tests/test_orch.py",
      "kriterium": "K1/K3",
      "wirkung": "hoch",
      "aufwand": "M"
    },
    {
      "rang": 4,
      "massnahme": "D4: Immutable Evaluierungskohorte mit vollständigem Schema; Attempt-Audit, erzwungene Lessons-Metadaten/Review und Datei-Hashmanifest für SSOT.",
      "datei": "orchestrator/nexus_orch/core.py:71-98; orchestrator/nexus_orch/evaluate.py:49-85; evaluation/nexus_eval_auswertung.py:18-36; orchestrator/sync_nexus.ps1:24-28; orchestrator/sync_nexus_rclone.ps1:47-51; orchestrator/tests/test_orch.py",
      "kriterium": "K2/K3/K4",
      "wirkung": "hoch",
      "aufwand": "M"
    },
    {
      "rang": 5,
      "massnahme": "D5: Fail-fast Windows-Setup/Sync, Paketressourcen und Smokechecks, Readiness/Budget-/Latenzmessung sowie Transferdokumentation und fachlicher AEC-Goldsatz.",
      "datei": "orchestrator/setup.ps1:2-11; orchestrator/sync_nexus.ps1:15-19; orchestrator/sync_nexus_rclone.ps1:18-19,47-51; orchestrator/pyproject.toml:14-15; orchestrator/nexus_orch/core.py; orchestrator/nexus_orch/providers.py; orchestrator/nexus_orch/cli.py; orchestrator/README.md; orchestrator/tests/",
      "kriterium": "K4",
      "wirkung": "hoch",
      "aufwand": "L"
    }
  ]
}
```
