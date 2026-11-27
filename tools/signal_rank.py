"""Deterministic signal ranking and conditional lookup over the EXISTING P205 signal-energy matrix.

Status: PROPOSED (ID06, 2026-11-27, issue #153, Review A findings A1-A4). Not ADOPTED.

No second router SSOT: signals, experts and routes are read from the existing ID02 builder
WORK/P205_FT/2026-11-23_ID02/26_11_23_1104_ID02_build_P205_FT_AUDIT_DB.py (data constants only;
its main() is never called). This module only adds a frozen ranking contract on top:

* Scales: consequence C, urgency U, dependencies D, uncertainty X are integers 0..4 (P205 DDL).
* Weights: E = 4C + 3U + 2D + X, 0..40 (P205 metadata score_formula), integer arithmetic only.
* Bands: P0 >= 28, P1 20..27, P2 12..19, P3 <= 11 (P205 MoE-Router v1.0).
* Order: sort key (-E, -C, signal_id); input order is irrelevant.
* Mandatory union: result = topK ∪ {gate in STOP/BLOCKED or C == 4}, in rank order; len may exceed K.
* Routing: routes of the builder ordered by sequence_no; unknown/missing -> SOURCE_IDENTITY, BLOCKED.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from types import ModuleType
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
P205_BUILDER = ROOT / "WORK/P205_FT/2026-11-23_ID02/26_11_23_1104_ID02_build_P205_FT_AUDIT_DB.py"
CONTRACT_VERSION = "signal-rank-1.0.0"
WEIGHTS = (4, 3, 2, 1)  # C, U, D, X
SCALE_MIN, SCALE_MAX = 0, 4
MANDATORY_GATES = frozenset({"STOP", "BLOCKED"})


class SignalError(ValueError):
    """Raised when a signal violates the frozen scale/energy/band contract."""


@dataclass(frozen=True)
class Signal:
    signal_id: str
    title: str
    domain: str
    evidence_class: str
    consequence: int
    urgency: int
    dependencies: int
    uncertainty: int
    energy: int
    priority: str
    release_gate: str


def energy(c: int, u: int, d: int, x: int) -> int:
    """Return E = 4C+3U+2D+X after integer range checks (0..4)."""
    for name, v in (("C", c), ("U", u), ("D", d), ("X", x)):
        if not isinstance(v, int) or isinstance(v, bool) or not SCALE_MIN <= v <= SCALE_MAX:
            raise SignalError(f"{name}={v!r} outside integer scale {SCALE_MIN}..{SCALE_MAX}")
    return sum(w * v for w, v in zip(WEIGHTS, (c, u, d, x)))


def band(e: int) -> str:
    """Map energy to priority band P0..P3."""
    if e >= 28:
        return "P0"
    if e >= 20:
        return "P1"
    if e >= 12:
        return "P2"
    return "P3"


def validate(s: Signal) -> Signal:
    """Fail closed if stored energy or band disagree with the frozen formula."""
    e = energy(s.consequence, s.urgency, s.dependencies, s.uncertainty)
    if e != s.energy:
        raise SignalError(f"{s.signal_id}: stored energy {s.energy} != computed {e}")
    if band(e) != s.priority:
        raise SignalError(f"{s.signal_id}: stored priority {s.priority} != band {band(e)}")
    return s


def rank_key(s: Signal) -> tuple[int, int, str]:
    """Stable total order: energy desc, consequence desc, signal_id asc."""
    return (-s.energy, -s.consequence, s.signal_id)


def is_mandatory(s: Signal) -> bool:
    """Mandatory signals survive any Top-K cut."""
    return s.release_gate in MANDATORY_GATES or s.consequence == SCALE_MAX


def select(signals: Iterable[Signal], k: int) -> list[str]:
    """Return topK ∪ mandatory signal_ids in rank order (independent of input order)."""
    if k < 0:
        raise ValueError("k must be >= 0")
    ranked = sorted((validate(s) for s in signals), key=rank_key)
    ids = [s.signal_id for s in ranked]
    if len(set(ids)) != len(ids):
        raise SignalError("duplicate signal_id")
    return [s.signal_id for i, s in enumerate(ranked) if i < k or is_mandatory(s)]


def selection_hash(selection: Sequence[str], k: int) -> str:
    """SHA-256 over canonical JSON of contract version, k and selection."""
    payload = json.dumps({"contract": CONTRACT_VERSION, "k": k, "selection": list(selection)},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_p205() -> ModuleType:
    """Import the existing P205 builder for its data constants (no side effects)."""
    spec = importlib.util.spec_from_file_location("p205_builder", P205_BUILDER)
    if spec is None or spec.loader is None:
        raise FileNotFoundError(P205_BUILDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def p205_signals(mod: ModuleType | None = None) -> list[Signal]:
    """Existing P205 SIGNALS tuples as validated Signal records."""
    mod = mod or load_p205()
    return [validate(Signal(*row)) for row in mod.SIGNALS]


def route(signal_id: str, routes: Iterable[Sequence[object]]) -> list[dict[str, object]]:
    """Ordered expert route from the existing ROUTES table; fail closed if absent."""
    hits = sorted((r for r in routes if r[1] == signal_id), key=lambda r: int(r[2]))
    if not hits:
        return [{"expert_id": "SOURCE_IDENTITY", "assigned_role_id": None, "human_gate": "ID01",
                 "status": "BLOCKED"}]
    return [{"expert_id": r[3], "assigned_role_id": r[4], "human_gate": r[5], "status": r[6]} for r in hits]


def as_records(signals: Iterable[Signal]) -> list[dict[str, object]]:
    """Plain dicts for JSON-schema validation and export."""
    return [asdict(s) for s in signals]
