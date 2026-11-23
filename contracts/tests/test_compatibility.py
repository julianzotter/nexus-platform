from dataclasses import replace
from decimal import Decimal as D
import pytest
from nexus.bootstrap.synthetic import example_capabilities, example_model
from nexus.domain.contracts.base import ContractError
from nexus.domain.contracts.model import Frame, TemperatureChange, ZERO
from nexus.domain.services.compatibility import build_compatibility_report, requirements


def test_supported_synthetic_case():
    assert build_compatibility_report(example_model(), example_capabilities()).ok


def test_schema_version_unsupported():
    caps = replace(example_capabilities(), supported_model_schemas=("different",))
    assert build_compatibility_report(example_model(), caps).issues[0].code == "E_SCHEMA"


def test_result_type_unsupported():
    caps = replace(example_capabilities(), supported_results=("N",))
    assert "E_RESULT" in {i.code for i in build_compatibility_report(example_model(), caps).issues}


def test_tension_only_has_independent_member_capability():
    model = example_model()
    model = replace(model, members=(replace(model.members[0], kind="tension_only"),))
    assert not build_compatibility_report(model, example_capabilities()).ok


def test_nodal_only_loading_still_requires_complete_model_profile():
    model = example_model()
    needed = requirements(model, model.states[0])
    assert needed.member_kinds == ("beam",)
    assert needed.load_kinds == ("nodal_force",)
    caps = example_capabilities()
    profile = replace(caps.profiles[0], load_kinds=())
    assert not build_compatibility_report(model, replace(caps, profiles=(profile,))).ok


def test_selfweight_without_explicit_load_is_checked():
    model = example_model()
    state = replace(model.states[0], gravity_m_s2=(D(0), D(0), D("-9.81")))
    model = replace(model, loads=(), states=(state,))
    caps = example_capabilities()
    assert not build_compatibility_report(model, caps).ok
    caps = replace(caps, profiles=(replace(caps.profiles[0], supports_gravity=True),))
    assert build_compatibility_report(model, caps).ok


def test_zero_load_state_is_not_skipped():
    model = replace(example_model(), loads=())
    caps = example_capabilities()
    caps = replace(caps, profiles=(replace(caps.profiles[0], member_kinds=("cable",)),))
    assert not build_compatibility_report(model, caps).ok


def test_simultaneous_load_kinds_require_one_covering_profile():
    model = example_model()
    model = replace(model, loads=model.loads + (TemperatureChange("T1", "LC1", "temperature_change", "M1", D(10)),))
    caps = example_capabilities()
    second = replace(caps.profiles[0], id="thermal-only", load_kinds=("temperature_change",))
    caps = replace(caps, profiles=caps.profiles + (second,))
    assert not build_compatibility_report(model, caps).ok
    complete = replace(second, id="combined", load_kinds=("nodal_force", "temperature_change"))
    assert build_compatibility_report(model, replace(caps, profiles=(complete,))).ok


def test_duplicate_profile_ids_are_rejected_not_overwritten():
    caps = example_capabilities()
    with pytest.raises(ContractError, match="duplicate capability profile"):
        replace(caps, profiles=caps.profiles + caps.profiles)


def test_alternative_profiles_with_unique_ids_remain_distinct():
    caps = example_capabilities()
    second = replace(caps.profiles[0], id="other", load_kinds=())
    assert len(replace(caps, profiles=caps.profiles + (second,)).profiles) == 2


def test_rotated_support_requires_explicit_capability():
    model = example_model()
    frame = Frame((D(0), D(1), D(0)), (D(-1), D(0), D(0)), (D(0), D(0), D(1)))
    model = replace(model, supports=(replace(model.supports[0], frame=frame),))
    assert not build_compatibility_report(model, example_capabilities()).ok


def test_compatibility_report_is_deterministic():
    caps = replace(example_capabilities(), supported_results=())
    one = build_compatibility_report(example_model(), caps)
    assert one == build_compatibility_report(example_model(), caps)
