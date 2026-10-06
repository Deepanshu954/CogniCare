# CogniCare: API Design Specification

All endpoints are prefixed with `/api/v1`.
Error responses conform to the standard error structure:
```json
{
  "error": {
    "code": "STRING_CODE",
    "message": "Human readable explanation.",
    "details": {}
  },
  "request_id": "req_uuid"
}
```

## 1. Authentication (`/api/v1/auth`)
| Method | Path | Description | Access |
|---|---|---|---|
| `POST` | `/auth/register` | Register new user (Elderly or Caregiver) | Public |
| `POST` | `/auth/login` | Login with email/password; returns access token & sets HTTP-only refresh cookie | Public |
| `POST` | `/auth/refresh` | Refresh access session | Public (Cookie) |
| `POST` | `/auth/logout` | Invalidate current session and clear cookie | Authenticated |
| `GET` | `/auth/me` | Fetch current user and linked profile | Authenticated |

## 2. Patients & Caregiver Management (`/api/v1/patients`)
| Method | Path | Description | Access |
|---|---|---|---|
| `GET` | `/patients` | List accessible patients for the authenticated user | Caregiver / Admin |
| `POST` | `/patients` | Create patient profile and establish primary link | Caregiver / Admin |
| `GET` | `/patients/{patientId}` | Get patient details and settings | Authorized User |
| `PATCH` | `/patients/{patientId}` | Update patient preferences | Authorized Caregiver |
| `GET` | `/patients/{patientId}/caregivers` | List linked caregivers and roles | Authorized User |
| `POST` | `/patients/{patientId}/caregivers/invite` | Invite caregiver by email with permissions | Primary Caregiver |
| `GET` | `/patients/{patientId}/summary` | Aggregate dashboard summary for patient | Authorized User |

## 3. Care Management: Medications & Routines
| Method | Path | Description | Access |
|---|---|---|---|
| `GET` | `/patients/{patientId}/medications` | List active medications | Patient / Caregiver |
| `POST` | `/patients/{patientId}/medications` | Create medication and schedules | Caregiver |
| `PATCH` | `/patients/{patientId}/medications/{id}` | Update medication dosage or schedule | Caregiver |
| `DELETE` | `/patients/{patientId}/medications/{id}` | Deactivate medication | Caregiver |
| `GET` | `/patients/{patientId}/routines` | List daily routines (meals, hydration, exercise) | Patient / Caregiver |
| `POST` | `/patients/{patientId}/routines` | Create routine schedule | Caregiver |
| `PATCH` | `/patients/{patientId}/routines/{id}` | Update routine | Caregiver |

## 4. Reminders & Adherence (`/api/v1/patients/{patientId}/reminders`)
| Method | Path | Description | Access |
|---|---|---|---|
| `GET` | `/patients/{patientId}/reminders/today` | List today's upcoming and past reminders | Patient / Caregiver |
| `POST` | `/patients/{patientId}/reminders` | Create one-off custom reminder | Caregiver |
| `POST` | `/patients/{patientId}/reminders/{id}/acknowledge` | Mark reminder acknowledged / taken | Patient / Caregiver |
| `POST` | `/patients/{patientId}/reminders/{id}/skip` | Skip reminder with optional reason | Patient / Caregiver |
| `POST` | `/patients/{patientId}/reminders/{id}/snooze` | Snooze reminder by N minutes | Patient |

## 5. Cognitive Activities & Sessions (`/api/v1/activities` & `/api/v1/patients/{patientId}/sessions`)
| Method | Path | Description | Access |
|---|---|---|---|
| `GET` | `/activities` | Browse catalog of available cognitive games | Authenticated |
| `GET` | `/activities/{id}` | Get activity details, rules, and current version | Authenticated |
| `POST` | `/patients/{patientId}/activity-sessions` | Start a new cognitive session | Patient |
| `GET` | `/patients/{patientId}/activity-sessions/{sessionId}` | Get current session state and questions | Patient |
| `POST` | `/patients/{patientId}/activity-sessions/{sessionId}/answers` | Submit question answer with latency | Patient |
| `POST` | `/patients/{patientId}/activity-sessions/{sessionId}/complete` | Complete session, calculate score & accuracy | Patient |
| `GET` | `/patients/{patientId}/activity-sessions` | Historical sessions and scores | Patient / Caregiver |

## 6. Cognitive Analytics & Longitudinal Trends
| Method | Path | Description | Access |
|---|---|---|---|
| `GET` | `/patients/{patientId}/cognition/overview` | Overall performance metrics and adherence | Patient / Caregiver |
| `GET` | `/patients/{patientId}/cognition/trends` | Time-series data points for charts (7d, 30d, 90d) | Caregiver / Reviewer |
| `GET` | `/patients/{patientId}/cognition/baseline` | Established baseline metrics | Caregiver / Reviewer |
| `GET` | `/patients/{patientId}/cognition/signals` | Support and screening observation signals | Caregiver / Reviewer |

## 7. AI Assistant (`/api/v1/patients/{patientId}/assistant`)
| Method | Path | Description | Access |
|---|---|---|---|
| `POST` | `/patients/{patientId}/conversations` | Start or resume chat conversation | Patient / Caregiver |
| `GET` | `/patients/{patientId}/conversations` | List conversation sessions | Patient / Caregiver |
| `POST` | `/patients/{patientId}/conversations/{id}/messages` | Send user message; returns grounded AI reply | Patient / Caregiver |
| `GET` | `/patients/{patientId}/conversations/{id}/messages` | Get message history | Patient / Caregiver |

## 8. Safety & Alerts (`/api/v1/patients/{patientId}/safety`)
| Method | Path | Description | Access |
|---|---|---|---|
| `POST` | `/patients/{patientId}/sos` | Trigger immediate Emergency SOS alert | Patient / Caregiver |
| `GET` | `/patients/{patientId}/alerts` | List open and past safety alerts | Caregiver / Admin |
| `POST` | `/patients/{patientId}/alerts/{alertId}/acknowledge` | Caregiver acknowledges alert | Caregiver |
| `POST` | `/patients/{patientId}/alerts/{alertId}/resolve` | Caregiver resolves alert with note | Caregiver |

## 9. Reports & Summaries (`/api/v1/patients/{patientId}/reports`)
| Method | Path | Description | Access |
|---|---|---|---|
| `GET` | `/patients/{patientId}/reports` | List historical weekly/monthly reports | Caregiver / Reviewer |
| `POST` | `/patients/{patientId}/reports/generate` | Trigger generation of weekly summary report | Caregiver |
| `GET` | `/patients/{patientId}/reports/{reportId}` | Retrieve full report with metrics & AI summary | Caregiver / Reviewer |

## 10. System Health (`/api/v1/health`)
| Method | Path | Description | Access |
|---|---|---|---|
| `GET` | `/health/live` | Container liveness check | Public |
| `GET` | `/health/ready` | Readiness check (database & redis ping) | Public |
| `GET` | `/openapi.json` | Complete OpenAPI 3.1 specification | Public |
