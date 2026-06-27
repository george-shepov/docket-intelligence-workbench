from __future__ import annotations

from threading import RLock
from uuid import UUID

import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from docket_workbench import __version__
from docket_workbench.domain.models import CourtCase, DocketChange, DocketEntry
from docket_workbench.services.snapshots import build_snapshot, compare_snapshots
from docket_workbench.sources.cuyahoga import CuyahogaCommonPleasAdapter

app = FastAPI(
    title="Docket Intelligence Workbench",
    version=__version__,
    description="Public core for monitored court dockets and historical record comparison.",
)


class CaseCreate(BaseModel):
    case_number: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=300)
    court: str = Field(min_length=1, max_length=300)
    county: str | None = Field(default=None, max_length=120)
    source_key: str = Field(default="oh.cuyahoga.common_pleas", max_length=100)
    source_url: str | None = None
    monitoring_frequency: str = "daily"


class SnapshotCompareRequest(BaseModel):
    case_id: UUID
    previous: list[DocketEntry]
    current: list[DocketEntry]
    source_url: str | None = None


class CuyahogaParseRequest(BaseModel):
    html: str
    source_url: str | None = None


class CuyahogaParseResponse(BaseModel):
    entries: list[DocketEntry]


class MemoryCaseRepository:
    """Temporary foundation store; PostgreSQL persistence is the next porting step."""

    def __init__(self) -> None:
        self._items: dict[UUID, CourtCase] = {}
        self._lock = RLock()

    def create(self, item: CourtCase) -> CourtCase:
        with self._lock:
            if any(existing.case_number == item.case_number for existing in self._items.values()):
                raise ValueError("Case number already exists")
            self._items[item.id] = item
        return item

    def list(self) -> list[CourtCase]:
        with self._lock:
            return sorted(self._items.values(), key=lambda case: case.created_at)

    def get(self, case_id: UUID) -> CourtCase | None:
        with self._lock:
            return self._items.get(case_id)

    def clear(self) -> None:
        with self._lock:
            self._items.clear()


cases = MemoryCaseRepository()
cuyahoga = CuyahogaCommonPleasAdapter()


@app.get("/healthz")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.post("/api/v1/cases", response_model=CourtCase, status_code=status.HTTP_201_CREATED)
def create_case(request: CaseCreate) -> CourtCase:
    try:
        case = CourtCase.model_validate(request.model_dump())
        return cases.create(case)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.get("/api/v1/cases", response_model=list[CourtCase])
def list_cases() -> list[CourtCase]:
    return cases.list()


@app.get("/api/v1/cases/{case_id}", response_model=CourtCase)
def get_case(case_id: UUID) -> CourtCase:
    case = cases.get(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@app.post("/api/v1/dockets/compare", response_model=list[DocketChange])
def compare_dockets(request: SnapshotCompareRequest) -> list[DocketChange]:
    previous = build_snapshot(
        case_id=request.case_id,
        entries=request.previous,
        source_url=request.source_url,
    )
    current = build_snapshot(
        case_id=request.case_id,
        entries=request.current,
        source_url=request.source_url,
    )
    return compare_snapshots(previous, current)


@app.post("/api/v1/sources/cuyahoga/parse", response_model=CuyahogaParseResponse)
def parse_cuyahoga(request: CuyahogaParseRequest) -> CuyahogaParseResponse:
    try:
        entries = list(
            cuyahoga.parse(
                request.html.encode("utf-8"),
                source_url=request.source_url,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return CuyahogaParseResponse(entries=entries)


def run() -> None:
    uvicorn.run("docket_workbench.api.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run()
