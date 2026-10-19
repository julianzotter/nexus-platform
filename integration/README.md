# Registry → Dashboard integration (review candidate)

Contract: `nexus-registry-dashboard/1.0.0`, JSON Schema Draft 2020-12.
Producer: `tools/export_dashboard.py`. Consumer: the `integration/` reader in
[NEXUS dashboard](https://github.com/julianzotter/NEXUS-AI-ECOSYSTEM-LOOP_3D-STUDIO-VISUALS-DASHBOARD-).
The contract module and schema must remain byte-identical in both repositories;
an incompatible change requires a new contract version and coordinated PRs.

## Data mapping

| Platform input | Export / graph | Semantics |
|---|---|---|
| `registry/knowledge/*.json` | `knowledge[].record` / `nodes[].record` | Original record, stable ID and status preserved |
| `knowledge_health.assess_item` | `knowledge[].health` / `nodes[].health` | Schema/reference/sign-off metadata assessment only |
| `registry/file-registry.jsonl` | Input hash and source ID checks | File reference presence, not authenticated original source |
| `reports/monitor/report.json` | `monitor` | Original check states, observation time, commit, run and attempt; no stdout/stderr |
| Export execution | `generated_at`, source file SHA-256 | Distinct from monitor observation; no live runtime or approval claim |
| No relationship registry | `edges: []` | No invented graph relationships |

## Use

In a complete platform checkout, install `jsonschema`, then:

```powershell
python tools/export_dashboard.py --revision <checked-out-40-character-commit>
# With an existing monitor report from exactly that revision:
python tools/export_dashboard.py --revision <commit> --monitor reports/monitor/report.json
```

After merge, the existing Monitor workflow creates
`reports/monitor/dashboard-snapshot.json` in its ordinary run artifact, even after
a failing check if valid input can still be exported. No schedule or credentials
are added. Malformed records or a mismatched monitor revision fail export; the
original monitor report is retained. CI success is not an engineering release.

Download the artifact through an authenticated GitHub session, extract the JSON
locally, and pass its path to the dashboard reader. There is no automatic transfer,
cross-repository secret, remote fetch, Drive writeback or bidirectional sync.
Only share the snapshot with recipients allowed to read its source records.

## Acceptance / remaining gates

- Unit tests cover roundtrip, input hashes, broken references, missing inputs,
  duplicate IDs, unknown versions, timezone and mismatched monitor revision.
- Contract and production release remain pending independent software,
  governance and systems reviews, consolidation, delta correction/re-review,
  and explicit human decision as required by `AGENTS.md`.
- WORK context read: `11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH`, policy 0.4.0-pilot.
  Its external-integration/release block remains in effect.
- This adapter is a read-only review implementation. It does not authenticate
  an existing sign-off, verify norm conformity, calculate structural results or
  remediate demonstration claims in legacy dashboards/backends.
