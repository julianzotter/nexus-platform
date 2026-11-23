"""Explicit mapping losses, with no assertion of universal IFC/DXF equivalence."""
from dataclasses import dataclass
from typing import Literal
from .base import Contract, identifier, require
from .model import AnalysisModel


@dataclass(frozen=True, slots=True)
class MappingIssue(Contract):
    source_ref: str
    code: str
    severity: Literal["warning", "error", "loss"]
    message: str


@dataclass(frozen=True, slots=True)
class MappingReport(Contract):
    source_format: str
    target_schema: str
    issues: tuple[MappingIssue, ...]

    @property
    def lossless(self) -> bool:
        return not any(issue.severity in ("loss", "error") for issue in self.issues)


@dataclass(frozen=True, slots=True)
class ImportedModel(Contract):
    model: AnalysisModel | None
    report: MappingReport

    def _validate(self) -> None:
        require(self.model is not None or not self.report.lossless,
                "missing model requires reported loss/error")
