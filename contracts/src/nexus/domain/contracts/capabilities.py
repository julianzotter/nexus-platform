"""Capability claims are adapter-specific and scoped, never vendor-wide promises."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from .base import Contract, identifier, require
from .model import Algorithm, LoadKind, MemberKind, Quantity, Theory

ReferenceKind = Literal["none", "unstrained_length", "initial_axial_force", "reference_geometry"]


@dataclass(frozen=True, slots=True)
class CapabilityProfile(Contract):
    """One alternative: all represented state requirements must fit together."""
    id: str
    theory: Theory
    member_kinds: tuple[MemberKind, ...]
    load_kinds: tuple[LoadKind, ...]
    reference_kinds: tuple[ReferenceKind, ...]
    algorithms: tuple[Algorithm, ...]
    form_target_kinds: tuple[Literal["axial_force", "sag"], ...] = ()
    supports_gravity: bool = False
    supports_initial_state: bool = False
    supports_rotated_supports: bool = False

    def _validate(self) -> None:
        identifier(self.id)
        require(bool(self.member_kinds) and bool(self.reference_kinds), "empty capability profile")
        require(bool(self.algorithms), "algorithms required")
        for values in (self.member_kinds, self.load_kinds, self.reference_kinds,
                       self.form_target_kinds, self.algorithms):
            require(len(values) == len(set(values)), "duplicate capability entries")


@dataclass(frozen=True, slots=True)
class SolverCapabilities(Contract):
    schema_version: Literal["nexus-capabilities/0.1"]
    solver_name: str
    solver_version: str
    adapter_version: str
    execution_kind: Literal["fixture_only", "solver"]
    supported_model_schemas: tuple[str, ...]
    supported_results: tuple[Quantity, ...]
    profiles: tuple[CapabilityProfile, ...]
    known_limitations: tuple[str, ...]
    evidence_refs: tuple[str, ...]

    def _validate(self) -> None:
        for value in (self.solver_name, self.solver_version, self.adapter_version):
            identifier(value)
        require(bool(self.supported_model_schemas) and bool(self.profiles), "empty capabilities")
        for values in (self.supported_model_schemas, self.supported_results):
            require(len(values) == len(set(values)), "duplicate capability entries")
        ids = [p.id for p in self.profiles]
        require(len(ids) == len(set(ids)), "duplicate capability profile IDs")


@dataclass(frozen=True, slots=True)
class CompatibilityIssue(Contract):
    code: Literal["E_SCHEMA", "E_RESULT", "E_STATE_PROFILE"]
    object_ref: str
    required_capability: str
    message: str


@dataclass(frozen=True, slots=True)
class CompatibilityReport(Contract):
    schema_version: Literal["nexus-compatibility/0.1"]
    model_id: str
    model_revision: str
    adapter_version: str
    issues: tuple[CompatibilityIssue, ...]

    @property
    def ok(self) -> bool:
        return not self.issues
