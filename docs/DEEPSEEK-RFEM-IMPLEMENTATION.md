# NEXUS × DeepSeek Harness × RFEM — sofort umsetzbarer Pilot
Version 0.1.0 · ENTWURF / REVIEW_REQUIRED · 12.11.2026, Europe/Vienna
Owner: ID01 Julian Zotter. Implementierung: OpenAI Codex /root; unabhängige Review-Instanz separat. Keine Produktions- oder Tragwerksfreigabe.

## 1. Ziel und Architekturentscheidung
Erster Slice: vorhandene NEXUS-Orchestrierung um direkten offiziellen DeepSeek-Provider erweitern und einen isolierten parametrischen RFEM-6-Rahmen aus einem deterministischen Modellvertrag erzeugen. Harness dient zunächst als vorhandene Bedien-/Agentenumgebung. Ein lokaler Harness-HTTP-Gateway ist keine Voraussetzung; Port 2778 und Gateway-Token aus dem gelieferten Beispiel sind nicht als lokaler Ist-Zustand verifiziert.

NEXUS ist für Routing, Privacy-Gate, Workorder und Audit verantwortlich. Python validiert Parameter, Einheiten, Objektbeziehungen und Freigabebindung. RFEM ist der Fachsolver. Das LLM liefert einen Vorschlag, keine vertrauenswürdigen Zahlen oder automatisch autorisierten API-Aufrufe. Der bestehende `mcp_bridge/nexus_mcp_server.py` wird später um typisierte Tools erweitert; kein zweiter unkoordinierter MCP-Master. RFEM5-COM bleibt ein separater Bestands-/Lesepfad.

| Slice | Konkrete Umsetzung | Akzeptanz / Gate |
|---|---|---|
| P0 Provider | `routing.json`: deepseek-flash ohne Thinking; deepseek-v4-pro für Review mit explizitem Thinking. Neue eigene Routen ohne implizite Cloud-Fallbacks. | Konfiguration gültig; Privacy-Route unverändert lokal; `/models` live 200 und erwartete IDs. |
| P0 Credentials | ENV bevorzugt; optional lokaler DSH-Store, nur lesend, ACL-/Owner-/Dateiprüfung; keine Schlüsselwerte in Git/Browser/Logs. | Tatsächliches DSH-Schema und Windows-ACL belegen; bei anderem Schema STOP. |
| P0 Browser | Alte `vc_apikey_*`-Slots beim Laden entfernen; keine neuen persistierten Keys; generierte Vorschau ohne Same-Origin. Alter direkter DeepSeek-Browserpfad deaktiviert. | Keine Key-Persistenz; Cleanup-Fehler sichtbar; Browserlauf noch auszuführen. |
| P1 RFEM Preflight | SDK-Signaturen offline; danach `get_application_info()` lesend am lokalen Host. | Tatsächlicher RFEM-Build und passendes SDK; separater Dlubal-Key; Host erreichbar. |
| P1 Modellvertrag | 4 Knoten, 3 Stäbe, 2 vollständige Einspannungen, Last auf Riegel; Material/Querschnitt; SI, Vorzeichen, lineare Analyse, SDK-/Buildprofil und Inputhash. | Wiederholbar identische Topologie/Hash; negative Eingaben abgewiesen; Lastparameter verwendet. |
| P1 isoliertes Modell | Neues eindeutig benanntes RFEM-Modell; kein Bestandsmodell öffnen/überschreiben; Objekte schreiben und rücklesen. | Geometrie, Referenzen, Lager, Lasten, Analyse und Katalogidentitäten passend; Objektproperties zusätzlich fachlich prüfen. |
| P2 Solver/Ergebnis | Eigene `--calculate`-Option nach Inputfreigabe; Warnungen nicht überspringen; Ergebnisse erst versions-/lastfallgebunden auswerten. | Echte Solverquittung + Resultattabellen + unabhängige Referenz; anschließend ID01. |

