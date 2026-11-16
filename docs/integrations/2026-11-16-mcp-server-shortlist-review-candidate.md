---
name: mcp-server-shortlist-review-candidate
description: Bewertung der Server aus dem MCP-Verzeichnis github.com/mcp für NEXUS; Abgleich PR #69 (model-effort-router); Drive-Skript-Hinweise
version: 0.1.0
status: REVIEW_CANDIDATE – keine Aktivierung, keine Installation
timestamp: 2026-11-16T22:05+01:00
---

# MCP-Shortlist für NEXUS (Review-Kandidat)

Executor: Claude (claude.ai-Session), Modell Claude Opus 5.5. Die Rollen-ID in NEXUS-ROLES ist für diese Instanz nicht zugeordnet (UNKNOWN).
Governance gelesen: WORK `Folder.md` (status_checked_at 2026-11-12). Dort sind externe Integration und Human Release BLOCKED. Dieses Dokument aktiviert deshalb nichts.

## 1. Abgleich PR #69 – `skills/model-effort-router/SKILL.md`
- PR #69 ist seit **2026-11-12 20:49 UTC gemergt** (Merge-Commit `ab63ca1`).
- Die Statusmeldung im Chat („Konfliktauflösung nicht durchgeführt“) ist damit **veraltet**.
- Was in `main` umgesetzt ist (geprüft an Commit `c7aeccb`):
  - Das Frontmatter enthält nur `name` und `description`.
  - Version, Status, Owner und Runtime stehen im Dokumentkörper.
  - Der Acceptance-Gate ist verpflichtend, `EXEC != PEERREVIEW` ist geregelt.
  - Die drei Worked Examples sind enthalten, alle mit `applied: NOT APPLIED`.
  - Die Snapshot-Werte sind als historisch markiert; die offiziellen Quellen wurden am 2026-11-12 geprüft.
- **Offen** (laut Promotion-Checkliste der Datei):
  - Skill-Validierung und CI-Belege zum aktuellen Head
  - unabhängiges Review mit Hash
  - Freigabe der Aktivierung durch ID01
- **Status bleibt v0.2.0 / ENTWURF. Keine Änderung nötig.**

## 2. Bestand (vor jeder Neuaufnahme)
| Server | Fundort | Status |
|---|---|---|
| `nexus-bridge` (eigen) | `mcp_bridge/mcp.local.example.json` | vorhanden; Schreiben nur mit `NEXUS_MCP_WRITE=1` |
| GitHub (offiziell, HTTP) | `mcp_bridge/mcp.local.example.json` | vorhanden |
| Context7 | `docs/dashboards/google-ai-stack-serie/mcp_config.json` | vorhanden (Antigravity) |
| Notion, Google Drive, Gmail u. a. | claude.ai-Konnektoren | bereits verbunden, keine lokale MCP-Instanz nötig |

## 3. Bewertung der Liste (github.com/mcp, Screenshot 2026-11-16)
Kriterien:
- Nutzen für NEXUS (Ingestion, Test, Registry, Code)
- Datenabfluss nach außen
- Schreibrechte
- Konflikt mit den Regeln R1 (nichts löschen), „Drive = SSOT“ und Source-Governance

