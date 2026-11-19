# NEXUS × DSH × RFEM5 COM / RFEM6 API II — Einrichtung und Resultat

Stand: 12.11.2026, Europe/Vienna. Status: isolierter Entwicklungs-Draft auf PR83, keine Produktions- oder Ingenieurfreigabe. Executor: OpenAI Codex /root; role_id ID02; Modell-ID unbekannt. Separater Reviewer: /root/rfem_diff_review, ebenfalls OpenAI Codex; kein DeepSeek-Review behauptet.

## Ergebnis und Grenzen

Der gemeinsame deterministische Geometriekern erzeugt aus expliziten SI-Eingaben Knoten, Linien, Stützen und Geschossträger. Getrennte Katalogquerschnitte für Stützen und Träger. Keine Lager, Lasten, CLT-Flächen, Exzentrizitäten, Gelenke oder normativen Nachweise werden erfunden. Das Ergebnis ist ein Geometrie-/Stabgerüst, kein freigegebenes Rechenmodell.

Prompt → bestehendes DSH → JSON-Vorschlag → Schema-/Topologieprüfung → deterministischer Python-Kern → Dry-run-JSON. Eine separate ausdrücklich ausgewählte CLI-Aktion kann danach RFEM-Objekte übertragen. Modellantworten werden niemals als Python ausgeführt. `geometry-plan` kann keine Live-Übertragung wählen. Quellenangaben in Modellantworten sind untrusted; Schema-PASS ist kein Quellen- oder Freigabenachweis.

Synthetischer Test: X-Felder 4 und 5 m; Y-Feld 3 m; Geschosse 3 und 3 m. Ergebnis: 18 Knoten, 26 Linien, 26 Stäbe; 73 reale Protobuf-Objekte inklusive Material und zwei Querschnitten. `dlubal.api==2.16.6`: deterministischer Serialisierungs-Roundtrip PASS. Testkatalog S235 / IPE 100 dient ausschließlich der Schnittstellenprüfung und ist keine W012-Bemessung.

W012-Eingaben fehlen: quellengebundene Achsen, Höhen, Orientierung, BSH-/CLT-Zuordnung und Katalognamen. Für das Projekt ist G0 weiterhin BLOCKED. Die Beispielgeometrie ist ausdrücklich SYNTHETIC und kein W012-Modell.

## Bestand und Integration

- PR83: https://github.com/julianzotter/nexus-platform/pull/83 ; geprüfter Vorgänger `50dd64a3680836c3e43fb194b8d15bb097313bfd`. Dessen DeepSeek-API-Provider und `rfem_prompt`-Route bleiben erhalten.
- Neue `rfem_plan`-Route verwendet ausschließlich den vorhandenen DSH-Prozess mit seinem Headless-Profil, ohne Cloud-Fallback. Kein zweiter Key-Store und keine Übernahme gespeicherter GUI-Schlüssel in synchronisierte Dateien.
- Das separate RFEM_Python_Client-Repository wurde geprüft. `RFEM/initModel.py` verwendet SOAP/suds und ist kein API-II-gRPC-Adapter; deshalb nicht als gRPC transportiert oder umbenannt.
- PR84: https://github.com/julianzotter/nexus-platform/pull/84 enthält eine weitere DeepSeek-/Portalrahmen-Implementierung. Diese Erweiterung übernimmt keine konkurrierenden Credential- oder Provideränderungen daraus. Vor Zusammenführung beide PRs auf einen Schnittstellen-/Modellvertrag konsolidieren; kein automatischer Merge.
- Bestehender RFEM5-Konnektionsablauf wiederverwendet: Typbibliothek, `GetActiveObject`, `LockLicense`, `GetActiveModel`, Pfadprüfung, `UnlockLicense` im finally. Schreibaufrufe nach Dlubal-COM-Dokumentation; Windows-Marshalling noch nicht live geprüft.

## Windows: lokale Umgebung vorbereiten

Im ausgecheckten Review-Branch im Repository-Root starten. Keine API-Keys in Repository, Drive, JSON-Eingaben oder Kommandozeilenargumente schreiben.

```powershell
$repo = (git rev-parse --show-toplevel).Trim()
Set-Location $repo
py -3.12 -m venv .venv-rfem
$python = Join-Path $repo '.venv-rfem\Scripts\python.exe'
$env:PYTHONPATH = Join-Path $repo 'orchestrator'
& $python -m pip install pytest
& $python -m pip install -r orchestrator/requirements-rfem5.txt
```