## 2. Harness auf Windows einrichten
Der DeepSeek-Provider wurde laut ID01 bereits als `deepseek-official` gespeichert. Keinen zweiten Schlüssel erzeugen. In der tatsächlich installierten Harness-Version Settings → Models öffnen, vorhandenen Provider und Modellkatalog prüfen. Redigierte Speicherbestätigung ist Konfigurationsnachweis, kein Auth-Test. Den Startbefehl der installierten Desktop-/Source-Version verwenden; `pnpm run dsh web` ist kein versionsunabhängig zugesicherter Standard.

Offizielle Harness-Dokumentation beschreibt `$DSH_HOME/.credentials.yaml` und redigierte Rückgabe an die UI. YAML-Datei und Redigierung beweisen keine Verschlüsselung. Der hier implementierte Adapter akzeptiert nach Dateirechteprüfung ausschließlich einen Top-Level-String `DEEPSEEK_API_KEY`. Die reale DSH-Struktur muss lokal geprüft werden, ohne Schlüsselwerte auszugeben; ein anderes strukturiertes Storeformat wird abgewiesen statt geraten. Ein dokumentierter Harness-Credential-Resolver ist dann vorzuziehen. Keine Migration oder Veränderung vorhandener Credentials.

Der bestätigte Benutzerpfad aus dem bisherigen Arbeitskontext lautet `C:\Users\Julian Zotter\.dsh\.credentials.yaml`; dieser Windows-Host ist hier nicht zugänglich. `DSH_HOME` wird respektiert; sonst Benutzerprofil/.dsh. DeepSeek-Key und Dlubal-Key sind getrennte Berechtigungen.

