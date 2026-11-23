---
name: ft-beam-cad-drawing
description: Generate auditable 2D CAD tender/construction drawing candidates for P205 Eisteiche precast/half-precast concrete beams from approved FT-Matrix semantics plus plan geometry. Produces DXF + vector PDF/PS + manifest, with strict source/hash/readback gates. Use for FT-Träger-Matrix → Schalungs-/Bewehrungsschema, not for structural calculation.
---

# FT beam CAD drawing

Status: candidate skill. Engineering release is never implied.

## Purpose
Create deterministic 2D drawing candidates for P205 / Schule an den Eisteichen:
- precast or half-precast beam + in-situ concrete zone;
- openings and corbels;
- Pos.1–5 reinforcement labels/geometry when resolved;
- dimensions, QA labels and bill-of-bars summary;
- DXF plus vector PDF/PS plot.

## Authority split
- Excel / approved project sources: design semantics.
- TWP/DXF/IFC or approved plan geometry: exact beam outline/corbels/opening geometry.
- This skill: drawing adapter only.
- It MUST NOT calculate EC2 resistance or invent missing reinforcement geometry.

## Source gate
Do not select "latest" by filename.
A production drawing run requires:
1. explicit workbook/file ID and SHA-256;
2. source status = REVIEWED or FILE_VERIFIED;
3. exact sheet/beam identity;
4. plan geometry source for exact outline/corbels;
5. no unresolved P0 source conflict for the element.

If exact geometry is missing, only `SCHEMATIC` mode is permitted and the plot must be watermarked.

Known P205 status 2026-11-23:
- RevF is a repair candidate, NOT a released workbook.
- RevE / Vers-D / Vers-D_jz are stable comparison baselines but contain known open defects.
- Therefore project-wide production batch export is BLOCKED until an approved recalculated workbook is frozen.

## Workflow
1. `extract_matrix.py`: read cached matrix semantics only, with expected workbook SHA.
2. Join matrix semantics with approved TWP/DXF/IFC geometry into a drawing spec.
3. `ft_beam_cad.py`: generate DXF + PDF/PS + manifest.
4. Re-open DXF and run entity/layer/count checks.
5. Compare key dimensions/opening stations to the drawing spec.
6. Human CAD/structural review.
7. Batch rollout only after one representative beam PASS.

## Default layers
- FT_RAHMEN
- FT_SCHALUNG
- FT_KONSOLE
- FT_DURCHBRUCH
- FT_BEW_POS1
- FT_BEW_POS2
- FT_BEW_POS3
- FT_BEW_POS4
- FT_BEW_POS5
- FT_BEMASSUNG
- FT_TEXT
- FT_QA

## CLI
```bash
python scripts/extract_matrix.py workbook.xlsx --sheet 4OG-2 --expected-sha256 <sha> --out 4OG-2.matrix.json
python scripts/ft_beam_cad.py 4OG-2.drawing.json --out RELEASES/4OG-2 --paper A3 --formats dxf,pdf,ps
python -m unittest discover -s tests -p "test_*.py" -v
```

## P205 mapping currently evidenced
Result-sheet rows used by the existing real generator:
- station: row 10
- beam b/h: rows 16/17
- opening b/h/hu: rows 19/20/21
- Pos.1–5: rows 161/163/165/167/169
- η: row 252

These are source mappings, not normative rules. Keep them versioned in the source-map output.

## Drawing levels
- SCHEMATIC: matrix-only representation; no claim of fabrication geometry.
- TENDER: approved outline + openings + labels + quantities; reinforcement may remain symbolic.
- REBAR_DETAIL: requires resolved bar geometry, anchorage/hooks and approved cover. Fail closed otherwise.

## QA
Every run writes `manifest.json` with source IDs/hashes, generator version, output hashes and mode.
Never suppress unresolved issues; write them to the QA layer and manifest.
