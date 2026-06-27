from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from typing import Iterable
from uuid import UUID

from docket_workbench.domain.models import (
    ChangeKind,
    DocketChange,
    DocketEntry,
    DocketSnapshot,
)

_WHITESPACE = re.compile(r"\s+")


def normalize_text(value: str) -> str:
    """Normalize source text without changing its substantive meaning."""
    return _WHITESPACE.sub(" ", value).strip()


def entry_identity(entry: DocketEntry) -> str:
    """Build a stable identity for matching an entry between snapshots."""
    if entry.source_id:
        return f"source:{entry.source_id}"

    raw = "|".join(
        (
            entry.filed_on.isoformat(),
            normalize_text(entry.side).casefold(),
            normalize_text(entry.entry_type).casefold(),
            str(entry.position),
        )
    )
    return "derived:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _canonical_entry(entry: DocketEntry) -> dict[str, object]:
    return {
        "source_id": entry.source_id,
        "filed_on": entry.filed_on.isoformat(),
        "side": normalize_text(entry.side),
        "entry_type": normalize_text(entry.entry_type),
        "description": normalize_text(entry.description),
        "document_url": str(entry.document_url) if entry.document_url else None,
        "position": entry.position,
    }


def snapshot_hash(entries: Iterable[DocketEntry]) -> str:
    payload = [_canonical_entry(entry) for entry in entries]
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def build_snapshot(
    *,
    case_id: UUID,
    entries: Iterable[DocketEntry],
    source_url: str | None = None,
    captured_at: datetime | None = None,
) -> DocketSnapshot:
    entry_tuple = tuple(entries)
    return DocketSnapshot(
        case_id=case_id,
        captured_at=captured_at or datetime.now(timezone.utc),
        source_url=source_url,
        content_sha256=snapshot_hash(entry_tuple),
        entries=entry_tuple,
    )


def compare_snapshots(
    previous: DocketSnapshot,
    current: DocketSnapshot,
) -> list[DocketChange]:
    if previous.case_id != current.case_id:
        raise ValueError("Snapshots must belong to the same case")

    previous_by_key = _group_by_identity(previous.entries)
    current_by_key = _group_by_identity(current.entries)
    changes: list[DocketChange] = []

    all_keys = sorted(set(previous_by_key) | set(current_by_key))
    for key in all_keys:
        old_entries = previous_by_key.get(key, [])
        new_entries = current_by_key.get(key, [])
        pair_count = min(len(old_entries), len(new_entries))

        for index in range(pair_count):
            old = old_entries[index]
            new = new_entries[index]
            if _canonical_entry(old) != _canonical_entry(new):
                changes.append(
                    DocketChange(
                        kind=ChangeKind.MODIFIED,
                        identity=key,
                        summary=f"Modified docket entry dated {new.filed_on.isoformat()}",
                        previous=old,
                        current=new,
                    )
                )

        for old in old_entries[pair_count:]:
            changes.append(
                DocketChange(
                    kind=ChangeKind.REMOVED,
                    identity=key,
                    summary=f"Entry no longer present in latest snapshot: {old.entry_type}",
                    previous=old,
                )
            )

        for new in new_entries[pair_count:]:
            changes.append(
                DocketChange(
                    kind=ChangeKind.ADDED,
                    identity=key,
                    summary=f"New docket entry: {new.entry_type}",
                    current=new,
                )
            )

    return changes


def _group_by_identity(entries: Iterable[DocketEntry]) -> dict[str, list[DocketEntry]]:
    grouped: dict[str, list[DocketEntry]] = defaultdict(list)
    for entry in entries:
        grouped[entry_identity(entry)].append(entry)
    return grouped
