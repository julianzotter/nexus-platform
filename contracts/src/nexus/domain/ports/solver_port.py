from typing import Protocol
from nexus.domain.contracts.model import AnalysisModel
from nexus.domain.contracts.results import AnalysisResults
from nexus.domain.contracts.capabilities import SolverCapabilities


class SolverPort(Protocol):
    def capabilities(self) -> SolverCapabilities: ...
    def solve(self, model: AnalysisModel) -> AnalysisResults: ...
