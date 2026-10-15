# NEXUS Development Contract v0.1 — REVIEW CANDIDATE

Stand: 2026-10-15. Autor/Executor: OpenAI Codex in dieser Sitzung. Kein Claude-/Gemini-Review ausgeführt. Dieser Contract operationalisiert den jüngsten Entwicklungsauftrag; er ist keine Behauptung bereits geänderter kanonischer Governance-Dateien.

## 1. Ubiquitous Language — zuerst Begriffe

| Begriff | Gemeinsame Bedeutung |
|---|---|
| ID01 | Mensch und verantwortliche Freigabeinstanz; kein ChatGPT-Konto |
| Konto/Runtime | Tatsächliche Zugriffs-/Ausführungsinstanz, getrennt von Agentenrolle |
| System Contract | Ziel, Hierarchie, Schichten, Algorithmus, Schnittstellen, Abnahme und Entwicklungsspielraum |
| Agent Contract | Rolle, Auftrag, verfügbare Fähigkeiten, Eingaben, Ausgaben, Grenzen, Nachweise |
| Skill | Wiederverwendbare Anweisung mit optionalen Skripten; in Entwicklung nicht der einzig zulässige Ausführungsweg |
| Shared Understanding | Versionierter gemeinsamer Stand von Ziel, Begriffen, Annahmen und Entscheidungen |
| DELTA | Explizite Änderung zwischen Run N und N-1 beziehungsweise N-2; kein universeller Prozentwert |
| Refinement | Gezielte Änderung anhand beobachteter Defizite oder neuer Evidenz |
| Backpropagation | Rückführung eines Fehlers auf betroffene Anforderung, Annahme, Daten oder Schnittstelle; hier kein neuronales Gradientenverfahren |
| Acceptance pass rate | Anteil bestandener expliziter Tests; keine allgemeine Accuracy |
| Confidence | Nur mit Herkunft/Methode sinnvoll; ohne Grundlage null |
| Partial Delivery | Verwertbares Ergebnis mit offenen Punkten; keine behauptete technische Freigabe |
| Freeze | Identische Dateiversionen und Prüfsummen für beide unabhängigen Reviewer |

## 2. GRILL-ME — Design challengen, dann Shared Understanding

Vor komplexer Umsetzung: Ziel und Grenzen hinterfragen; einfache Aufgaben direkt ausführen. Fragen, die aus vorhandenen Quellen lösbar sind, selbst klären. Nur fehlende entscheidende Angaben an ID01 zurückgeben.

Entscheidungen für diesen Slice:
- User definiert Input und gewünschten Output; System wählt einen angemessenen Weg.
- Hierarchie und funktionale Schichten → Algorithmus und Schnittstellen → Skills → Agentenausführung.
- Entwicklung offen: direkte Skripte, Experimente, neue Werkzeuge und alternative Ansätze zulässig, sofern tatsächlich verfügbar und innerhalb der bestehenden Zugriffsrechte.
- Keine E-Mails versenden; keine bestehenden Nutzer-/Projektdateien löschen. Historie erhalten.
- Kleine reversible Entwicklungsänderungen im autorisierten Ziel weiterführen; keine wiederholten Freigabeschleifen für denselben Umfang.
- Annahmen kennzeichnen und testen; an unabhängigen Aufgaben weiterarbeiten. Fehlende Informationen niemals durch erfundene Rechen- oder Prüfergebnisse ersetzen.
- Peer Review verbessert den Entwicklungsstand. Offene fachliche Nachweise dürfen nicht als bestanden oder für produktive Tragwerksfreigaben ausgegeben werden.

## 3. System Contract — adaptiver Algorithmus

1. INTAKE: User-Input, Zieloutput, Datenquellen, Abnahmekriterien und tatsächliche Fähigkeiten aufnehmen.
2. DISCOVER: Vorhandene Quellen, Code, Skills, Artefakte und vorangegangene Runs suchen; Wiederverwendung prüfen.
3. ROUTE: Einfache Aufgabe direkt lösen. Bei Komplexität Brainstorming, GRILL-ME oder Fachreview gezielt hinzufügen.
4. DESIGN/BUILD: Kleinsten vollständigen funktionalen Slice umsetzen; Annahmen explizit speichern.
5. EVALUATE: Tatsächlich ausgeführte Tests, Aufwand und Wiederverwendbarkeit erfassen. Nicht ausgeführte Prüfungen bleiben NOT_RUN.
6. DELTA: Ausgangsartefakt erhalten, Änderungen speichern; N gegen N-1, N-2 und die verwendete Baseline-Version prüfen.
7. CHALLENGE: Vorwärts auf Integration und Folgen, rückwärts auf Anforderungen und Quellen, lateral auf einfachere Alternativen und Wiederverwendung schauen. Fehler auf ihre Ursache zurückführen.
8. REFINE/SHARE: Nur betroffene Teile verbessern; Ergebnis mit Evidenz und offenen Punkten zentral ablegen. Erfüllte Abnahme beendet den Loop; Plateau oder Budgetende erzeugt Partial Delivery und nächste gezielte Aktion.

Jeder Loop hat ein explizites, veränderbares Arbeitsbudget; kein unendliches Wiederholen und kein pauschales 5-%-Konvergenzversprechen. Accuracy nur gegenüber belastbarer Referenz messen; Modell-Selbsteinschätzung nicht als Messwert behandeln.

## 4. Funktionale Schichten und Übergaben

