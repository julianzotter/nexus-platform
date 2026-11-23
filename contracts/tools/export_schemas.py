"""Regenerate structural schemas from the authoritative Python contract types."""
import json
from pathlib import Path
from nexus.adapters.schema_export import export_schema
from nexus.domain.contracts.model import AnalysisModel, ResultRequest
from nexus.domain.contracts.capabilities import SolverCapabilities, CompatibilityReport
from nexus.domain.contracts.results import AnalysisResults
from nexus.domain.contracts.checks import CheckResult
from nexus.domain.contracts.exchange import MappingReport


def main() -> None:
    folder = Path(__file__).resolve().parents[1] / "schemas"
    folder.mkdir(exist_ok=True)
    contracts = {"analysis_model": AnalysisModel, "result_request": ResultRequest,
                 "solver_capabilities": SolverCapabilities, "compatibility_report": CompatibilityReport,
                 "analysis_results": AnalysisResults, "check_result": CheckResult,
                 "mapping_report": MappingReport}
    for name, contract in contracts.items():
        text = json.dumps(export_schema(contract), indent=2, ensure_ascii=False) + "\n"
        (folder / f"{name}.schema.json").write_text(text, encoding="utf-8")
    print(f"exported {len(contracts)} schemas")


if __name__ == "__main__":
    main()