| Prio | Server | NEXUS-Nutzen | Risiko / Auflage | Empfehlung |
|---|---|---|---|---|
| P1 | **MarkItDown** (microsoft, `markitdown-mcp`, pip) | PDF/DOCX/XLSX → Markdown für `knowledge-ingestion` und für Normen und Statiken | Ein Tool `convert_to_markdown(uri)` akzeptiert auch `http(s):` → Egress möglich. Nur `file:`-URIs aus freigegebenen Ordnern zulassen; vorher Klassifizierung über `source-governance` | **Pilot** |
| P1 | **Playwright** (microsoft, `@playwright/mcp`) | E2E-Tests der Standalone-Dashboards (Selbsttest-Muster wie CASEFLOW `?selftest=1`) | Browser mit Netzzugriff. Nur localhost oder eigene Artefakte, Isolated Profile | **Pilot** |
| P1 | GitHub | Repository-, Issue- und PR-Workflows | bereits im Bestand | behalten |
| P1 | Context7 | aktuelle Library-Dokumentation | bereits im Bestand | behalten |
| P2 | **DBHub** (bytebase, `@bytebase/dbhub`) | SQLite-Lesezugriff auf `AnythingSearch.db` / Registry statt Ad-hoc-Skripten | nur `--readonly`, `--max-rows`, SQLite-Datei lokal; kein Produktions-DSN | Pilot nach P1 |
| P2 | Serena (oraios) | semantische Code-Navigation im großen `nexus-platform`-Repo | Schreib- und Edit-Tools vorhanden → nur Leseprofil | optional |
| P3 | draw.io (jgraph) | Architekturdiagramme aus Mermaid | gering | bei Bedarf |
| – | Tavily, Firecrawl, Brightdata, Apify, Skyvern | Webrecherche und Scraping | externe Datenflüsse und Kosten; die Websuche der Hosts deckt den Bedarf | nicht jetzt |
| – | Desktop Commander | Shell und Dateisystem | widerspricht R1 (Löschen) und Writer-Kontrolle; Bridge-Policy greift nicht | **ablehnen** |
| – | Basic Memory, Memanto | zweites Wissens- und Memory-System | widerspricht „Drive = SSOT“ und „eine AIM-Liste“ | **ablehnen** |
| – | Supabase, Azure, Fabric | – | nicht im Stack | nein |
| – | Netdata, Unity, Figma, JobSpy, Solana, Korean Law, kordoc, Omnara, jCodeMunch (Lizenz), Applama | kein Bezug zu NEXUS | – | nein |

Popularitätszahlen aus dem Verzeichnis (Sterne) sind kein Eignungsnachweis.

## 4. Pilotplan (eine Scheibe, messbar)
1. **MarkItDown:** Konvertierung von 3 freigegebenen PDFs (1 Norm-Auszug, 1 Statik, 1 Scan).
   - Akzeptanz: Text vorhanden, Tabellen lesbar, Scan als „leer/OCR nötig“ erkannt, kein `http`-Aufruf im Log.
2. **Playwright:** CASEFLOW `index.html?selftest=1` lokal starten.
   - Akzeptanz: T1–T9 = PASS, über das MCP-Tool ausgelesen.
3. **DBHub:** `--readonly` auf einer Kopie von `AnythingSearch.db`.
   - Akzeptanz: ein `SELECT` liefert ein Ergebnis, ein `DELETE` wird abgewiesen.
4. **Freigabe:** Ergebnisse als WORK-Report. Danach drei Review-Perspektiven gemäß AGENTS.md §8, dann die Entscheidung von ID01.

Konfigurationsvorlage (deaktiviert, mit Platzhaltern): `mcp_bridge/mcp.candidates.example.json`.
Versionen werden beim Pilot fest gepinnt. Bis dahin sind sie UNVERIFIED.

## 5. Drive-/PowerShell-Hinweise (aus Chat) – Abgleich
| Hinweis | Bestand NEXUS | Aktion |
|---|---|---|
| Google Drive for Desktop, Laufwerk `G:\Meine Ablage` | genutzt (`NEXUS_WORK_ROOT`, `sync_nexus.ps1`) | keine |
| Execution Policy `RemoteSigned` global | `install_autosync.ps1` nutzt `-ExecutionPolicy Bypass` je Prozess | global nicht ändern; der Prozess-Scope ist enger |
| Ordner „Offline verfügbar“ | nicht dokumentiert | Empfehlung: `WORK` und `mcp_bridge` offline halten, damit die Bridge nicht auf den Cloud-Sync wartet |
| Keys nie in `.ps1` | GitHub-Secrets und `${ENV}` werden bereits genutzt | keine |
| Skriptordner in PATH | nicht nötig; die Bridge wird über die absoluten Pfade in der MCP-Konfiguration gestartet | keine |

## 6. Bekannte Blocker (aus Folder.md, unverändert)
- WORK hat weiterhin `anyone: writer`. Die Entfernung ist von ID01 freigegeben, aber noch nicht umgesetzt.
- Ein neuer MCP-Server mit Schreibrechten verschärft das Problem. Deshalb gilt bis zur Behebung: nur Lesemodus.
