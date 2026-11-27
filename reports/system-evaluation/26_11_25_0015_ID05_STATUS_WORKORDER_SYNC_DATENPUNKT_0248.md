---
name: 26_11_25_0015_ID05_STATUS_WORKORDER_SYNC_DATENPUNKT_LEDGER-PENDING
version: "1.0"
status: REVIEW
timestamp: "2026-11-25T00:15:45+01:00"
timezone: Europe/Vienna
agent_id: ID05
role_id: ID05
owner_id: ID05
issuer_id: ID01
executor_instance: OpenAI Codex /root
provider: OpenAI
model_id: null
role_register_version: NEXUS-ROLES-v1.2
ticket_id: WO-20261124-ID05-SYSTEMEVAL
registration_status: REGISTRATION_PENDING
ledger_id: null
release_status: NO_RELEASE
hash_scope: body_utf8_after_closing_frontmatter_lf
hash: 97c0dabb7bc624189fce3fc6417c2f05948dbf24e6d3cfc0bef04b10067bdf54
task_state: VALIDATED
review_status: REVIEW_PENDING
---
# Work-Order-Sync und privater Panel-Datenpunkt

[Auftrag](https://drive.google.com/file/d/1ekmdh6AIdLuOd35jpCq3kQhLlwze6CsP/view) · [Diskussion #129](https://github.com/julianzotter/nexus-platform/pull/129) · [Panel v8](https://nexus-sync-diagnose.julianzotter.chatgpt.site) · [Privater Datenpunkt](https://nexus-work-sync.julianzotter.chatgpt.site/api/v1/work-orders/WO-20261124-ID05-SYSTEMEVAL)

## Nachweise

| Prüfung | Ausführung | Ergebnis |
|---|---|---|
| Drive READ | Original vor und nach dem Sync aus WORK als Rohbytes gelesen, 5.287 Bytes. | DRIVE_READBACK_OK · SHA-256 `d778a2c99a31bc8a3ea5a976d332d56a6ffbdaaeff46072cdfd4aac476f90973` |
| Drive WRITE | Zwei neu erzeugte Deployment-Archive in WORK abgelegt und vollständig über die zurückgegebenen IDs gelesen. | Beide byteidentisch, Belege unten. |
| GitHub READ | Originalpfad an `main`-Commit `3372255c0d6cbaf6f33c4ab2d893d7e3c20df961` und am PR-Head `93b1d8c613550c872af9291ad35af5cbdb906965` geprüft. | Zielpfad 404 bei bestätigtem Commit. GITHUB_MISSING_ON_TARGET_BRANCH. Work Order am PR-Head byteidentisch mit Drive. Ursache des Zielbranchzustands offen. |
| GitHub WRITE | Zwei Archive über einen Commit an den bestehenden Auftragsbranch angehängt, Diff vor dem Branch-Update kontrolliert, beide Git-Blobs roh zurückgelesen. | [Commit 9bb2aebb4c7fc854dccaae9802a36067a7a4eaa8](https://github.com/julianzotter/nexus-platform/commit/9bb2aebb4c7fc854dccaae9802a36067a7a4eaa8) · beide Bytes identisch zu WORK. |
| Site WRITE und READ | Privater Work-Order-Datenpunkt, Sites-Dienstzugang, PUT gefolgt von GET und Objektvergleich. | HTTP 200 STORED und HTTP 200 GET mit identischem Inhalt. Ziel ist ein persistenter R2-Datensatz. |
| Browser | Öffentliche Panelansicht in Chrome geöffnet, Refresh angeklickt. Ohne private Sitzung unveränderte Panelrevision und ausstehenden Zugriff beobachtet. | Abruf 25.11., 00:13:34 MEZ, Projektquelle 23.11., 13:43:51 MEZ. Keine fachliche Hochstufung. Der eingeloggte Eigentümerpfad wurde per Dienstzugriff am Datenpunkt, der personalisierte Klick im Konto von ID01 nicht geprüft. |

Die neue Site mit dem Datenpunkt ist auf den Eigentümer beschränkt. Der bestehende Panel-Abruf lädt diesen Datenpunkt zusätzlich zum publizierten Projekt-JSON. Bei Browser-Sitzungen ohne freigeschalteten Zugriff führt „Privaten Datenpunkt öffnen“ zur authentifizierten Ansicht. Die Abrufzeit bezeichnet den Seiten-/API-Read, `checkedAt` den tatsächlichen Quellenabgleich. Die älteren statischen Projektkennzahlen behalten ihren eigenen Stand.

## Veröffentlichung und Archiv

| Artefakt | Revision / Ablage | SHA-256 des tar.gz |
|---|---|---|
| Panel v8 | Site-Commit `cf26470a4e9cfbda7bd1caf8ddd5396a1938f500` · [WORK](https://drive.google.com/file/d/14pr_e7yBoH5QrhRS2-mAzpLe8Mm8pkME/view) · [GitHub-Archiv](https://github.com/julianzotter/nexus-platform/blob/9bb2aebb4c7fc854dccaae9802a36067a7a4eaa8/backups/control-panel/26_11_25_0012_ID05_PANEL_SITE_V8.tar.gz) | `b606c262af0343307ad619afc3cc05070bfa3425874b5112c7c79ca1d3b4a2dc` |
| Privater Datenpunkt v1 | Site-Commit `c7022ea945e9d7d03781f07f8603ab62e3643f9c` · [WORK](https://drive.google.com/file/d/1nSrGT4P-VVsk1u0eQ0Dzj8CRG7KZfBZx/view) · [GitHub-Archiv](https://github.com/julianzotter/nexus-platform/blob/9bb2aebb4c7fc854dccaae9802a36067a7a4eaa8/backups/control-panel/26_11_25_0012_ID05_WORKORDER_ENDPOINT_V1.tar.gz) | `b076b34bf4117551f354b60dffdaa854c1e1b2d6853a29e4746adec9515b340c` |

## Betriebsregel für weitere NEXUS-Aufträge

Zu Beginn und nach Kontextverlust aktuelle AGBs, Manifest, Baseline und relevante neue Work Orders lesen. Drive und GitHub READ und autorisierte WRITE je Runtime getrennt prüfen. Den vorgesehenen Bericht oder das Archiv als Schreibprobe verwenden, zurücklesen und mit Quelle und SHA-256 vergleichen. Provider-ID, Zielordner oder Branch und Commit protokollieren. Chat-Connector, Sites-Dienst und Actions-Runner sind verschiedene Verbindungen. Bericht und Review-Snapshot vor der Schlussmeldung sichern. Dies ist die von ID01 angeforderte Arbeitsregel für Reporting und Archivierung.

## Datenpunkt nachführen

Der Endpunkt ist ein geprüfter Datenstand je Auftrag. Der Browser liest bei Refresh den letzten persistierten Beleg. Ein Quellenabgleich muss die Provider eigenständig lesen. Für `WO-20261124-ID05-SYSTEMEVAL` gilt diese Reihenfolge:

1. WORK-Original `1ekmdh6AIdLuOd35jpCq3kQhLlwze6CsP` roh lesen. PR 129 sowie den vollständigen Head von Ziel- und PR-Branch in `julianzotter/nexus-platform` holen. Pfad `reports/system-evaluation/26_11_24_2351_ID05_WORKORDER_SYSTEMEVAL_LEDGER-PENDING.md` an beiden Commits prüfen. Aktuelle AGBs `10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg`, relevanten WORK- und PR-Rücklauf plus Reviews lesen. Original anschließend erneut aus Drive lesen. Bei geänderten Bytes den Vergleich neu beginnen.
2. Sites-Projekt `appgprj_6b0618d628b48191b31ca037b31cd0b5` muss weiterhin allein dem Eigentümer zugänglich sein. Nur den zu dieser Site gehörenden Dienstzugang aus get_site im Speicher verwenden. GET des vorhandenen JSON-Belegs. Schema beibehalten, checkedAt in UTC, echte Revisionen und Quellenzustände einsetzen. Nur ein bestätigter fehlender Pfad im lesbaren Commit zählt als GITHUB_MISSING_ON_TARGET_BRANCH. Ungeprüfte Zustellung, ACK, Review oder Freigabe offen halten.
3. Nur an den obigen HTTPS-Endpunkt ohne Redirect senden. Header OAI-Sites-Authorization Bearer (Laufzeitwert), X-Nexus-Sync verified-v1, Content-Type application/json; Länge mitsenden. Bei abweichenden Quellen Ergebnisebenen einzeln dokumentieren. Nach PUT den Inhalt per GET vergleichen. Idempotenter Wiederanlauf ist vorgesehen, bei konkurrierenden/stale Writes 409 neu lesen. Bei Quellfehler bleiben der letzte Beleg und seine Prüfzeit erhalten.

Registrierung beim benannten Ledger-Schreiber und fachliche ID01-Freigabe offen. Der neue Schedulerplatz war durch das Kontolimit (15) blockiert. Eine geplante Ausführung erfordert ihren eigenen Run-Beleg.
