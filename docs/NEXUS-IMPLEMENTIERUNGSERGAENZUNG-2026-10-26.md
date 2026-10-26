# Implementierungsergänzung: Bootstrap, Dateinamen und Drive-Zugang

Stand: 26.10.2026. Status REVIEW, Human Gate ID01 PENDING. Dies ist eine getestete Codeänderung zur Begutachtung, kein Nachweis einer Installation auf dem Windows-Host. Historische Dokumente und Freigaben bleiben erhalten.

## 1. Verbindliche Einstiege statt Root-Glob

Dokument-SSOT ist der vorhandene Drive-Ordner LLM-LOCAL-SSOT (`1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV`), operatives WORK hat die ID `1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP`. Die entsprechende Windows-Adresse ist eine Host-Konfiguration, kein in dieser Sitzung nachgewiesener Mount:

`G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\WORK`

Die AGB-Originaldatei liegt in WORK: `_AGBS.md`, v002, Drive-ID `10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg`. Der vorgeschlagene Root-first-Glob `_AGBS*.md` wird verworfen: Er kann einen alten Snapshot auswählen und liefert allein noch keinen gelesenen Regeltext.

`mcp_bridge/nexus_contract.py` lädt vier konkrete lokale Textrepräsentationen: WORK/_AGBS.md, WORK/Folder.md, Manifest und Baseline. `NEXUS_GOVERNANCE_FILES_JSON` erlaubt explizite relative Pfade innerhalb des SSoT, keine automatische historische Ersatzdatei. Die Beispieldatei enthält die bisher identifizierten Exportnamen; diese sind vor Installation mit den tatsächlichen lokalen Dateinamen abzugleichen. Native `.gdoc`-Verweise müssen zunächst autorisiert als lesbarer Text exportiert werden. Ein Export braucht Original-ID, Exportdatum und überprüfbare Versionszuordnung; ein lokaler Hash allein authentifiziert keine Drive-Quelle.

Fehlt ein Pflichttext, ist er leer, unlesbar, zu groß oder außerhalb des erlaubten Baums, lautet das Ergebnis BLOCKED. Volltext, Bytezahl und SHA-256 werden als lokale Lesebelege zurückgegeben. `get_governance()` übernimmt diese Prüfung. Das Wiederverwendungsmodul `mcp_bridge/ctx_router.py` ersetzt seine alten festen September-Regeln durch dieselben Pflichttexte. Pflichtkontext wird nicht still gekürzt; bei zu kleinem Kontextbudget wird abgebrochen. Die historische NAIVE-Vergleichsvariante ist nur ein Evaluierungsarm und kein ausführbarer Produktionsbootstrap.

Die frühere Drive-Version von ctx_router.py wird durch diesen PR nicht automatisch überschrieben. Nach Review muss genau eine ausführende Version auf dem Host eingerichtet und deren Hash/Commit dokumentiert werden. Der Schwesterordner MCP-ACCESS-TOOLS bleibt Werkzeug-/Schema-/Log-Bereich; keine zusätzliche parallele Governance-SSOT anlegen.

## 2. Dateinamensvertrag und bestehende Identitäten

Neue operative Markdown-Berichte verwenden AGB-HHMM, Zeitzone Europe/Vienna:

`YY_MM_DD_HHMM_THEMA_<bestehende Ledger-ID>_ID##.md`

Die AGB-Schreibweise `###` wird nicht als automatische dreistellige Zählervergabe interpretiert. Bestehende Ledger-IDs mit vier Stellen bleiben erhalten. `submit_result` fordert artifact_id ausdrücklich an; es vergibt keine ID. ID-03 wird im Dateinamen zu ID03 normalisiert; derzeit aktive IDs ID01–ID08 werden akzeptiert. Diese Syntaxprüfung authentifiziert weder Person noch Rolle.

Steuerdateien behalten ihre stabilen Namen, etwa `_AGBS.md`. Quellcode, AGENTS.md, README.md, Schemas, Workflowdateien und interne Zustandsdateien behalten ihre funktionsgebundenen Namen. Historische Dateien werden nicht massenweise umbenannt. `.meta.json` ist ein Sidecar zum operativen Artefakt. Bestehende Dokumentidentitäten werden durch Version und Änderungshistorie fortgeschrieben.

