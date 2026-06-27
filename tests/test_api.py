from fastapi.testclient import TestClient

from docket_workbench.api.main import app, cases


client = TestClient(app)


def setup_function() -> None:
    cases.clear()


def test_health() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_read_case() -> None:
    created = client.post(
        "/api/v1/cases",
        json={
            "case_number": "CR-26-000001",
            "title": "Synthetic demonstration case",
            "court": "Example Court of Common Pleas",
            "county": "Example",
            "source_key": "oh.example.common_pleas",
            "monitoring_frequency": "daily",
        },
    )

    assert created.status_code == 201
    case_id = created.json()["id"]

    fetched = client.get(f"/api/v1/cases/{case_id}")
    assert fetched.status_code == 200
    assert fetched.json()["case_number"] == "CR-26-000001"
