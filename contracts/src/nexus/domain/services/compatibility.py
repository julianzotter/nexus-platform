"""Conservative state-wide capability matching, including nodal-only cases."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
from nexus.domain.contracts.base import Contract
from nexus.domain.contracts.capabilities import (
    CapabilityProfile, CompatibilityIssue, CompatibilityReport, SolverCapabilities,
)
from nexus.domain.contracts.model import AnalysisModel, AnalysisState, Frame, ZERO


@dataclass(frozen=True, slots=True)
class RequirementProfile(Contract):
    state_id: str
    theory: str
    algorithm: str
    member_kinds: tuple[str, ...]
    load_kinds: tuple[str, ...]
    reference_kinds: tuple[str, ...]
    form_target_kinds: tuple[str, ...]
    gravity: bool
    initial_state: bool
    rotated_supports: bool


def requirements(model: AnalysisModel, state: AnalysisState) -> RequirementProfile:
    cases = {factor.case_id for factor in state.case_factors if factor.factor != 0}
    return RequirementProfile(
        state.id, state.theory, state.numerics.algorithm,
        tuple(sorted({m.kind for m in model.members})),
        tuple(sorted({load.kind for load in model.loads if load.case_id in cases})),
        tuple(sorted({m.reference_state.kind if m.reference_state else "none"
                      for m in model.members})),
        tuple(sorted({t.kind for t in state.form_targets})),
        state.gravity_m_s2 != ZERO, state.initial_state_id is not None,
        any(support.frame != Frame() for support in model.supports),
    )


def covers(profile: CapabilityProfile, needed: RequirementProfile) -> bool:
    return (
        profile.theory == needed.theory
        and needed.algorithm in profile.algorithms
        and set(needed.member_kinds) <= set(profile.member_kinds)
        and set(needed.load_kinds) <= set(profile.load_kinds)
        and set(needed.reference_kinds) <= set(profile.reference_kinds)
        and set(needed.form_target_kinds) <= set(profile.form_target_kinds)
        and (not needed.gravity or profile.supports_gravity)
        and (not needed.initial_state or profile.supports_initial_state)
        and (not needed.rotated_supports or profile.supports_rotated_supports)
    )


def build_compatibility_report(
    model: AnalysisModel, caps: SolverCapabilities,
) -> CompatibilityReport:
    issues: list[CompatibilityIssue] = []
    if model.schema_version not in caps.supported_model_schemas:
        issues.append(CompatibilityIssue("E_SCHEMA", "model", model.schema_version,
                                         "model schema unsupported"))
    requested = {selection.quantity for selection in model.result_request.selections}
    for quantity in sorted(requested - set(caps.supported_results)):
        issues.append(CompatibilityIssue("E_RESULT", "result_request", quantity,
                                         "result quantity unsupported"))
    for state in sorted(model.states, key=lambda item: item.id):
        needed = requirements(model, state)
        if not any(covers(profile, needed) for profile in caps.profiles):
            issues.append(CompatibilityIssue("E_STATE_PROFILE", f"state:{state.id}",
                                             repr(needed), "no profile covers the complete state"))
    return CompatibilityReport("nexus-compatibility/0.1", model.model_id, model.revision,
                               caps.adapter_version, tuple(issues))
