# AI-CAD-FEM Reference Roadmap
State: REVIEW_REQUIRED

## Reuse first
1. `plugins/nexus-aec-engineering/skills/cad-statik-pipeline/`: neutral structural model, DXF/IFC/SAF/RF5/RF6, compare/fingerprint.
2. `plugins/nexus-aec-engineering/skills/rfem5-com/`: guarded RFEM5 COM bridge.
3. `rfem_parametric/`: SQE/W012 geometry-only pilot.
4. `usecases/P205-EISTEICHE-BT-WEST/`: P205 usecase mirror.
5. Drive DeepSeek 2026-08-28 archive: architecture/code seeds only.

## True runs
- RUN-01: preserve/classify/register knowledge.
- RUN-02: define `FT_BEAM_CANONICAL_MODEL`.
- RUN-03: P205 one-beam vertical slice Excel → JSON → DXF → IFC/GLB → readback.
- RUN-04: canonical/NSM → RFEM working-copy readback.
- RUN-05: SQE source freeze and geometry Golden Slice.
- RUN-06: FAVO250 source-authority map + usecase.
- RUN-07: CI/productization and Human Gate.

No LLM is calculation authority.
