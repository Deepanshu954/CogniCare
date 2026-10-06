import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_and_login_elderly(client):
    email = "margaret.test@example.com"
    reg_data = {
        "email": email,
        "password": "SecurePassword123!",
        "display_name": "Margaret Jenkins",
        "role": "ELDERLY",
        "phone_number": "+1-555-0199",
        "emergency_notes": "Allergic to penicillin",
    }
    # 1. Register
    reg_resp = client.post("/api/v1/auth/register", json=reg_data)
    assert reg_resp.status_code == 201
    data = reg_resp.json()
    assert "access_token" in data
    assert data["user"]["email"] == email
    assert data["user"]["role"] == "ELDERLY"
    assert data["user"]["patient_profile"] is not None

    # Verify cookies
    assert "cognicare_access_token" in reg_resp.cookies
    assert "cognicare_refresh_token" in reg_resp.cookies

    # 2. Duplicate registration fails
    dup_resp = client.post("/api/v1/auth/register", json=reg_data)
    assert dup_resp.status_code == 409

    # 3. Login
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePassword123!"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    # 4. Get Current User Profile
    me_resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["email"] == email
    assert me_data["profile"]["display_name"] == "Margaret Jenkins"


def test_login_invalid_credentials(client):
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "wrongpassword"},
    )
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "UNAUTHORIZED"


def test_me_unauthorized(client):
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code == 401
