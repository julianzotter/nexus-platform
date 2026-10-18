---
document_id: NEXUS-WO-GEMINI-ARGON-BRIDGE-001
version: 0.1.0
timestamp: '2026-10-16T17:30:00+02:00'
status: BLOCKED_EXTERNAL_RUNTIME
goal: 'Gemini Argon schreibt und liest rohe Markdown-Artefakte ohne manuelles Kopieren'
reported_by: Julian_Zotter
evidence_class: USER_QUOTED_RUNTIME_MESSAGE
screenshots_examined_in_this_run: false
observed_claim: 'Gemini Argon kann weder Computerdateien noch Google-Drive-Dateien ablegen; bietet Code im Chat an'
local_session_capability: 'Drive-Raw-Markdown-Upload und vollständiger Readback tatsächlich bereits ausgeführt'
foreign_session_capability: NOT_TESTED
completion: NOT_COMPLETED
prohibited_completion_claims: ['Skript erstellt ohne gespeicherte Datei', 'eingerichtet ohne Ausführungsbeleg', 'Connector verbunden bedeutet Schreibrecht']
blocking_dependencies: ['Aufrufbare Tool-/API-Verbindung aus Argons tatsächlicher Runtime', 'Autorisierter ausführender Host mit Drive-Schreibrecht']
---
# Entscheidung
Keine manuelle Copy-Paste-Schleife als Systemlösung. Der Fehler ist fehlende ausführbare Verbindung, nicht ein fehlender Prompt. Die Schreibrechte dieser ChatGPT-Sitzung werden nicht auf Gemini übertragen. Die wiedergegebene Aussage belegt keine allgemeine Unfähigkeit aller Gemini-Produkte und keinen überprüften Screenshotstatus.

## Vier technische Wege
| Weg | Reale Voraussetzung | Eignung und Grenze |
|---|---|---|
| 1. Native Agent-Tools | Argons konkrete Runtime stellt authentifizierte Raw-Datei-Create/Update/Read bereit | Am kleinsten, falls tatsächlich vorhanden; durch Roundtrip prüfen, nicht annehmen. |
| 2. Gemini-API-Function-Calling → kontrollierter Drive-Writer | Ausführende Anwendung, Gemini-API-Zugang und Drive-OAuth für den Zielordner | Empfohlene dauerhafte Architektur. Das Modell fordert Funktionen an; die Anwendung führt sie aus. Ein Gemini-Webchat erhält diese Verbindung nicht allein durch einen Prompt. |
| 3. n8n-Workflow → Drive-Dateioperationen | Betriebenes n8n, Drive-Credentials und authentifizierter Eingang aus der Agent-Runtime | Praktischer Low-Code-Adapter; kein offener Schreibwebhook. Installation und Runtimeeingang hier nicht vorhanden. |
| 4. Installierter Workstation-Agent → synchronisierter Ordner/GitHub | Erreichbarer Windows-Host, installierter Dienst/Task und getestete Sync-Richtung | PowerShell ist möglich, aber Chatcode allein ist weder Installation noch Syncnachweis. Hier kein Zugriff auf die Workstation. |

Ein MCP-Server kann Weg 1 oder 2 transportieren, sofern die betreffende Runtime ihn unterstützt; MCP allein verleiht keine OAuth-Rechte. Keine neue ungetestete OneDrive-Zwischenkopie einführen, solange der direkte Writer genügt.

## Minimaler verbindlicher Roundtrip
1. Authentifizierte Runtime und erlaubten WORK-Zielordner identifizieren; aktuelle Folder.md vollständig lesen, Policyhash als Read-Receipt halten.
2. Eindeutigen Auftrag mit idempotentem task_key und Roh-Markdown entgegennehmen; Timestamp/Titel, YAML und Quellen prüfen.
3. Raw-UTF8-Datei erstellen, bestehende Datei nur über bekannte ID und kontrollierte Revision aktualisieren. Keine Konvertierung zu Google Docs.
4. Vollständigen Inhalt zurücklesen und SHA256 vergleichen. Erst danach Artefakt-ID/URL, Hash und Run-ID an Argon zurückgeben.
5. Neustart und Wiederholung dürfen keine zweite logische Datei erzeugen. Fehlende Berechtigung, konkurrierende Änderung und unklarer Sendeausgang müssen sichtbar blockieren.
6. Zustellung und ACK getrennt prüfen; gefälschter Actor oder freie Human-ID sind kein Freigabenachweis.

## Iterative Verfeinerung / Selbstheilung
Ein Fehler eröffnet ein dauerhaftes Troubleshooting-Ticket mit Fehlerklasse und letzter erfolgreicher Phase. Nur wiederholbare, autorisierte Schritte mit begrenztem Retrybudget automatisch wiederholen. AUTH_REQUIRED, falscher Tenant und unklare Schreibwirkung bleiben blockiert und werden gemeldet; kein endloser Retry und kein blindes Überschreiben. Nach Korrektur denselben Roundtrip plus Negativfälle erneut ausführen.

## Aktueller Nachweis
Diese Datei wird durch die vorhandene ChatGPT-Drive-Verbindung automatisch abgelegt und zurückgelesen. Das ist ein echter Schreibbeleg dieser Sitzung, kein bestandener Argon-Test. Argons PowerShell-Skript liegt dieser Sitzung nicht als Datei vor; seine Existenz oder Funktionsfähigkeit wird nicht bestätigt.

## Primärquellen
- https://ai.google.dev/gemini-api/docs/function-calling
- https://developers.google.com/workspace/drive/api/guides/manage-uploads
- https://developers.google.com/workspace/drive/api/reference/rest/v3/files/update
- https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googledrive/file-operations/

## Änderungslog
v0.1.0 — Nutzermeldung von Gemini Argon als externen Integrationsfehler erfasst; direkte Bridge empfohlen, vier ausführbare Anschlusswege und falsifizierbare Roundtrip-Abnahme definiert. Kein Fremdaccountzugriff behauptet.
