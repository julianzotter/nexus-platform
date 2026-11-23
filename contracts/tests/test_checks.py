from dataclasses import replace
from decimal import Decimal as D
from pathlib import Path
import pytest
from nexus.adapters.json_codec import loads_contract
from nexus.domain.contracts.base import ContractError
from nexus.domain.contracts.checks import CheckResult, StandardReference


def test_standard_id_edition_and_na_edition_are_separate():
    reference = StandardReference("SYNTHETIC-RULE", "1", ("software-only",), "SYNTHETIC-NA", "2")
    assert reference.edition != reference.national_annex_edition
    with pytest.raises(ContractError, match="NA"):
        replace(reference, national_annex_edition=None)


def test_finding_evidence_cannot_point_to_unknown_reference():
    path = Path(__file__).resolve().parents[1] / "examples/check_result.json"
    check = loads_contract(path.read_bytes(), CheckResult)
    assert check.status == "not_evaluated"
    with pytest.raises(ContractError, match="evidence"):
        replace(check, evidence=())
    with pytest.raises(ContractError, match="together"):
        replace(check.findings[0], value=D(1))
