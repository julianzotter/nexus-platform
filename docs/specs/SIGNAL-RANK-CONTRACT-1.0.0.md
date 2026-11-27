---
name: SIGNAL-RANK-CONTRACT-1.0.0
description: Frozen deterministic ranking, scale, tie-break and mandatory-union contract over the existing P205 signal-energy matrix and MoE router (issue #153, findings A1-A4)
version: 1.0.0
status: PROPOSED (not ADOPTED; needs ID03 spec acceptance, independent ID04/ID07 review, ID01 decision)
author: ID06 (Claude, claude-opus-5-5)
timestamp: 2026-11-27T10:30+01:00
implementation: tools/signal_rank.py
tests: tests/test_signal_rank.py, tests/golden/signal_rank_v1.json
schema: schemas/signal-matrix-entry.schema.json
governance: Baseline r3 gdrive:1pU3N_82s_6tkgEqQYdobHmyaYh8bu9cz (sha256 edd53ac1…), MUST-11/17/23/25/105/155
---
# Signal-Rank Contract 1.0.0

## 1 Single source (no second router SSOT)
| Element | Canonical source (unchanged) |
|---|---|
| Signals S01–S08 | `WORK/P205_FT/2026-11-23_ID02/26_11_23_1104_ID02_build_P205_FT_AUDIT_DB.py` → `SIGNALS` |
| Experts | same file → `EXPERTS` |
| Routes | same file → `ROUTES` |
| Formula, bands, router rules | `…_P205_FT-MOE-ROUTER_v1.0_LEDGER-PENDING.md` |
| Materialised view | `…_P205_FT-SIGNAL-ENERGY-MATRIX.csv` |

The contract reads these constants; it stores no own signal or route table.

## 2 Scales and weights
| Field | Type | Range | Weight |
|---|---|---|---|
| C consequence | int | 0–4 | 4 |
| U urgency | int | 0–4 | 3 |
| D dependencies | int | 0–4 | 2 |
| X uncertainty | int | 0–4 | 1 |

E = 4C + 3U + 2D + X, integer, 0–40. Floats/bools/out-of-range → `SignalError`.

Bands: P0 ≥ 28 · P1 20–27 · P2 12–19 · P3 ≤ 11. Stored `energy`/`priority` must equal computed values, else `SignalError` (fail closed, no silent correction).

## 3 Order
Sort key `(-E, -C, signal_id)` (energy desc, consequence desc, id asc, byte-wise). Total order; input order is irrelevant. Duplicate `signal_id` → `SignalError`.

## 4 Selection (Conditional Lookup)
`select(signals, K) = topK ∪ M`, rank-ordered, where M = {s | release_gate ∈ {STOP, BLOCKED} ∨ C = 4}. Result length ≥ min(K, n); may exceed K. K < 0 → error.

Decision open (N1): `C = 4` as mandatory criterion is an ID06 proposal; in P205, 6/8 signals have C = 4.

## 5 Routing (MoE)
`route(id)` = existing ROUTES for id, ordered by `sequence_no`. Unknown id → `[SOURCE_IDENTITY, role null, gate ID01, BLOCKED]` (router rule 1). Every route expert must exist in EXPERTS.

## 6 Reproducibility
`selection_hash = sha256(json({"contract","k","selection"}, sort_keys, separators=(",",":")))`.
Pinned: K = 3 → `809734ebde69bf1ae1fdba0de45ea54828bad7407e5d4a24a80cda44a3a37baa` (independently recomputable with `printf … | sha256sum`).

## 7 Golden slice (9 test functions, 11 cases)
| Test | Asserts |
|---|---|
| 01 | schema + formula for all P205 and synthetic rows |
| 02 | order equals existing P205 CSV view |
| 03 | permutation invariance (21 + 24 permutations) |
| 04 | tie-break C then id |
| 05 ×3 | mandatory union for K = 0/3/7 |
| 06 | low-energy STOP survives Top-K |
| 07 | fail closed: scale, float, energy, band, duplicate |
| 08 | routing reuse + fail-closed unknown id |
| 09 | pinned selection hash |

Reproduce: `python -m pytest -q tests/test_signal_rank.py`.

## 8 Out of scope
Generalisation beyond P205, expert-person profiles (supplement §4), engineering release. Signal energy prioritises work; it is no structural proof (P205 router v1.0).