RFEM6-Version zuerst in der Anwendung feststellen. Der hier geprüfte Adapter ist absichtlich auf SDK 2.16.6 / RFEM 6.16 begrenzt. Historisch wurde ein Host-SDK 2.12.8 gemeldet; dessen aktueller Hoststand ist unbekannt. Bei abweichendem RFEM-Build nicht blind das SDK aktualisieren: passende SDK-Version isoliert prüfen und den Adaptervertrag unabhängig nachtesten. Für einen tatsächlich bestätigten RFEM-6.16-Host:

```powershell
& $python -m pip install -r orchestrator/requirements-rfem6.txt
& $python -m pytest -q tests/test_geometry_engine.py tests/test_deepseek_route.py tests/test_rfem_parametric.py
& $python -m nexus_orch.cli geometry --spec orchestrator/examples/synthetic-frame.json --out .local-rfem-runs --target sdk-check
```

SDK-Check verwendet keinen RFEM-Server. Ein erfolgreicher Protobuf-Test bestätigt weder Lizenz noch Verbindung oder Materialbibliothek.

## RFEM6 API II: Verbindung und neuer Modelltransfer

In RFEM den tatsächlich aktiven gRPC-Endpoint und die API-Berechtigung prüfen. Der Adapter verwendet nur Loopback, standardmäßig Port 9000. Dlubal-Zugang bleibt im lokal unterstützten Dlubal-Key-Store; kein Key wird im Code eingebettet.

```powershell
& $python -m nexus_orch.cli rfem-preflight --target rfem6 --port 9000
```

Dieser Aufruf liest Anwendungsversion und offene Modell-IDs. Erst bei passendem Build, bestätigtem Zugang und autorisiertem synthetischem Neumodelltest:

```powershell
& $python -m nexus_orch.cli geometry --spec orchestrator/examples/synthetic-frame.json --out .local-rfem-runs --target rfem6-new --port 9000
```

Der Adapter prüft den neuen UUID-Modellnamen gegen die offene Modellliste, legt ausschließlich ein neues Modell an und verwendet dessen explizite ModelId für jeden Objekt-Write/Readback. `skip_invalid_attributes=False`. Knotenkoordinaten, Linienverweise und Stabzuordnung werden rückgelesen. Ein Katalogname aus der Eingabe ersetzt keine unabhängige Prüfung der in RFEM aufgelösten Material-/Querschnittswerte. Modelle bleiben ungespeichert; kein Save-, Calculate-, Delete- oder Close-Aufruf. Bei Teilfehler den protokollierten Modellnamen/ModelId prüfen und nicht blind wiederholen.

## RFEM5 COM: Identität und leeres Arbeitsmodell

RFEM5 muss auf demselben Windows-PC laufen. COM-Bitness, registrierte Typbibliothek und RF-COM-Lizenz prüfen. Für den Transfer ausschließlich ein separat angelegtes, gespeichertes, vollständig leeres Testmodell öffnen — niemals das Quellmodell. In diesem Pilot werden auch vorhandene Materialien und Querschnitte als nicht leer gewertet; ein neues RFEM-Modell kann Bibliotheksinhalte erben und deshalb korrekt abgewiesen werden.

```powershell
$typeLibrary = Join-Path $env:CommonProgramFiles 'Dlubal\RFEM5_64.dll'
$workingModel = Read-Host 'Vollständiger Pfad des separat geöffneten leeren RF5-Testmodells'
& $python -m nexus_orch.cli rfem-preflight --target rfem5 --type-library $typeLibrary --expected-model $workingModel
```

Nur für den separat autorisierten Transfer in dieses identifizierte leere Modell:

```powershell
& $python -m nexus_orch.cli geometry --spec orchestrator/examples/synthetic-frame.json --out .local-rfem-runs --target rfem5-empty --type-library $typeLibrary --expected-model $workingModel
```

Lizenz-Lock, exakter Pfad und Leerheitsprüfung precedieren jede Mutation. Typbibliotheksfelder werden vor der ersten Mutation aufgelöst. Anschließend Material → Querschnitte → Knoten → Linien → Stäbe innerhalb PrepareModification/FinishModification. Rücklesen von Koordinaten und Referenzen; finally-Unlock. Keine Speicherung oder Berechnung. Die Python-COM-Arrayübergabe und tatsächlichen Typbibliotheks-/Katalogfelder sind hostseitig NOT_RUN; der erste reale Test ist eine Integrationsprüfung, keine zugesicherte Lauffähigkeit.

