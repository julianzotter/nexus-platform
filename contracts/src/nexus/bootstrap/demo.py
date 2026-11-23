"""Run a fixture replay from files. No external solver access."""
from pathlib import Path
from nexus.adapters.fixture_solver import FixtureSolver
from nexus.adapters.json_codec import loads_contract
from nexus.application.analysis import run_analysis
from nexus.domain.contracts.capabilities import SolverCapabilities
from nexus.domain.contracts.model import AnalysisModel
from nexus.domain.contracts.results import AnalysisResults


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    examples = root / "examples"
    model = loads_contract((examples / "model.json").read_bytes(), AnalysisModel)
    caps = loads_contract((examples / "capabilities.json").read_bytes(), SolverCapabilities)
    fixture = loads_contract((examples / "results_fixture.json").read_bytes(), AnalysisResults)
    results = run_analysis(model, FixtureSolver(caps, fixture))
    print(f"fixture replay PASS: {len(results.values)} scalar values; no calculation performed")


if __name__ == "__main__":
    main()
