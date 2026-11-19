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

## Windows capability preflight (strictly non-mutating)

On the Windows RFEM host, in the NEXUS repository and its intended Python runtime:

```powershell
python rfem_parametric/preflight.py --out rfem_preflight_001.json
python -m unittest discover -s rfem_parametric -p "test_*.py" -v
```

The report lists installed `comtypes`/`dlubal.api` package versions and whether
`DEEPSEEK_API_KEY` is present **in that Python process**. It never opens `.dsh`
credentials, prints a key, launches RFEM, probes COM/gRPC, calls an API or runs
the solver. Reuse DSH's existing authenticated launcher, which must pass the
credential into the NEXUS child process without writing it to a project file.

Real connection proof remains a separate Windows-only gate: RFEM5 COM ProgID,
license lock and explicit model readback; RFEM6 API-II server, SDK/build match,
API entitlement, explicit model-id readback. Before any new-model write, a
unique name must be verified against `get_model_list()` and returned object IDs
must be checked by `get_object_list()`. The live writer currently fails closed.

## Windows Gate 2: explicit read-only connection tests

After refreshing this draft branch in an isolated Windows worktree, open the
installed RFEM program and use the intended Python interpreter.

```powershell
powershell -ExecutionPolicy Bypass -File .\rfem_parametric\Run-NexusRfemGates.ps1 `
  -PythonExe python -OutputDir .\rfem_gate_run_001 -DeepSeekAuth -RFEM5Attach
```

DeepSeek authentication requires `DEEPSEEK_API_KEY` already in the process
environment; the existing authorized DSH launcher must supply it. No `.dsh`
file is read. RFEM5 probes only attachment to an already running COM server;
the license and any actual model readback remain a separate gate.

```powershell
powershell -ExecutionPolicy Bypass -File .\rfem_parametric\Run-NexusRfemGates.ps1 `
  -PythonExe python -OutputDir .\rfem_gate_run_002 `
  -RFEM6ModelName "EXACT_OPEN_MODEL_NAME" -ApprovedSpecJson .\W012_approved.json
```

RFEM6 requires an already running API-II server and matching `dlubal.api` SDK.
The readback resolves a unique model name to its `ModelId.guid` and compares
node coordinates and member line topology to the approved JSON. Its reports
separate `BLOCKED` from `MISMATCH` and `PASS_GEOMETRY`. Load, support and design
checks are excluded. No create, update, save, delete or solve calls are made.

To preflight a proposed isolated new model name without creating or reserving it:

```powershell
powershell -ExecutionPolicy Bypass -File .\rfem_parametric\Run-NexusRfemGates.ps1 `
  -PythonExe python -OutputDir .\rfem_gate_run_003 `
  -RFEM6NewCandidate "NEXUS_W012_TEST_001"
```

`NAME_AVAILABLE_NOT_RESERVED` is **not** a guarantee against a later race;
creation remains fail-closed, with a fresh uniqueness check required immediately
before any separately authorized API write.