## DSH/Harness: bestehenden Provider nutzen

Die geprüfte offizielle Harness-Quelle ist Commit `e8f7b93a344964de3dca1ace9e72b6e4d6de87cb`. Adapteraufruf:

```text
dsh --profile headless --permission-mode read-only --approval-policy never --json -
```

Promptübergabe über stdin, `shell=False`, fester Befehl, begrenzter Timeout; Erfolg erfordert Exit 0 und genau ein `final`-Event mit `reason.kind=completed` und nichtleerem `text`. Fehlertexte/Schlüssel werden nicht in RFEM-Receipts übernommen. `status` prüft für DSH nur ausführbaren Befehl und Arbeitsordner, keine authentifizierte Modellverfügbarkeit. Tatsächliche Modell-ID bleibt null, wenn der Adapter sie nicht belegen kann.

Wichtig: Das Headless-Standardprofil deaktiviert den verwalteten Credential-Store. Ein unter Models im GUI gespeicherter `deepseek-official`-Eintrag reicht daher nicht automatisch für diesen Headless-Aufruf. Bestehendes lokales Profil prüfen. Laut offizieller DSH-Dokumentation entweder den vom Headless-Profil unterstützten Environment-Zugang verwenden oder den bestehenden lokalen Headless-Overlay um die unten stehenden Aktivierungen ergänzen. Vorhandene Overlayeinträge erhalten; nicht vollständig überschreiben. Schlüsseldateien nicht exportieren oder in dieses Repository kopieren.

```yaml
- id: credentials
  disabled: false
- id: authorization
  disabled: false
- id: deepseek-account
  disabled: false
```

Overlayort laut DSH: `$DSH_HOME/profiles/headless/cordis.patch.yml`. Bei deinem installierten DSH-Build mit dessen eigener Dokumentation abgleichen. Der Adapter wählt keine Modell-ID über undokumentierte Flags; die bestehende Session-/Deploymentauswahl gilt. Read-only/never begrenzt die DSH-Datei-/Approvalpolicy, ist jedoch keine allgemeine Netzwerksperre für fremde MCP-Tools. Profil und externe Toolrechte separat begrenzen. Keine echten Projektdaten zum ersten Verbindungstest senden.

Vorbereitung eines synthetischen Prompttests:

```powershell
$env:NEXUS_DSH_WORKDIR = $repo
$fixture = Get-Content orchestrator/examples/synthetic-frame.json -Raw
@('Gib exakt dieses synthetische JSON-Objekt zurück, ohne Markdown oder Änderungen:', $fixture) | Set-Content -Encoding utf8 .local-rfem-prompt.txt
& $python -m nexus_orch.cli geometry-plan --prompt-file .local-rfem-prompt.txt --out .local-rfem-runs
```

Ein valides Ergebnis erzeugt ausschließlich Dry-run-Dateien. Code, Markdown-Fences, zusätzliche Schemafelder, doppelte JSON-Schlüssel, nichtfinite/negative Maße und fehlende PROJECT-Quellen werden abgewiesen. Bestehendes Privacy-Routing bleibt aktiv; es ist markerbasiert und ersetzt keine explizite Datenklassifikation.

## JSON-Protokoll und Wiederanlauf

Jeder Lauf erhält einen neuen UTC-/UUID-Unterordner. `input.json` enthält kanonisierte Originaleingaben; `geometry.json` die deterministische Geometrie. `input_file_sha256` bindet tatsächlich gespeicherte Inputbytes; `normalized_spec_sha256` bindet die normierte Spezifikation (z. B. 4 und 4.0 sind semantisch gleich). `hashes.json` bestätigt Rohbytehashes von Input, Geometrie, Receipt und Fortschrittsjournal; der Hashmanifest hasht sich nicht selbst.

`progress.jsonl` wird mit flush/fsync vor Modellerstellung (eindeutiger Intentname), nach Empfang der ModelId und vor weiteren Writes fortgeschrieben. `receipt.json` erhält Teilzustand/Fehlertyp; kein Erfolg durch Exception-Unterdrückung: CLI liefert Exit 2 bei FAILED_OR_BLOCKED. Ein Abbruch genau zwischen externem Create und lokalem ACK kann nicht atomar verhindert werden; vor Retry nach dem protokollierten eindeutigen Namen suchen. Erfolgreicher RFEM-Readback bleibt vom SDK-Test getrennt.