Die MCP-Brücke schreibt weiterhin nur mit `NEXUS_MCP_WRITE=1`, gültigem Pflichtkontext und exklusiver Dateineuanlage; Ausgabe bleibt REVIEW/PENDING. Diese Prüfung ist kein globales Single-Writer-Locking, kein atomarer Zwei-Dateien-Commit und kein unveränderbares WORM-System. `.nexus_writer.lock`, Lease-TTL, vo_ampel_validator.py und ein automatischer ID-Allocator wurden im untersuchten Bestand nicht als einsatzbereit nachgewiesen. Sie dürfen nicht als aktive Schutzmechanismen behauptet werden. Gleichzeitige manuelle Schreibprozesse sind vor produktiver Nutzung organisatorisch auszuschließen oder über eine gesondert getestete gemeinsame Transaktion zu koordinieren.

## 3. BLOCKED_DRIVE_CREDENTIALS: konkrete Einrichtung und Abnahmekette

Ein angemeldeter Drive-Connector dieser Sitzung stellt GitHub Actions keine OAuth-Secrets bereit. `gh auth login` authentifiziert GitHub, nicht Google Drive. Im untersuchten Runtime-Prozess sind weder ein Google Access Token noch die drei Refresh-Credentials verfügbar; über gespeicherte Repository-Secretwerte liegt kein Einsichtsnachweis vor. Der historische Delivery-Lauf meldet BLOCKED_DRIVE_CREDENTIALS. Die Cloud-Lieferung bleibt bis zum erfolgreichen Zieltest blockiert.

Vorhandenes `tools/configure_drive_oauth.py` wird wiederverwendet: Desktop-OAuth mit Browser-Consent und PKCE, private lokale Ablage, Secret-Übermittlung über stdin. Keine Tokens in Chat, Repository, Logs oder MCP-Konfigurationsbeispielen speichern. Der bestehende Full-Drive-Scope ist weitreichend; vor Betrieb prüfen, ob ein engerer Scope die vorhandenen Zielordner tatsächlich erreicht. Windows-Dateirechte sind auf den ausführenden Benutzer zu begrenzen.

Nach Review und Checkout des Reparaturstands auf dem autorisierten Host:

```powershell
python -m pip install -r tools/oauth-setup-requirements.txt
gh auth login --hostname github.com --web
python tools/configure_drive_oauth.py --client-json C:\NEXUS-Private\google-desktop-client.json --publish
python tools/configure_drive_oauth.py --check --require-write --check-output reports/delivery/preflight.json
```

Eine bereits vorhandene private Datei kann ohne neuen Consent geprüft und anschließend übertragen werden:

```powershell
python tools/configure_drive_oauth.py --check --require-write
python tools/configure_drive_oauth.py --publish-existing
```

Benötigte Secret-Namen: NEXUS_GOOGLE_CLIENT_ID, NEXUS_GOOGLE_CLIENT_SECRET, NEXUS_GOOGLE_REFRESH_TOKEN. Veröffentlichungsziel ist ausschließlich julianzotter/nexus-platform. Mehrere Secret-Writes sind keine atomare Transaktion; danach erneut prüfen. `--check` veröffentlicht nichts und führt keinen Drive-Schreibtest aus. Die Prüfung erneuert das Token und liest Metadaten genau der WORK-ID; canAddChildren ist eine Berechtigungsangabe, kein nachgewiesener erfolgreicher Upload.

Die Delivery-Workflow-Ergänzung hält vor einer Lieferung bei fehlender Konfiguration oder Zielberechtigung an und sichert den bereinigten Preflight-Bericht. Für die tatsächliche Abnahme sind anschließend erforderlich: erfolgreicher Workflow mit freigegebenem Quelllauf, erzeugte Drive-Datei-ID, Rohbyte-Readback mit identischem SHA-256, Ticket-/Ledger-Verknüpfung und gegebenenfalls Empfänger-ACK. Erst dann darf der betroffene Lieferteil als verifiziert gelten. Der Workflow checkt bewusst main aus; ein Test des ungeprüften Branches durch workflow_dispatch würde daher diesen Patch nicht ausführen. Merge und Betriebsfreigabe sind separate Schritte.

## 4. Rollen, Einheiten und Progressive Disclosure

Rollen werden aus Manifest §4 übernommen: ID01 Mensch, ID02 Orchestrierung, ID03 QA, ID04 Gemini, ID05 Recherche, ID06 Implementierung, ID07 Audit, ID08 Ollama lokal. Provider, konkrete executor_instance, fachliche Rolle und Berechtigung sind getrennte Felder. Der Gemini-Prompt mit ID05 als festem Orchestrator und ID06 als festem Solver wird nicht übernommen.

