# DeepSeek 2026-08-28 AI-CAD-FEM Reuse Catalog
State: REVIEW_REQUIRED

## KEEP
- architecture: source/Excel → canonical model → deterministic QA → CAD/BIM/FEM adapters;
- existing real FT Excel→DXF/PDF mapping;
- 224-opening regression candidate dataset;
- cad-statik-pipeline and rfem5-com;
- provenance/hash/readback/Human Gate.

## ADAPT
- `ft_beam_bim_connector.py`: split monolith; remove hardcodes.
- `three_js_ft_viewer.js`: viewer only, fed from canonical JSON.
- IFC prototype: correct spatial tree, void relationship, IfcReinforcingBar/Psets.
- QTO: derive from actual bar geometry/BBS.

## REJECT AS-IS
- `steelMass = volume * 120`;
- `mass_per_floor = total_steel * 0.4`;
- fixed Pos.1–5 geometry;
- keyword matching as source verification;
- unverified alpha_cc/NAD constants;
- unconditional production-ready claims.

Target: `contracts/ft-beam/`, adapters, qto, cad, bim, viewers, qa regression.
