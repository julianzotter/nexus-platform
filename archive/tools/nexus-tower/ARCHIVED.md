# ARCHIVIERT 2026-11-26 (ID01-Entscheidung, Dashboard-Konsolidierung Schritt 1)

Nicht mehr verwenden. Nachfolger:

| Alt (nexus_tower.py, Port 8765) | Neu |
|---|---|
| `name_check()` | `local_stack/nexus_local/naming.py::name_check` (unverändert, Urteile identisch) |
| MCP `naming_check` | MCP-Gateway `127.0.0.1:8766/mcp`, Tool `naming_check` (optional `subdir`) |
| MCP `gate_status` | MCP-Gateway, Tool `gate_status` (optional `subdir`) |
| MCP `work_state` | MCP-Gateway, Tool `work_list` (bestehend, neueste zuerst) |
| HTML-Seite :8765 | Control Panel `apps/control-panel/` (Ansicht NEXUS-Registry · Report-Dateien) + Control Tower :8770 |
| CI-Namensprüfung | `tools/naming_gate.py` importiert jetzt `naming.py` |

Start des Nachfolgers: `local_stack` (Start-NexusLocal.cmd), siehe `local_stack/README.md`.
Der Code bleibt hier unverändert zur Nachvollziehbarkeit (Stand v0.2.1).