## 3. NEXUS lokal prüfen
Aus dem kontrollierten Repository-Checkout, im Review-Branch:
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .\orchestrator
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_deepseek_integration.py -v
.\.venv\Scripts\python.exe tools\deepseek_auth_probe.py --execute
```
Der Probe liest nur `/models`, schreibt keine Konfiguration und gibt keine Keys aus. Hier ausgeführter Lauf: `BLOCKED / DSH_STORE_NOT_AVAILABLE_ON_THIS_HOST`; HTTP-200/401-Fälle sind bisher Mock-Tests. Keine echte Authentifizierung behauptet.

Erst nach erfolgreichem lokalem Auth-Test und freigegebenem synthetischem Input:
```powershell
.\.venv\Scripts\python.exe -m nexus_orch.cli run deepseek_chat "Antworte ausschließlich OK."
```
`available()` bedeutet nur auflösbare Credential-Bindung. Es ist kein Provider-Healthcheck. Token-/Zeitgrenzen im Adapter sind gesetzt; Kosten-/Datenfreigabe bleibt pro Auftrag erforderlich.

## 4. RFEM vorbereiten und parametrisieren
Für neue Modelle gRPC verwenden. Offizielle API-Signatur: `rfem.Application(api_key_value=... oder api_key_name=..., url=..., port=...)`; `api_key=` aus dem gelieferten Beispiel ist kein dokumentierter Parameter. `create_model(name=...)` ist keyword-only und liefert eine Modell-ID. Dokumentierter gRPC-Standardport ist 9000; lokale Programmeinstellung ist maßgeblich. 8081–8090 nicht als gRPC-Standard übernehmen.

Zunächst:
```powershell
.\.venv\Scripts\python.exe tools\rfem\rfem_preflight.py
.\.venv\Scripts\python.exe tools\rfem\rfem_preflight.py --read-live --api-key-name <vorhandener-Dlubal-Key-Alias>
```
`<vorhandener-Dlubal-Key-Alias>` bezeichnet eine bestehende lokale Referenz, keinen Schlüsselwert. Aktuellen RFEM-Build zuerst lesen und dazu passendes SDK installieren; kein ungeprüftes Upgrade. Der ausführbare Objektadapter dieses Piloten ist explizit auf SDK 2.16.6 / RFEM 6.16 begrenzt. Bei einem abweichenden bestehenden Build, etwa dem früher erwähnten SDK 2.12.8, wird ein entsprechendes Profil erst nach lokaler SDK-Prüfung ergänzt.

Modellplanung ohne RFEM-Zugriff:
```powershell
.\.venv\Scripts\python.exe tools\rfem\rfem_frame_adapter.py --span-m 6 --height-m 3 --roof-line-load-N-m 10000
```
Die Werte sind ein synthetisches Software-Testmodell, keine Vorbemessung für W012. Koordinaten: globale Z-Richtung positiv nach unten; Rahmenkopf z = −H. Die Linienlast wirkt tatsächlich auf Stab 3. Eigengewicht ist für den Test ausgeschaltet; lineare Analyse explizit. Lastkombinationen, Normnachweise, Stabilität und Projektfreigabe gehören nicht zu diesem Slice.

Nach Prüfung des ausgegebenen Vertrags und Inputhash: zusätzlich `--create-live --approved-input-sha <geprüfter Hash>`. Berechnung erfordert außerdem `--calculate`. Diese lokale CLI-Attestation ist keine kryptografische Authentifizierung und darf nicht ungeschützt als Remote-Tool exponiert werden. Keine automatische Wiederholung nach Teilfehlern; isoliertes Modell zunächst abgleichen. Solvererfolg ist keine technische Freigabe. Ergebnisvergleich und E/I-/Materialkennwerte bleiben gesonderte Nachweise.

## 5. Tool- und Datenvertrag
Erste registrierbare Toolkandidaten: `rfem_preflight_read`, `rfem_plan_frame`, `rfem_create_isolated`, `rfem_calculate_isolated`, später `rfem_export_results`. Planung und Lesen benötigen keine Modellschreibberechtigung. Create und Calculate benötigen eine im vertrauenswürdigen Host gebundene konkrete Autorisierung mit Inputhash/Modell-ID. Kein frei formulierter Python- oder Shell-Code aus LLM-Ausgaben.

DeepSeek Chat und Fetch sind getrennte Basisslices. Responses wird als Vertrag vorbereitet, erst nach stabilem Live-Chat aktiviert. Normale modellgenerierte Tool-Roundtrips funktionieren auch mit Chat Completions; die dokumentierte Einschränkung betrifft extern eingefügte Tool-Calls mitten im Verlauf. Responses-Historie ist clientseitig vollständig mitzuführen; GitHub-/Context7-Tools benötigen ihre eigenen tatsächlichen Connectorrechte.

## 6. Nachweise und Grenzen
Lokal: 16 Basis-/Security-/Geometrietests PASS; drei SDK-Tests separat mit echtem SDK und simuliertem Host; 17 RFEM-Protobuf-Objekte konstruiert und deterministisch serialisiert/rückgelesen. Das belegt SDK-Form und Mock-Verhalten, keinen RFEM-Serverlauf. Live-Credentials, Windows-ACL-Prüfung, RFEM-Verbindung, echtes `.rf6`, Solver und Ergebnisvergleich sind offen. Offizieller Harness-Gateway-Port lokal nicht bestätigt.

ID01 vor Merge; unabhängiges versionsgebundenes Review. Bestehende WORK-Registry und Ledger beibehalten; diese Repository-Fassung ist REVIEW_SNAPSHOT / REGISTRATION_PENDING. Kein fremdes ACK, keine globale Synchronisation behauptet. DBHub bleibt SECURITY_BLOCKED bis gepatchte Version mindestens 0.22.6 plus tatsächlicher DB-Rechte-/Schreibnegativtest und Abnahme vorliegen.

## Primärquellen, gelesen 12.11.2026
- Harness Models/Credentials: https://deepseek-harness.github.io/deepseek-harness/en/guide/providers
- DeepSeek Chat, Fetch, Responses, Models: https://api-docs.deepseek.com/api/create-chat-completion/ ; https://api-docs.deepseek.com/api/fetch/ ; https://api-docs.deepseek.com/api/create-response/ ; https://api-docs.deepseek.com/api/list-models/
- Tool-Call-Abgrenzung: https://api-docs.deepseek.com/guides/tool_calls/
- Dlubal Installation/Signaturen: https://apidocs.dlubal.com/installation_python.html ; https://apidocs.dlubal.com/source/rst_methods/rfem_methods.html ; https://apidocs.dlubal.com/source/rst_methods/rfem/create_model.html
- Explizite Analyse: https://apidocs.dlubal.com/source/rst_objects/rfem/loading/static_analysis_settings.html
- DBHub Originaladvisory: https://github.com/bytebase/dbhub/security/advisories/GHSA-mwwr-p57h-56pf
