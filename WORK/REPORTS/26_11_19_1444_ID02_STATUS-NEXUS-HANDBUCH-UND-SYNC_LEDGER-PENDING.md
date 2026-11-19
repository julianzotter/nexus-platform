---
title: "NEXUS im Betrieb – Statusbericht zu Handbuch, Implementierung und Synchronisierung"
timestamp: "2026-11-19T14:44:00+01:00"
timezone: Europe/Vienna
version: "1.0"
role_id: ID02
executor: OpenAI Codex
status: ABWEICHUNG_NO_RELEASE
registration_status: REGISTRATION_PENDING
ledger_id: null
related_issue: "julianzotter/nexus-platform#73"
canonical_folder_id: 1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP
---

# NEXUS im Betrieb
## Konsolidierter Statusbericht zu Handbuch, Implementierung und Synchronisierung

**Entscheidung zum 19. November 2026:** Das CAD-/RFEM-Handbuch ist an beiden Zielorten lesbar. Für den automatisierten Betrieb fehlen erfolgreiche Zeitplanläufe. Dieser Bericht sichert die wesentlichen Entscheidungen des Chats als eigenen Reviewstand. Drive WORK führt das Original, das private Repository `julianzotter/nexus-platform` den Review-Snapshot. [WORK-Regel](https://drive.google.com/open?id=1nDjF78dq3l8PGpXsauzBz1bzHescDSwv) · [AGB v007.1](https://drive.google.com/open?id=10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg)

### 1 · Welche Inhalte sind gesichert?

| Gegenstand | Nachweis und Reichweite |
|---|---|
| „Vom Plan zum Prüfmodell“, v1.0, 19.11.2026 | VERIFIED. Vollständige Texte aus [WORK](https://drive.google.com/open?id=1XK5YeJu4VcejNOZ22g9KSgFxllpd-pQe) und [GitHub main](https://github.com/julianzotter/nexus-platform/blob/main/docs/handbooks/26_11_19_1434_ID02_NEXUS_Vom_Plan_zum_Pruefmodell_v1.0.md) stimmen überein. Schwerpunkt CAD, RFEM und Wissensablage. Dokumentstatus PROPOSED, Registrierung ausständig. |
| Allgemeines NEXUS-Benutzerhandbuch und Implementierungsguide | VERIFIED als [Drive-Arbeitsgrundlage vom 18.11.](https://drive.google.com/open?id=1YiVFpt9z0PaxnpvvSdfeGvBLu-SW97iJ). Das Session-Transkript umfasst Handbuch, SQLite, Python-Builder und File-Registry. Ein gleichlautender GitHub-Dateistand und die Urheberschaft durch Gemini sind für diese Quelle offen. |
| DeepSeek-Harness und Windows-Betrieb | [Architekturskizze](https://drive.google.com/open?id=1yiI_yLaIQaYb22ubaGwTW0E6QpJob1Y-) und Statusberichte [Teil 1](https://drive.google.com/open?id=19RbupTeNYu1kl0v41DzDWVPSaD1ueyEU) / [Teil 2](https://drive.google.com/open?id=157nBKsS9ksXnlsoBFtBxwDKVwPsgjwI_). Identische Repo-Kopien und produktive Integration sind unbestätigt. |

### 2 · Welche Sync-Nachweise liegen vor?

| Workflow | Geprüfter GitHub-Job | Ergebnis |
|---|---|---|
| Monitor | [44530320979](https://github.com/julianzotter/nexus-platform/actions/runs/44530320979) | FAIL. Repository-Validierung und Evidenzprüfung scheiterten in Schritt 5 und 6. Der Gate-Bericht meldet unvollständige Abdeckung. |
| Drive-Poller | [44482543204](https://github.com/julianzotter/nexus-platform/actions/runs/44482543204) | FAIL. Lesen der Änderungen und Checkpoint-Prüfung scheiterten in Schritt 5 und 6. |
| GitHub → WORK | [44530389047](https://github.com/julianzotter/nexus-platform/actions/runs/44530389047) | FAIL. Drive-Preflight scheiterte in Schritt 6. Der Gate-Bericht nennt beim Token-Refresh `OAUTH_HTTP_400_INVALID_GRANT` und übersprungene Zustellung. |

Das [Gate-Protokoll 14:40 MEZ](https://drive.google.com/open?id=1E2GAT93pa4TLWzzI-3kwfHj7keDRAd4a) dokumentiert für Monitor und Poller jeweils **0/3 erfolgreiche Zeitplanläufe** im ausgewerteten Fenster. Ein Poller-Checkpoint belegt das Lesen einer Änderung. Für einen Ende-zu-Ende-Sync gehört zusätzlich der Rücklesebeleg für das tatsächlich zugestellte Artefakt dazu.

**Zugriff:** Die direkt gelesenen [WORK-Berechtigungen](https://drive.google.com/drive/folders/1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP) zeigen Julian Zotter als Owner, den Anzeigenamen „Couric Dssign“ als Writer und zusätzlich `anyone:writer`. Für Couric sind damit individuelle Schreibrechte belegt. GitHub-Konto, Repo-Adminrechte und effektiver Schutz von main bleiben hier ungeprüft. ID01 soll bei der Einschränkung des allgemeinen Linkzugriffs die benannte Couric-Freigabe erhalten.

### 3 · Implementierung in abnehmender Priorität

1. **Betrieb wieder nachweisen.** Zuständige Administration prüft OAuth-Client und Token-Zuordnung, erneuert bei Bedarf die Autorisierung und testet lesend den exakten WORK-Ordner. Parallel Ursache der unvollständigen Monitor-Abdeckung beheben. Danach je Workflow drei aufeinanderfolgende echte Zeitplanläufe gemäß [Gate-Protokoll / Issue #73](https://github.com/julianzotter/nexus-platform/issues/73) dokumentieren. Pro Lauf Trigger, Run-ID, Commit, Zeit, Coverage bzw. Checkpoint und Ergebnis festhalten. Für die Zustellung zusätzlich Datei-ID, Zielpfad und SHA-256 aus Rücklesen erfassen. Baseline aus Laufdauer, Fehlerrate der letzten zehn Läufe, Zeit seit letztem belegtem Sync und Zeit bis zur Wiederherstellung bilden.
2. **Validator als kleinen Python-Kern pilotieren.** Ein freigegebenes Testprojekt und eine Quellrevision wählen. Python prüft zuerst SSOT und RACI (C01–C02), nach Entwurf alle C01–C10 einschließlich V01–V15. Beispielabnahme: GWP ohne Bezugsfläche oder Quellversion → kein PASS. Unfreigegebener Sendeversuch → BLOCK und Audit-Eintrag. Gleiche versionierte Eingaben müssen im Regelkern identische Prüfresultate liefern. Fachliche Freigabe an Person, Empfänger und konkreten Ausgabestand binden. PowerShell bzw. Batch starten denselben Python-Einstieg und reichen Exitcode und Protokoll weiter. Markdown-Skills beschreiben diesen Ablauf. Implementierungsstand der sieben vorgeschlagenen Skills einzeln prüfen.
3. **Refresh, Wissensbasis und lokale API anschließen.** Freigegebene Dateien per Dry-Run inventarisieren. Quell-ID, Revision, Hash und Fundstelle erfassen. SQLite-Transaktion für Beobachtung, Versionsbezug und Checkpoint verwenden. Abnahme: zweiter Lauf mit identischer Datei erzeugt keine weitere Beobachtung, geänderte Quelle erhält eine neue Revision, frühere bleibt lesbar. FTS5-Suche und lesende MCP-Tools zunächst auf einer Kopie prüfen. Schreibende Tools an dieselbe Freigabeprüfung binden. Weitere Guard-, RAG- und Scheduler-Produkte aus dem Chat sind Evaluierungskandidaten. Vor Auswahl Offline-Betrieb, Lizenz, Versionsbindung und Restore mit eigenen Testdaten nachweisen.

**Abschlusskriterium:** Dateiablage, technische Laufnachweise, Ledger-Eintrag und menschliche Freigabe separat protokollieren. Die Übernahme dieses Berichts kann anhand der beiden Zielkopien überprüft werden. Die Gesamtfreigabe bleibt beim zuständigen Menschen.
