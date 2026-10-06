# CogniCare API Reference

This document describes the primary REST endpoints exposed by the CogniCare backend API under the `/api/v1` prefix.

## Base URL
- Local Development: `http://localhost:8000/api/v1`
- Swagger UI Documentation: `http://localhost:8000/docs`
- ReDoc Interactive Documentation: `http://localhost:8000/redoc`

---

## 1. Authentication (`/auth`)

### Register User
- **Method**: `POST /auth/register`
- **Request Body**:
  ```json
  {
    "email": "sarah@example.com",
    "password": "Password123!",
    "display_name": "Sarah Vance",
    "role": "CAREGIVER",
    "phone_number": "+1 555-0199"
  }
  ```
- **Response (HTTP 201)**: Returns user record and JWT bearer token.

### Login
- **Method**: `POST /auth/login`
- **Rate Limit**: 20 requests per minute per IP.
- **Request Body**:
  ```json
  {
    "email": "sarah@example.com",
    "password": "Password123!"
  }
  ```
- **Response (HTTP 200)**:
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "expires_in": 86400,
    "user": { ... }
  }
  ```

---

## 2. Patients & Caregivers (`/patients`)

- `GET /patients` — List accessible patients.
- `POST /patients` — Register a patient profile.
- `GET /patients/{id}/summary` — Retrieve adherence and cognitive overview.
- `POST /patients/{id}/caregivers` — Link an authorized caregiver.

---

## 3. Care & Reminders (`/patients/{id}`)

- `GET /patients/{id}/medications` — List active medications.
- `POST /patients/{id}/medications` — Prescribe medication with dosage and schedule time.
- `GET /patients/{id}/reminders/today` — Retrieve today's scheduled reminder items.
- `POST /patients/{id}/reminders/{rem_id}/acknowledge` — Senior 1-tap "I did this!" confirmation.
- `POST /patients/{id}/reminders/{rem_id}/snooze` — Snooze reminder by 15 minutes.

---

## 4. Cognitive Health (`/patients/{id}/cognition`)

- `GET /patients/{id}/cognition/activities` — List available cognitive activities (Memory, Working Memory, Stroop, Orientation).
- `POST /patients/{id}/cognition/sessions/start` — Launch randomized activity session.
- `POST /patients/{id}/cognition/sessions/{sid}/submit` — Submit answers and receive deterministic score:
  ```json
  {
    "responses": [
      { "question_id": 1, "answer": "cat", "latency_ms": 1200 }
    ]
  }
  ```
- `GET /patients/{id}/cognition/overview` — Get composite scores, 30-day baseline, and drift.
- `GET /patients/{id}/cognition/trends` — Retrieve historical time-series data for charting.

---

## 5. Conversational Assistant (`/patients/{id}/assistant`)

- `POST /patients/{id}/assistant/messages` — Send message with context grounding and policy enforcement:
  ```json
  {
    "message": "Did I take my morning pills?"
  }
  ```
  *Note*: Rejects attempts to modify dosages or seek clinical diagnosis with predefined healthcare disclaimers.

---

## 6. Safety & SOS Alerts (`/patients/{id}`)

- `POST /patients/{id}/sos` — Trigger emergency SOS event. Dispatches CRITICAL alert.
- `GET /patients/{id}/alerts` — List safety alerts by severity (CRITICAL, HIGH, MEDIUM, INFO).
- `POST /patients/{id}/alerts/{aid}/resolve` — Resolve alert with mandatory resolution note.

---

## 7. Caregiver Reports (`/patients/{id}/reports`)

- `POST /patients/{id}/reports/generate` — Generate weekly AI summary with objective metrics.
- `GET /patients/{id}/reports/latest` — Retrieve the most recent report.
