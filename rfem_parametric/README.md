# W012 Eibengasse Hoftrakt — parametric RFEM pilot (draft)

Status: REVIEW_CANDIDATE / GEOMETRY_ONLY / NO_SOLVER / NO_RFEM_LIVE_READBACK.
Authoritative project geometry, material and section nomenclature are not supplied.
The package does not establish a calculation model suitable for engineering release.

## Existing NEXUS infrastructure

- RFEM 5: Existing Windows COM bridge with `RFEM5.Application` and `LockLicense()`. This
  pilot exports a neutral RFEM5 transfer preview. It **does not invoke COM write methods**.
- RFEM 6: Reuse Dlubal API II (`dlubal.api`) and existing NEXUS RFEM6 MCP bridge.
  `targets.rfem6_objects` produces documented API-II objects. A separate
  `rfem6_new_model` function accepts only an isolated `NEXUS_W012_TEST_*` model
  name; it is never called from the CLI.
- RFEM version, license/API key, working-copy destination and SDK minor must be
  verified **on the Windows machine** before a live model can be generated.

## Parameters (SI units)

Provide a JSON file, with exact project-approved values and verified RFEM catalog
names for `material`, `section_columns` and `section_beams`:

```json
{
  "project": "W012_EIBENGASSE_HOFTRAKT",
  "spans_x_m": [3.0, 4.0],
  "spans_y_m": [5.0],
  "storeys_m": [3.0, 3.0],
  "material": "TEST_MATERIAL",
  "section_columns": "TEST_COLUMN",
  "section_beams": "TEST_BEAM"
}
```

The numerical example above is **SYNTHETIC_TEST_DATA**, not W012 design input.
Do not use it for an RFEM model of the real building.

## Dry-run

```powershell
python rfem_parametric/cli.py W012_parameters.json --target rfem5
python rfem_parametric/cli.py W012_parameters.json --target rfem6
python -m unittest discover -s rfem_parametric -p "test_*.py" -v
```

The CLI only prints a numbered geometry/adapter-preview JSON and SHA-256.
It does **not** connect to RFEM, save files, modify loaded models, add supports,
define actions or load combinations, or call a solver. Tests use mock Dlubal objects.
No default structural model or support restraint is inferred.

## Human gates

1. Verify architectural grid, levels, axes, storey and material specifications for W012.
2. Independent geometry/topology peer review; freeze parameters and hash.
3. On a **new RFEM working copy**, verify versions, COM/API availability,
   materials, sections, supports and load cases in the real application.
4. Only after separately authorized real API-write tests add RFEM5 COM writing and
   RFEM6 model transfer; read back node/member counts and actual native file hash.
5. Calculate/design only upon additional explicit engineering approval.

## Primary documentation

- https://apidocs.dlubal.com/quick_start.html
- https://apidocs.dlubal.com/installation_python.html
- https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001921
- Existing NEXUS: `plugins/nexus-aec-engineering/skills/rfem6-mcp-engineering/`.
# JSON audit receipt: --out creates a NEW file, never replaces an existing one.
# Example: python rfem_parametric/cli.py validated_w012.json --target rfem6 --out w012_rfem6_dryrun.json
# Prompt -> DeepSeek proposal -> human input verification -> FrameSpec JSON -> offline Python -> RFEM preview JSON.
# AI-generated dimensions or engineering inputs are NOT accepted as verified project evidence.
