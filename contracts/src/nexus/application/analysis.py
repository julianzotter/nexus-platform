from nexus.domain.contracts.base import ContractError, require
from nexus.domain.contracts.model import AnalysisModel
from nexus.domain.contracts.results import AnalysisResults
from nexus.domain.ports.solver_port import SolverPort
from nexus.domain.services.compatibility import build_compatibility_report
from nexus.domain.services.result_validation import validate_results


class UnsupportedModelError(ContractError):
    """The selected adapter cannot represent the entire requested analysis."""


def run_analysis(model: AnalysisModel, solver: SolverPort) -> AnalysisResults:
    caps = solver.capabilities()
    report = build_compatibility_report(model, caps)
    if not report.ok:
        raise UnsupportedModelError(repr(report.issues))
    results = solver.solve(model)
    require((results.solver_name, results.solver_version, results.adapter_version,
             results.execution_kind) ==
            (caps.solver_name, caps.solver_version, caps.adapter_version, caps.execution_kind),
            "result producer does not match selected capabilities")
    validate_results(model, results)
    return results
