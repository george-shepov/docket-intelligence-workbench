from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Mapping

from docket_workbench.domain.models import DocketEntry


@dataclass(frozen=True, slots=True)
class SourceRequest:
    case_number: str
    source_url: str | None = None


@dataclass(frozen=True, slots=True)
class SourceCapture:
    source_key: str
    case_number: str
    captured_at: datetime
    source_url: str | None
    raw_content: bytes
    entries: tuple[DocketEntry, ...]
    metadata: Mapping[str, str]


class CourtSourceAdapter(ABC):
    """Contract implemented by each court-specific data source."""

    source_key: str

    @abstractmethod
    async def capture(self, request: SourceRequest) -> SourceCapture:
        """Retrieve and parse the current public record for one case."""
        raise NotImplementedError

    @abstractmethod
    def parse(
        self,
        raw_content: bytes,
        *,
        source_url: str | None = None,
    ) -> tuple[DocketEntry, ...]:
        """Parse an already captured source without network access."""
        raise NotImplementedError
