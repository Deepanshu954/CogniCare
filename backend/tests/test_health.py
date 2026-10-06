import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_liveness(client):
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "request_id" in data
    assert response.headers.get("X-Request-ID") == data["request_id"]

def test_readiness(client):
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["database"] == "connected"