| Schicht | Verantwortung | Übergabe |
|---|---|---|
| Intent | User Request und Abnahme | request_id, inputs, desired_output, checks |
| Knowledge | Quellenidentität vor Semantik | source_id, version, locator, hash, evidence_status |
| Planning | adaptives Routing, Optionen | plan, assumptions, selected_path, budget |
| Execution | Skript/Skill/Agent/Tool | actual_executor, capability, output, errors |
| Evaluation | deterministische Tests und Fachprüfung | measured_checks, open_findings, evaluator |
| Memory | Run-N/N-1/N-2, DELTA, Baseline | run_number, hashes, patches, evaluation |
| Sharing | zentrale, wiederauffindbare Artefakte | artifact_uri, version, review_state, next_action |

GitHub führt Code und Contracts. Drive führt Wissensquellen, WorkOrders und freigegebene Artefakte. SQLite ist abgeleiteter lokaler Zustand außerhalb des Drive-Syncs. Keine eigenen Masterbestände pro Konto. Zwischen Code-Contract und geltender Governance muss ein sichtbarer Vorschlag/Adoptionsstatus bestehen.

## 5. Agent Contract — gleiche Struktur, unterschiedliche Aufgaben

Je Instanz erfassen: role, actual_executor/provider/model soweit bekannt, objective, input_refs, output_contract, available_tools, optional_skills, experiment_scope, checks, fallback, escalation, run_budget, artifact_destination.

Claude-Review: Architektur, Modulgrenzen, Schnittstellen, unnötige Komplexität, Fehlerpfade und vereinfachende Alternativen.
Gemini-Review: Algorithmus, Daten-/Evidenzverträge, N-1/N-2-Konsistenz, Tests, Gegenbeispiele und Baseline-Abgleich.

Beide erhalten denselben eingefrorenen Bundle-Hash und zunächst keine Antwort des anderen Reviewers. Erst nach den unabhängigen Antworten erfolgt Synthese. Unaufgelöste entscheidungsrelevante Konflikte an ID01; unabhängige Entwicklungsarbeit läuft weiter. Keine Modellverfügbarkeit oder unabhängige Instanz simulieren.

## 6. Minimaler Run Contract

Erforderlich: task_id, run_number, timestamp, baseline hash, output hash, delta, N-1/N-2 comparison, checks, assumptions, evidence/review status und nächster Schritt. Betriebsmetriken nur bei tatsächlicher Messung ergänzen.

Der Prototyp cycle.py speichert die erste Ausgabe als Checkpoint, danach Top-Level-JSON-Deltas; verschachtelte Werte werden atomar ersetzt. Checks sind eingegebene Beobachtungen eines Evaluators, keine automatische Richtigkeitsgarantie. Baseline-Hashing dokumentiert die verwendete Version; eine vollständige semantische Governance-Prüfung wird nicht vorgetäuscht.

## 7. Robuste Redundanz und Lernzyklus

Alternative prüfen, bevor ein zweiter Stack gebaut wird. Fallback muss seine Grenzen ausweisen und dieselben Abnahmekriterien verwenden. Tests gegen Negativfälle ergänzen. Erkenntnisse als wiederverwendbare Kandidaten speichern, ohne automatisch kanonischen Status zu vergeben.

Pace Layers: Run-Zustand und Experimente ändern sich schnell; Skills und Adapter nach Tests; Schnittstellen und Governance langsamer und nachvollziehbar. Das ist ein Entwurfsprinzip, kein hier implementierter autonomer Regeldienst.

## 8. Abnahme und Grenzen dieses Slices

- Ein einfacher Auftrag benötigt keinen Multi-Agenten-Overhead.
- Drei Runs sind rekonstruierbar; N-1/N-2-Deltas sichtbar; Baseline-Wechsel erkannt.
- Fehlerhafte Hashes, ungültige Checks und unzulässige Review-Pfade werden erkannt.
- Plateau/Budgetende liefert den letzten Stand statt Fortschritt zu verlieren.
- Beide Reviewaufträge referenzieren denselben Bundle-Hash; tatsächliche Reviews bleiben bis zum Eingang NOT_RUN.
- Keine Cloud-Aufrufe, Mailfunktionen, Löschfunktionen, Secrets, Merges oder Deployments im Prototyp.
- Kein produktiver Drive/SQLite/KG-End-to-End-Nachweis und kein Engineering-Nachweis durch den synthetischen Demo-Lauf.

## 9. Kooperationsvertrag: Knowledge-Index-Agent und ID03

Der vom Nutzer genannte Skill `aec-knowledge-index-agent` ist ein anzubindender Kandidat; seine tatsächliche Ausführung und seine genaue Quelle wurden in diesem Slice nicht verifiziert. Ein Skillname ist keine Agentenidentität. ID03 bezeichnet nach dem gelesenen kanonischen Manifest die QA-/Peer-Review-Rolle; Konto, Provider und ausführende Instanz werden separat dokumentiert.

Übergabe: Index-Agent → Quellen-/Registry-Kandidaten mit stabilen source_id, version/hash, locator, Extraktionsmethode und Unsicherheiten → ID03 prüft Identität, Nachvollziehbarkeit, Schema und Stichproben → Findings referenzieren source_id/run_number → ausführende Instanz korrigiert gezielt → DELTA und erneuter Review. Kein selbst vergebener unabhängiger Review: Autor und Reviewer müssen unterschiedliche tatsächliche Instanzen sein. Fehlender Reviewer blockiert keine übrigen Entwicklungsarbeiten; review_status bleibt NOT_RUN.

Gemeinsamer Ablageanker: dieser versionierte Contract im zentralen GitHub-Repository. WorkOrder-/Wissensverweise verwenden die bestehenden Drive-SSOT- und WORK-IDs; ein Drive-Vertragszeiger darf keine zweite unabhängig bearbeitete Masterfassung erzeugen. In diesem Slice wird kein Drive-Objekt angelegt und kein Agent automatisch geweckt. Zustellung, Ausführung und Empfangsbestätigung sind getrennte nachweispflichtige Zustände.
