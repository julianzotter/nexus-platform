"""Golden-slice regression tests for tools/signal_rank.py (issue #153, Review A A1-A4)."""
from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("signal_rank", ROOT / "tools" / "signal_rank.py")
sr = importlib.util.module_from_spec(_spec)
sys.modules["signal_rank"] = sr  # dataclasses resolve cls.__module__
_spec.loader.exec_module(sr)

GOLDEN = json.loads((ROOT / "tests/golden/signal_rank_v1.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((ROOT / "schemas/signal-matrix-entry.schema.json").read_text(encoding="utf-8"))
P205 = sr.load_p205()
SIGNALS = sr.p205_signals(P205)
SYNTH = [sr.Signal(**row) for row in GOLDEN["synthetic"]]
PINNED_HASH_K3 = "809734ebde69bf1ae1fdba0de45ea54828bad7407e5d4a24a80cda44a3a37baa"


def test_01_p205_rows_match_schema_and_formula() -> None:
    assert len(SIGNALS) == 8
    for rec in sr.as_records(SIGNALS) + GOLDEN["synthetic"]:
        jsonschema.validate(rec, SCHEMA)
    assert all(s.energy == 4 * s.consequence + 3 * s.urgency + 2 * s.dependencies + s.uncertainty for s in SIGNALS)


def test_02_golden_order_equals_existing_p205_view() -> None:
    order = [s.signal_id for s in sorted(SIGNALS, key=sr.rank_key)]
    assert order == GOLDEN["p205_order"]
    csv = (sr.P205_BUILDER.parent / "26_11_23_1104_ID02_P205_FT-SIGNAL-ENERGY-MATRIX.csv").read_text(encoding="utf-8-sig")
    assert [line.split(",")[0] for line in csv.splitlines()[1:]] == order


def test_03_permutation_invariance() -> None:
    base = sr.select(SIGNALS, 3)
    perms = [list(reversed(SIGNALS))] + [random.Random(seed).sample(SIGNALS, len(SIGNALS)) for seed in range(20)]
    assert all(sr.select(p, 3) == base for p in perms)
    for p in itertools.permutations(SYNTH):
        assert sr.select(list(p), 1) == GOLDEN["synthetic_select_k1"]


def test_04_tie_break_consequence_then_id() -> None:
    top3 = [s.signal_id for s in sorted(SIGNALS, key=sr.rank_key)[:3]]
    assert top3 == ["S01", "S02", "S07"]  # E=40, C=4 -> signal_id asc
    assert sr.select(SYNTH, 2) == GOLDEN["synthetic_select_k2"]  # E=20 tie: C3 before C2


@pytest.mark.parametrize("k", ["0", "3", "7"])
def test_05_mandatory_union_p205(k: str) -> None:
    assert sr.select(SIGNALS, int(k)) == GOLDEN["p205_select"][k]


def test_06_low_energy_stop_survives_topk() -> None:
    sel = sr.select(SYNTH, 1)
    assert "T-C" in sel and "T-D" not in sel and len(sel) == 2


def test_07_fail_closed_on_scale_energy_band_duplicate() -> None:
    good = SYNTH[0]
    with pytest.raises(sr.SignalError):
        sr.energy(5, 0, 0, 0)
    with pytest.raises(sr.SignalError):
        sr.energy(1.0, 0, 0, 0)  # type: ignore[arg-type]
    with pytest.raises(sr.SignalError):
        sr.validate(sr.Signal(**{**GOLDEN["synthetic"][0], "energy": 21}))
    with pytest.raises(sr.SignalError):
        sr.validate(sr.Signal(**{**GOLDEN["synthetic"][0], "priority": "P0"}))
    with pytest.raises(sr.SignalError):
        sr.select([good, good], 1)


def test_08_routing_reuses_existing_routes_and_fails_closed() -> None:
    r = sr.route("S01", P205.ROUTES)
    assert [x["expert_id"] for x in r] == ["EXCEL_ENGINE", "RED_TEAM_AUDIT"]
    assert [x["assigned_role_id"] for x in r] == ["ID06", "ID07"]
    assert all(x["human_gate"] == "ID01" for x in r)
    assert sr.route("S99", P205.ROUTES) == [{"expert_id": "SOURCE_IDENTITY", "assigned_role_id": None,
                                              "human_gate": "ID01", "status": "BLOCKED"}]
    experts = {e[0] for e in P205.EXPERTS}
    assert {r[3] for r in P205.ROUTES} <= experts  # no route to an undeclared expert


def test_09_selection_hash_reproducible_and_pinned() -> None:
    h = sr.selection_hash(sr.select(SIGNALS, 3), 3)
    assert h == sr.selection_hash(sr.select(list(reversed(SIGNALS)), 3), 3)
    assert h == PINNED_HASH_K3
