---
name: rfem6-mcp-engineering
description: Orchestrate RFEM 6 through discovered local Dlubal MCP or gRPC capabilities. Use for setup, read-only model audits, node/member/cable/load changes, nonlinear calculations, result extraction, RFEM5-to-6 migration and Seilstatik Böblingen. Preserve source identity, working copies and human engineering release.
---
# RFEM 6 MCP Engineering

## Contract
Input: task, authoritative model locator/hash, project scope, coordinate system,
units, available tool schemas and authorized change scope.
Output: runtime manifest, model snapshot, bounded changes/results, QA findings,
evidence files and explicit status. Use SI internally; record display conversions.
Do not claim normative compliance from a solver run alone.

## Execute
1. Discover actual Dlubal tools and schemas. Read [runtime-setup.md](references/runtime-setup.md)
   before setup. No exposed local tool means PRECHECK_BLOCKED: report and stop RFEM work.
   Never probe cloud/Colab localhost as though it were the user's RFEM workstation.
2. Identify RFEM/API/MCP versions, transport, model ID/path, source file hash,
   fingerprint, axes, units, calculation state and capabilities. Health/TCP success
   is transport evidence only. Do not assume tool names or parameter signatures.
3. Run G0 first: read geometry, connectivity, supports, materials, sections,
   prestress, load cases/combinations and existing results. No calculation/save.
4. For RFEM5 sources, audit RFEM6 import against frozen reference: add-ons,
   nonlinearity, form finding, releases and combinations. Load
   [boeblingen.md](references/boeblingen.md) only for that project.
5. Classify the delta before execution:
   - G0: read only, no calculation or model save.
   - G1: authorized coordinates/loads/parameters and calculation on a verified
     working copy; capture before/after and read back every change.
   - G2: topology, node/member creation/deletion, support/system concept changes:
     require the engineer's explicit decision for the concrete delta.
   - G3: canonical source overwrite/promotion: explicit authorization plus
     immutable predecessor and full hash.
   - G4: engineering, order or installation release: human sign-off only.
6. Execute only the authorized delta. Prefer typed tools; use a reviewed bounded
   script only when necessary. Do not silently enable arbitrary script tools.
   Log outcomes and readbacks without secrets. Verify native RFEM6 save format.
7. Bind results to exact model state/calculation/combination. Record convergence,
   units, sign convention and raw-response hash. Reject stale/nonfinite results.
   Run [validate_result.py](scripts/validate_result.py) on normalized envelopes;
   PASS proves envelope consistency only, not RFEM truth or structural adequacy.
8. Check force/moment equilibrium with documented absolute/relative tolerances,
   cable tension behavior, deformation limits and independent benchmark. Verify
   normative edition and national annex before any EC design check.
9. Save evidence using [audit-contract.md](references/audit-contract.md), with
   separate chronological log/current status. Report PRECHECK_PASS,
   PRECHECK_BLOCKED, BLOCKED or REVIEW_CANDIDATE accurately. End engineering
   output with FINAL_RELEASE = HUMAN_SIGNOFF_REQUIRED.

## Stop conditions
Stop dependent writes/calculation on ambiguous model/source identity, missing
inputs, unauthorized delta, unit mismatch, failed readback or nonconvergence.
Preserve findings; never replace them with mock PASS.
