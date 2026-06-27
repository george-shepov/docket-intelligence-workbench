from __future__ import annotations

from datetime import UTC, date, datetime
from enum import StrEnum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class MonitoringFrequency(StrEnum):
    HOURLY = "hourly"
    TWICE_DAILY = "twice_daily"
    DAILY = "daily"
    WEEKLY = "weekly"
    MANUAL = "manual"


class ChangeKind(StrEnum):
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"


class CourtCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    case_number: Annotated[str, Field(min_length=1, max_length=100)]
    title: Annotated[str, Field(min_length=1, max_length=300)]
    court: Annotated[str, Field(min_length=1, max_length=300)]
    county: str | None = Field(default=None, max_length=120)
    source_key: Annotated[str, Field(min_length=1, max_length=100)]
    source_url: HttpUrl | None = None
    monitoring_frequency: MonitoringFrequency = MonitoringFrequency.DAILY
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("case_number", "title", "court", "county", "source_key", mode="before")
    @classmethod
    def strip_strings(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class DocketEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str | None = Field(default=None, max_length=200)
    filed_on: date
    side: str = Field(default="", max_length=100)
    entry_type: str = Field(default="", max_length=200)
    description: str = Field(default="", max_length=20_000)
    document_url: HttpUrl | None = None
    position: int = Field(ge=0)

    @field_validator("source_id", "side", "entry_type", "description", mode="before")
    @classmethod
    def normalize_strings(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        return " ".join(value.split())


class DocketSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    case_id: UUID
    captured_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source_url: HttpUrl | None = None
    content_sha256: Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
    entries: tuple[DocketEntry, ...]


class DocketChange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: ChangeKind
    identity: str
    summary: str
    previous: DocketEntry | None = None
    current: DocketEntry | None = None