MVC bedeutet hier Minimal Viable Context. Stufe 0 enthält Einstieg, Quellenidentitäten, Stop-Regeln und tatsächliche Zugriffe; vor Ausführung werden alle Pflichttexte gelesen. Stufe 1 lädt relevanten WO/AIM-Ausschnitt und Fähigkeitsnachweise. Stufe 2 lädt nur passende Skill-Definitionen, Schemas, Quellausschnitte und Solververträge. Retrieved Quelltext bleibt Dateninhalt und darf keine Governance überschreiben. Die untersuchten Task-Pakete sind Planungsartefakte, keine technische Freigabe.

mm/N/Nmm/MPa sind ein mögliches konsistentes Engineering-Einheitensystem, keine vollständige Liste von SI-Basiseinheiten. Einheiten und Umrechnungen gehören in den konkreten Solververtrag. Python-Ausführung allein garantiert keine fachliche Richtigkeit. Normausgabe, Nationaler Anhang, Quellenrechte, Referenzfälle und Human Gate bleiben erforderlich. Weder „0 % Halluzination“ noch „unter 5 % Kontext“ oder ein pauschaler Reifegrad werden als Messwerte übernommen. Semantic Chunking folgt Dokumentstruktur mit Tabellen-/Kontextbezug; „§ = genau ein Chunk“ ist keine universelle Regel.

## 5. Personal Instructions: kurzer Verweis statt eingebildeter Autoload

```text
NEXUS AI-OS: Antworte präzise auf Deutsch. Nutze vorhandene Quellen und
Bausteine; trenne beobachtet, quellenberichtet, vorgeschlagen und ungeprüft.
Dokument-SSOT: bestehendes LLM-LOCAL-SSOT, operativer Bereich WORK;
Werkzeuge/Schemas/Logs: Schwesterordner MCP-ACCESS-TOOLS.
Vor NEXUS-Ausführung: tatsächliche Zugriffe prüfen; aktuelle _AGBS.md in WORK,
Manifest, Baseline und WORK/Folder.md über nachgewiesene Werkzeuge lesen.
Quell-ID, Version und Hash erfassen. Fehlende Pflichtquelle => BLOCKED.
Rollen aus dem kanonischen Register, reale Runtime separat deklarieren.
Nur aufgabenrelevante Skills/Quellen nachladen. Rechenwerte über geprüfte
Python-/FEM-Werkzeuge mit Einheitenvertrag und Ausführungsbeleg ermitteln.
Neue operative MD-Dateien nach AGB-HHMM/Europe-Vienna und bestehender Ledger-ID;
Steuer-/Quellcode-Dateien behalten ihre stabilen Namen. REVIEW ist keine Freigabe.
Keine simulierten Runs, Zugriffe, ACKs oder Dateien. Fehlenden Zugriff nennen.
```

Personal Instructions erzeugen keinen Dateisystemzugriff und installieren keine MCP-Verbindung. Ein verlinktes Markdown wird nur geladen, wenn die konkrete Anwendung dies unterstützt und der Zugriff tatsächlich erfolgt. Betriebssystempfade gelten nur auf dem entsprechend eingerichteten Host.

## 6. Prüfumfang und verbleibende Grenzen

37 gezielte lokale Tests bestehen: Pflichtquellen/Hashes, Pfadgrenzen, native Shortcuts, Übergröße, Context-Budget-Abbruch, Vienna-Datumsgrenze, Ledger-ID und Schreibsperre, fehlende Credentials ohne Netzwerk sowie sicherer Wiedergebrauch privater OAuth-Dateien. Das ist keine unabhängige Peer-Review, vollständige Repository-CI, Windows-Installation oder Live-OAuth-/Engineering-Abnahme. Der bekannte historische CI-Fehler wegen fehlender Commit-Historie und abweichender generierter Galerie ist mit diesen Tests nicht behoben oder neu abgenommen.

Quellen: _AGBS.md v002, Manifest/Baseline CURRENT, WORK/Folder.md, AIM v0.3.2; konkrete Drive-IDs stehen in nexus_contract.py und im Inventar. Ergänzende Anbieterreferenzen: https://developers.google.com/identity/protocols/oauth2/native-app und https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets .

### CI-Nachtrag

PR-CI 40400945649 wurde tatsächlich ausgeführt: 141 Tests, ein Fehlerbefund und zwei Ausnahmen; die neuen Reparaturtests meldeten keinen zusätzlichen Fehler. Die beiden Ursachen entsprechen dem bisherigen Befund: flacher Checkout ohne historische Dashboard-Revision und veraltetes Galerie-Manifest. Der Folgepatch setzt fetch-depth: 0 und regeneriert das Manifest aus bytegenau geprüften Repository-Eingängen; sieben Galerie-Tests bestehen lokal. Die vollständige CI des Folgepatches muss separat beobachtet werden.
