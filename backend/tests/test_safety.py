import pytest


def test_sos_lifecycle_and_caregiver_notifications(client):
    # 1. Register Caregiver
    cg_res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "carol.alert@example.com",
            "password": "Password123!",
            "display_name": "Carol Danvers",
            "role": "CAREGIVER",
        },
    )
    assert cg_res.status_code == 201
    cg_token = cg_res.json()["access_token"]
    cg_headers = {"Authorization": f"Bearer {cg_token}"}

    # 2. Caregiver creates Patient profile
    pat_res = client.post(
        "/api/v1/patients",
        headers=cg_headers,
        json={"display_name": "George Bailey", "email": "george.sos@example.com"},
    )
    assert pat_res.status_code == 201
    patient_id = pat_res.json()["id"]

    # 3. Patient triggers SOS
    sos_res = client.post(
        f"/api/v1/patients/{patient_id}/sos",
        headers=cg_headers,  # Or patient headers
        json={"message": "Fell in garden near porch", "location_note": "Backyard"},
    )
    assert sos_res.status_code == 201
    alert = sos_res.json()
    assert alert["alert_type"] == "SOS"
    assert alert["severity"] == "CRITICAL"
    assert alert["status"] == "OPEN"
    alert_id = alert["id"]

    # 4. Caregiver checks notifications
    notif_res = client.get("/api/v1/notifications", headers=cg_headers)
    assert notif_res.status_code == 200
    notifs = notif_res.json()
    assert len(notifs) >= 1
    assert "Emergency SOS" in notifs[0]["title"]

    # 5. Caregiver acknowledges alert
    ack_res = client.post(
        f"/api/v1/patients/{patient_id}/alerts/{alert_id}/acknowledge",
        headers=cg_headers,
    )
    assert ack_res.status_code == 200
    assert ack_res.json()["status"] == "ACKNOWLEDGED"

    # 6. Caregiver resolves alert with note
    res_res = client.post(
        f"/api/v1/patients/{patient_id}/alerts/{alert_id}/resolve",
        headers=cg_headers,
        json={"note": "Arrived on scene. Patient is safe, no injuries."},
    )
    assert res_res.status_code == 200
    resolved = res_res.json()
    assert resolved["status"] == "RESOLVED"
    assert len(resolved["events"]) >= 3
