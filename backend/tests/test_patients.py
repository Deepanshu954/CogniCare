import pytest


def test_caregiver_patient_lifecycle_and_isolation(client):
    # 1. Register Caregiver Sarah
    cg_res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "sarah.caregiver@example.com",
            "password": "CaregiverPass123!",
            "display_name": "Sarah Connor",
            "role": "CAREGIVER",
        },
    )
    assert cg_res.status_code == 201
    sarah_token = cg_res.json()["access_token"]
    sarah_headers = {"Authorization": f"Bearer {sarah_token}"}

    # 2. Sarah creates patient profile for Margaret
    pat_res = client.post(
        "/api/v1/patients",
        headers=sarah_headers,
        json={
            "display_name": "Margaret Connor",
            "email": "margaret.connor@example.com",
            "emergency_notes": "Mild short-term memory loss; needs morning reminder",
            "accessibility_preferences": {"high_contrast": True, "large_text": True},
        },
    )
    assert pat_res.status_code == 201
    patient = pat_res.json()
    patient_id = patient["id"]
    assert patient["display_name"] == "Margaret Connor"
    assert len(patient["caregivers"]) == 1
    assert patient["caregivers"][0]["relationship_type"] == "Primary Caregiver"

    # 3. Add emergency contact
    contact_res = client.post(
        f"/api/v1/patients/{patient_id}/emergency-contacts",
        headers=sarah_headers,
        json={
            "name": "Dr. Emily Watson",
            "relationship_type": "Primary Neurologist",
            "phone": "+1-555-0144",
            "priority": 1,
        },
    )
    assert contact_res.status_code == 200
    assert contact_res.json()["name"] == "Dr. Emily Watson"

    # 4. Add Consent
    consent_res = client.post(
        f"/api/v1/patients/{patient_id}/consents",
        headers=sarah_headers,
        json={
            "purpose": "VOICE_PROCESSING",
            "policy_version": "v1.0",
            "granted": True,
        },
    )
    assert consent_res.status_code == 200
    assert consent_res.json()["purpose"] == "VOICE_PROCESSING"

    # 5. Get Patient Summary
    summary_res = client.get(
        f"/api/v1/patients/{patient_id}/summary",
        headers=sarah_headers,
    )
    assert summary_res.status_code == 200
    summary = summary_res.json()
    assert summary["display_name"] == "Margaret Connor"
    assert summary["status"] == "EXCELLENT"

    # 6. Data Isolation Verification: Unlinked Caregiver Bob cannot access Margaret
    bob_res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "bob.stranger@example.com",
            "password": "StrangerPass123!",
            "display_name": "Bob Stranger",
            "role": "CAREGIVER",
        },
    )
    assert bob_res.status_code == 201
    bob_headers = {"Authorization": f"Bearer {bob_res.json()['access_token']}"}

    # Bob attempts to get Margaret's details -> must return 403 Forbidden
    forbidden_res = client.get(f"/api/v1/patients/{patient_id}", headers=bob_headers)
    assert forbidden_res.status_code == 403
    assert forbidden_res.json()["error"]["code"] == "FORBIDDEN"
