from dataclasses import replace
from decimal import Decimal as D
import pytest
from nexus.bootstrap.synthetic import example_capabilities, example_model, example_results
from nexus.adapters.fixture_solver import FixtureSolver
from nexus.application.analysis import UnsupportedModelError, run_analysis
from nexus.domain.contracts.base import ContractError
from nexus.domain.contracts.results import Convergence, StateResult
from nexus.domain.services.result_validation import require_design_ready, validate_results


def test_fixture_replay_runs_without_solver_and_cannot_pass_design_gate():
    model = example_model()
    results = run_analysis(model, FixtureSolver(example_capabilities(), example_results(model)))
    with pytest.raises(ContractError, match="fixture"):
        require_design_ready(results)


def test_adapter_itself_checks_capabilities():
    model = example_model()
    adapter = FixtureSolver(replace(example_capabilities(), supported_results=()), example_results(model))
    with pytest.raises(ContractError, match="unsupported"):
        adapter.solve(model)
    with pytest.raises(UnsupportedModelError):
        run_analysis(model, adapter)


def test_result_wrong_model_hash_rejected():
    model = example_model()
    with pytest.raises(ContractError, match="hash"):
        validate_results(model, replace(example_results(model), model_hash="0"*64))


def test_result_wrong_identity_rejected():
    model = example_model()
    with pytest.raises(ContractError, match="identity"):
        validate_results(model, replace(example_results(model), model_revision="other"))


def test_solved_result_requires_every_selected_station_and_object():
    model = example_model()
    results = example_results(model)
    with pytest.raises(ContractError, match="missing"):
        validate_results(model, replace(results, values=results.values[:-1]))


def test_duplicate_results_rejected():
    model = example_model()
    results = example_results(model)
    with pytest.raises(ContractError, match="duplicate scalar"):
        replace(results, values=results.values + (results.values[0],))


@pytest.mark.parametrize("kwargs", [{"unit": "N"}, {"frame": "member_local"},
                                     {"value": D("NaN")}, {"station": D("0.5")}])
def test_invalid_scalar_metadata_rejected(kwargs):
    with pytest.raises(ContractError):
        replace(example_results(example_model()).values[0], **kwargs)


def test_result_unknown_object_not_silently_accepted():
    model = example_model()
    result = example_results(model)
    values = (replace(result.values[0], object_id="unknown"),) + result.values[1:]
    with pytest.raises(ContractError, match="unknown scalar"):
        validate_results(model, replace(result, values=values))


def test_partial_results_are_retained_but_block_design():
    model = example_model()
    results = example_results(model)
    partial = replace(results, execution_kind="solver", values=(), states=(
        StateResult("STATE1", "partial", Convergence("failed", "fixture divergence", D(1), 10)),))
    validate_results(model, partial)
    with pytest.raises(ContractError, match="partial"):
        require_design_ready(partial)


def test_claimed_solved_without_known_convergence_is_rejected():
    with pytest.raises(ContractError):
        StateResult("S", "solved", Convergence("unknown", "not reported"))


def test_wrong_adapter_identity_is_rejected_by_application():
    model = example_model()
    result = replace(example_results(model), adapter_version="other")
    adapter = FixtureSolver(example_capabilities(), result)
    with pytest.raises(ContractError, match="producer"):
        run_analysis(model, adapter)


def test_fixture_cannot_claim_real_solver_execution():
    model = example_model()
    with pytest.raises(ContractError, match="claim"):
        FixtureSolver(replace(example_capabilities(), execution_kind="solver"), example_results(model))
