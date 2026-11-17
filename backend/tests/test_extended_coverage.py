import pytest
from datetime import datetime, timezone


def test_patient_extended_lifecycle(client):
    # 1. Register Caregiver
    cg_res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "dr.elena@example.com",
            "password": "Password123!",
            "display_name": "Dr. Elena Vance",
            "role": "CAREGIVER",
        },
    )
    assert cg_res.status_code == 201
    auth_header = {"Authorization": f"Bearer {cg_res.json()['access_token']}"}

    # 2. Create Patient
    pat_res = client.post(
        "/api/v1/patients",
        headers=auth_header,
        json={"display_name": "Gordon Freeman", "email": "gordon@example.com"},
    )
    assert pat_res.status_code == 201
    patient_id = pat_res.json()["id"]

    # 3. Update Patient Preferences
    patch_res = client.patch(
        f"/api/v1/patients/{patient_id}",
        headers=auth_header,
        json={
            "display_name": "Dr. Gordon Freeman",
            "emergency_notes": "Allergic to penicillin.",
            "accessibility_preferences": {
                "font_size": "LARGE",
                "high_contrast": True,
                "sound_enabled": True,
            },
        },
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["display_name"] == "Dr. Gordon Freeman"
    assert patch_res.json()["emergency_notes"] == "Allergic to penicillin."

    # 4. Add Emergency Contact
    contact_res = client.post(
        f"/api/v1/patients/{patient_id}/emergency-contacts",
        headers=auth_header,
        json={
            "name": "Eli Vance",
            "relationship_type": "Colleague / Guardian",
            "phone": "+1-555-0199",
            "priority": 1,
        },
    )
    assert contact_res.status_code == 200
    assert contact_res.json()["name"] == "Eli Vance"

    # 5. Add Consent Record
    consent_res = client.post(
        f"/api/v1/patients/{patient_id}/consents",
        headers=auth_header,
        json={
            "purpose": "DATA_SHARING",
            "policy_version": "v1.0",
            "granted": True,
        },
    )
    assert consent_res.status_code == 200
    assert consent_res.json()["purpose"] == "DATA_SHARING"
    assert consent_res.json()["granted"] is True

    # 6. Invite another Caregiver
    sec_cg = client.post(
        "/api/v1/auth/register",
        json={
            "email": "alyx.vance@example.com",
            "password": "Password123!",
            "display_name": "Alyx Vance",
            "role": "CAREGIVER",
        },
    )
    assert sec_cg.status_code == 201
    invite_res = client.post(
        f"/api/v1/patients/{patient_id}/caregivers/invite",
        headers=auth_header,
        json={
            "caregiver_email": "alyx.vance@example.com",
            "relationship_type": "Daughter",
            "permissions": ["VIEW_PROFILE", "VIEW_COGNITION", "VIEW_REMINDERS"],
        },
    )
    assert invite_res.status_code == 200
    assert invite_res.json()["caregiver_email"] == "alyx.vance@example.com"


def test_care_medication_routine_extended(client):
    # Setup caregiver & patient
    cg_res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "nurse.joy@example.com",
            "password": "Password123!",
            "display_name": "Nurse Joy",
            "role": "CAREGIVER",
        },
    )
    auth_header = {"Authorization": f"Bearer {cg_res.json()['access_token']}"}

    pat_res = client.post(
        "/api/v1/patients",
        headers=auth_header,
        json={"display_name": "Professor Oak", "email": "oak@example.com"},
    )
    patient_id = pat_res.json()["id"]

    # 1. Create Medication
    med_res = client.post(
        f"/api/v1/patients/{patient_id}/medications",
        headers=auth_header,
        json={
            "name": "Memantine",
            "dosage_text": "5mg",
            "instructions": "Take once daily",
            "schedules": [
                {
                    "schedule_type": "DAILY",
                    "time_of_day": "09:00",
                    "criticality": "HIGH",
                }
            ],
        },
    )
    assert med_res.status_code == 201
    med_id = med_res.json()["id"]

    # 2. Update Medication
    patch_med = client.patch(
        f"/api/v1/patients/{patient_id}/medications/{med_id}",
        headers=auth_header,
        json={"dosage_text": "10mg", "instructions": "Take twice daily with water"},
    )
    assert patch_med.status_code == 200
    assert patch_med.json()["dosage_text"] == "10mg"

    # 3. Create Routine
    rout_res = client.post(
        f"/api/v1/patients/{patient_id}/routines",
        headers=auth_header,
        json={
            "routine_type": "EXERCISE",
            "title": "Garden Walk",
            "description": "Walk around garden for 15 minutes",
            "scheduled_time": "10:00",
        },
    )
    assert rout_res.status_code == 201
    assert rout_res.json()["title"] == "Garden Walk"

    # 4. Fetch Today's Reminders & Skip One
    today_res = client.get(f"/api/v1/patients/{patient_id}/reminders/today", headers=auth_header)
    assert today_res.status_code == 200
    rems = today_res.json()
    assert len(rems) >= 1
    rem_to_skip = rems[0]

    skip_res = client.post(
        f"/api/v1/patients/{patient_id}/reminders/{rem_to_skip['id']}/skip",
        headers=auth_header,
        json={"reason": "Patient resting peacefully"},
    )
    assert skip_res.status_code == 200
    assert skip_res.json()["status"] == "SKIPPED"

    # 5. Deactivate Medication
    del_res = client.delete(f"/api/v1/patients/{patient_id}/medications/{med_id}", headers=auth_header)
    assert del_res.status_code == 204


