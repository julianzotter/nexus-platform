from typing import Protocol
from nexus.domain.contracts.exchange import ImportedModel, MappingReport
from nexus.domain.contracts.model import AnalysisModel


class ExchangePort(Protocol):
    """An analytical-model exchange port, not a universal drawing-data port."""
    def read(self, source: bytes) -> ImportedModel: ...
    def write(self, model: AnalysisModel) -> tuple[bytes, MappingReport]: ...
