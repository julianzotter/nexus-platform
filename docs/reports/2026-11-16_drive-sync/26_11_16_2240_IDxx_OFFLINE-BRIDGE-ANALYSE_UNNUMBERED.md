---
name: offline-bridge-analyse
description: Analyse "Available offline" für NEXUS-Bridge-Ordner, Drive-MCP-Status, Governance-Dateiformat-Blocker; Prüfskript
version: 1.0
status: ANALYSE_COMPLETE – Offline-Setzung manuell durch ID01 (kein API-Weg, PC nicht verbunden)
timestamp: 2026-11-16T22:40+01:00
---
# Offline-Einstellungen + Bridge-Verhalten (2026-11-16 22:40)

## Befunde
| # | Befund | Beleg | Wirkung |
|---|---|---|---|
| O1 | „Available offline“ ist eine lokale Einstellung von Google Drive for desktop (Stream-Modus); kein Drive-API-/MCP-Endpunkt setzt sie | Drive-Connector-Tools: create/update/move/share/download, keine Offline-Option | nur manuell oder per Computer-Use am PC |
| O2 | `mcp_bridge` läuft aus dem lokalen Repo `C:\Users\<USER>\nexus-platform\mcp_bridge` (mcp.local.example.json); der Drive-Ordner `mcp_bridge` (1uTf…) ist nur Spiegel | Bridge-Config | Offline-Markierung von `mcp_bridge` in Drive bringt nichts |
| O3 | **Manifest + Baseline sind Google Docs** (`00_NEXUS_MANIFEST__CURRENT__2026-09-28`, `00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28`); die Bridge erwartet `.md`-Dateien unter `LLM-LOCAL-SSOT` | NEXUS_GOVERNANCE_FILES_JSON; Drive-Suche | Lokal nur `.gdoc`-Zeiger → Policy-Check = MISSING → Bridge-Writes BLOCKED (AGENTS §11), **unabhängig von Offline** |
| O4 | `_AGBS.md` 6× vorhanden: kanonisch `WORK/_AGBS.md` (MD, 9,4 kB, 11.11.); 4 Google Docs „_AGBS.md“ im Root (18.10.), 1 MD-Spiegel (1,5 kB, 01.11.) | Drive-Suche | Verwechslungsgefahr für Agenten |
| O5 | `LLM-LOCAL-SSOT` doppelt: kanonisch `_developement/LLM-LOCAL-SSOT` (1j3F…), zweiter im Root (1hMh…, enthält `INDEX_LNK_BENCHMARK`) | Drive-Suche | Agenten können falschen Ordner beschreiben |
| O6 | WORK weiterhin `anyone: writer` (live geprüft 22:3x) | get_file_permissions | Connector kann Rollen nur erhöhen (share_file), nicht entfernen → manuell |
| O7 | Google-Drive-MCP ist bereits verbunden (Lesen + Schreiben: Dateien anlegen, verschieben, umbenennen, freigeben, herunterladen); kein Löschen von Berechtigungen, keine Offline-Steuerung | diese Session | kein zusätzlicher Connect nötig |

## Empfohlene Offline-Ordner (G:\Meine Ablage\_developement\…)
| Ordner | Offline | Grund |
|---|---|---|
| `LLM-LOCAL-SSOT` (inkl. WORK) | JA | Bridge liest `_AGBS.md`, `Folder.md`, Manifest/Baseline vor jedem Write |
| `MCP-ACCESS-TOOLS` | JA | lokale Starter `.bat`/`.py` (nexus_tower, nexus_catalog_sync, nexus_ssot_mcp) |
| `mcp_bridge` (Drive-Spiegel) | nein | Bridge läuft von C: |

## Prüfung (binär)
Skript `26_11_16_2235_IDxx_DRIVE-OFFLINE-CHECK_UNNUMBERED.ps1` (in MCP-ACCESS-TOOLS): Leselatenz Governance-Dateien < 200 ms + Netz-aus-Test → PASS. Erwartung heute: FAIL bei Manifest/Baseline (O3) bis zur MD-Umstellung.

## Entscheidungen ID01
- E-O3: Manifest + Baseline als `.md` führen (Google Doc wird Archiv) – sonst bleibt die Bridge blockiert.
- E-O4/O5: Root-Duplikate `_AGBS.md` (4 GDocs) und Root-`LLM-LOCAL-SSOT` umbenennen mit Präfix `_DUPLICATE_` (move-only).
- E-O6: WORK „Allgemeiner Zugriff“ → Eingeschränkt (Drive-Weboberfläche).
