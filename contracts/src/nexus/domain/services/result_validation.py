"""Result completeness and release prerequisites, without a design-code verdict."""
from __future__ import annotations
from decimal import Decimal
from nexus.domain.contracts.base import require
from nexus.domain.contracts.model import AnalysisModel
from nexus.domain.contracts.results import AnalysisResults, result_key
from .canonical import content_hash


def requested_keys(model: AnalysisModel) -> set[tuple[str, str, str, str, Decimal | None]]:
    return {
        (state_id, selection.object_kind, object_id, selection.quantity, station)
        for state_id in model.result_request.state_ids
        for selection in model.result_request.selections
        for object_id in selection.object_ids
        for station in selection.stations or (None,)
    }


def validate_results(model: AnalysisModel, results: AnalysisResults) -> None:
    require((results.model_id, results.model_revision) == (model.model_id, model.revision),
            "result model identity mismatch")
    require(results.model_hash == content_hash(model), "result model hash mismatch")
    require({state.state_id for state in results.states} == set(model.result_request.state_ids),
            "result state coverage mismatch")
    actual = {result_key(value) for value in results.values}
    expected = requested_keys(model)
    require(actual <= expected, "unrequested or unknown scalar result")
    for state in results.states:
        if state.status == "solved":
            require({key for key in actual if key[0] == state.state_id} ==
                    {key for key in expected if key[0] == state.state_id},
                    "solved state has missing scalar results")
            theory = next(s.theory for s in model.states if s.id == state.state_id)
            if theory != "linear_static":
                require(state.convergence.status == "converged",
                        "nonlinear state requires convergence evidence")


def require_design_ready(results: AnalysisResults) -> None:
    """Necessary gate only. Does not certify mechanics or engineering approval."""
    require(results.execution_kind == "solver", "fixture results are not engineering evidence")
    require(all(state.status == "solved" for state in results.states),
            "partial/failed results cannot enter a design check")
