"""Raw result identity, convergence and explicit scalar-result linkage."""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Literal
from .base import Contract, identifier, require, sha256_text
from .model import MEMBER_QUANTITIES, NODE_QUANTITIES, Quantity

Unit = Literal["N", "Nm", "m", "rad"]
RESULT_UNITS: dict[str, str] = {
    **dict.fromkeys(("N", "V_y", "V_z", "R_x", "R_y", "R_z"), "N"),
    **dict.fromkeys(("M_y", "M_z", "T", "M_R_x", "M_R_y", "M_R_z"), "Nm"),
    **dict.fromkeys(("u_x", "u_y", "u_z"), "m"),
    **dict.fromkeys(("phi_x", "phi_y", "phi_z"), "rad"),
}


@dataclass(frozen=True, slots=True)
class Convergence(Contract):
    status: Literal["converged", "not_required", "failed", "unknown"]
    criterion: str
    normalized_residual: Decimal | None = None
    iterations: int | None = None

    def _validate(self) -> None:
        require(bool(self.criterion.strip()), "convergence criterion/source required")
        if self.normalized_residual is not None:
            require(self.normalized_residual >= 0, "residual must be nonnegative")
        if self.iterations is not None:
            require(self.iterations >= 0, "iterations must be nonnegative")


@dataclass(frozen=True, slots=True)
class StateResult(Contract):
    state_id: str
    status: Literal["solved", "partial", "failed"]
    convergence: Convergence
    warnings: tuple[str, ...] = ()

    def _validate(self) -> None:
        identifier(self.state_id)
        if self.status == "solved":
            require(self.convergence.status in ("converged", "not_required"),
                    "solved state requires verified convergence status")


@dataclass(frozen=True, slots=True)
class ResultValue(Contract):
    state_id: str
    object_kind: Literal["node", "member"]
    object_id: str
    quantity: Quantity
    value: Decimal
    unit: Unit
    frame: Literal["global", "member_local"]
    sign_convention: Literal["nexus-results/0.1"]
    station: Decimal | None = None

    def _validate(self) -> None:
        identifier(self.state_id)
        identifier(self.object_id)
        require(self.unit == RESULT_UNITS[self.quantity], "wrong result unit")
        member = self.object_kind == "member"
        allowed = MEMBER_QUANTITIES if member else NODE_QUANTITIES
        require(self.quantity in allowed, "result quantity/object mismatch")
        require(self.frame == ("member_local" if member else "global"), "wrong result frame")
        require((self.station is not None) == member, "station/object mismatch")
        if self.station is not None:
            require(0 <= self.station <= 1, "station outside [0,1]")


@dataclass(frozen=True, slots=True)
class AnalysisResults(Contract):
    schema_version: Literal["nexus-results/0.1"]
    model_id: str
    model_revision: str
    model_hash: str
    hash_profile: Literal["nexus-c14n/0.1"]
    solver_name: str
    solver_version: str
    adapter_version: str
    execution_kind: Literal["fixture_only", "solver"]
    states: tuple[StateResult, ...]
    values: tuple[ResultValue, ...]
    evidence_refs: tuple[str, ...]

    def _validate(self) -> None:
        sha256_text(self.model_hash)
        for value in (self.model_id, self.model_revision, self.solver_name,
                      self.solver_version, self.adapter_version):
            identifier(value)
        require(bool(self.states) and bool(self.evidence_refs), "state and evidence required")
        ids = [state.state_id for state in self.states]
        require(len(ids) == len(set(ids)), "duplicate result states")
        keys = [result_key(value) for value in self.values]
        require(len(keys) == len(set(keys)), "duplicate scalar results")
        require(all(value.state_id in ids for value in self.values), "unknown result state")


def result_key(value: ResultValue) -> tuple[str, str, str, str, Decimal | None]:
    return value.state_id, value.object_kind, value.object_id, value.quantity, value.station
