# NEXUS · AEC Control Panel (v8, versioniert)

Status: ENTWURF · Branch `claude/project-thread-kiyti8` · keine Freigabe (Human Gate ID01).

## Herkunft

| Ordner | Quelle | SHA-256 Archiv |
|---|---|---|
| `site/` | `backups/control-panel/26_11_25_0012_ID05_PANEL_SITE_V8.tar.gz` (`dist/`) | `b606c262…b4a2dc` |
| `workorder-api/` | `backups/control-panel/26_11_25_0012_ID05_WORKORDER_ENDPOINT_V1.tar.gz` (`dist/`) | `b076b34b…b340c` |
| `data/control-data.base.json` | `dist/control-data.json` aus v8, unverändert (manuelle Abschnitte) | – |

Änderungen gegenüber dem Archiv (nur `site/`):
- `app.js`: neue Ansicht `#registry` (NEXUS-Registry), akzeptiert `schemaVersion` 4.1.0 **und** 4.2.0.
- `index.html`: Navigationslink „NEXUS-Registry“.

## Build

```sh
python tools/build_control_data.py --source-commit "$(git rev-parse HEAD)"
# -> apps/control-panel/dist/ (site + control-data.json + .sha256), gitignored
```

- Deterministisch: `asOf` = Commit-Zeit, keine Wall-Clock-Felder → gleicher Commit = gleiche Bytes.
- Validierung: `schemas/control-data.schema.json` (Draft 2020-12), fail-closed.
- CI: `.github/workflows/nexus-monitor.yml` baut nach `export_dashboard.py`, Artefakt `nexus-monitor-<run>` enthält `apps/control-panel/dist/`.
- Test: `tests/test_build_control_data.py`.

| Abschnitt | Quelle | Art |
|---|---|---|
| `roles` | `registry/roles/role_capability_matrix.json` | generiert (ersetzt manuelle v8-Rollen) |
| `nexus.workflows` | `orchestrator/registry/workflow-registry.json` (17 WF) | generiert |
| `nexus.skills` | `skills/**/SKILL.md` via `tools/skill_inventory.py` | generiert |
| `nexus.ledger` | `governance/work-snapshot/00_ID_LEDGER.csv` (Snapshot 2026-11-16) | generiert |
| `nexus.reportFiles` | `reports/**`, `WORK/REPORTS/**` gegen Namensregel + ID-Ledger | generiert |
| `nexus.monitor` | `reports/monitor/nexus.snapshot.json` via `tools/export_dashboard.py` | generiert, sonst `NO_DATA` |
| projects, orders, architecture, moe, chatTasks, computerJobs, navigation, reports, policy, links | `data/control-data.base.json` | manuell |

## Annahmen (zu bestätigen)

- A1: Rollen-Badge-Abbildung `ACTIVE→ACTIVE`, `OPTIONAL→AVAILABLE`, `INACTIVE→UNASSIGNED`, `ID01→OWNER`.
- A2: Deployment bleibt manuell (ChatGPT Sites, `hosting.json` erwartet `static.directory: dist`).
- A3: Ledger-Spiegel ist Stand 2026-11-16; aktuelles Ledger liegt im Drive (`LLM-LOCAL-SSOT`) und wird nicht live gelesen.
- `monitor.js`, `team.js` sind im Archiv enthalten, werden von `index.html` aber nicht geladen (Altbestand, unverändert übernommen).

## Vorschlag: Konsolidierung der Dashboards (4 + ID03-Draft)

| Dashboard | Ort | Zweck | Vorschlag |
|---|---|---|---|
| Control Panel v8 | `apps/control-panel/` (ChatGPT Sites) | öffentliche/private Statusansicht | **Kanonisch**: einzige Anzeige-Oberfläche |
| Control Tower | `local_stack/nexus_local/control_tower.py` (127.0.0.1:8770) | lokaler Task-Manager mit Mutationen (Token) | bleibt als **lokales Schreib-Backend**; liest/schreibt dieselbe `control-data`-Struktur, eigene UI → Panel-Ansicht |
| nexus-tower | `tools/nexus-tower/` (127.0.0.1:8765, ENTWURF) | WORK-Ordner-Status + MCP (read-only) | MCP-Tools `work_state`, `naming_check`, `gate_status` in den Control Tower übernehmen, Ordner danach archivieren |
| Control-Panel-Draft v1.x (ID03) | `prototypes/nexus-control-tower-draft-v1/` (seit 2026-11-25 auf main) | read-only Knowledge-/WORK-Monitoring, Same-Origin-Refresh | Refresh-/Stale-Guards als Panel-Ansicht übernehmen; danach archivieren (Abstimmung mit ID03) |
| Daten-Dashboard | `prototypes/data-dashboard/` | Prototyp KPI/Diagramme | KPI-/Chart-Bausteine als Panel-Ansicht übernehmen, Prototyp archivieren |

Zielbild: **1 Datenvertrag** (`schemas/control-data.schema.json`) · **1 Generator** (`tools/build_control_data.py`) · **1 Anzeige** (Panel) · **1 lokales Backend** (Control Tower inkl. MCP).