Promptläufe ergänzen `proposal-origin.json` mit Prompt-SHA256, Provider, gegebenenfalls Session-ID und Modell-ID sowie `proposal-hashes.json`. Kein Rohprompt und kein API-Key im Ergebnisprotokoll. DSH selbst kann seine eigene Sessionhistorie lokal führen.

## Resultatbericht: Tests, Review, offene Nachweise

Aktuell lokal: 70 Tests und 2 Subtests PASS (`PYTHONPATH=orchestrator python -m pytest -q tests orchestrator/tests/test_orch.py`). Die Ausführung betrifft einen authentifiziert geladenen PR83-Quellsubset, nicht den vollständigen Repository-Checkout. Initial fehlten Evaluierungsdateien im Subset; nach Laden der unveränderten Vorgängerdateien bestand die Suite. Ein echter Test-Discovery-Fehler in PR83 (`tests/test_deepseek_route.py` importierte sich selbst) wurde durch einen eindeutig benannten Import behoben.

Separater Diff-Reviewer prüfte den finalen Stand mit 70 Tests + 2 Subtests sowie git diff --check: Bounded PASS. Zusätzlich geprüft: lesender Preflight, reale SDK-/Mock-Hostprüfung der ModelId-Bindung, Modellnamenskollisionsprüfung und Preflight-Fehlerprüfung; finaler Delta-Review ebenfalls Bounded PASS für den isolierten Draft. Korrigierte Reviewbefunde: DSH-Readiness, große Ganzzahlen, dauerhafter Teilmodell-Checkpoint, eindeutige Hashbereiche.

Kompatibilitätsänderung: Der Legacy-PR83-Preview delegiert an den gemeinsamen Kern. Seine Z-Koordinaten sind jetzt explizit negativ für positive Gebäudehöhen bei RFEM_GLOBAL_Z_DOWN; außerdem ändern sich Stabreihenfolge/IDs. Alte Preview-Dateien neu erzeugen und nicht nach alten Stabnummern verbinden. Legacy-Eingaben ohne Quellen bleiben `LEGACY_UNVERIFIED_PREVIEW`; der alte Live-Einstieg bleibt gesperrt.

NOT_RUN/BLOCKED: echte DSH-/DeepSeek-Authentifizierung, Windows-COM-Marshalling, realer RFEM6-Host, Katalogauflösung und Readback, W012-Modellgenerierung, Solver, RFEM-Dateispeicherung, numerischer Ergebnisvergleich, technischer Human Release. Keine fachliche Tragwerksberechnung ausgeführt. Drive-WORK-Ablage, Ledger und bestehende file-registry sind durch diesen Code-Draft nicht aktualisiert: REGISTRATION_PENDING.

## Primärquellen / überprüfter Stand

- NEXUS PR83: https://github.com/julianzotter/nexus-platform/pull/83
- Überlappender PR84: https://github.com/julianzotter/nexus-platform/pull/84
- DSH Headless-Quellvertrag: https://github.com/deepseek-ai/deepseek-harness/blob/e8f7b93a344964de3dca1ace9e72b6e4d6de87cb/packages/bundle/headless/README.md
- DSH Terminalereignis: https://github.com/deepseek-ai/deepseek-harness/blob/e8f7b93a344964de3dca1ace9e72b6e4d6de87cb/packages/bundle/headless/src/json-stream.ts
- RFEM6 Application: https://apidocs.dlubal.com/source/rst_methods/rfem_methods.html
- RFEM6 Create: https://apidocs.dlubal.com/source/rst_methods/rfem/create_model.html
- RFEM6 Objektliste: https://apidocs.dlubal.com/source/rst_methods/rfem/create_object_list.html
- RFEM5 COM-Objekte: https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001379
- DeepSeek Chat: https://api-docs.deepseek.com/api/create-chat-completion/
- DeepSeek Responses: https://api-docs.deepseek.com/api/create-response/ ; kein separater Responses-Transport in diesem DSH-Adapter implementiert.
- Governance: WORK Folder.md 11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH, AGB v006 10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg, aktuelles Manifest und Baseline am 12.11.2026 gelesen. Fehlender Ledgerabschluss ist keine technische Freigabe.
