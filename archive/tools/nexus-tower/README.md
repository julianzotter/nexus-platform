# nexus-tower (review snapshot, status ENTWURF)

Local, read-only NEXUS Control Tower. One Python file, standard library only.

- `nexus_tower.py` serves a status page for the WORK folder on `http://localhost:8765`
  and a local MCP endpoint on `http://localhost:8765/mcp` (JSON-RPC over HTTP POST).
- `nexus_tower_start.bat` starts it on Windows by double-click.
- It reads file names, modification times, sizes and the header of the newest ID03
  status report. It writes nothing and binds to 127.0.0.1 only.

MCP tools (all read-only): `work_state`, `naming_check`, `gate_status`.

`naming_check` applies the file rule of `_AGBS.md` v005 (`YY_MM_DD_HHMM_ID##_THEMA_###`).
`AGENTS.md` item 4 and `governance/current/_AGBS.md` now state the same order.
CI applies the same check to files added in a pull request via `tools/naming_gate.py`
(plus a role-ID check against `registry/roles/role_capability_matrix.json`).

Relation to existing code: `mcp_bridge/nexus_mcp_server.py` is a stdio MCP bridge with
a gated write tool. This tool is HTTP, read-only and adds the naming check and the page.

Tested: `tests/test_nexus_tower.py` (name rule, MCP dispatch, HTTP round trip on Linux).
Not tested: Windows, the Google Drive mount, a real MCP client.
