from fastapi.testclient import TestClient

from backend.api.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_task() -> None:
    response = client.post(
        "/v1/tasks/analyze",
        json={"task": "buat laporan"},
    )
    assert response.status_code == 200
    assert response.json()["analysis"]["normalized_goal"] == "buat laporan"


def test_analyze_rejects_unknown_fields() -> None:
    response = client.post(
        "/v1/tasks/analyze",
        json={"task": "buat laporan", "admin": True},
    )
    assert response.status_code == 422
