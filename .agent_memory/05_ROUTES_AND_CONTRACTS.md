# CogniCare: Routes & API Contracts Verification

## 1. Backend REST Endpoints (`/api/v1`)

### Authentication (`/api/v1/auth`)
- `POST /api/v1/auth/register` — Register new user (Elderly or Caregiver).
- `POST /api/v1/auth/login` — Authenticate and receive JWT access token.
- `GET /api/v1/auth/me` — Retrieve active user session profile.
- `POST /api/v1/auth/refresh` — Refresh access token.
- `POST /api/v1/auth/logout` — Revoke session cookie.

### Patient Management (`/api/v1/patients`)
- `GET /api/v1/patients` — List accessible patients for the authenticated user.
- `POST /api/v1/patients` — Register a new patient profile.
- `GET /api/v1/patients/{id}` — Retrieve full patient details and preferences.
- `PATCH /api/v1/patients/{id}` — Update preferences and emergency notes.
- `GET /api/v1/patients/{id}/summary` — Retrieve executive summary (medication count, alert state).
- `POST /api/v1/patients/{id}/emergency-contacts` — Add emergency contacts.
- `GET /api/v1/patients/{id}/emergency-contacts` — List emergency contacts.
- `POST /api/v1/patients/{id}/consents` — Grant caregiver data consent.
- `POST /api/v1/patients/{id}/caregivers` — Link a designated caregiver.

### Care & Reminders (`/api/v1/patients/{id}`)
- `POST /api/v1/patients/{id}/medications` — Add medication prescription.
- `GET /api/v1/patients/{id}/medications` — List active medications.
- `POST /api/v1/patients/{id}/routines` — Add daily routine activity.
- `GET /api/v1/patients/{id}/routines` — List daily routines.
- `GET /api/v1/patients/{id}/reminders/today` — Retrieve today's scheduled reminders.
- `POST /api/v1/patients/{id}/reminders/generate` — Generate daily agenda items.
- `POST /api/v1/patients/{id}/reminders/{rem_id}/acknowledge` — 1-tap "I did this!" acknowledgment.
- `POST /api/v1/patients/{id}/reminders/{rem_id}/snooze` — Snooze reminder by 15 minutes.
- `POST /api/v1/patients/{id}/reminders/{rem_id}/skip` — Record skip reason.

### Cognitive Health (`/api/v1/patients/{id}/cognition`)
- `GET /api/v1/patients/{id}/cognition/activities` — List available games (Memory, Sequence, Stroop, Orientation).
- `POST /api/v1/patients/{id}/cognition/sessions/start` — Launch game session with randomized questions.
- `POST /api/v1/patients/{id}/cognition/sessions/{sid}/submit` — Submit answers, receive mathematical score.
- `GET /api/v1/patients/{id}/cognition/overview` — Get domain scores, 30-day baseline, and drift.
- `GET /api/v1/patients/{id}/cognition/trends` — Retrieve historical time-series performance points.

### Conversational Assistant (`/api/v1/patients/{id}/assistant`)
- `POST /api/v1/patients/{id}/assistant/conversations` — Start or retrieve active conversation.
- `POST /api/v1/patients/{id}/assistant/messages` — Send message with context grounding and policy guardrails.
- `GET /api/v1/patients/{id}/assistant/messages` — Retrieve conversation transcript.

### Safety & Alerts (`/api/v1/patients/{id}/safety`)
- `POST /api/v1/patients/{id}/sos` — Trigger emergency SOS event.
- `GET /api/v1/patients/{id}/alerts` — List safety alerts by severity.
- `POST /api/v1/patients/{id}/alerts/{aid}/acknowledge` — Acknowledge alert.
- `POST /api/v1/patients/{id}/alerts/{aid}/resolve` — Resolve alert with mandatory resolution note.

### Caregiver Reports (`/api/v1/patients/{id}/reports`)
- `POST /api/v1/patients/{id}/reports/generate` — Generate weekly AI summary with objective metrics.
- `GET /api/v1/patients/{id}/reports/latest` — Retrieve most recent generated report.

---

## 2. Frontend Routes (`frontend/src/app`)

- `/` — Landing page with 1-click quick demo launch.
- `/login` — Unified authentication screen.
- `/register` — Account creation with role selection (Senior vs Caregiver).
- `/app/my-day` — Elderly home dashboard with oversized action tiles and scheduled agenda.
- `/app/activities` — Cognitive exercises portal.
- `/app/activities/[id]` — Interactive game runner for all 4 cognitive assessments.
- `/app/assistant` — Ambient conversational companion with voice synthesis and recognition.
- `/app/safety` — Emergency SOS screen with 5-second cancel countdown.
- `/caregiver/dashboard` — Caregiver executive control tower with patient switcher, charts, and alerts.
- `/caregiver/reports` — Weekly AI report generator with print/PDF layout.
