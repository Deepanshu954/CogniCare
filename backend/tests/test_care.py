import pytest


def test_medication_routine_reminder_lifecycle(client):
    # 1. Register Caregiver
    cg_res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "sarah.med@example.com",
            "password": "Password123!",
            "display_name": "Sarah MedCare",
            "role": "CAREGIVER",
        },
    )
    assert cg_res.status_code == 201
    auth_header = {"Authorization": f"Bearer {cg_res.json()['access_token']}"}

    # 2. Create Patient
    pat_res = client.post(
        "/api/v1/patients",
        headers=auth_header,
        json={"display_name": "Arthur Dent", "email": "arthur.med@example.com"},
    )
    assert pat_res.status_code == 201
    patient_id = pat_res.json()["id"]

    # 3. Create Medication with Schedule
    med_res = client.post(
        f"/api/v1/patients/{patient_id}/medications",
        headers=auth_header,
        json={
            "name": "Donepezil",
            "dosage_text": "10mg",
            "instructions": "Take once daily in the evening with food",
            "schedules": [
                {
                    "schedule_type": "DAILY",
                    "time_of_day": "20:00",
                    "criticality": "HIGH",
                }
            ],
        },
    )
    assert med_res.status_code == 201
    med = med_res.json()
    assert med["name"] == "Donepezil"
    assert len(med["schedules"]) == 1

    # 4. Create Routine (Morning Hydration)
    routine_res = client.post(
        f"/api/v1/patients/{patient_id}/routines",
        headers=auth_header,
        json={
            "routine_type": "HYDRATION",
            "title": "Morning Water Glass",
            "description": "Drink full glass of warm water",
            "scheduled_time": "08:30",
        },
    )
    assert routine_res.status_code == 201
    assert routine_res.json()["title"] == "Morning Water Glass"

    # 5. Fetch Today's Reminders
    rem_res = client.get(f"/api/v1/patients/{patient_id}/reminders/today", headers=auth_header)
    assert rem_res.status_code == 200
    reminders = rem_res.json()
    assert len(reminders) >= 2

    med_reminder = next(r for r in reminders if "Donepezil" in r["title"])
    hydration_reminder = next(r for r in reminders if "Morning Water Glass" in r["title"])

    assert med_reminder["status"] == "SCHEDULED"
    assert hydration_reminder["status"] == "SCHEDULED"

    # 6. Acknowledge Medication Reminder
    ack_res = client.post(
        f"/api/v1/patients/{patient_id}/reminders/{med_reminder['id']}/acknowledge",
        headers=auth_header,
    )
    assert ack_res.status_code == 200
    assert ack_res.json()["status"] == "ACKNOWLEDGED"
    assert ack_res.json()["acknowledged_at"] is not None

    # 7. Snooze Hydration Reminder
    snooze_res = client.post(
        f"/api/v1/patients/{patient_id}/reminders/{hydration_reminder['id']}/snooze",
        headers=auth_header,
        json={"snooze_minutes": 20},
    )
    assert snooze_res.status_code == 200
    assert snooze_res.json()["status"] == "SNOOZED"
    assert snooze_res.json()["snooze_until"] is not None

    # 8. Check Patient Summary reflects adherence
    summary_res = client.get(f"/api/v1/patients/{patient_id}/summary", headers=auth_header)
    assert summary_res.status_code == 200
    summary = summary_res.json()
    assert summary["today_completed_reminders"] >= 1
    assert summary["total_medications"] == 1
