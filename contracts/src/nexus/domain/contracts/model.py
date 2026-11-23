"""Analytical model contract. Canonical units: m, N, Pa, kg, s, K, rad."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

from .base import Contract, identifier, require, unique_ids

Vector3 = tuple[Decimal, Decimal, Decimal]
ZERO: Vector3 = (Decimal(0), Decimal(0), Decimal(0))
MemberKind = Literal["beam", "truss", "tension_only", "compression_only", "cable"]
Theory = Literal["linear_static", "large_displacement_static", "form_finding"]
Quantity = Literal["N", "V_y", "V_z", "M_y", "M_z", "T", "u_x", "u_y", "u_z",
                   "phi_x", "phi_y", "phi_z", "R_x", "R_y", "R_z", "M_R_x", "M_R_y", "M_R_z"]
MEMBER_QUANTITIES = {"N", "V_y", "V_z", "M_y", "M_z", "T"}
NODE_QUANTITIES = {"u_x", "u_y", "u_z", "phi_x", "phi_y", "phi_z", "R_x", "R_y", "R_z",
                   "M_R_x", "M_R_y", "M_R_z"}


@dataclass(frozen=True, slots=True)
class Frame(Contract):
    """Right-handed local basis expressed in global/model components."""
    x: Vector3 = (Decimal(1), Decimal(0), Decimal(0))
    y: Vector3 = (Decimal(0), Decimal(1), Decimal(0))
    z: Vector3 = (Decimal(0), Decimal(0), Decimal(1))

    def _validate(self) -> None:
        axes = (self.x, self.y, self.z)
        for i in range(3):
            for j in range(3):
                dot = sum((a*b for a, b in zip(axes[i], axes[j])), Decimal(0))
                require(abs(dot - Decimal(i == j)) <= Decimal("1e-12"),
                        "frame must be orthonormal")
        cross = (self.x[1]*self.y[2]-self.x[2]*self.y[1],
                 self.x[2]*self.y[0]-self.x[0]*self.y[2],
                 self.x[0]*self.y[1]-self.x[1]*self.y[0])
        require(all(abs(a-b) <= Decimal("1e-12") for a, b in zip(cross, self.z)),
                "frame must be right-handed")


@dataclass(frozen=True, slots=True)
class Node(Contract):
    id: str
    coordinates_m: Vector3

    def _validate(self) -> None:
        identifier(self.id)


@dataclass(frozen=True, slots=True)
class Material(Contract):
    id: str
    name: str
    law: Literal["linear_elastic_isotropic"]
    young_modulus_Pa: Decimal
    poisson_ratio: Decimal
    density_kg_m3: Decimal
    thermal_expansion_per_K: Decimal

    def _validate(self) -> None:
        identifier(self.id)
        require(self.young_modulus_Pa > 0, "E must be positive")
        require(Decimal(-1) < self.poisson_ratio < Decimal("0.5"), "invalid nu")
        require(self.density_kg_m3 > 0, "density must be positive")


@dataclass(frozen=True, slots=True)
class Section(Contract):
    id: str
    material_id: str
    area_m2: Decimal
    Iy_m4: Decimal
    Iz_m4: Decimal
    torsional_constant_m4: Decimal

    def _validate(self) -> None:
        identifier(self.id)
        identifier(self.material_id)
        require(self.area_m2 > 0, "area must be positive")
        require(min(self.Iy_m4, self.Iz_m4, self.torsional_constant_m4) >= 0,
                "section constants must be nonnegative")


@dataclass(frozen=True, slots=True)
class UnstrainedLength(Contract):
    kind: Literal["unstrained_length"]
    length_m: Decimal
    reference_temperature_K: Decimal

    def _validate(self) -> None:
        require(self.length_m > 0, "unstrained length must be positive")
        require(self.reference_temperature_K > 0, "absolute temperature must be positive")


@dataclass(frozen=True, slots=True)
class InitialAxialForce(Contract):
    kind: Literal["initial_axial_force"]
    tension_positive_force_N: Decimal
    reference_temperature_K: Decimal

    def _validate(self) -> None:
        require(self.reference_temperature_K > 0, "absolute temperature must be positive")


@dataclass(frozen=True, slots=True)
class ReferenceGeometry(Contract):
    """Node coordinates explicitly define the unstrained reference geometry."""
    kind: Literal["reference_geometry"]
    reference_temperature_K: Decimal

    def _validate(self) -> None:
        require(self.reference_temperature_K > 0, "absolute temperature must be positive")


ReferenceState = UnstrainedLength | InitialAxialForce | ReferenceGeometry


@dataclass(frozen=True, slots=True)
class Member(Contract):
    id: str
    start_node_id: str
    end_node_id: str
    kind: MemberKind
    section_id: str
    frame: Frame
    reference_state: ReferenceState | None = None

    def _validate(self) -> None:
        for value in (self.id, self.start_node_id, self.end_node_id, self.section_id):
            identifier(value)
        require(self.start_node_id != self.end_node_id, "member endpoints must differ")
        if self.kind == "cable":
            require(self.reference_state is not None, "cable requires explicit reference state")


Dof = Literal["u_x", "u_y", "u_z", "phi_x", "phi_y", "phi_z"]


@dataclass(frozen=True, slots=True)
class Support(Contract):
    id: str
    node_id: str
    fixed_dofs: tuple[Dof, ...]
    frame: Frame

    def _validate(self) -> None:
        identifier(self.id)
        identifier(self.node_id)
        require(bool(self.fixed_dofs), "support must restrain at least one DOF")
        require(len(set(self.fixed_dofs)) == len(self.fixed_dofs), "duplicate support DOFs")


@dataclass(frozen=True, slots=True)
class NodalForce(Contract):
    id: str
    case_id: str
    kind: Literal["nodal_force"]
    node_id: str
    global_vector_N: Vector3


@dataclass(frozen=True, slots=True)
class NodalMoment(Contract):
    id: str
    case_id: str
    kind: Literal["nodal_moment"]
    node_id: str
    global_vector_Nm: Vector3


@dataclass(frozen=True, slots=True)
class UniformMemberLoad(Contract):
    id: str
    case_id: str
    kind: Literal["uniform_member_load"]
    member_id: str
    vector_N_per_m: Vector3
    frame: Literal["global", "member_local"]


@dataclass(frozen=True, slots=True)
class TemperatureChange(Contract):
    id: str
    case_id: str
    kind: Literal["temperature_change"]
    member_id: str
    delta_K: Decimal


@dataclass(frozen=True, slots=True)
class MemberPrestress(Contract):
    id: str
    case_id: str
    kind: Literal["member_prestress"]
    member_id: str
    tension_positive_force_N: Decimal


Load = NodalForce | NodalMoment | UniformMemberLoad | TemperatureChange | MemberPrestress
LoadKind = Literal["nodal_force", "nodal_moment", "uniform_member_load",
                   "temperature_change", "member_prestress"]


@dataclass(frozen=True, slots=True)
class LoadCase(Contract):
    id: str
    name: str

    def _validate(self) -> None:
        identifier(self.id)


@dataclass(frozen=True, slots=True)
class CaseFactor(Contract):
    case_id: str
    factor: Decimal

    def _validate(self) -> None:
        identifier(self.case_id)


@dataclass(frozen=True, slots=True)
class ForceTarget(Contract):
    member_id: str
    kind: Literal["axial_force"]
    tension_positive_force_N: Decimal

    def _validate(self) -> None:
        identifier(self.member_id)
        require(self.tension_positive_force_N > 0, "form-finding target must be tensile")


@dataclass(frozen=True, slots=True)
class SagTarget(Contract):
    """Signed projection from the endpoint chord at a stated member station."""
    member_id: str
    kind: Literal["sag"]
    sag_m: Decimal
    station_fraction: Decimal
    global_direction_unit: Vector3

    def _validate(self) -> None:
        identifier(self.member_id)
        require(Decimal(0) < self.station_fraction < Decimal(1), "interior station required")
        norm2 = sum((v*v for v in self.global_direction_unit), Decimal(0))
        require(abs(norm2-1) <= Decimal("1e-12"), "sag direction must be a unit vector")


FormTarget = ForceTarget | SagTarget


Algorithm = Literal["linear_direct", "newton_raphson", "arc_length"]


@dataclass(frozen=True, slots=True)
class NumericalSettings(Contract):
    algorithm: Algorithm
    max_iterations: int
    relative_equilibrium_tolerance: Decimal

    def _validate(self) -> None:
        require(self.max_iterations > 0, "positive iteration limit required")
        require(0 < self.relative_equilibrium_tolerance < 1,
                "relative equilibrium tolerance must lie in (0,1)")


@dataclass(frozen=True, slots=True)
class AnalysisState(Contract):
    id: str
    theory: Theory
    case_factors: tuple[CaseFactor, ...]
    numerics: NumericalSettings
    gravity_m_s2: Vector3 = ZERO
    initial_state_id: str | None = None
    form_targets: tuple[FormTarget, ...] = ()

    def _validate(self) -> None:
        identifier(self.id)
        ids = [factor.case_id for factor in self.case_factors]
        require(len(ids) == len(set(ids)), "duplicate case factors")
        targets = [target.member_id for target in self.form_targets]
        require(len(targets) == len(set(targets)), "one form target per member")
        require((self.theory == "form_finding") == bool(self.form_targets),
                "form targets required exactly for form-finding states")
        require(self.initial_state_id != self.id, "state cannot initialize itself")
        require((self.theory == "linear_static") == (self.numerics.algorithm == "linear_direct"),
                "algorithm and analysis theory disagree")


@dataclass(frozen=True, slots=True)
class ResultSelection(Contract):
    quantity: Quantity
    object_kind: Literal["node", "member"]
    object_ids: tuple[str, ...]
    stations: tuple[Decimal, ...] = ()

    def _validate(self) -> None:
        require(bool(self.object_ids), "result object selection is required")
        require(len(set(self.object_ids)) == len(self.object_ids), "duplicate result objects")
        allowed = MEMBER_QUANTITIES if self.object_kind == "member" else NODE_QUANTITIES
        require(self.quantity in allowed, "quantity and object kind disagree")
        require(bool(self.stations) == (self.object_kind == "member"),
                "member results require stations; node results have no stations")
        require(all(0 <= s <= 1 for s in self.stations), "station outside [0,1]")
        require(len(set(self.stations)) == len(self.stations), "duplicate stations")


@dataclass(frozen=True, slots=True)
class ResultRequest(Contract):
    state_ids: tuple[str, ...]
    selections: tuple[ResultSelection, ...]

    def _validate(self) -> None:
        require(bool(self.state_ids) and bool(self.selections), "explicit result request required")
        require(len(set(self.state_ids)) == len(self.state_ids), "duplicate requested states")


@dataclass(frozen=True, slots=True)
class AnalysisModel(Contract):
    schema_version: Literal["nexus-model/0.1"]
    model_id: str
    revision: str
    units_profile: Literal["SI-m-N-Pa-kg-s-K-rad/1"]
    origin_m: Vector3
    global_frame: Frame
    nodes: tuple[Node, ...]
    members: tuple[Member, ...]
    materials: tuple[Material, ...]
    sections: tuple[Section, ...]
    supports: tuple[Support, ...]
    loads: tuple[Load, ...]
    load_cases: tuple[LoadCase, ...]
    states: tuple[AnalysisState, ...]
    result_request: ResultRequest

    def _validate(self) -> None:
        identifier(self.model_id)
        identifier(self.revision)
        validate_model(self)


def validate_model(model: AnalysisModel) -> None:
    for name in ("nodes", "members", "materials", "sections", "supports", "loads",
                 "load_cases", "states"):
        unique_ids(getattr(model, name), name)
    require(bool(model.nodes) and bool(model.members) and bool(model.states),
            "nonempty nodes, members and states required")
    nodes = {n.id: n for n in model.nodes}
    sections = {s.id: s for s in model.sections}
    materials = {m.id for m in model.materials}
    for section in model.sections:
        require(section.material_id in materials, "unknown section material")
    for member in model.members:
        require(member.start_node_id in nodes and member.end_node_id in nodes,
                "unknown member endpoint")
        require(member.section_id in sections, "unknown member section")
        a, b = nodes[member.start_node_id], nodes[member.end_node_id]
        delta = tuple(y-x for x, y in zip(a.coordinates_m, b.coordinates_m))
        length2 = sum((d*d for d in delta), Decimal(0))
        require(length2 > 0, "coincident member endpoints")
        projection = sum((d*x for d, x in zip(delta, member.frame.x)), Decimal(0))
        require(projection > 0, "member local x must point start to end")
        remainder = sum(((d-projection*x)**2 for d, x in zip(delta, member.frame.x)), Decimal(0))
        require(remainder <= length2*Decimal("1e-20"), "member x not aligned with chord")
        if member.kind == "beam":
            sec = sections[member.section_id]
            require(min(sec.Iy_m4, sec.Iz_m4, sec.torsional_constant_m4) > 0,
                    "beam requires positive Iy, Iz and torsional constant")
    for support in model.supports:
        require(support.node_id in nodes, "unknown support node")
    validate_loads(model)
    validate_states(model)
    validate_request(model)


def validate_loads(model: AnalysisModel) -> None:
    nodes = {n.id for n in model.nodes}
    members = {m.id for m in model.members}
    cases = {case.id for case in model.load_cases}
    for load in model.loads:
        require(bool(load.id.strip()), "load ID required")
        require(load.case_id in cases, "unknown load case")
        if isinstance(load, (NodalForce, NodalMoment)):
            require(load.node_id in nodes, "unknown nodal load target")
        else:
            require(load.member_id in members, "unknown member load target")


def validate_states(model: AnalysisModel) -> None:
    states = {state.id: state for state in model.states}
    cases = {case.id for case in model.load_cases}
    members = {member.id: member for member in model.members}
    for state in model.states:
        require(all(f.case_id in cases for f in state.case_factors), "unknown factored case")
        require(state.initial_state_id is None or state.initial_state_id in states,
                "unknown initial state")
        for target in state.form_targets:
            require(target.member_id in members, "unknown form target member")
            require(members[target.member_id].kind == "cable", "form target requires cable")
        visited: set[str] = set()
        current: str | None = state.id
        while current is not None:
            require(current not in visited, "cyclic analysis initial states")
            visited.add(current)
            current = states[current].initial_state_id


def validate_request(model: AnalysisModel) -> None:
    require(set(model.result_request.state_ids) <= {s.id for s in model.states},
            "unknown requested analysis state")
    for selection in model.result_request.selections:
        ids = ({n.id for n in model.nodes} if selection.object_kind == "node"
               else {m.id for m in model.members})
        require(set(selection.object_ids) <= ids, "unknown requested result object")
    keys: list[tuple[str, str, str, Decimal | None]] = []
    for selection in model.result_request.selections:
        for object_id in selection.object_ids:
            for station in selection.stations or (None,):
                keys.append((selection.object_kind, object_id, selection.quantity, station))
    require(len(keys) == len(set(keys)), "overlapping result selections")
