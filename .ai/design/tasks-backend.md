# Backend Task List: CogniCare

- [x] Task 1: Backend Scaffold & Core Configuration
  - Set up `backend/` project structure, `pyproject.toml` / `requirements.txt`.
  - Configure `app/core/config.py`, `app/core/security.py`, `app/core/database.py`, `app/core/exceptions.py`.
  - Create global RFC 7807-compatible error handler and CORS middleware.
  - Verify FastAPI boots cleanly with `/health/live`.

- [x] Task 2: Identity & Authentication Module
  - Models: `User`, `Profile`.
  - Password hashing with PBKDF2/bcrypt, JWT access token issuing, HTTP-only refresh cookie support.
  - Endpoints: `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `POST /api/v1/auth/logout`, `GET /api/v1/auth/me`.
  - Tests: `test_auth.py` verifying registration, login, token refresh, and invalid credentials.

- [x] Task 3: Patient Profile & Caregiver Relationship Module
  - Models: `PatientProfile`, `CaregiverLink`, `EmergencyContact`, `Consent`.
  - Granular RBAC permissions verification (`VIEW_PROFILE`, `MANAGE_REMINDERS`, `VIEW_COGNITION`).
  - Endpoints: `GET /api/v1/patients`, `POST /api/v1/patients`, `GET /api/v1/patients/{id}`, `POST /api/v1/patients/{id}/caregivers/invite`.
  - Tests: `test_patients.py` verifying caregiver linkage and data isolation.

- [x] Task 4: Medication Management Module
  - Models: `Medication`, `MedicationSchedule`.
  - CRUD logic for patient prescriptions, dosage text, times of day, and criticality.
  - Endpoints: `GET /api/v1/patients/{id}/medications`, `POST /api/v1/patients/{id}/medications`, `PATCH /api/v1/patients/{id}/medications/{medId}`, `DELETE /api/v1/patients/{id}/medications/{medId}`.
  - Tests: `test_medications.py`.

- [x] Task 5: Routines & Reminder Engine
  - Models: `Routine`, `Reminder`, `ReminderEvent`.
  - Dispatching and tracking today's scheduled care items.
  - Endpoints: `GET /api/v1/patients/{id}/reminders/today`, `POST /api/v1/patients/{id}/reminders/{remId}/acknowledge`, `POST /api/v1/patients/{id}/reminders/{remId}/snooze`, `POST /api/v1/patients/{id}/reminders/{remId}/skip`.
  - Tests: `test_reminders.py` testing reminder acknowledgment and state transitions.

- [x] Task 6: Cognitive Activity Catalog & Interactive Sessions
  - Models: `CognitiveActivity`, `CognitiveActivityVersion`, `ActivitySession`, `ActivityAnswer`.
  - Preloaded catalog: Memory Recall, Word Sequence, Attention Stroop, Orientation Matching.
  - Endpoints: `GET /api/v1/activities`, `POST /api/v1/patients/{id}/activity-sessions`, `POST /api/v1/patients/{id}/activity-sessions/{sessionId}/answers`, `POST /api/v1/patients/{id}/activity-sessions/{sessionId}/complete`.
  - Tests: `test_activity_sessions.py`.

- [x] Task 7: Cognitive Scoring, Baselines & Longitudinal Trends
  - Models: `CognitiveBaseline`, `CognitiveTrendSnapshot`, `SupportSignal`.
  - Mathematical scoring formula (accuracy, response latency, completion rate, difficulty weight).
  - Trend analysis engine (7d & 30d rolling windows, variance, trend direction).
  - Endpoints: `GET /api/v1/patients/{id}/cognition/overview`, `GET /api/v1/patients/{id}/cognition/trends`, `GET /api/v1/patients/{id}/cognition/signals`.
  - Tests: `test_cognition_trends.py`.

- [x] Task 8: AI Assistant & Safety Guardrail Service
  - Models: `Conversation`, `Message`, `MemoryItem`.
  - Provider abstraction: `AIProvider` with `OpenAIProvider` and deterministic `MockAIProvider`.
  - Context builder with grounded application data (`get_today_tasks`, `get_upcoming_reminders`).
  - Strict medical safety filter: rejects diagnostic inquiries and dosage changes.
  - Endpoints: `POST /api/v1/patients/{id}/conversations`, `POST /api/v1/patients/{id}/conversations/{cId}/messages`.
  - Tests: `test_assistant.py`.

- [x] Task 9: Safety & Alert Management
  - Models: `Alert`, `AlertEvent`, `Notification`.
  - Deterministic SOS trigger endpoint creating urgent alert and dispatching notification.
  - Endpoints: `POST /api/v1/patients/{id}/sos`, `GET /api/v1/patients/{id}/alerts`, `POST /api/v1/patients/{id}/alerts/{alertId}/acknowledge`, `POST /api/v1/patients/{id}/alerts/{alertId}/resolve`.
  - Tests: `test_safety.py`.

- [x] Task 10: Caregiver Analytics & Weekly Report Generator
  - Model: `Report`.
  - Code-calculated objective metrics (Adherence %, Average response speed, Sessions completed, Open alerts).
  - Deterministic + AI-narrative weekly report builder.
  - Endpoints: `GET /api/v1/patients/{id}/reports`, `POST /api/v1/patients/{id}/reports/generate`, `GET /api/v1/patients/{id}/reports/{rId}`.
  - Tests: `test_reports.py`.

- [x] Task 11: System Health, Audit Logging & Demo Seeder
  - Model: `AuditLog`.
  - Middleware recording critical actor actions.
  - Seeder script generating 2 elderly users, 2 caregivers, 4 activities, prescriptions, routines, 30 days of cognitive history, and active alerts.
  - Verification with CLI seeder command.

- [x] Task 12: Backend Integration & Pytest Verification
  - Run full test suite with Pytest.
  - Verify all endpoints, edge cases, error codes, and RBAC policies pass cleanly.
