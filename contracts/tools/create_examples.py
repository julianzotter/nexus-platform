import json
from pathlib import Path
from nexus.bootstrap.synthetic import example_capabilities, example_model, example_results
from nexus.domain.contracts.checks import CheckResult, EvidenceReference, Finding
from nexus.domain.contracts.exchange import MappingReport
from nexus.domain.services.canonical import canonical_bytes, content_hash
from nexus.domain.services.compatibility import build_compatibility_report


def main() -> None:
    model = example_model()
    caps = example_capabilities()
    results = example_results(model)
    check = CheckResult(
        "nexus-check/0.1", content_hash(model), content_hash(results), "fixture-status", "0.1.0",
        ("software contract demonstration",), ("engineering design",), (),
        (EvidenceReference("E1", "docs/QA.md", "0.1.0", "fixture-only"),),
        (Finding("F1", "model", "STATE1", "not_evaluated", "No design calculation supplied", ("E1",)),),
    )
    objects = {"model": model, "result_request": model.result_request, "capabilities": caps,
               "results_fixture": results, "check_result": check,
               "compatibility_report": build_compatibility_report(model, caps),
               "mapping_report": MappingReport("nexus-json/0.1", model.schema_version, ())}
    folder = Path(__file__).resolve().parents[1] / "examples"
    folder.mkdir(exist_ok=True)
    for name, contract in objects.items():
        payload = json.loads(canonical_bytes(contract))
        (folder / f"{name}.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"exported {len(objects)} synthetic fixtures; no structural calculation")


if __name__ == "__main__":
    main()
