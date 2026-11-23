# NEXUS / P205 / Control Panel – Repair Status

Datum: 23.11.2026, 14:10 MEZ  
Rolle: ID02  
Status: `PARTIAL_COMPLETE / LOCAL_WINDOWS_EXECUTION_REQUIRED`

## VERIFIED

- GitHub PR #116 ist über Merge-Commit `e5e559509d32aed1d6ad500176a5d95d85fa197a` gemergt.
- Der Merge schließt die fachlichen P205-Gates nicht; der gemergte Manifeststand führt `engineering_release=BLOCKED` und `registration_status=REGISTRATION_PENDING`.
- Das private Control Panel ist als Version 6 aus Source-Commit `022b8f045253f0c9bbacfab2e33654bb26309b8e` erfolgreich deployed.
- Version 6 zeigt PR #116 als `MERGED` und prüft veröffentlichte `control-data.json` alle 10 s auf Änderungen.
- GitHub-Workflows `nexus-monitor.yml`, `nexus-drive-poll.yml` und `nexus-delivery.yml` sind konfiguriert. Der letzte belegte Betriebsstatus bleibt wegen `OAUTH_HTTP_400_INVALID_GRANT` und `MONITOR_NOT_COMPLETE` nicht grün.

## IMPLEMENTED

- Vollständiges PowerShell-Skript `P205_FT_Excel_Native_Recalc_v1_2.ps1` mit Pflichtparametern, SHA-256-Gate, read-only Source, `CalculateFullRebuild`, Save/Close/Readback-Kopie und COM-Cleanup.
- Statische Vertragstests verhindern die ursprüngliche uninitialisierte `$source`-Variable und prüfen Fail-Closed-/Audit-Invarianten.

## OFFEN / REIHENFOLGE

1. ID06: Skript am freigegebenen Windows-/Excel-Ziel als vollständige Datei ausführen; JSON-Receipt und Output-Workbook sichern.
2. ID04: Planrevision und RFEM-Metadaten (Modell, Stab, lokale x-Position, Kombination, Achsen, Einheiten, Vorzeichen) binden.
3. ID03/ID07: identisches Evidence Pack und alle gespeicherten Auslastungen >105 % unabhängig prüfen.
4. ID03: Registry/Ledger-Reconciliation abschließen.
5. ID01: explizite technische Freigabe oder Ablehnung dokumentieren.

## PANEL-GRENZE

Der 10-s-Browserabruf erkennt nur Änderungen einer bereits publizierten Paneldatei. Er ist kein Ersatz für Drive-/GitHub-Polling, lokale Watchdog-Prozessprüfung oder Agenten-ACKs.
