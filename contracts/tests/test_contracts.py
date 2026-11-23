from dataclasses import FrozenInstanceError, replace
from decimal import Decimal as D
import pytest
from nexus.bootstrap.synthetic import example_model
from nexus.domain.contracts.base import ContractError
from nexus.domain.contracts.model import (
    AnalysisState, ForceTarget, Frame, InitialAxialForce, Member, Node, NumericalSettings,
    ReferenceGeometry, ResultRequest, ResultSelection, SagTarget, UnstrainedLength,
)


@pytest.mark.parametrize("invalid", [D("NaN"), D("Infinity"), D("-Infinity"), 1.0, "1"])
def test_node_rejects_non_decimal_or_nonfinite(invalid):
    with pytest.raises(ContractError):
        Node("N", (invalid, D(0), D(0)))


def test_literal_is_checked_at_runtime():
    with pytest.raises(ContractError, match="literal"):
        replace(example_model(), units_profile="mm-N-MPa")


def test_nested_lists_are_rejected_rather_than_shallow_frozen():
    with pytest.raises(ContractError, match="tuple"):
        Node("N", [D(0), D(0), D(0)])


def test_dataclass_and_nested_values_are_immutable():
    model = example_model()
    with pytest.raises(FrozenInstanceError):
        model.nodes[0].id = "changed"
    with pytest.raises(TypeError):
        model.nodes[0].coordinates_m[0] = D(9)


@pytest.mark.parametrize("name", ["", " padded", "padded "])
def test_invalid_identifiers(name):
    with pytest.raises(ContractError):
        Node(name, (D(0), D(0), D(0)))


@pytest.mark.parametrize("collection", ["nodes", "members", "materials", "sections", "supports", "loads", "load_cases", "states"])
def test_duplicate_ids_rejected(collection):
    model = example_model()
    values = getattr(model, collection)
    with pytest.raises(ContractError, match="duplicate"):
        replace(model, **{collection: values + (values[0],)})


def test_unknown_member_endpoint():
    model = example_model()
    with pytest.raises(ContractError, match="endpoint"):
        replace(model, members=(replace(model.members[0], end_node_id="missing"),))


def test_coincident_nodes_with_distinct_ids_rejected():
    model = example_model()
    with pytest.raises(ContractError, match="coincident"):
        replace(model, nodes=(model.nodes[0], replace(model.nodes[1], coordinates_m=model.nodes[0].coordinates_m)))


def test_no_arbitrary_minimum_member_length_is_invented():
    model = example_model()
    tiny = replace(model.nodes[1], coordinates_m=(D("0.000000001"), D(0), D(0)))
    assert replace(model, nodes=(model.nodes[0], tiny)).nodes[1] == tiny


@pytest.mark.parametrize("field,value", [("young_modulus_Pa", D(0)), ("density_kg_m3", D(-1)),
                                         ("poisson_ratio", D("0.5")), ("thermal_expansion_per_K", D("NaN"))])
def test_material_constraints(field, value):
    with pytest.raises(ContractError):
        replace(example_model().materials[0], **{field: value})


def test_unknown_material_and_support_and_load_targets():
    model = example_model()
    for kwargs in (
        {"sections": (replace(model.sections[0], material_id="missing"),)},
        {"supports": (replace(model.supports[0], node_id="missing"),)},
        {"loads": (replace(model.loads[0], node_id="missing"),)},
        {"loads": (replace(model.loads[0], case_id="missing"),)},
    ):
        with pytest.raises(ContractError):
            replace(model, **kwargs)


def test_cable_needs_explicit_reference_but_tension_only_does_not():
    member = example_model().members[0]
    with pytest.raises(ContractError, match="reference"):
        replace(member, kind="cable")
    assert replace(member, kind="tension_only").reference_state is None
    assert replace(member, kind="cable", reference_state=ReferenceGeometry("reference_geometry", D(293)))


@pytest.mark.parametrize("length", [D(0), D(-1), D("NaN")])
def test_unstrained_length_validation(length):
    with pytest.raises(ContractError):
        UnstrainedLength("unstrained_length", length, D(293))


def test_reference_variant_has_no_swappable_unit_field():
    with pytest.raises(TypeError):
        UnstrainedLength("unstrained_length", D(1), D(293), unit="N")


def test_frames_are_right_handed_and_orthonormal():
    with pytest.raises(ContractError):
        Frame(z=(D(0), D(0), D(-1)))
    with pytest.raises(ContractError):
        Frame(x=(D(2), D(0), D(0)))


def test_member_frame_must_follow_chord():
    model = example_model()
    rotated = Frame((D(0), D(1), D(0)), (D(-1), D(0), D(0)), (D(0), D(0), D(1)))
    with pytest.raises(ContractError, match="local x|aligned"):
        replace(model, members=(replace(model.members[0], frame=rotated),))


def test_reaction_moment_can_be_requested_without_reaction_forces():
    request = ResultRequest(("S",), (ResultSelection("M_R_y", "node", ("N",)),))
    assert request.selections[0].quantity == "M_R_y"


def test_result_request_requires_explicit_nonempty_selection():
    with pytest.raises(ContractError):
        ResultRequest((), ())
    with pytest.raises(ContractError):
        ResultSelection("N", "member", ("M",), ())


def test_duplicate_and_unknown_result_selection():
    model = example_model()
    selection = model.result_request.selections[0]
    with pytest.raises(ContractError, match="overlapping"):
        replace(model, result_request=replace(model.result_request, selections=(selection, selection)))
    with pytest.raises(ContractError, match="unknown requested"):
        replace(model, result_request=replace(model.result_request, state_ids=("missing",)))


def test_state_cycles_and_unknown_dependencies_rejected():
    model = example_model()
    a = replace(model.states[0], initial_state_id="STATE2")
    b = replace(model.states[0], id="STATE2", initial_state_id="STATE1")
    with pytest.raises(ContractError, match="cyclic"):
        replace(model, states=(a, b))
    with pytest.raises(ContractError, match="unknown initial"):
        replace(model, states=(a,))


def test_formfinding_target_is_bound_to_an_explicit_state():
    model = example_model()
    cable = replace(model.members[0], kind="cable", reference_state=ReferenceGeometry("reference_geometry", D(293)))
    target = SagTarget("M1", "sag", D("0.1"), D("0.5"), (D(0), D(0), D(-1)))
    state = AnalysisState("STATE1", "form_finding", (), NumericalSettings("newton_raphson", 50, D("0.0001")), form_targets=(target,))
    assert replace(model, members=(cable,), states=(state,))
    with pytest.raises(ContractError, match="form targets"):
        replace(model.states[0], form_targets=(target,))


def test_numerical_settings_are_explicit_and_validated():
    for setting in (dict(max_iterations=0), dict(relative_equilibrium_tolerance=D("NaN"))):
        with pytest.raises(ContractError):
            replace(example_model().states[0].numerics, **setting)
