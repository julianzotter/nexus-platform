"""Synthetic software fixtures. Scalar values are NOT calculated responses."""
from decimal import Decimal as D
from nexus.domain.contracts.model import (
    AnalysisModel, AnalysisState, CaseFactor, Frame, LoadCase, Material, Member,
    NodalForce, Node, NumericalSettings, ResultRequest, ResultSelection, Section, Support,
)
from nexus.domain.contracts.capabilities import CapabilityProfile, SolverCapabilities
from nexus.domain.contracts.results import AnalysisResults, Convergence, ResultValue, StateResult
from nexus.domain.services.canonical import content_hash


def example_model() -> AnalysisModel:
    frame = Frame()
    return AnalysisModel(
        schema_version="nexus-model/0.1", model_id="SYNTHETIC-CONTRACT-FIXTURE", revision="1",
        units_profile="SI-m-N-Pa-kg-s-K-rad/1", origin_m=(D(0), D(0), D(0)), global_frame=frame,
        nodes=(Node("N1", (D(0), D(0), D(0))), Node("N2", (D(2), D(0), D(0)))),
        members=(Member("M1", "N1", "N2", "beam", "S1", frame),),
        materials=(Material("MAT1", "synthetic-elastic-material", "linear_elastic_isotropic",
                            D("210000000000"), D("0.3"), D("7850"), D("0.000012")),),
        sections=(Section("S1", "MAT1", D("0.01"), D("0.0001"), D("0.0001"), D("0.00001")),),
        supports=(Support("SUP1", "N1", ("u_x", "u_y", "u_z", "phi_x", "phi_y", "phi_z"), frame),),
        loads=(NodalForce("LOAD1", "LC1", "nodal_force", "N2", (D(0), D(0), D(-1000))),),
        load_cases=(LoadCase("LC1", "synthetic-load-case"),),
        states=(AnalysisState("STATE1", "linear_static", (CaseFactor("LC1", D(1)),),
                              NumericalSettings("linear_direct", 1, D("0.000001"))),),
        result_request=ResultRequest(("STATE1",), (
            ResultSelection("u_z", "node", ("N2",)),
            ResultSelection("M_R_y", "node", ("N1",)),
            ResultSelection("N", "member", ("M1",), (D(0), D(1))),
        )),
    )


def example_capabilities() -> SolverCapabilities:
    return SolverCapabilities(
        "nexus-capabilities/0.1", "FixtureReplay", "no-solver", "0.1.0", "fixture_only",
        ("nexus-model/0.1",), ("u_z", "M_R_y", "N"),
        (CapabilityProfile("fixture-linear-beam", "linear_static", ("beam",),
                           ("nodal_force",), ("none",), ("linear_direct",)),),
        ("Replays supplied values; does not solve equilibrium or implement any design standard.",),
        ("docs/QA.md#fixture-only",),
    )


def example_results(model: AnalysisModel) -> AnalysisResults:
    """All-zero fixture intentionally has no mechanics-validation claim."""
    values = (
        ResultValue("STATE1", "node", "N2", "u_z", D(0), "m", "global", "nexus-results/0.1"),
        ResultValue("STATE1", "node", "N1", "M_R_y", D(0), "Nm", "global", "nexus-results/0.1"),
        ResultValue("STATE1", "member", "M1", "N", D(0), "N", "member_local", "nexus-results/0.1", D(0)),
        ResultValue("STATE1", "member", "M1", "N", D(0), "N", "member_local", "nexus-results/0.1", D(1)),
    )
    return AnalysisResults(
        "nexus-results/0.1", model.model_id, model.revision, content_hash(model), "nexus-c14n/0.1",
        "FixtureReplay", "no-solver", "0.1.0", "fixture_only",
        (StateResult("STATE1", "solved", Convergence("not_required", "software fixture only")),),
        values, ("docs/QA.md#fixture-only",),
    )
