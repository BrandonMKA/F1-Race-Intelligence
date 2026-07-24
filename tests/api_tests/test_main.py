from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_root() -> None:
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "name": "F1 Race Intelligence API",
        "status": "running",
        "documentation": "/docs",
    }


def test_openapi_is_available() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == (
        "F1 Race Intelligence API"
    )