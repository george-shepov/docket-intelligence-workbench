from datetime import date
from uuid import uuid4

from docket_workbench.domain.models import ChangeKind, DocketEntry
from docket_workbench.services.snapshots import build_snapshot, compare_snapshots


def entry(description: str, *, source_id: str, position: int = 0) -> DocketEntry:
    return DocketEntry(
        source_id=source_id,
        filed_on=date(2026, 6, 20),
        side="P1",
        entry_type="Motion",
        description=description,
        position=position,
    )


def test_compare_snapshots_detects_added_removed_and_modified_entries() -> None:
    case_id = uuid4()
    previous = build_snapshot(
        case_id=case_id,
        entries=[
            entry("Original description", source_id="1"),
            entry("Removed later", source_id="2", position=1),
        ],
    )
    current = build_snapshot(
        case_id=case_id,
        entries=[
            entry("Corrected description", source_id="1"),
            entry("New entry", source_id="3", position=1),
        ],
    )

    changes = compare_snapshots(previous, current)

    assert {change.kind for change in changes} == {
        ChangeKind.ADDED,
        ChangeKind.REMOVED,
        ChangeKind.MODIFIED,
    }


def test_snapshot_hash_is_deterministic() -> None:
    case_id = uuid4()
    first = build_snapshot(case_id=case_id, entries=[entry("Same", source_id="1")])
    second = build_snapshot(case_id=case_id, entries=[entry("Same", source_id="1")])

    assert first.content_sha256 == second.content_sha256
