<!-- READABLE TEXT SNAPSHOT; not original provider bytes; canonical source: https://docs.google.com/document/d/1OCkf0HslAhXIMmsKzu2zdBr2VyYc3Juxi6ILE1lLJg0/edit -->
﻿________________


title: NEXUS AI-OS - Betriebshandbuch (User Manual) version: v0.1.0 status: ENTWURF date: 2026-10-26 gate: PENDING (Human Gate ID-01)
NEXUS AI-OS - System- und Betriebshandbuch
1. Systemarchitektur (4-Layer Semantic Wiki)
Das NEXUS AI-OS basiert auf einer lokalfokussierten, deterministischen Architektur. LLMs dienen als Orchestratoren und Parser; die Berechnungshoheit (Solver Authority) liegt zwingend bei lokalen Python-Kernen.
2. Speicher- und Ordnerhierarchie (Routing)
2.1 WORK-Ordner (Staging / Ausführung)
* Zweck: Temporärer Ausführungsbereich für aktive Agenten, Dispatcher und offene Work Orders (WO).
* Inhalt: _FRONTMATTER.md Vorlagen, aktive Tickets (Status 0-2), temporäre Logfiles der laufenden Python-Skripte.
* Regel: Sobald ein Task den Status 3 (umgesetzt_und_validiert) erreicht oder abgebrochen (rejected) wird, verlässt er den Work-Ordner.
2.2 GitHub Repositories (nexus-platform / SSOT)
* Zweck: Single Source of Truth (SSOT), Versionierung, Austausch mit Entwicklern/externen Instanzen.
* Inhalt:
   * Steuerdateien (z.B. _AGBs.md, NEXUS Manifest)
   * Python-Rechenkerne und Watchdog-Skripte
   * Abgeschlossene AIM-Register (ab Status 3)
   * Dieses Betriebshandbuch
* Regel: Änderungen hier erfordern einen validierten Git-Commit (git add, git commit, git push).
2.3 Archiv & Artefakte (Google Drive / OneDrive)
* Zweck: Langzeitspeicher für Binärdaten und projektbezogene Ausgaben.
* Inhalt: Generierte PDFs, IFC/DXF-Modelle, Bilder, umfangreiche Datensätze, statische Backups.
3. Systemverhalten & Rekursive Tasks
* Watchdog-Prozess: Ein Python-Skript überwacht den Work-Ordner auf neue Dateien, parst das Frontmatter und triggert den relevanten Agenten.
* Fehler-Rekursion (DELTA-Refinement): Wenn ein Solver einen Syntaxfehler im LLM-Output erkennt, wird das Logfile (Error-Report) in den Work-Ordner geschrieben und das LLM automatisch zu einer erneuten Iteration (Roundtrip) gezwungen.
4. Protokollierung & Reporting
* Laufzeit-Logs: Werden vom Python logging-Modul generiert (Timestamp, Agent-ID, Task-ID, Error-Codes).
* Zustands-Logs (History): Jede konzeptionelle Änderung wird als Delta im Markdown-Dokument (unten angehängt) mit Referenz auf den Vorgänger-Snapshot dokumentiert.