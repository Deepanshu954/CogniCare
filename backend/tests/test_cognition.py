import pytest


def test_cognitive_activity_session_and_scoring(client):
    # 1. Check activities catalog
    act_res = client.get("/api/v1/activities")
    assert act_res.status_code == 200
    activities = act_res.json()
    assert len(activities) >= 4
    types = [a["activity_type"] for a in activities]
    assert "MEMORY_RECALL" in types
    assert "ATTENTION_STROOP" in types
    assert "WORD_SEQUENCE" in types
    assert "ORIENTATION_MATCH" in types

    memory_act = next(a for a in activities if a["activity_type"] == "MEMORY_RECALL")

    # 2. Register Elderly User
    el_res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "margaret.game@example.com",
            "password": "Password123!",
            "display_name": "Margaret Gamer",
            "role": "ELDERLY",
        },
    )
    assert el_res.status_code == 201
    auth_header = {"Authorization": f"Bearer {el_res.json()['access_token']}"}
    patient_id = el_res.json()["user"]["patient_profile"]["id"]

    # 3. Start Session
    sess_res = client.post(
        f"/api/v1/patients/{patient_id}/activity-sessions",
        headers=auth_header,
        json={"activity_id": memory_act["id"], "difficulty": 1},
    )
    assert sess_res.status_code == 201
    session = sess_res.json()
    session_id = session["id"]
    assert session["status"] == "IN_PROGRESS"
    assert session["activity_title"] == "Visual Memory Pairs"

    # 4. Submit 4 Answers with varying latency
    answers = [
        {"question_id": "q1", "user_answer": "Sunflower", "is_correct": True, "response_time_ms": 1400},
        {"question_id": "q2", "user_answer": "Robin", "is_correct": True, "response_time_ms": 1600},
        {"question_id": "q3", "user_answer": "Teacup", "is_correct": True, "response_time_ms": 1200},
        {"question_id": "q4", "user_answer": "Apple", "is_correct": False, "response_time_ms": 2500},
    ]

    for ans in answers:
        sub_res = client.post(
            f"/api/v1/patients/{patient_id}/activity-sessions/{session_id}/answers",
            headers=auth_header,
            json=ans,
        )
        assert sub_res.status_code == 200
        assert sub_res.json()["question_id"] == ans["question_id"]

    # 5. Complete Session
    comp_res = client.post(
        f"/api/v1/patients/{patient_id}/activity-sessions/{session_id}/complete",
        headers=auth_header,
    )
    assert comp_res.status_code == 200
    comp_data = comp_res.json()
    assert comp_data["status"] == "COMPLETED"
    assert comp_data["accuracy_rate"] == 75.0  # 3 of 4 correct
    assert comp_data["avg_response_time_ms"] > 0
    assert comp_data["total_score"] > 60.0  # Normalized reproducible score
    assert comp_data["feedback_message"] is not None

    # 6. Fetch Cognitive Overview
    overview_res = client.get(
        f"/api/v1/patients/{patient_id}/cognition/overview",
        headers=auth_header,
    )
    assert overview_res.status_code == 200
    overview = overview_res.json()
    assert overview["total_sessions_completed"] == 1
    assert overview["current_composite_score"] > 0
    assert "Memory Recall" in overview["category_scores"]

    # 7. Fetch Cognitive Trends
    trends_res = client.get(
        f"/api/v1/patients/{patient_id}/cognition/trends",
        headers=auth_header,
    )
    assert trends_res.status_code == 200
    trends = trends_res.json()
    assert len(trends) >= 1
    assert trends[-1]["score"] == comp_data["total_score"]
