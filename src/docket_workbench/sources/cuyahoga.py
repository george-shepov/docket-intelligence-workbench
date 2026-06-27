from __future__ import annotations

from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from docket_workbench.domain.models import DocketEntry
from docket_workbench.sources.base import CourtSourceAdapter, SourceCapture, SourceRequest

_TABLE_ID = "SheetContentPlaceHolder_caseDocket_gvDocketInformation"
_DATE_FORMATS = ("%m/%d/%Y", "%m/%d/%y")


class CuyahogaCommonPleasAdapter(CourtSourceAdapter):
    """Parser-first adapter for Cuyahoga County Common Pleas docket HTML."""

    source_key = "oh.cuyahoga.common_pleas"

    async def capture(self, request: SourceRequest) -> SourceCapture:
        raise NotImplementedError(
            "Live capture is intentionally deferred; use parse() with a saved public HTML capture."
        )

    def parse(
        self,
        raw_content: bytes,
        *,
        source_url: str | None = None,
    ) -> tuple[DocketEntry, ...]:
        soup = BeautifulSoup(raw_content, "html.parser")
        table = soup.find("table", id=_TABLE_ID)
        if table is None:
            table = soup.find("table", class_="gridview")
        if table is None:
            raise ValueError("Cuyahoga docket table was not found")

        entries: list[DocketEntry] = []
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 4:
                continue

            filed_on = _parse_date(cells[0].get_text(" ", strip=True))
            if filed_on is None:
                continue

            document_url: str | None = None
            if len(cells) >= 5:
                link = cells[4].find("a", href=True)
                if link is not None:
                    href = str(link["href"]).strip()
                    document_url = urljoin(source_url or "", href) if href else None

            source_id = row.get("data-entry-id") or row.get("id")
            entries.append(
                DocketEntry(
                    source_id=str(source_id) if source_id else None,
                    filed_on=filed_on,
                    side=cells[1].get_text(" ", strip=True),
                    entry_type=cells[2].get_text(" ", strip=True),
                    description=cells[3].get_text(" ", strip=True),
                    document_url=document_url,
                    position=len(entries),
                )
            )

        return tuple(entries)


def _parse_date(value: str):
    for date_format in _DATE_FORMATS:
        try:
            return datetime.strptime(value.strip(), date_format).date()
        except ValueError:
            continue
    return None
