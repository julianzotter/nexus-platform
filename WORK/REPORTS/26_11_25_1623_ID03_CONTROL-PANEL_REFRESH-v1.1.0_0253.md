---
created_at: 2026-11-25T16:23:00+01:00
role_id: ID03
version: DRAFT-v1.1.0
status: PEER_REVIEW_PENDING
registration_status: LEDGER-PENDING
release_status: NO_RELEASE
---
# NEXUS Control Panel – v1.1.0 Refresh Draft / Review
## Ausgangsbefund
Produktives ChatGPT-Sites-Panel v4.1 laut ID01-Screenshots und ID05-Chat mit Datenstand 2026-11-23 13:43:51 Europe/Vienna. Seitenabruf 25.11. aktualisiert nur die Browserdarstellung, nicht die Quellendaten. Perplexity-Drafts 0.1.0/0.3.0 sind keine bestätigten produktiven Deployments.
## Implementierung 25.11.2026
Neue versionierte HTML-Datei mit echtem HTTPS GET auf /api/v1/control-panel/snapshot (same origin); manuell auslösbarem Button ↻; serverseitig erwarteter JSON-Vertrag observedAt, sourceRevision, workOrders[], reports[]; Content-Type, HTTP, Timeouts, Größen-/Shape-Prüfung; älteren Snapshot verwerfen; gleiche Beobachtungszeit mit abweichender Revision als Konflikt behandeln; last-good snapshot bei Fehler belassen und STALE anzeigen. Sichere DOM-textContent-Ausgabe statt HTML-Injection. KI-Inventar 219/44/1967 ausdrücklich HISTORISCH. Keine eingebetteten Secrets.
## Grenzen / Evidence Gates
Der JSON-Snapshot-Backend-Endpunkt ist eine erforderliche Schnittstelle und bisher NICHT als verfügbar nachgewiesen. Google Drive, GitHub und private Sites-API sind nicht direkt aus der HTML-Datei erreichbar. Keine produktive Source→Snapshot-Pipeline, kein Browser-E2E, kein Sites-Deployment, kein CI-Test in dieser Durchführung. Der vorhandene Refresh-Button der Sites-v4.1-Seite bleibt UNVERÄNDERT.
## GitHub / Artefakte
Versioned HTML: https://github.com/julianzotter/nexus-platform/blob/main/prototypes/nexus-control-tower-draft-v1/releases/26_11_25_1623_ID03_NEXUS-CONTROL-PANEL_DRAFT-v1.1.0.html
Commit: 986e9d2158b2c29e8d5d6bd3318d345188074e26
Arbeitsverzeichnis: https://drive.google.com/drive/folders/1t7T-KWn2s9HUctXGg-HY04z3xLamRJ5g
WORK: https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP
## Peer-Review / Auftrag
ID02: Browser-UX, Datenmodell, Inventur-Provenienz prüfen; dokumentierte Findings.
ID03: Governance, Repo/WORK, Delivery/ACK, kein Selbstreview.
ID05: Perplexity-Chat und Ablagebehauptungen gegen Belege prüfen.
ID06: Quelle bereitstellen, Feed vertraglich implementieren, automatisierte Tests Delta/Replay/401/403/Timeout/Conflict, echte Browser-Abnahme. Bestehendes Issue #73 weiterführen.
No peer ACK documented. ID01 release gate outstanding.
## Nächster technischer Schritt
Echten autorisierten und read-only serverseitigen Feed an Site-Origin bereitstellen, dann Owner-Browser GET-Readback nachweisen. Ohne Sites-Editor-/Runtime-Zugriff kein Deployment erzwingen.
