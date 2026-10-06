import pytest


def test_weekly_report_generation_and_metrics(client):
    # 1. Register Caregiver
    cg_res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "dr.house@example.com",
            "password": "Password123!",
            "display_name": "Dr. Gregory House",
            "role": "CAREGIVER",
        },
    )
    assert cg_res.status_code == 201
    cg_token = cg_res.json()["access_token"]
    cg_headers = {"Authorization": f"Bearer {cg_token}"}

    # 2. Create Patient
    pat_res = client.post(
        "/api/v1/patients",
        headers=cg_headers,
        json={"display_name": "James Wilson", "email": "wilson.patient@example.com"},
    )
    assert pat_res.status_code == 201
    patient_id = pat_res.json()["id"]

    # 3. Generate Weekly Report
    gen_res = client.post(
        f"/api/v1/patients/{patient_id}/reports/generate",
        headers=cg_headers,
    )
    assert gen_res.status_code == 201
    report = gen_res.json()
    assert report["patient_id"] == patient_id
    assert "adherence_percentage" in report["metrics_snapshot"]
    assert "cognitive_composite_score" in report["metrics_snapshot"]
    assert "James Wilson" in report["ai_narrative_summary"]
    assert "does not constitute a clinical" in report["ai_narrative_summary"]

    report_id = report["id"]

    # 4. List Reports
    list_res = client.get(f"/api/v1/patients/{patient_id}/reports", headers=cg_headers)
    assert list_res.status_code == 200
    reports = list_res.json()
    assert len(reports) >= 1

    # 5. Get Report by ID
    get_res = client.get(f"/api/v1/patients/{patient_id}/reports/{report_id}", headers=cg_headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == report_id
