from pathlib import Path

from docket_workbench.sources.cuyahoga import CuyahogaCommonPleasAdapter


def test_parser_reads_sanitized_cuyahoga_fixture() -> None:
    html = Path("tests/fixtures/cuyahoga_docket.html").read_bytes()
    adapter = CuyahogaCommonPleasAdapter()

    entries = adapter.parse(
        html,
        source_url="https://cpdocket.cp.cuyahogacounty.gov/",
    )

    assert len(entries) == 2
    assert entries[0].source_id == "entry-1001"
    assert entries[0].entry_type == "Motion"
    assert str(entries[0].document_url) == (
        "https://cpdocket.cp.cuyahogacounty.gov/Document/1001"
    )
    assert entries[1].description == "Brief in opposition."
