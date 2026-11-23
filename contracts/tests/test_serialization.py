from dataclasses import replace
from decimal import Decimal as D
from pathlib import Path
import json
import pytest
from jsonschema import Draft202012Validator
from nexus.bootstrap.synthetic import example_model
from nexus.adapters.json_codec import JsonModelExchange, loads_contract
from nexus.adapters.schema_export import export_schema
from nexus.domain.contracts.base import ContractError
from nexus.domain.contracts.model import AnalysisModel, ResultRequest
from nexus.domain.contracts.capabilities import CompatibilityReport, SolverCapabilities
from nexus.domain.contracts.results import AnalysisResults
from nexus.domain.contracts.checks import CheckResult
from nexus.domain.contracts.exchange import MappingReport
from nexus.domain.services.canonical import canonical_bytes, content_hash, decimal_text

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = {"analysis_model": ("model", AnalysisModel),
             "result_request": ("result_request", ResultRequest),
             "solver_capabilities": ("capabilities", SolverCapabilities),
             "compatibility_report": ("compatibility_report", CompatibilityReport),
             "analysis_results": ("results_fixture", AnalysisResults),
             "check_result": ("check_result", CheckResult),
             "mapping_report": ("mapping_report", MappingReport)}


def test_json_model_roundtrip_is_identical():
    model = example_model()
    exchange = JsonModelExchange()
    blob, report = exchange.write(model)
    imported = exchange.read(blob)
    assert report.lossless and imported.report.lossless
    assert imported.model == model


@pytest.mark.parametrize("name", CONTRACTS)
def test_generated_schema_and_strict_codec_accept_synthetic_fixture(name):
    fixture, cls = CONTRACTS[name]
    schema = export_schema(cls)
    Draft202012Validator.check_schema(schema)
    raw = (ROOT / "examples" / f"{fixture}.json").read_bytes()
    Draft202012Validator(schema).validate(json.loads(raw))
    contract = loads_contract(raw, cls)
    assert loads_contract(canonical_bytes(contract), cls) == contract
    assert json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text()) == schema


@pytest.mark.parametrize("container", ["root", "member", "material"])
def test_unknown_fields_are_rejected_in_schema_and_runtime(container):
    payload = json.loads(canonical_bytes(example_model()))
    target = {"root": payload, "member": payload["members"][0], "material": payload["materials"][0]}[container]
    target["unsupported_feature"] = "must-not-disappear"
    assert not Draft202012Validator(export_schema(AnalysisModel)).is_valid(payload)
    with pytest.raises(ContractError):
        loads_contract(json.dumps(payload).encode(), AnalysisModel)


def test_duplicate_json_keys_rejected():
    with pytest.raises(ContractError, match="duplicate JSON"):
        loads_contract(b'{"model_id":"one","model_id":"two"}', AnalysisModel)


def test_float_json_tokens_rejected():
    raw = canonical_bytes(example_model()).replace(b'"210000000000"', b'210000000000.0')
    with pytest.raises(ContractError, match="floating-point"):
        loads_contract(raw, AnalysisModel)


def test_schema_is_not_a_substitute_for_cross_reference_validation():
    payload = json.loads(canonical_bytes(example_model()))
    payload["members"][0]["end_node_id"] = "missing"
    Draft202012Validator(export_schema(AnalysisModel)).validate(payload)
    with pytest.raises(ContractError, match="endpoint"):
        loads_contract(json.dumps(payload).encode(), AnalysisModel)


@pytest.mark.parametrize("first,second", [("1.0", "1.00"), ("-0", "0"), ("1E+3", "1000")])
def test_decimal_canonicalization_is_representation_independent(first, second):
    assert decimal_text(D(first)) == decimal_text(D(second))


def test_hash_binds_full_payload_and_preserves_order():
    model = example_model()
    changed = replace(model, revision="2")
    reordered = replace(model, nodes=tuple(reversed(model.nodes)))
    assert content_hash(model) != content_hash(changed)
    assert content_hash(model) != content_hash(reordered)
    raw = json.dumps(json.loads(canonical_bytes(model)), indent=4).encode()
    assert content_hash(loads_contract(raw, AnalysisModel)) == content_hash(model)


def test_nan_and_python_floats_cannot_be_hashed():
    for value in (D("NaN"), 1.25):
        with pytest.raises(ContractError):
            content_hash(value)
