"""Replay a supplied fixture. No calculation and no engineering capability claim."""
from dataclasses import dataclass
from nexus.domain.contracts.base import require
from nexus.domain.contracts.model import AnalysisModel
from nexus.domain.contracts.results import AnalysisResults
from nexus.domain.contracts.capabilities import SolverCapabilities
from nexus.domain.services.compatibility import build_compatibility_report
from nexus.domain.services.result_validation import validate_results


@dataclass(frozen=True, slots=True)
class FixtureSolver:
    declared_capabilities: SolverCapabilities
    fixture: AnalysisResults

    def __post_init__(self) -> None:
        require(self.declared_capabilities.execution_kind == "fixture_only",
                "fixture adapter cannot claim solver execution")
        require(self.fixture.execution_kind == "fixture_only", "fixture must be labelled")

    def capabilities(self) -> SolverCapabilities:
        return self.declared_capabilities

    def solve(self, model: AnalysisModel) -> AnalysisResults:
        report = build_compatibility_report(model, self.capabilities())
        require(report.ok, f"unsupported model: {report.issues}")
        validate_results(model, self.fixture)
        return self.fixture
