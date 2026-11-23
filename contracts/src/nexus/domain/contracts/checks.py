"""Evidence-bound generic findings. No Eurocode/AISC algorithm is supplied."""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Literal
from .base import Contract, identifier, require, sha256_text


@dataclass(frozen=True, slots=True)
class StandardReference(Contract):
    document_id: str
    edition: str
    clauses: tuple[str, ...]
    national_annex_id: str | None = None
    national_annex_edition: str | None = None
    amendments: tuple[str, ...] = ()

    def _validate(self) -> None:
        identifier(self.document_id)
        identifier(self.edition)
        require(bool(self.clauses), "specific clauses required")
        require((self.national_annex_id is None) == (self.national_annex_edition is None),
                "NA identifier and edition must be supplied together")


@dataclass(frozen=True, slots=True)
class EvidenceReference(Contract):
    id: str
    uri: str
    version: str
    locator: str
    sha256: str | None = None

    def _validate(self) -> None:
        for value in (self.id, self.uri, self.version, self.locator):
            identifier(value)
        if self.sha256 is not None:
            sha256_text(self.sha256)


@dataclass(frozen=True, slots=True)
class Finding(Contract):
    id: str
    object_ref: str
    state_id: str
    status: Literal["pass", "fail", "not_evaluated"]
    message: str
    evidence_ids: tuple[str, ...]
    value: Decimal | None = None
    unit: str | None = None

    def _validate(self) -> None:
        for text in (self.id, self.object_ref, self.state_id, self.message):
            identifier(text)
        require(bool(self.evidence_ids), "every finding needs evidence")
        require((self.value is None) == (self.unit is None), "value and unit required together")


@dataclass(frozen=True, slots=True)
class CheckResult(Contract):
    schema_version: Literal["nexus-check/0.1"]
    model_hash: str
    results_hash: str
    method_id: str
    method_version: str
    scope: tuple[str, ...]
    exclusions: tuple[str, ...]
    standards: tuple[StandardReference, ...]
    evidence: tuple[EvidenceReference, ...]
    findings: tuple[Finding, ...]

    def _validate(self) -> None:
        sha256_text(self.model_hash)
        sha256_text(self.results_hash)
        identifier(self.method_id)
        identifier(self.method_version)
        require(bool(self.scope) and bool(self.findings), "scope and findings required")
        ids = [evidence.id for evidence in self.evidence]
        require(len(ids) == len(set(ids)), "duplicate evidence IDs")
        finding_ids = [finding.id for finding in self.findings]
        require(len(finding_ids) == len(set(finding_ids)), "duplicate finding IDs")
        require(all(set(finding.evidence_ids) <= set(ids) for finding in self.findings),
                "unknown finding evidence")

    @property
    def status(self) -> Literal["pass", "fail", "not_evaluated"]:
        if any(f.status == "fail" for f in self.findings):
            return "fail"
        if any(f.status == "not_evaluated" for f in self.findings):
            return "not_evaluated"
        return "pass"
