from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_fastest_laps_rejects_invalid_limit() -> None:
    response = client.get("/api/analytics/events/1/fastest-laps?limit=0")

    assert response.status_code == 422


def test_fastest_laps_rejects_excessive_limit() -> None:
    response = client.get("/api/analytics/events/1/fastest-laps?limit=100")

    assert response.status_code == 422


def test_stints_rejects_long_driver_code() -> None:
    response = client.get("/api/analytics/events/1/stints" "?driver_code=VERSTAPPEN")

    assert response.status_code == 422
