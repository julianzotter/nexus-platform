---
name: oauth-registry-ledger-repair
version: 1.0.0
status: CODE_TESTED_LIVE_BLOCKED_GOOGLE_CONSENT
agent_id: ID02
executor: OpenAI Codex
executor_instance: /root
model_id: null
ticket_id: nexus-platform#96
ledger_number: null
registration_status: REGISTRATION_PENDING
technical_approval: false
observed_at: 2026-11-16T23:35:00+01:00
---
# NEXUS: OAuth, Registry und Ledger – Reparaturstand
## Ergebnis
Reparaturimplementierung: https://github.com/julianzotter/nexus-platform/pull/96
Geprüfter ausführbarer Stand: 5e138028437dc05e0a2e570f0bcb16731e4ad65d.
CI: https://github.com/julianzotter/nexus-platform/actions/runs/43971269697
| Prüfung | Belegter Status |
|---|---|
| Repository-CI | PASS: 280 Tests und 34 Subtests; zusätzlicher CPLM-Lauf 36 Tests PASS |
| Windows PowerShell 5.1 | CI-Job PASS, einschließlich Syntaxprüfung beider neuer Starter |
| Gezielte lokale Prüfungen | 70 PASS: 15 Control/CAS, 17 Persistence, 16 OAuth, 9 Legacy, 5 Operation-Diagnose, 8 Bootstrap |
| Unabhängiger Review | REVIEW_PASS auf exakt obigem Commit, getrennte Codex-Instanz /root/review_remaining_repair; 21 Dateien gegen Commit-Blobs geprüft |
| Zwölf bisher fehlende Quellidentitäten | Vollständige Drive-Rohbytes/SHA256 unabhängig geprüft, neun vorhandene CSV-Hashes abgeglichen |
| Ledger-Probereparatur | PASS: genau 0210/0211 geändert, alle 201 Datensätze erhalten, Wiederholung idempotent |
| Tatsächlicher Aufruf dieser Runtime | BLOCKED_DRIVE_CREDENTIALS, Exit 2, vor jeder kanonischen Drive-Änderung |
| Live-OAuth/CAS/Registry/Delivery | NOT_VERIFIED; Google-Zustimmung auf dem PC erforderlich |
Keine erfolgreiche Live-Reparatur des HTTP400 behauptet. Der verbundene Drive-Connector arbeitet; die getrennten GitHub-Workflow-Credentials stehen dieser Runtime nicht zur Verfügung. Kein Refresh-Token, Client-Secret oder eigenständiger Access-Token im verfügbaren Prozess und keine lokale private OAuth-Datei vorhanden. Der konkrete OAuth-Fehlergrund ist vor neuem bereinigtem Preflight nicht bekannt.
## Umgesetzte Korrekturen
1. OAuth-Erneuerung: --renew statt Ablehnung einer bereits bestehenden Credential-Datei; frische Google-Zustimmung; WORK-Prüfung ausschließlich mit dem neuen Kandidaten; privater Byte-Snapshot; lokale Exklusivsperre und atomarer Austausch. Unter Windows ACL-Begrenzung vor dem Schreiben. Fehlgeschlagene Prüfung ersetzt alte Credentials nicht. Serverfehltexte und Tokenwerte werden nicht ausgegeben; nur freigegebene OAuth-Fehlercodes. INVALID_GRANT/INVALID_CLIENT usw. bleiben unterscheidbar; HTTP400 allein wird nicht als Ablauf diagnostiziert.
2. Registry-/Ledger-Writer: ID-erhaltende bedingte Drive-v2-Medienwrites als Kandidat. Vor kanonischen Writes muss eine separate, vorab identifizierte Probe-Datei absichtlich falsche und veraltete ETags mit HTTP412 zurückweisen; von zwei gleichzeitigen Writes mit identischem ETag darf genau einer committen. Rohbyte-Readback prüft das Ergebnis. Fehlende Unterstützung -> STOP. Keine unbedingte Ersatzoperation, kein bloßer Lockdateiname, kein blinder Retry nach Timeout.
3. Registrierungsvertrag: unveränderten JSONL-Byte-Präfix erhalten; gültige vorhandene Datei-/Provider-Revisions-/Hash-Ereignisse deduplizieren, auch von anderen Operationen/Writern. Name, Provider-ID, URI, Rohbytehash/-scope, Prüfstatus und zeitzonenbehafteter Registrierungszeitpunkt müssen passen. Derselbe Provider-Stand mit widersprüchlichem Hash blockiert. Abschlussprüfung nutzt dieselbe Identitätsregel.
4. Recovery: unveränderliche run_id-spezifische Vorher-Dateien und Receipts, auch bei Ledger-Erfolg mit späterem Registry-Konflikt. Probe-ID und Status werden vor Create protokolliert; ein PENDING-/FAILED-Probejournal autorisiert keinen Write.
5. Laufender Sync: normale GitHub-Delivery verlangt nun Registrierung statt bloßem Upload. Drei Writer-Workflows teilen nexus-drive-canonical-writer. Diese Actions-Warteschlange sperrt keine externen direkten Drive-Schreiber; es gibt keine globale Lock-Behauptung.
## Parallele Claude-Änderung integriert
Während dieser Reparatur wurden #94/#95 gemergt. Der dort neue registry_append.py verglich Hashes und ersetzte danach unbedingt. Das ist keine atomare Compare-and-swap-Operation.
Der direkte Legacy-Write-CLI ist gesperrt; sein Hilfs-Writer verlangt ConditionalDrive und einen expliziten Ableitungs-Preimage-Hash. Der Legacy-Workflow akzeptiert nur die bekannte ursprüngliche ID06-Batchreferenz und führt den geprüften kanonischen Reparaturplan aus. Kein zweiter ungeschützter Produktionspfad.
Erste CI dieser PR fand nur eine alte Diagnose-Fixture, die einen direkt gelieferten Access-Token verwendete, aber Token-Refresh als Operation erwartete. Fixture auf Refresh-Credentials korrigiert; separate Prüfung des direkt gelieferten Tokens ergänzt. Aktuelle CI und beide Windows-/Repository-Jobs PASS.
## Konkreter Ledger-Delta
Bestehende Ledger-ID bleibt 1Qso4VQE-cySJdxo6j-MNjxxOc5-GJlrK.
0210: DRIVE_ID=1M2ZvxwSuaIsKe_-VW_xiTWUCwBOGIXni; SHA256=aa2648127fb96426a6ccaf1432fe9ad3220b080264bde213494df26a20385b0e.
0211: DRIVE_ID=1Qso4VQE-cySJdxo6j-MNjxxOc5-GJlrK; historischer Vorreparatur-Hash=8b7cafe7f00d3e0b0db9792a1fe8c81fc258cc5de81e6760bcbfd24b37a89cff.
Die NOTE kennzeichnet diesen Hash ausdrücklich als ursprüngliche zusammengeführte CSV-Version vom 16.11. 21:50:08.974Z; der neue aktuelle Hash wird extern im JSONL-Ereignis/Receipt nachgewiesen. Keine selbstreferenzielle aktuelle Datei-Hashbehauptung.
Deterministisch berechneter korrigierter CSV-Hash beim eingefrorenen Ausgangsstand:
f3a83fe732d2c88dedb3b1e5e9b5ee96235d40b1daae4934cd7e421b7e729027.
Vorbild-JSONL: 460 Ereignisse, SHA256=e233e9acbeb835413f3a6950393e03028cdfd0aad4c7387e083440ef850d4eac.
Diese Hashes sind Quellen-/Offline-Nachweise, keine Behauptung einer bereits ausgeführten Cloud-Mutation.
## Ein erforderlicher lokaler Start
Nach Übernahme der gemergten Reparatur im nexus-platform-Checkout:
powershell -ExecutionPolicy Bypass -File .\tools\windows\repair_nexus_sync.ps1
Der Starter erneuert Google-Zustimmung, prüft und veröffentlicht Credentials, repariert Registry/Ledger mit Live-Probe und stößt Delivery an. Fehlt eine lokale OAuth-Konfiguration, fragt er nach dem ursprünglichen Google-Desktop-OAuth-Client-JSON als lokaler Datei. Keine Secrets in Chat/WORK eingeben.
DELIVERY_DISPATCHED bedeutet nur eingereicht. Erfolgreiche Delivery samt Rohbyte-/Registry-Readback muss der nachfolgende Actions-Lauf belegen.
Konkrete Anleitungen im Repository: docs/NEXUS-OAUTH-RECOVERY.md und docs/NEXUS-CONTROL-REGISTER-REPAIR.md.
## Grenzen und Quellen
Keine ACL-Änderung, keine Datei-/Branchlöschung, keine neue Ledgernummer und keine technische Freigabe. Der separate PC-Offline-Test bleibt eigenständig ausständig.
Aktuelle AGB v006: https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view
Aktuelle Folder.md: https://drive.google.com/file/d/1nDjF78dq3l8PGpXsauzBz1bzHescDSwv/view
Kanonisches Register: https://drive.google.com/file/d/15m8T5cWbogIup9snzFwiB1g9HqNCoGow/view
Koordination: https://github.com/julianzotter/nexus-platform/issues/73
Die Wiederherstellung wird nicht durch das Vorliegen dieses Berichts abgeschlossen. Dieses Artefakt bleibt bis zum tatsächlichen geschützten Write und Readback REGISTRATION_PENDING und wird dem eingefrorenen Reparaturplan mit eigener Drive-ID und Rohbytehash hinzugefügt.