def test_safety_resolve_and_notifications(client):
    # Setup caregiver & patient
    cg_res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "clara.oswald@example.com",
            "password": "Password123!",
            "display_name": "Clara Oswald",
            "role": "CAREGIVER",
        },
    )
    auth_header = {"Authorization": f"Bearer {cg_res.json()['access_token']}"}

    pat_res = client.post(
        "/api/v1/patients",
        headers=auth_header,
        json={"display_name": "The Doctor", "email": "doctor@example.com"},
    )
    patient_id = pat_res.json()["id"]

    # 1. Trigger SOS
    sos_res = client.post(
        f"/api/v1/patients/{patient_id}/sos",
        headers=auth_header,
        json={"message": "Accidental trigger during test"},
    )
    assert sos_res.status_code == 201
    alert_id = sos_res.json()["id"]

    # 2. Acknowledge Alert
    ack_res = client.post(
        f"/api/v1/patients/{patient_id}/alerts/{alert_id}/acknowledge",
        headers=auth_header,
    )
    assert ack_res.status_code == 200
    assert ack_res.json()["status"] == "ACKNOWLEDGED"

    # 3. Resolve Alert
    res_res = client.post(
        f"/api/v1/patients/{patient_id}/alerts/{alert_id}/resolve",
        headers=auth_header,
        json={"note": "Checked on patient, all is well and safe."},
    )
    assert res_res.status_code == 200
    assert res_res.json()["status"] == "RESOLVED"
    assert res_res.json()["resolved_at"] is not None

    # 4. List Notifications and Mark as Read
    notifs_res = client.get("/api/v1/notifications", headers=auth_header)
    assert notifs_res.status_code == 200
    notifs = notifs_res.json()
    if len(notifs) > 0:
        notif_id = notifs[0]["id"]
        read_res = client.post(f"/api/v1/notifications/{notif_id}/read", headers=auth_header)
        assert read_res.status_code == 200


def test_cognition_overview_and_signals(client):
    # Setup caregiver & patient
    cg_res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "amy.pond@example.com",
            "password": "Password123!",
            "display_name": "Amy Pond",
            "role": "CAREGIVER",
        },
    )
    auth_header = {"Authorization": f"Bearer {cg_res.json()['access_token']}"}

    pat_res = client.post(
        "/api/v1/patients",
        headers=auth_header,
        json={"display_name": "Rory Williams", "email": "rory@example.com"},
    )
    patient_id = pat_res.json()["id"]

    # 1. Cognition Overview
    cov_res = client.get(f"/api/v1/patients/{patient_id}/cognition/overview", headers=auth_header)
    assert cov_res.status_code == 200
    cov = cov_res.json()
    assert "current_composite_score" in cov
    assert "baseline_score" in cov
    assert "category_scores" in cov

    # 2. Cognition Trends
    trends_res = client.get(f"/api/v1/patients/{patient_id}/cognition/trends", headers=auth_header)
    assert trends_res.status_code == 200
    trends = trends_res.json()
    assert isinstance(trends, list)

    # 3. Cognition Support Signals
    sig_res = client.get(f"/api/v1/patients/{patient_id}/cognition/signals", headers=auth_header)
    assert sig_res.status_code == 200
    assert isinstance(sig_res.json(), list)
