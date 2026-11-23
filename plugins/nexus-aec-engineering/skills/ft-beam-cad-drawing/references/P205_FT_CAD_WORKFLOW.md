# P205 Eisteiche — FT beam CAD integration

## Current source status, 2026-11-23
There is no proven error-free released workbook.

- RevF, Drive `1BPpKIENzRPrCu0qhdn34YuErKzMZ8oyy`: latest repair candidate, 2,179 changed formulas; caches/results not consistently recalculated; open source/mapping defects remain.
- RevE, Drive `1oVj79Li7EiYxo2SnrvgtNGzbF3tmqbiQ`: stable comparison baseline; cell-identical to Vers-D / Vers-D_jz, but contains known defects.
- Dashboard v1.1, Drive `1eSOB7LU5rQKGJuCfIPevlKYjuXSecErb`: uses Vers-D/RevE-identical data; 3D, utilization, reports and references; not a released engineering result.
- Design Guide source: `DESIGN GUIDE — FT-BETONTRÄGER BEMESSUNGS (ABLAUFSCHEMA ALEX 26.02.2026)`, Drive `1O2JOE2tE8gOgw91wk6QFYePTXwKMYV2C`.

## Design Guide integration
Per result sheet / beam axis:
1. RFEM input link.
2. Correct BT resistance mapping.
3. Global L/S/F design status.
4. Opening block.
5. Pos.1–5 reinforcement selection/verification.
6. η and quantities.
7. QA/log/Human Gate.

The CAD adapter starts only after step 6 has a frozen source revision. It does not choose reinforcement.

## Data split
### Matrix semantics
- station;
- section b/h at opening;
- opening b/h/hu;
- Pos.1–5 strings;
- η;
- quantities and identifiers when verified.

### Plan geometry
Use TWP/DXF/IFC for:
- exact beam outline and depth changes;
- corbel geometry;
- support faces;
- opening orientation and exact spatial placement;
- plan title block and reference axes.

Do not reconstruct exact outline from matrix opening columns alone.

## Pilot drawing package
Pilot: one representative beam, preferably 4OG-2 because existing artifacts and checks exist.

A3 pilot contains:
- longitudinal formwork elevation;
- corbels/supports;
- openings with station/dimensions;
- one or more cross-sections;
- opening detail Pos.1–5;
- symbolic rebar where exact geometry is unresolved;
- QTO/BBS summary;
- source IDs/hash, workbook/sheet and QA state;
- watermark when not released.

## Batch rollout
After pilot PASS:
- enumerate approved EG, 1OG, 2OG, 3OG and 4OG result sheets;
- generate one drawing manifest per axis;
- aggregate plan index by floor;
- create PDF/PS plan set;
- preserve DXF as machine-readable source;
- compare output manifest against Excel overview quantities and LV/tender package.

## Tender package
Recommended package:
```
P205_FT_DRAWINGS/
  00_PLANINDEX/
  EG/
  1OG/
  2OG/
  3OG/
  4OG/
  DXF/
  PDF/
  PS/
  BBS/
  MANIFESTS/
```

Each plan references:
- workbook Drive ID/hash;
- sheet;
- TWP geometry source ID/revision;
- generator commit/SHA;
- drawing status;
- review/Human Gate.

## Release gate
Do not mark FOR CONSTRUCTION while:
- RevF or successor has not undergone native Excel full rebuild/readback;
- 32 missing force cells are unresolved;
- ambiguous BT mappings / local geometry conflicts are unresolved for the beam;
- required reinforcement geometry/anchorage is unresolved;
- cross-format drawing readback and human review are missing.
