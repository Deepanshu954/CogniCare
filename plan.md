# AI-Powered Cognitive Health & Care Assistant
## End-to-End Product, System, API, AI/ML and Implementation Master Plan

> **Document status:** Final architecture baseline  
> **Project form:** Web-first, responsive PWA  
> **Primary domain:** Cognitive support and everyday care assistance for elderly people with cognitive impairment  
> **Medical positioning:** Support / decision-assistance only; not a diagnostic system and not a replacement for a clinician  
> **Delivery model:** No fixed calendar deadline. Build through capability gates and stabilize each layer before expanding it.

---

# 0. Executive Decision Summary

This project will be built as a **web-first, responsive Progressive Web App (PWA)** rather than maintaining two separate frontends from the beginning.

The system will have two primary experiences:

1. **Elderly user experience**
   - very large, low-complexity interface
   - voice/text interaction
   - cognitive activities
   - daily routine
   - medication/routine reminders
   - simple alerts and SOS

2. **Caregiver experience**
   - patient management
   - routine/medication management
   - cognitive history and trends
   - adherence and activity summaries
   - alerts
   - AI-generated weekly summaries
   - reports
   - privacy/consent controls

The technical architecture will be a **modular monolith**, not microservices.

### Final primary stack

| Layer | Decision |
|---|---|
| Web framework | Next.js App Router + TypeScript |
| UI | React + Tailwind CSS + accessible component primitives |
| Client server-state | TanStack Query |
| Frontend validation | Zod |
| Backend | Python + FastAPI |
| Backend validation | Pydantic |
| ORM | SQLAlchemy 2.x |
| Database migrations | Alembic |
| Primary database | PostgreSQL |
| Vector search | pgvector |
| Cache / queue broker | Redis |
| Background jobs | Celery or equivalent Redis-backed worker |
| AI text/tool orchestration | Provider abstraction; OpenAI Responses API as first implementation |
| Realtime voice | OpenAI Realtime API adapter as first implementation |
| Speech fallback | Provider abstraction for STT/TTS |
| Charts | Recharts or equivalent |
| Browser offline storage | IndexedDB |
| PWA | Service Worker + Web App Manifest |
| Push | Web Push |
| Auth | Secure HTTP-only cookies + short-lived access session |
| Password hashing | Argon2id |
| Testing | Pytest + Vitest + Playwright |
| API contract | OpenAPI |
| CI/CD | GitHub Actions |
| Containers | Docker / Docker Compose |
| Observability | Structured logs + OpenTelemetry + error tracking |
| Security baseline | OWASP ASVS 5.0 + OWASP Top 10 2025 |
| Accessibility target | WCAG 2.2 AA-oriented implementation |
| Source control | Git + GitHub |

### Core architectural principle

```text
                 ┌────────────────────────────┐
                 │        Next.js / PWA        │
                 │ Elderly UI + Caregiver UI   │
                 └──────────────┬─────────────┘
                                │ HTTPS
                                ▼
                 ┌────────────────────────────┐
                 │        FastAPI API          │
                 │ Auth / RBAC / Business      │
                 │ Rules / Validation          │
                 └──────────────┬─────────────┘
                                │
             ┌──────────────────┼───────────────────┐
             ▼                  ▼                   ▼
      ┌─────────────┐   ┌──────────────┐    ┌──────────────┐
      │ PostgreSQL  │   │    Redis     │    │ AI Services  │
      │ source data │   │ cache/jobs   │    │ LLM/Voice/ML │
      └─────────────┘   └──────────────┘    └──────────────┘
             │                  │                   │
             └──────────────────┼───────────────────┘
                                ▼
                    ┌────────────────────────┐
                    │ Background Worker(s)   │
                    │ reminders / reports /  │
                    │ AI jobs / notifications│
                    └────────────────────────┘
```

---

# 1. Project Vision

## 1.1 What we are building

A unified digital assistant that helps elderly people with cognitive difficulties manage everyday life while giving caregivers a structured, understandable view of activities, adherence, trends, and safety signals.

The platform combines:

- conversational assistance
- voice interaction
- cognitive activities
- cognitive-task scoring
- personalized activity recommendations
- medication reminders
- daily routine management
- hydration and meal reminders
- caregiver monitoring
- safety alerts
- longitudinal trend analysis
- weekly reports
- privacy and consent controls
- optional advanced computer-vision/location features

## 1.2 What this project is not

The system must **not** be presented as:

- a dementia diagnostic tool
- a clinical decision replacement
- a medical emergency response service
- a certified medical device
- a system that proves cognitive decline from one test
- an autonomous medical decision maker

Every cognitive trend is a **support signal** that may warrant caregiver or professional review.

---

# 2. Product Goals

## Primary goals

1. Make everyday support easier for elderly users.
2. Reduce caregiver burden caused by fragmented information.
3. Provide consistent cognitive engagement.
4. Track longitudinal performance rather than isolated scores.
5. Provide safe, explainable AI-assisted summaries.
6. Improve visibility into routine/medication adherence.
7. Provide configurable safety and escalation workflows.
8. Demonstrate meaningful AI/ML engineering and measurable validation.
9. Build a maintainable full-stack system rather than a collection of disconnected demos.

## Secondary goals

- multilingual interaction
- personalization
- offline cognitive activities
- PWA installation
- caregiver notifications
- semantic memory for assistant conversations
- optional computer vision
- future health-data interoperability

---

# 3. Target Users and Roles

## 3.1 Elderly user

Typical needs:

- minimal navigation
- large controls
- simple wording
- voice interaction
- visual confirmation
- predictable routine
- cognitive activities
- reminders
- emergency contact

## 3.2 Caregiver / family member

Typical needs:

- connect to one or more elderly users
- create routines and medications
- view activity history
- view cognitive trends
- review alerts
- receive reminder escalations
- read AI summaries
- manage permissions and consent

## 3.3 Clinician / reviewer (optional)

Read-only or limited-access role.

Must not automatically receive all information.

Access should be explicit and permission-based.

Possible use:

- review longitudinal trends
- review caregiver-generated notes
- inspect reports
- provide feedback

## 3.4 Platform administrator

Administrative functions only:

- account management
- system health
- feature flags
- audit review
- activity/template management
- prompt/model version management
- incident investigation

Admin access must not mean unrestricted access to all patient data.

---

# 4. Capability Map

```text
ACCOUNT
├── Registration
├── Login
├── Session management
├── Password reset
├── Profile
└── Preferences

PATIENT CARE
├── Patient profile
├── Caregiver relationship
├── Daily routine
├── Medication
├── Reminders
└── Adherence

COGNITIVE SUPPORT
├── Activity catalog
├── Activity sessions
├── Scoring
├── Historical trends
├── Baseline
└── Personalization

AI ASSISTANT
├── Text chat
├── Voice conversation
├── Context
├── Tool calling
├── Memory
├── Summarization
└── Safety/guardrails

SAFETY
├── SOS
├── Inactivity
├── Alert lifecycle
├── Caregiver escalation
├── Optional location
└── Optional fall detection

ANALYTICS
├── Cognitive metrics
├── Adherence metrics
├── Engagement
├── Trend analysis
├── Alert analytics
└── Reports

PLATFORM
├── Notifications
├── PWA
├── Offline support
├── Audit logs
├── Observability
├── Security
└── Admin
```

---

# 5. Functional Requirements

## FR-01 Authentication

Users must be able to:

- register
- verify account
- log in
- log out
- refresh session
- change password
- reset forgotten password
- manage active sessions
- view current account

## FR-02 Role and authorization

The platform must enforce:

- elderly role
- caregiver role
- reviewer/clinician role
- admin role

Authorization must be server-side.

Frontend route protection alone is insufficient.

## FR-03 Patient management

Caregivers must be able to:

- create patient profile
- edit patient profile
- connect/disconnect caregiver relationship
- configure emergency contacts
- configure preferred language
- configure accessibility preferences
- manage consent

## FR-04 Cognitive activities

System must:

- present activities
- start sessions
- accept answers
- calculate activity-level results
- save response timing
- track attempts
- maintain history
- determine recommended difficulty
- generate trends

## FR-05 Routine and medication

Caregivers must be able to:

- create medication schedule
- update medication schedule
- pause medication schedule
- create daily routines
- set reminders
- choose reminder priority
- configure escalation rules

Patients must be able to:

- see current reminders
- acknowledge reminders
- skip reminders with reason
- mark reminder as completed

## FR-06 AI assistant

The assistant must:

- support simple conversational interaction
- answer routine/context questions using trusted application data
- explain today's tasks
- assist with navigation
- help initiate activities
- help retrieve non-sensitive stored information
- summarize recent activity
- escalate according to configured rules

## FR-07 Safety

System must support:

- SOS
- alert creation
- alert acknowledgement
- escalation
- alert resolution
- configurable inactivity checks

Advanced:

- fall detection
- location/geofence
- wandering support

## FR-08 Caregiver dashboard

Dashboard must show:

- today's status
- cognitive activity
- adherence
- alerts
- recent interactions
- trends
- weekly summary
- history

## FR-09 Reporting

System must:

- create weekly reports
- expose report history
- allow secure viewing/download
- show underlying data period
- identify AI-generated sections

## FR-10 Notifications

System must support:

- in-app notifications
- web push
- email fallback for selected events
- notification preferences
- escalation rules
- notification delivery history

---

# 6. Non-Functional Requirements

## Performance

Target goals for the prototype:

- normal API operations should feel interactive
- dashboard data should load quickly
- cognitive activity responses should feel immediate
- background jobs must not block interactive requests

Do not claim any performance target as achieved until measured.

## Reliability

- retries for transient background failures
- idempotent reminder/alert actions
- durable source of truth in PostgreSQL
- notification status tracking
- outbox pattern for important asynchronous events

## Security

- HTTPS everywhere
- HTTP-only secure auth cookies
- Argon2id password hashing
- RBAC
- input validation
- CSRF protection where cookie-authenticated requests require it
- rate limiting
- audit logging
- secret management
- dependency scanning
- authorization tests

## Privacy

- explicit consent
- least-privilege data access
- configurable retention
- data export/delete workflows
- no unnecessary audio retention
- no raw camera storage by default
- sensitive logging avoided
- patient-level access restrictions

## Accessibility

Target a WCAG 2.2 AA-oriented experience:

- keyboard accessibility
- large touch targets
- visible focus state
- screen-reader labels
- adequate text sizing
- simple language
- reduced-motion support
- semantic HTML
- accessible error states
- voice interaction where appropriate

## Explainability

AI-generated insight should expose:

- period analyzed
- relevant metrics
- direction of change
- confidence/qualification
- data limitations
- non-diagnostic disclaimer

---

# 7. Architecture Decision: Modular Monolith

## Decision

Use one FastAPI backend organized by domain modules.

Do not start with microservices.

### Backend domains

```text
auth/
patients/
caregivers/
consents/
medications/
reminders/
activities/
cognition/
assistant/
memory/
safety/
notifications/
analytics/
reports/
files/
admin/
audit/
```

## Why

Microservices would introduce:

- network failure between services
- distributed transactions
- more deployment complexity
- more observability burden
- harder local development

A modular monolith still allows future extraction if a component becomes independently scalable.

---

# 8. Frontend Application Structure

## 8.1 Public routes

```text
/
 /about
 /how-it-works
 /safety
 /privacy
 /terms
 /accessibility
 /contact
```

## 8.2 Authentication routes

```text
/auth/login
/auth/register
/auth/verify-email
/auth/forgot-password
/auth/reset-password
```

## 8.3 Elderly routes

```text
/app/my-day
/app/assistant
/app/activities
/app/activities/[activityId]
/app/reminders
/app/safety
/app/profile
/app/settings
```

## 8.4 Caregiver routes

```text
/caregiver/dashboard
/caregiver/patients
/caregiver/patients/[patientId]
/caregiver/patients/[patientId]/cognition
/caregiver/patients/[patientId]/care
/caregiver/patients/[patientId]/medications
/caregiver/patients/[patientId]/reminders
/caregiver/patients/[patientId]/alerts
/caregiver/patients/[patientId]/reports
/caregiver/patients/[patientId]/assistant-history
/caregiver/settings
```

## 8.5 Reviewer routes

```text
/reviewer/patients
/reviewer/patients/[patientId]
/reviewer/patients/[patientId]/trends
/reviewer/patients/[patientId]/reports
```

## 8.6 Admin routes

```text
/admin
/admin/users
/admin/activities
/admin/prompts
/admin/models
/admin/feature-flags
/admin/audit
/admin/system
```

---

# 9. Final API Design

## 9.1 API conventions

Base URL:

```text
/api/v1
```

### Standards

- UUID identifiers
- ISO 8601 UTC timestamps
- JSON request/response
- cursor pagination for large lists
- stable enum values
- explicit API version
- OpenAPI schema
- request ID on every response
- consistent error structure

### Pagination

```text
GET /api/v1/patients?limit=20&cursor=<cursor>
```

Response:

```json
{
  "data": [],
  "meta": {
    "next_cursor": "...",
    "has_more": true
  }
}
```

### Error format

```json
{
  "error": {
    "code": "REMINDER_NOT_FOUND",
    "message": "The requested reminder does not exist.",
    "details": {}
  },
  "request_id": "req_..."
}
```

### Idempotency

Use `Idempotency-Key` for important state-changing operations such as:

- creating reminders
- acknowledging reminders
- creating safety alerts
- triggering report generation

---

# 10. Authentication Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/register` | Create account |
| POST | `/auth/verify-email` | Verify email |
| POST | `/auth/resend-verification` | Resend verification |
| POST | `/auth/login` | Create session |
| POST | `/auth/refresh` | Refresh session |
| POST | `/auth/logout` | End current session |
| POST | `/auth/logout-all` | End all sessions |
| POST | `/auth/forgot-password` | Start password reset |
| POST | `/auth/reset-password` | Finish password reset |
| POST | `/auth/change-password` | Change password |
| GET | `/auth/sessions` | List active sessions |
| DELETE | `/auth/sessions/{sessionId}` | Revoke session |

### Auth decision

For the browser application, prefer:

```text
HTTP-only
Secure
SameSite
short-lived session/access credential
refresh mechanism
```

Do not store long-lived auth tokens in `localStorage`.

---

# 11. Current User / Profile Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/me` | Current authenticated user |
| PATCH | `/me` | Update own account |
| GET | `/me/profile` | Profile |
| PATCH | `/me/profile` | Update profile |
| GET | `/me/preferences` | Preferences |
| PATCH | `/me/preferences` | Update preferences |
| GET | `/me/accessibility` | Accessibility preferences |
| PATCH | `/me/accessibility` | Update accessibility preferences |
| GET | `/me/privacy` | Privacy controls |
| PATCH | `/me/privacy` | Update privacy controls |

---

# 12. Patient Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/patients` | Create patient |
| GET | `/patients` | List accessible patients |
| GET | `/patients/{patientId}` | Patient details |
| PATCH | `/patients/{patientId}` | Update patient |
| DELETE | `/patients/{patientId}` | Deactivate/delete patient according to policy |
| GET | `/patients/{patientId}/summary` | High-level current summary |
| GET | `/patients/{patientId}/timeline` | Unified activity timeline |

---

# 13. Caregiver Relationship Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/patients/{patientId}/caregivers/invitations` | Invite caregiver |
| GET | `/patients/{patientId}/caregivers` | List caregivers |
| PATCH | `/patients/{patientId}/caregivers/{caregiverId}` | Change permissions |
| DELETE | `/patients/{patientId}/caregivers/{caregiverId}` | Remove caregiver |
| GET | `/caregiver/invitations` | Pending invitations |
| POST | `/caregiver/invitations/{invitationId}/accept` | Accept |
| POST | `/caregiver/invitations/{invitationId}/reject` | Reject |

### Permission examples

```text
VIEW_PROFILE
VIEW_COGNITION
VIEW_REMINDERS
MANAGE_REMINDERS
VIEW_ALERTS
MANAGE_ALERTS
VIEW_REPORTS
MANAGE_CONSENT
```

Never use a single broad `is_caregiver=true` flag as the final authorization mechanism.

---

# 14. Consent Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/patients/{patientId}/consents` | View consent state |
| POST | `/patients/{patientId}/consents` | Grant consent |
| PATCH | `/patients/{patientId}/consents/{consentId}` | Change consent |
| POST | `/patients/{patientId}/consents/{consentId}/revoke` | Revoke |
| GET | `/patients/{patientId}/privacy-events` | Privacy history |

Consent purposes can include:

```text
VOICE_PROCESSING
CAMERA_PROCESSING
LOCATION_ACCESS
AI_PERSONALIZATION
ANALYTICS
CAREGIVER_ACCESS
OPTIONAL_RESEARCH
```

---

# 15. Emergency Contact Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/patients/{patientId}/emergency-contacts` | List |
| POST | `/patients/{patientId}/emergency-contacts` | Create |
| PATCH | `/patients/{patientId}/emergency-contacts/{contactId}` | Update |
| DELETE | `/patients/{patientId}/emergency-contacts/{contactId}` | Remove |

---

# 16. Medication Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/patients/{patientId}/medications` | List medications |
| POST | `/patients/{patientId}/medications` | Create |
| GET | `/patients/{patientId}/medications/{medicationId}` | Get |
| PATCH | `/patients/{patientId}/medications/{medicationId}` | Update |
| POST | `/patients/{patientId}/medications/{medicationId}/pause` | Pause |
| POST | `/patients/{patientId}/medications/{medicationId}/resume` | Resume |
| DELETE | `/patients/{patientId}/medications/{medicationId}` | Remove |

Do not let the LLM directly create or edit medication records.

The assistant can produce a structured request, but the API must validate and authorize the actual action.

---

# 17. Routine Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/patients/{patientId}/routines` | List routines |
| POST | `/patients/{patientId}/routines` | Create routine |
| GET | `/patients/{patientId}/routines/{routineId}` | Get routine |
| PATCH | `/patients/{patientId}/routines/{routineId}` | Update routine |
| DELETE | `/patients/{patientId}/routines/{routineId}` | Delete |
| POST | `/patients/{patientId}/routines/{routineId}/complete` | Mark routine complete |

Routine types:

```text
MEDICATION
MEAL
HYDRATION
EXERCISE
APPOINTMENT
COGNITIVE_ACTIVITY
SLEEP
CUSTOM
```

---

# 18. Reminder Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/patients/{patientId}/reminders` | List reminders |
| POST | `/patients/{patientId}/reminders` | Create |
| GET | `/patients/{patientId}/reminders/today` | Today's reminders |
| GET | `/patients/{patientId}/reminders/{reminderId}` | Details |
| PATCH | `/patients/{patientId}/reminders/{reminderId}` | Update |
| DELETE | `/patients/{patientId}/reminders/{reminderId}` | Delete |
| POST | `/patients/{patientId}/reminders/{reminderId}/acknowledge` | Acknowledge |
| POST | `/patients/{patientId}/reminders/{reminderId}/skip` | Skip |
| POST | `/patients/{patientId}/reminders/{reminderId}/snooze` | Snooze |
| GET | `/patients/{patientId}/reminders/{reminderId}/events` | Reminder history |

Reminder status:

```text
SCHEDULED
DELIVERED
ACKNOWLEDGED
SKIPPED
MISSED
ESCALATED
CANCELLED
```

---

# 19. Cognitive Activity Catalog Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/activities` | Browse activities |
| GET | `/activities/{activityId}` | Activity metadata |
| GET | `/activities/{activityId}/version` | Active version |
| GET | `/patients/{patientId}/activities/recommended` | Personalized recommendations |
| GET | `/patients/{patientId}/activities/history` | Activity history |

Activity categories:

```text
MEMORY_RECALL
SEQUENCE
ATTENTION
ORIENTATION
RECOGNITION
MATCHING
PATTERN
PROBLEM_SOLVING
LANGUAGE
REACTION
```

---

# 20. Cognitive Session Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/patients/{patientId}/activity-sessions` | Start session |
| GET | `/patients/{patientId}/activity-sessions/{sessionId}` | Session details |
| POST | `/patients/{patientId}/activity-sessions/{sessionId}/answers` | Submit answer |
| POST | `/patients/{patientId}/activity-sessions/{sessionId}/complete` | Complete |
| POST | `/patients/{patientId}/activity-sessions/{sessionId}/abandon` | Abandon |
| GET | `/patients/{patientId}/activity-sessions` | History |

A submitted answer should store:

```text
question_id
answer
correctness
response_time_ms
attempt_number
difficulty
timestamp
```

---

# 21. Cognitive Analytics Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/patients/{patientId}/cognition/overview` | Current overview |
| GET | `/patients/{patientId}/cognition/trends` | Trend series |
| GET | `/patients/{patientId}/cognition/baseline` | Baseline |
| GET | `/patients/{patientId}/cognition/by-category` | Category breakdown |
| GET | `/patients/{patientId}/cognition/sessions` | Session analytics |
| GET | `/patients/{patientId}/cognition/signals` | Support/screening signals |
| POST | `/patients/{patientId}/cognition/recompute` | Recompute derived metrics |

The term `signals` must be used instead of implying clinical diagnosis.

---

# 22. Personalization Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/patients/{patientId}/personalization` | Current personalization state |
| PATCH | `/patients/{patientId}/personalization` | Preferences |
| GET | `/patients/{patientId}/recommendations` | Recommendations |
| POST | `/patients/{patientId}/recommendations/{id}/accept` | Accept |
| POST | `/patients/{patientId}/recommendations/{id}/dismiss` | Dismiss |

Recommendation output:

```json
{
  "activity_id": "...",
  "difficulty": 2,
  "reason": "Recent attention tasks were more difficult than memory tasks.",
  "evidence": {
    "window_days": 14
  }
}
```

---

# 23. Assistant / Chat Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/patients/{patientId}/conversations` | Create conversation |
| GET | `/patients/{patientId}/conversations` | List conversations |
| GET | `/patients/{patientId}/conversations/{conversationId}` | Get conversation |
| POST | `/patients/{patientId}/conversations/{conversationId}/messages` | Send message |
| POST | `/patients/{patientId}/conversations/{conversationId}/summarize` | Summarize |
| DELETE | `/patients/{patientId}/conversations/{conversationId}` | Delete according to policy |

### Message flow

```text
User message
   ↓
FastAPI
   ↓
Authorize patient context
   ↓
Load safe context
   ↓
LLM orchestration
   ↓
Tool calls if needed
   ↓
Tool authorization
   ↓
Generate response
   ↓
Safety filter
   ↓
Persist message / summary
   ↓
Return response
```

---

# 24. Assistant Tool Contract

The assistant may request tools such as:

```text
get_today_tasks
get_upcoming_reminders
get_recent_activity_summary
get_recent_cognitive_summary
start_recommended_activity
get_user_preferences
get_safe_navigation_help
```

Higher-risk actions require explicit confirmation:

```text
create_reminder
change_reminder
change_medication
change_emergency_contact
share_data
change_consent
```

Never allow the model to directly execute arbitrary SQL or arbitrary backend functions.

---

# 25. Voice Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/voice/session` | Create short-lived realtime client credential/session |
| POST | `/voice/transcriptions` | Optional non-realtime audio transcription |
| POST | `/voice/preferences` | Voice/language preferences |

### Browser voice architecture

```text
Browser
  ↓
Request short-lived session credential
  ↓
Backend validates authenticated user
  ↓
Provider session created
  ↓
Browser connects to realtime voice service
  ↓
Voice conversation
  ↓
Backend tools used through controlled mechanism
```

The long-lived provider API secret must stay on the server.

---

# 26. Memory Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/patients/{patientId}/memory` | List approved memory items |
| POST | `/patients/{patientId}/memory` | Create memory item |
| PATCH | `/patients/{patientId}/memory/{memoryId}` | Update |
| DELETE | `/patients/{patientId}/memory/{memoryId}` | Delete |
| POST | `/patients/{patientId}/memory/rebuild-index` | Rebuild embeddings |

Memory categories:

```text
PREFERENCE
ROUTINE
PERSONAL_CONTEXT
CONVERSATION_SUMMARY
ASSISTANT_PREFERENCE
```

Do not automatically convert every conversation into permanent memory.

---

# 27. Safety / Alert Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/patients/{patientId}/sos` | Trigger SOS |
| GET | `/patients/{patientId}/alerts` | List alerts |
| POST | `/patients/{patientId}/alerts` | Create alert |
| GET | `/patients/{patientId}/alerts/{alertId}` | Get |
| PATCH | `/patients/{patientId}/alerts/{alertId}` | Update |
| POST | `/patients/{patientId}/alerts/{alertId}/acknowledge` | Acknowledge |
| POST | `/patients/{patientId}/alerts/{alertId}/resolve` | Resolve |
| POST | `/patients/{patientId}/alerts/{alertId}/escalate` | Escalate |
| GET | `/patients/{patientId}/alerts/{alertId}/events` | Alert history |

Alert states:

```text
OPEN
ACKNOWLEDGED
ESCALATED
RESOLVED
FALSE_POSITIVE
CANCELLED
```

---

# 28. Safety Configuration Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/patients/{patientId}/safety-settings` | Get |
| PATCH | `/patients/{patientId}/safety-settings` | Update |
| GET | `/patients/{patientId}/safety-rules` | List |
| POST | `/patients/{patientId}/safety-rules` | Create |
| PATCH | `/patients/{patientId}/safety-rules/{ruleId}` | Update |
| DELETE | `/patients/{patientId}/safety-rules/{ruleId}` | Remove |

Example safety rules:

```text
INACTIVITY
MISSED_CRITICAL_REMINDER
SOS
FALL_DETECTION
GEOFENCE
UNUSUAL_EVENT
```

---

# 29. Location Endpoints

Location is an **advanced feature**, not a foundational one.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/patients/{patientId}/location/consent` | Location permission state |
| POST | `/patients/{patientId}/location/events` | Store approved location event |
| GET | `/patients/{patientId}/location/latest` | Latest approved location |
| GET | `/patients/{patientId}/geofences` | List |
| POST | `/patients/{patientId}/geofences` | Create |
| PATCH | `/patients/{patientId}/geofences/{geofenceId}` | Update |
| DELETE | `/patients/{patientId}/geofences/{geofenceId}` | Remove |

Important web limitation:

Continuous background location is not equivalent to native mobile tracking. The browser requires user permission and secure context, and background behavior varies by platform/browser. Therefore critical wandering detection should ultimately have a native-device or wearable architecture if treated as a serious safety capability.

---

# 30. Notification Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/notifications` | In-app notifications |
| POST | `/notifications/{notificationId}/read` | Mark read |
| POST | `/notifications/read-all` | Mark all read |
| GET | `/notification-preferences` | Preferences |
| PATCH | `/notification-preferences` | Update |
| POST | `/push/subscriptions` | Register web push |
| DELETE | `/push/subscriptions/{subscriptionId}` | Remove |
| GET | `/push/subscriptions` | List subscriptions |
| POST | `/notifications/test` | Test delivery for development |

Notification channels:

```text
IN_APP
WEB_PUSH
EMAIL
OPTIONAL_SMS
```

Critical care should not depend only on browser notifications.

---

# 31. Reporting Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/patients/{patientId}/reports` | Report history |
| POST | `/patients/{patientId}/reports` | Generate report |
| GET | `/patients/{patientId}/reports/{reportId}` | View |
| GET | `/patients/{patientId}/reports/{reportId}/download` | Secure download |
| POST | `/patients/{patientId}/reports/{reportId}/regenerate` | Regenerate |
| DELETE | `/patients/{patientId}/reports/{reportId}` | Delete |

Reports should contain:

```text
report period
activity summary
cognitive trends
adherence
alerts
AI summary
underlying metrics
limitations/disclaimer
generation timestamp
model/prompt version
```

---

# 32. Analytics Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/patients/{patientId}/analytics/engagement` | Engagement |
| GET | `/patients/{patientId}/analytics/adherence` | Adherence |
| GET | `/patients/{patientId}/analytics/activity` | Activity |
| GET | `/patients/{patientId}/analytics/alerts` | Alert stats |
| GET | `/patients/{patientId}/analytics/trends` | Combined trends |

Admin analytics must be aggregate and de-identified unless explicit access is justified.

---

# 33. File Endpoints

Keep the first release intentionally narrow.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/files/upload-url` | Get presigned upload URL |
| POST | `/files/complete` | Confirm upload |
| GET | `/files/{fileId}` | Metadata |
| GET | `/files/{fileId}/download-url` | Temporary download URL |
| DELETE | `/files/{fileId}` | Delete |

Do not store raw medical documents unless the project purpose later justifies them.

---

# 34. Admin Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/admin/users` | User search |
| GET | `/admin/users/{userId}` | User details |
| PATCH | `/admin/users/{userId}` | Administrative action |
| GET | `/admin/activities` | Manage activity catalog |
| POST | `/admin/activities` | Create activity |
| PATCH | `/admin/activities/{id}` | Update |
| POST | `/admin/activities/{id}/publish` | Publish version |
| GET | `/admin/prompts` | Prompt versions |
| POST | `/admin/prompts` | Create prompt version |
| PATCH | `/admin/prompts/{id}` | Edit |
| GET | `/admin/models` | Model registry |
| POST | `/admin/models` | Register |
| GET | `/admin/feature-flags` | Feature flags |
| PATCH | `/admin/feature-flags/{id}` | Change flag |
| GET | `/admin/audit-logs` | Audit review |

---

# 35. System Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health/live` | Liveness |
| GET | `/health/ready` | Readiness |
| GET | `/version` | Application version |
| GET | `/openapi.json` | OpenAPI |
| GET | `/metrics` | Metrics, protected/internal |

---

# 36. WebSocket / Realtime Channels

REST remains the default API.

Use realtime only where it provides clear value.

## Candidate channels

```text
WS /ws/patients/{patientId}/alerts
WS /ws/patients/{patientId}/dashboard
WS /ws/assistant/{conversationId}
```

Use realtime for:

- incoming caregiver alert
- reminder status changes
- live assistant events
- dashboard refresh events

Do not replace the whole REST API with WebSockets.

---

# 37. Database Design

## Core identity

### users

```text
id UUID PK
email
password_hash
role
status
email_verified_at
last_login_at
created_at
updated_at
```

### sessions

```text
id UUID PK
user_id FK
refresh_token_hash
user_agent
ip_hash_or_metadata
expires_at
revoked_at
created_at
```

### profiles

```text
user_id FK
display_name
date_of_birth
preferred_language
timezone
avatar_file_id
created_at
updated_at
```

---

# 38. Patient Data Model

### patient_profiles

```text
id UUID PK
user_id FK
accessibility_preferences JSONB
care_preferences JSONB
emergency_plan JSONB
created_at
updated_at
```

### caregiver_links

```text
id UUID PK
patient_id FK
caregiver_user_id FK
relationship
permissions JSONB
status
created_at
revoked_at
```

### emergency_contacts

```text
id UUID PK
patient_id FK
name
relationship
phone
email
priority
is_active
created_at
```

### consents

```text
id UUID PK
patient_id FK
purpose
policy_version
granted
granted_at
revoked_at
source
```

---

# 39. Medication Data Model

### medications

```text
id UUID PK
patient_id FK
name
instructions
dosage_text
active
start_date
end_date
created_by
created_at
updated_at
```

### medication_schedules

```text
id UUID PK
medication_id FK
schedule_type
time_of_day
days_of_week
timezone
criticality
active
```

### reminder_events

```text
id UUID PK
reminder_id FK
event_type
occurred_at
actor_id
metadata JSONB
```

---

# 40. Cognitive Data Model

### cognitive_activities

```text
id UUID PK
activity_type
title
description
active_version_id
category
created_at
```

### cognitive_activity_versions

```text
id UUID PK
activity_id FK
version
difficulty
content JSONB
scoring_config JSONB
published_at
```

### activity_sessions

```text
id UUID PK
patient_id FK
activity_id FK
activity_version_id FK
started_at
completed_at
status
difficulty
total_score
accuracy
```

### activity_answers

```text
id UUID PK
session_id FK
question_id
answer JSONB
is_correct
response_time_ms
attempt_number
created_at
```

---

# 41. Trend Data Model

### cognitive_baselines

```text
id UUID PK
patient_id FK
metric
baseline_value
window_definition JSONB
calculated_at
```

### cognitive_trend_snapshots

```text
id UUID PK
patient_id FK
metric
period_start
period_end
value
baseline_difference
sample_count
confidence_metadata JSONB
```

### support_signals

```text
id UUID PK
patient_id FK
signal_type
severity
evidence JSONB
status
created_at
reviewed_at
```

---

# 42. Conversation Data Model

### conversations

```text
id UUID PK
patient_id FK
started_by
title
status
created_at
updated_at
```

### messages

```text
id UUID PK
conversation_id FK
role
content
content_type
provider
model
prompt_version
created_at
```

### memory_items

```text
id UUID PK
patient_id FK
memory_type
content
sensitivity_level
embedding
source_message_id
active
created_at
updated_at
```

Do not embed or persist everything automatically.

---

# 43. Safety Data Model

### alerts

```text
id UUID PK
patient_id FK
type
severity
source
status
summary
evidence JSONB
created_at
acknowledged_at
resolved_at
```

### alert_events

```text
id UUID PK
alert_id FK
event_type
actor_id
metadata JSONB
created_at
```

---

# 44. Notification Data Model

### push_subscriptions

```text
id UUID PK
user_id FK
endpoint
key_material_encrypted
user_agent
created_at
last_success_at
revoked_at
```

### notifications

```text
id UUID PK
user_id FK
type
channel
title
body
priority
reference_type
reference_id
status
sent_at
read_at
created_at
```

### notification_deliveries

```text
id UUID PK
notification_id FK
channel
provider
attempt
status
provider_message_id
error_code
created_at
```

---

# 45. Audit / Platform Data Model

### audit_logs

```text
id UUID PK
actor_user_id
patient_id nullable
action
resource_type
resource_id
result
request_id
ip_metadata
user_agent
metadata JSONB
created_at
```

### outbox_events

```text
id UUID PK
event_type
aggregate_type
aggregate_id
payload JSONB
status
attempts
available_at
processed_at
created_at
```

### ai_runs

```text
id UUID PK
patient_id
conversation_id nullable
task_type
provider
model
prompt_version
input_metadata
output_metadata
latency_ms
token_usage
safety_result
created_at
```

---

# 46. Database Principles

Use:

- foreign keys
- unique constraints
- check constraints
- sensible indexes
- soft-delete only where required
- transactions for multi-table state changes
- migrations for every schema change
- UTC timestamps
- JSONB only for genuinely flexible structures

Important indexes:

```text
users.email
caregiver_links.patient_id
caregiver_links.caregiver_user_id
reminders.patient_id + scheduled_time
activity_sessions.patient_id + started_at
activity_answers.session_id
alerts.patient_id + status
notifications.user_id + created_at
audit_logs.patient_id + created_at
```

For patient isolation, consider PostgreSQL Row-Level Security as an additional defense-in-depth control where the deployment architecture supports it.

---

# 47. AI Architecture

## Principle

Use specialized components rather than one model for everything.

```text
                  AI ORCHESTRATOR
                        │
        ┌───────────────┼─────────────────┐
        ▼               ▼                 ▼
  Conversation      Cognitive          Analytics
        │               │                 │
        ▼               ▼                 ▼
       LLM          Scoring Engine     Trend Engine
        │               │                 │
        ▼               ▼                 ▼
      Tools        Personalization     Support Signals
        │
        ▼
   App Services
```

---

# 48. LLM Responsibilities

The LLM can handle:

- natural-language understanding
- simple conversation
- summarization
- explanation
- structured intent generation
- caregiver report drafting
- navigation assistance

The LLM should not directly decide:

- medication dosage
- emergency severity
- medical diagnosis
- patient authorization
- consent state
- database permissions

Those remain deterministic application logic.

---

# 49. AI Tool Security

Every tool request goes through:

```text
LLM request
   ↓
Schema validation
   ↓
Authenticated user
   ↓
Patient relationship check
   ↓
Permission check
   ↓
Action risk check
   ↓
Optional confirmation
   ↓
Business logic
   ↓
Audit
```

No tool should receive arbitrary SQL.

No tool should bypass service-layer validation.

---

# 50. AI Context Construction

The context passed to the model should be composed from:

```text
current user
patient preferences
today's tasks
approved memories
relevant recent conversation summary
relevant current alerts
current routine context
```

Do not dump the entire database into the prompt.

Use a token-budgeted context builder.

---

# 51. AI Memory Strategy

Use two memory levels.

## Short-term

Current conversation window.

## Long-term

Explicitly approved summaries such as:

```text
"I prefer morning cognitive activities."
"I need larger text."
"My caregiver is my daughter."
```

Store and retrieve only when useful.

Do not turn potentially sensitive health statements into permanent memory automatically.

---

# 52. RAG / Vector Search

Use PostgreSQL + pgvector for semantic retrieval when needed.

Use it primarily for:

- approved conversational memory
- internal knowledge content
- activity explanations
- project-controlled knowledge

Do not use embeddings as a substitute for structured queries.

For example:

```text
"Did I take today's medicine?"
```

must query the reminder/medication tables.

It should not search a vector database and guess.

---

# 53. Cognitive Scoring Strategy

Do not claim a medical cognitive score.

Create a project-defined **activity performance score**.

Possible inputs:

```text
accuracy
response_time
attempts
completion
difficulty
consistency
```

Example:

```text
performance_score =
    weighted_accuracy
  + response_efficiency
  + consistency
  + completion
```

Weights must be documented and evaluated experimentally.

---

# 54. Baseline and Trend Engine

For each patient:

```text
historical activity data
        ↓
minimum data-quality check
        ↓
personal baseline
        ↓
rolling windows
        ↓
trend calculation
        ↓
change signal
        ↓
caregiver-facing explanation
```

Never trigger a strong conclusion from a single poor session.

The engine should be able to report:

```text
insufficient data
stable
improving
variable
possible decrease
```

---

# 55. Personalization Engine

## Stage A

Rule-based:

```text
poor recent performance
→ reduce difficulty

high consistency
→ increase difficulty

low engagement
→ vary activity type

strong preference
→ prioritize preferred task categories
```

## Stage B

ML recommender:

Inputs:

```text
historical scores
response times
completion
difficulty
activity category
time of day
preferences
recent engagement
```

Outputs:

```text
activity
difficulty
expected engagement
```

## Stage C

Research extension:

- contextual bandit
- learning-to-rank
- sequence model
- reinforcement-learning-inspired policy

Only use these after baseline evaluation exists.

---

# 56. Computer Vision Architecture

Advanced module only.

Potential capabilities:

```text
camera
  ↓
frame sampling
  ↓
pose/object model
  ↓
event classifier
  ↓
confidence threshold
  ↓
verification layer
  ↓
alert
```

### Fall detection

Must handle:

- false positives
- occlusion
- sitting vs falling
- camera angle
- lighting
- partial visibility

Do not automatically label every low-confidence event as a medical emergency.

### Privacy decision

Prefer on-device processing where practical.

Do not continuously store raw video unless there is an explicit, justified consented use case.

---

# 57. Reminder / Background Job Architecture

Use asynchronous workers.

```text
PostgreSQL transaction
      ↓
Outbox event
      ↓
Worker queue
      ↓
Reminder dispatcher
      ↓
Notification provider
      ↓
Delivery status
      ↓
Escalation rule
      ↓
Caregiver notification
```

Do not rely on a frontend timer for medication reminders.

The server must own the schedule.

---

# 58. Outbox Pattern

When an important database change occurs:

```text
BEGIN TRANSACTION
  update reminder
  insert outbox_event
COMMIT
```

Worker later publishes/processes the event.

This prevents:

```text
database updated
BUT
notification event lost
```

---

# 59. Notification Architecture

```text
Event
  ↓
Notification service
  ↓
Preference check
  ↓
Channel selection
  ↓
Delivery
  ↓
Delivery log
  ↓
Retry if transient
```

Possible fallback:

```text
web push
   ↓
if unavailable/failed
   ↓
email for configured event
```

Critical workflows should have clear escalation policy rather than assuming browser notifications are guaranteed.

---

# 60. PWA / Offline Architecture

## Offline-first content

Safe to cache:

- application shell
- icons/assets
- activity definitions
- selected cognitive activities
- non-sensitive UI configuration

Avoid caching:

- patient health details
- full conversation history
- emergency contacts
- raw audio
- sensitive reports

## Offline session

```text
Activity
 ↓
IndexedDB
 ↓
local session queue
 ↓
network returns
 ↓
sync API
 ↓
server validates
 ↓
server persists
 ↓
local queue clears
```

Use event IDs / idempotency keys to avoid double submission.

---

# 61. Current Web Platform Decisions

## Push

Use Service Worker + Web Push.

## Location

Require explicit user permission and HTTPS.

## Camera / microphone

Use only after explicit permission.

## Offline

Use Service Worker + IndexedDB.

## Mobile

Do not create a separate native mobile app until the web/PWA experience is stable.

If future background location, wearable data, or deeper OS integration becomes a serious requirement, introduce a native/mobile client as a second client of the same API.

---

# 62. Frontend Component Architecture

```text
components/
├── ui/
├── layout/
├── auth/
├── elderly/
│   ├── BigActionButton
│   ├── TodayCard
│   ├── ReminderCard
│   ├── ActivityCard
│   ├── VoiceButton
│   └── SosButton
├── caregiver/
│   ├── PatientHeader
│   ├── TrendChart
│   ├── AdherenceChart
│   ├── AlertList
│   └── WeeklySummary
├── assistant/
├── activities/
├── safety/
└── reports/
```

Keep domain components separate from generic UI primitives.

---

# 63. Frontend State Management

## Server state

Use TanStack Query.

Use it for:

- patients
- reminders
- activities
- dashboard data
- reports
- notifications

## UI state

Use React state/context first.

Only add a global state library where actual cross-page client state justifies it.

Avoid putting fetched server data into a second global store.

---

# 64. Backend Code Structure

```text
backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   └── permissions.py
│   │
│   ├── db/
│   │   ├── session.py
│   │   ├── models/
│   │   └── migrations/
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── patients.py
│   │       ├── reminders.py
│   │       ├── activities.py
│   │       ├── assistant.py
│   │       ├── safety.py
│   │       ├── analytics.py
│   │       ├── reports.py
│   │       └── ...
│   │
│   ├── services/
│   ├── schemas/
│   ├── repositories/
│   ├── workers/
│   ├── ai/
│   └── tests/
```

---

# 65. AI Provider Abstraction

Do not hard-code the entire application around one AI vendor.

Define interfaces such as:

```text
LLMProvider
EmbeddingProvider
SpeechToTextProvider
TextToSpeechProvider
RealtimeVoiceProvider
VisionProvider
```

Then implement:

```text
providers/
├── openai/
├── local/
└── mock/
```

This gives you:

- easier testing
- provider replacement
- local fallback
- lower vendor lock-in
- clearer architecture

---

# 66. API Security Middleware

Every protected request should go through:

```text
request
 ↓
request ID
 ↓
authentication
 ↓
rate limit
 ↓
input validation
 ↓
authorization
 ↓
service layer
 ↓
audit when required
 ↓
response
```

Never rely on page-level visibility for security.

---

# 67. Rate Limiting

Apply stricter limits to:

```text
login
password reset
verification email
voice session creation
AI requests
file upload
report generation
SOS abuse protection
```

Different roles/endpoints may have different budgets.

---

# 68. Abuse Protection

Add:

- login throttling
- CAPTCHA/challenge for abuse where needed
- request size limits
- file type limits
- content-length limits
- timeout limits
- AI token budget limits
- concurrency caps for long-running jobs

---

# 69. Security Standards

Use OWASP ASVS 5.0 as the detailed application-security verification baseline.

Use OWASP Top 10:2025 as the awareness checklist.

Security review categories:

```text
Broken access control
Security misconfiguration
Supply-chain failures
Cryptographic failures
Injection
Insecure design
Authentication failures
Data integrity failures
Security logging
Exceptional conditions
```

---

# 70. Privacy Architecture

## Data classification

```text
PUBLIC
INTERNAL
PERSONAL
SENSITIVE
HIGH-SENSITIVITY
```

Examples:

```text
PUBLIC
activity instructions

PERSONAL
name / preferences

SENSITIVE
cognitive performance / conversations

HIGH-SENSITIVITY
location / emergency data / potentially sensitive free text
```

Access rules should be driven by classification.

---

# 71. Data Retention Policy

Do not hard-code retention periods until the project's institutional/privacy requirements are reviewed.

Implement retention classes:

```text
SHORT_LIVED
STANDARD
LONG_TERM
AUDIT
USER_CONTROLLED
```

Every deletion or retention rule should be auditable.

---

# 72. AI Safety Layer

Before returning an AI response:

```text
response
 ↓
schema validation
 ↓
medical/safety policy checks
 ↓
sensitive-content handling
 ↓
tool/result consistency check
 ↓
final response
```

The assistant should refuse or redirect when:

- user requests diagnosis
- user asks to change medication dosage
- user reports a serious emergency
- model lacks required data
- output would be unsafe

---

# 73. Emergency Handling

Emergency events should be deterministic.

Example:

```text
SOS clicked
 ↓
server creates SOS alert
 ↓
notify configured caregiver(s)
 ↓
show emergency instructions
 ↓
record event
```

Do not let the LLM decide whether the SOS event is “serious enough.”

---

# 74. Reports: Deterministic + Generative

Do not ask the LLM to calculate statistics.

Correct pattern:

```text
Database
 ↓
Analytics service
 ↓
calculated metrics
 ↓
structured report object
 ↓
LLM wording/summarization
 ↓
final report
```

The numbers come from code.

The language comes from AI.

This makes results reproducible.

---

# 75. API Response Design

For resources:

```json
{
  "data": {
    "id": "..."
  }
}
```

For lists:

```json
{
  "data": [],
  "meta": {
    "next_cursor": null,
    "has_more": false
  }
}
```

For asynchronous jobs:

```json
{
  "data": {
    "job_id": "...",
    "status": "QUEUED"
  }
}
```

---

# 76. Long-Running Job Pattern

Use async jobs for:

- weekly reports
- large PDF generation
- re-indexing memory embeddings
- model analysis
- large data recomputation

Pattern:

```text
POST /reports
   ↓
202 Accepted
   ↓
job_id
   ↓
worker
   ↓
GET /reports/{id}
```

Do not block HTTP requests for long AI/ML tasks.

---

# 77. API Documentation

FastAPI will generate OpenAPI documentation from typed endpoint definitions and Pydantic schemas.

Maintain:

```text
/docs/API.md
/docs/openapi/
```

Every endpoint should document:

- authentication
- authorization
- request schema
- response schema
- errors
- example
- idempotency requirements
- pagination/filtering behavior

---

# 78. Environment Variables

Example:

```text
APP_ENV
APP_URL
API_URL

DATABASE_URL
REDIS_URL

JWT_SECRET
SESSION_SECRET
ENCRYPTION_KEY

OPENAI_API_KEY

WEB_PUSH_PUBLIC_KEY
WEB_PUSH_PRIVATE_KEY

EMAIL_PROVIDER_KEY

OBJECT_STORAGE_BUCKET
OBJECT_STORAGE_ACCESS_KEY
OBJECT_STORAGE_SECRET_KEY

SENTRY_DSN

OTEL_EXPORTER_ENDPOINT
```

Never commit real secrets.

Use `.env.example`, not `.env`.

---

# 79. Local Development

Required local services:

```text
Next.js
FastAPI
PostgreSQL
Redis
Worker
```

Preferred setup:

```text
docker compose up
```

Then:

```text
web → localhost
api → localhost
postgres → internal
redis → internal
worker → internal
```

---

# 80. Container Strategy

Create:

```text
Dockerfile.web
Dockerfile.api
Dockerfile.worker
docker-compose.yml
```

Do not put database initialization logic inside application startup if migrations should be controlled separately.

---

# 81. CI/CD Pipeline

Every pull request:

```text
format
lint
typecheck
unit tests
integration tests
build
dependency audit
secret scan
```

Main branch:

```text
build
test
container build
deploy
smoke test
```

Recommended repository protections:

- protected main branch
- pull request reviews
- required CI
- no direct secret commits
- commit history retained

---

# 82. Testing Strategy

## Unit tests

Frontend:

- utility functions
- score calculations
- formatting
- state transitions

Backend:

- permission rules
- scoring engine
- reminder scheduling
- escalation logic
- trend calculations

## Integration tests

Test:

```text
API
 ↓
service
 ↓
database
 ↓
worker/event
```

## End-to-end

Use Playwright for:

- registration
- login
- caregiver creates patient
- caregiver creates reminder
- patient acknowledges reminder
- patient completes cognitive activity
- caregiver views trend
- caregiver receives alert

---

# 83. AI Evaluation

Create a fixed evaluation set.

Categories:

```text
routine questions
reminder questions
navigation questions
ambiguous questions
safety-sensitive questions
medical-boundary questions
prompt-injection attempts
privacy-sensitive questions
```

Metrics:

```text
groundedness
relevance
instruction adherence
tool-call correctness
unsafe-response rate
hallucination rate
response latency
```

Store evaluation results by model/prompt version.

---

# 84. AI Regression Testing

Every meaningful prompt/model change should run the same evaluation set.

Record:

```text
model
prompt version
date
test set
score
failure examples
decision
```

Never change a production prompt and forget which version generated historical reports.

---

# 85. ML Evaluation

For personalization:

Compare:

```text
random recommendation
fixed-rule recommendation
ML recommendation
```

Possible metrics:

```text
completion rate
accepted recommendation rate
response time
accuracy
engagement
```

For classification tasks:

```text
precision
recall
F1
ROC-AUC where appropriate
confusion matrix
```

Do not select metrics without explaining why they fit the task.

---

# 86. Cognitive Trend Validation

Evaluate:

- stability under identical input
- sensitivity to missing data
- false-alert behavior
- baseline calculation
- effect of outliers
- short-history behavior

Example synthetic scenario:

```text
Day 1–7: stable
Day 8: one very low score
Day 9–14: stable
```

Expected:

```text
No strong decline signal from one outlier.
```

---

# 87. Usability Evaluation

Use real volunteers only with appropriate consent and project approval.

Test:

### Elderly experience

- can user start activity?
- can user acknowledge reminder?
- can user call assistant?
- can user trigger SOS?

### Caregiver experience

- can caregiver understand status?
- can caregiver identify missed reminders?
- can caregiver interpret trends?
- can caregiver respond to alert?

Measure:

```text
task completion rate
time on task
error rate
subjective usability
qualitative feedback
```

---

# 88. Performance Testing

Measure:

```text
API latency
p95 / p99
database query time
background job latency
AI response latency
concurrent users
error rate
```

Run controlled tests.

Do not present a single laptop benchmark as production scalability evidence.

---

# 89. Security Testing

Include:

```text
authentication tests
authorization tests
IDOR/BOLA tests
SQL injection
XSS
CSRF
rate limiting
session invalidation
input validation
file upload abuse
secret exposure
dependency vulnerabilities
```

Run automated and manual checks.

---

# 90. Accessibility Testing

Check:

```text
keyboard
screen reader
contrast
focus
zoom
large text
mobile touch targets
voice flow
error messaging
```

Test both normal and elderly-oriented interfaces.

---

# 91. Observability

Every request should have:

```text
request_id
trace_id where enabled
actor_id when authenticated
route
status
latency
```

Never log:

- passwords
- auth tokens
- full sensitive prompts
- full patient medical content
- raw audio

Log summarized/structured information instead.

---

# 92. Application Metrics

Track:

```text
api_request_count
api_error_count
api_latency
db_query_latency
worker_job_count
worker_failures
notification_delivery_rate
ai_request_count
ai_latency
ai_error_rate
activity_completion_rate
reminder_adherence
alert_resolution_time
```

Keep user-level analytics separate from operational metrics.

---

# 93. Feature Flags

Implement feature flags for:

```text
VOICE
PUSH
ML_PERSONALIZATION
AI_MEMORY
FALL_DETECTION
LOCATION
WEEKLY_REPORTS
CLINICIAN_ROLE
```

This allows advanced features to be enabled safely without code branching everywhere.

---

# 94. Recommended MVP

Even without a deadline, define a stable foundation.

The **Core Product** should include:

```text
Authentication
Patient + caregiver relationship
Patient profile
Consent
Medication
Routine
Reminder
Reminder acknowledgement
4+ cognitive activities
Activity scoring
Cognitive history
Cognitive trends
Text AI assistant
Caregiver dashboard
Alerts
Weekly summary
Security
Audit
PWA shell
```

---

# 95. Advanced Product

After Core Product:

```text
Voice assistant
Long-term assistant memory
Web push
Offline cognitive sessions
Adaptive rule-based difficulty
ML personalization
Advanced analytics
PDF reports
Reviewer role
```

---

# 96. Research / Innovation Product

After Advanced:

```text
ML recommendation comparison
Longitudinal trend detection
Computer vision fall detection
Geofence support
Mood/engagement research
Wearable data
Native mobile client
On-device AI
Privacy-preserving ML
FHIR interoperability
```

---

# 97. FHIR / Health Interoperability

Do not force FHIR into the first implementation.

However, keep the data model conceptually mappable to healthcare interoperability resources.

Potential mappings:

```text
Patient
RelatedPerson
MedicationRequest
Observation
CarePlan
Communication
Device
```

Use FHIR only when a real integration use case exists.

---

# 98. API / Domain Separation

Frontend must never directly access PostgreSQL.

Correct:

```text
Frontend
 ↓
FastAPI
 ↓
Service
 ↓
Repository
 ↓
Database
```

Incorrect:

```text
Frontend
 ↓
Database
```

AI provider access also goes through the backend/provider adapter where secrets or patient authorization are involved.

---

# 99. Service Layer Responsibilities

Example:

### ReminderService

```text
create_reminder
update_reminder
acknowledge_reminder
skip_reminder
calculate_next_occurrence
trigger_escalation
```

### CognitiveService

```text
start_session
submit_answer
calculate_score
complete_session
get_history
```

### TrendService

```text
calculate_baseline
calculate_trend
generate_support_signal
```

### AssistantService

```text
build_context
route_tools
run_model
validate_output
persist_message
```

Keep these rules out of route handlers.

---

# 100. Repository Layer

Repositories handle data access.

Example:

```text
PatientRepository
ReminderRepository
MedicationRepository
ActivityRepository
SessionRepository
AlertRepository
ConversationRepository
ReportRepository
AuditRepository
```

Services coordinate business logic.

Routes handle HTTP concerns.

---

# 101. Domain Events

Useful events:

```text
PATIENT_CREATED
CAREGIVER_CONNECTED
REMINDER_CREATED
REMINDER_DUE
REMINDER_MISSED
REMINDER_ACKNOWLEDGED
ACTIVITY_STARTED
ACTIVITY_COMPLETED
COGNITIVE_SIGNAL_CREATED
SOS_TRIGGERED
ALERT_ACKNOWLEDGED
ALERT_RESOLVED
REPORT_GENERATED
AI_RUN_COMPLETED
```

Events are internal contracts, not automatically public APIs.

---

# 102. State Machines

Explicitly model state where appropriate.

### Reminder

```text
SCHEDULED
 → DELIVERED
 → ACKNOWLEDGED
```

or

```text
SCHEDULED
 → MISSED
 → ESCALATED
 → RESOLVED
```

### Alert

```text
OPEN
 → ACKNOWLEDGED
 → RESOLVED
```

or

```text
OPEN
 → ESCALATED
 → ACKNOWLEDGED
 → RESOLVED
```

This prevents impossible state combinations.

---

# 103. Data Consistency Rules

Examples:

- acknowledgement must belong to the authenticated patient's reminder
- caregiver must have permission to change patient routines
- clinician/reviewer is read-only unless explicitly granted another capability
- deleted patient cannot receive new reminders
- revoked consent must stop the related processing capability
- report must reference a valid source period
- AI summary must reference the metrics used to produce it

---

# 104. Security and Authorization Matrix

| Operation | Elderly | Caregiver | Reviewer | Admin |
|---|---:|---:|---:|---:|
| View own profile | ✅ | ✅ | ✅ | ✅ |
| View patient profile | Own | Linked | Granted | Limited |
| Manage medications | Limited | ✅ | ❌ | Limited |
| Complete activities | ✅ | ❌ | ❌ | ❌ |
| View cognition | Own | ✅ | ✅ | Restricted |
| Manage caregiver link | ❌ | ✅ | ❌ | Limited |
| Trigger SOS | ✅ | ✅ configurable | ❌ | ❌ |
| Resolve alert | Own/configured | ✅ | ✅ if granted | Limited |
| Generate report | ❌ | ✅ | ✅ | Restricted |
| Manage system activities | ❌ | ❌ | ❌ | ✅ |

Exact permissions should be encoded as policies, not hard-coded page checks.

---

# 105. UI Requirements for Elderly Users

Use:

- large primary actions
- one clear action per screen where possible
- minimal menus
- consistent icon + text pairing
- readable typography
- persistent home/back control
- no dense tables
- clear success/failure states
- confirmation before destructive actions
- voice alternative where useful

Avoid:

- small text
- deep navigation
- complicated dashboards
- unnecessary animation
- jargon
- hidden actions

---

# 106. Caregiver Dashboard Information Hierarchy

Top:

```text
Patient
Current status
Urgent alerts
```

Then:

```text
Today's care
Cognitive trend
Medication adherence
Activity engagement
```

Then:

```text
Recent activity
Conversation summary
Reports
History
```

The dashboard should answer:

> “What happened, what is important, and what needs my attention?”

---

# 107. Cognitive Activity UX

Each session:

```text
Introduction
 ↓
Activity
 ↓
Immediate feedback (where appropriate)
 ↓
Next activity
 ↓
Completion
 ↓
Simple positive summary
```

Do not expose an alarming clinical-style score to the elderly user.

The caregiver view may contain research-oriented metrics with explanations.

---

# 108. Assistant UX

Examples:

```text
User:
"What do I have today?"

Assistant:
"You have your morning medicine at 9:00,
a memory activity at 11:00,
and lunch at 1:00."
```

For uncertain information:

```text
"I don't have enough information to answer that."
```

Never fabricate.

For medical questions:

```text
"I can help you find your saved information,
but I can't diagnose or change treatment."
```

---

# 109. Prompt Management

Prompts must be versioned.

Store:

```text
prompt_id
version
purpose
system_instructions
tool_policy
safety_rules
created_by
created_at
published_at
```

AI runs store the prompt version used.

This makes evaluation and debugging possible.

---

# 110. Model Registry

Store:

```text
provider
model
capability
version/identifier
status
cost metadata
evaluation result
enabled_for
```

Never silently change the model used for an important experiment.

---

# 111. AI Cost Controls

Implement:

- per-user request budgets
- max output tokens
- context size controls
- caching where safe
- summary compaction
- retry policy
- model tiering

Example:

```text
simple task → smaller/cheaper model
complex report → stronger model
realtime voice → realtime provider
```

---

# 112. Error Handling

Frontend should translate technical errors into user-friendly messages.

Backend should use stable error codes.

Example:

```text
AUTH_INVALID_CREDENTIALS
AUTH_SESSION_EXPIRED
FORBIDDEN_PATIENT_ACCESS
REMINDER_NOT_FOUND
ACTIVITY_SESSION_EXPIRED
CONSENT_REQUIRED
AI_PROVIDER_UNAVAILABLE
REPORT_JOB_FAILED
RATE_LIMITED
```

---

# 113. API Idempotency Rules

Example:

```text
POST /reminders/{id}/acknowledge
Idempotency-Key: uuid
```

If the client repeats the request:

```text
same key
→ same logical result
```

This is especially important for flaky mobile/web connections.

---

# 114. Database Transactions

Use transactions for:

### Reminder acknowledgement

```text
update reminder state
insert reminder event
possibly insert outbox event
```

### SOS

```text
create alert
insert alert event
insert notification event
```

### Caregiver removal

```text
revoke link
revoke permissions
audit action
```

---

# 115. Background Worker Jobs

Recommended jobs:

```text
send_due_reminders
detect_missed_reminders
escalate_alerts
generate_weekly_reports
recompute_trends
generate_embeddings
cleanup_expired_sessions
cleanup_expired_files
send_email_notifications
retry_failed_notifications
```

Each job must be retry-safe.

---

# 116. Search

Use PostgreSQL full-text search for structured/admin content.

Use pgvector only for semantic use cases.

Do not introduce Elasticsearch/OpenSearch unless scale or functionality requires it.

---

# 117. Caching

Cache:

- static activity catalog
- safe public configuration
- dashboard aggregates where useful
- non-sensitive reference data

Do not blindly cache sensitive patient responses.

Cache keys must include authorization scope where required.

---

# 118. Database-Level Privacy

Where practical:

- separate tenant/patient ownership fields
- use PostgreSQL row security as defense-in-depth
- avoid direct DB credentials in application logs
- restrict DB user privileges
- separate migration credentials from runtime credentials where practical

---

# 119. Backup and Recovery

For a serious deployment:

```text
automated PostgreSQL backups
restore verification
migration rollback/recovery plan
object storage lifecycle
Redis treated as disposable cache where possible
```

Do not treat Redis as the source of truth.

---

# 120. Deployment Architecture

## Recommended production layout

```text
                    CDN / HTTPS
                        │
                        ▼
                   Next.js App
                        │
                        ▼
                  FastAPI API
              ┌─────────┼──────────┐
              ▼         ▼          ▼
         PostgreSQL   Redis     AI Provider
              │         │          │
              │         ▼          │
              │      Worker        │
              │         │          │
              └─────────┼──────────┘
                        ▼
                 Object Storage
```

The exact cloud vendor is secondary to keeping this topology reproducible.

---

# 121. Environment Strategy

```text
development
staging
production
```

Never use production patient data in development.

Use:

- synthetic data
- masked test data
- dedicated staging database
- separate AI credentials
- separate push credentials

---

# 122. Seed Data

Create demo seed data:

```text
2 elderly users
2 caregivers
6–8 activities
sample medications
sample routines
sample reminder events
sample cognitive history
sample alerts
sample reports
```

This should make a demo reproducible with one command.

---

# 123. Demo Mode

Provide an optional clearly labeled:

```text
DEMO MODE
```

It may:

- use synthetic profiles
- disable real emergency messages
- use mock notification delivery
- use deterministic sample data

Never let demo mode be mistaken for real patient data.

---

# 124. Documentation Set

Repository should contain:

```text
README.md
PLAN.md
ARCHITECTURE.md
API.md
DATABASE.md
AI.md
SECURITY.md
PRIVACY.md
TESTING.md
DEPLOYMENT.md
CONTRIBUTING.md
CHANGELOG.md
```

---

# 125. Diagrams Required

Create:

1. System context diagram
2. High-level architecture
3. Deployment diagram
4. Use-case diagram
5. Domain model / ER diagram
6. Authentication sequence
7. Reminder sequence
8. Cognitive session sequence
9. AI assistant sequence
10. Alert escalation sequence
11. Report generation sequence
12. Offline sync sequence
13. Optional fall-detection pipeline

---

# 126. Main User Flows

## Flow A — First setup

```text
Register
 ↓
Verify
 ↓
Choose role
 ↓
Profile
 ↓
Consent
 ↓
Caregiver relationship
 ↓
Patient setup
 ↓
Dashboard
```

## Flow B — Daily activity

```text
Open app
 ↓
My Day
 ↓
Start cognitive session
 ↓
Complete activities
 ↓
Score
 ↓
Trend update
 ↓
Caregiver dashboard refresh
```

## Flow C — Reminder

```text
Schedule
 ↓
Reminder due
 ↓
Notification
 ↓
User acknowledges
 ↓
Event saved
 ↓
Adherence updated
```

## Flow D — Missed reminder

```text
Due
 ↓
No acknowledgement
 ↓
Missed threshold
 ↓
Escalation rule
 ↓
Caregiver notification
 ↓
Resolution
```

## Flow E — Assistant

```text
User asks
 ↓
Intent
 ↓
Relevant data/tool
 ↓
Tool result
 ↓
LLM response
 ↓
Safety validation
 ↓
Response
```

---

# 127. Acceptance Criteria — Core Product

The project is not “done” until all of these work:

### Identity

- registration works
- login works
- logout works
- unauthorized access is rejected

### Patient/caregiver

- caregiver can create/connect patient
- permissions are enforced
- patient sees only own data

### Cognitive

- activities run
- answers are persisted
- score is reproducible
- trend graph uses stored data
- no diagnostic claim is shown

### Care

- reminder can be created
- reminder is delivered
- acknowledgement is recorded
- missed reminder can escalate

### AI

- assistant can answer trusted routine questions
- assistant uses tools correctly
- unsafe medical claims are blocked
- AI failures degrade gracefully

### Dashboard

- caregiver sees current patient status
- trends work
- alerts work
- report works

### Security

- secrets are not exposed
- authorization is tested
- audit trail exists
- sensitive data is not logged

---

# 128. Acceptance Criteria — Advanced

- voice assistant works
- PWA install works
- push subscription works
- offline activity sync works
- personalization changes recommendations
- weekly report generation is reproducible
- AI evaluation suite runs automatically
- ML baseline is compared with advanced method

---

# 129. Acceptance Criteria — Research

- clear research question
- baseline method
- advanced method
- controlled experiment
- defined dataset
- evaluation metrics
- statistical/quantitative comparison where appropriate
- limitations documented
- reproducible experiment pipeline

---

# 130. Research Questions

Potential primary research question:

> Does personalized cognitive-activity selection based on longitudinal user performance improve engagement and task completion compared with fixed activity selection?

Secondary questions:

1. Does adaptive difficulty improve completion?
2. Can longitudinal metrics identify stable patterns better than single-session scores?
3. Does voice interaction reduce interface friction for elderly users?
4. Can caregiver dashboards improve information retrieval efficiency compared with raw logs?
5. How accurately can an AI summarizer produce evidence-grounded non-diagnostic summaries?

---

# 131. Dataset Strategy

Use three sources:

## Public datasets

Only where licensing and intended use are appropriate.

## Synthetic data

Use for:

- development
- edge cases
- load testing
- reproducible demonstrations

Label clearly as synthetic.

## Consent-based usability data

Use anonymized volunteer interactions for:

- usability
- activity interaction
- voice UX
- interface evaluation

Do not imply that small project data provides clinical validation.

---

# 132. Data Ethics

Before collecting user data:

- define purpose
- minimize fields
- obtain informed consent
- define retention
- define deletion
- protect raw media
- anonymize research exports
- avoid publishing identifying data

Keep research data separate from production data.

---

# 133. AI/ML Experiment Repository

```text
ml/
├── datasets/
├── notebooks/
├── preprocessing/
├── baselines/
├── experiments/
├── evaluation/
├── configs/
└── reports/
```

Every experiment should record:

```text
dataset version
feature version
model
hyperparameters
random seed
metrics
result
```

---

# 134. Versioning Strategy

Version:

```text
API
database migrations
activity definitions
activity scoring rules
prompts
AI models
ML models
reports
feature flags
```

Example:

```text
API v1
Prompt assistant-safe-v3
Scoring cognitive-v2
Recommender model-v1
```

---

# 135. Git Strategy

Recommended:

```text
main
develop (optional)
feature/*
fix/*
experiment/*
```

Commit examples:

```text
feat: add reminder acknowledgement endpoint
feat: add cognitive trend calculation
fix: prevent duplicate reminder acknowledgement
test: add caregiver permission tests
docs: add AI safety policy
```

---

# 136. Pull Request Checklist

Every PR should answer:

```text
What changed?
Why?
Which endpoints changed?
Which DB migrations changed?
What tests were added?
Any security impact?
Any privacy impact?
Any AI prompt/model impact?
Any API compatibility impact?
```

---

# 137. Quality Gates

Do not move forward if:

### Foundation gate

Auth or DB is unstable.

### Data gate

Patient isolation is not proven.

### Cognitive gate

Scores are not reproducible.

### AI gate

Unsafe responses are uncontrolled.

### Notification gate

Important events can be lost.

### Research gate

Baseline cannot be reproduced.

---

# 138. Implementation Order

No calendar is required. Follow these gates in order.

## Gate 0 — Product and architecture lock

Finalize:

- requirements
- roles
- page map
- API contract
- data model
- architecture
- security assumptions

## Gate 1 — Project foundation

Implement:

- repository
- Docker
- CI
- Next.js
- FastAPI
- PostgreSQL
- Redis
- migrations
- environment handling
- logging

## Gate 2 — Identity

Implement:

- registration
- verification
- login
- sessions
- logout
- roles
- permissions

## Gate 3 — Patient/caregiver core

Implement:

- patient profiles
- caregiver invitations
- permissions
- consent
- emergency contacts

## Gate 4 — Care management

Implement:

- medication
- routines
- reminders
- acknowledgement
- escalation
- notifications

## Gate 5 — Cognitive engine

Implement:

- activity catalog
- sessions
- scoring
- history
- baseline
- trend analytics

## Gate 6 — Dashboard

Implement:

- patient overview
- cognitive charts
- adherence
- alerts
- timeline
- report view

## Gate 7 — AI assistant

Implement:

- text chat
- context builder
- tool calling
- safety layer
- logging
- evaluation

## Gate 8 — Voice/PWA

Implement:

- realtime voice
- web push
- service worker
- IndexedDB
- offline queue
- sync

## Gate 9 — Personalization

Implement:

- rule engine
- recommendation model
- evaluation
- model registry

## Gate 10 — Advanced safety

Implement only after the rest is stable:

- computer vision
- fall detection
- location
- geofence
- optional native client

## Gate 11 — Research and hardening

Implement:

- experiment pipeline
- security testing
- usability study
- performance tests
- AI evaluation
- final documentation

---

# 139. Definition of Done

The product is complete when:

```text
✅ user accounts work
✅ patient/caregiver authorization is correct
✅ data isolation is tested
✅ routines and reminders work
✅ cognitive activities work
✅ scores are reproducible
✅ trends work
✅ dashboard works
✅ alerts work
✅ AI assistant works safely
✅ report generation works
✅ audit logs exist
✅ PWA works
✅ tests pass
✅ security checks pass
✅ deployment is reproducible
✅ research evaluation is reproducible
✅ documentation matches implementation
```

---

# 140. What Should NOT Be Built First

Do not begin with:

- fall detection
- wandering detection
- complex reinforcement learning
- native mobile app
- clinician integration
- FHIR interoperability
- large-scale distributed infrastructure
- custom LLM training

First make the core data and workflows correct.

---

# 141. Final Technology Decisions and Rationale

## Next.js + TypeScript

Chosen because it gives a strong web application foundation, App Router support, TypeScript, server/client composition, and a straightforward path to a responsive PWA.

## FastAPI

Chosen because the project has strong Python AI/ML requirements and FastAPI provides typed request handling, Pydantic validation, and generated OpenAPI documentation.

## PostgreSQL

Chosen as the system of record because the domain has strong relational structure and transactional workflows.

## SQLAlchemy + Alembic

Chosen because the backend is Python-based and the stack benefits from explicit ORM/data-access separation plus controlled migrations.

## Redis

Chosen for cache, transient state, rate limiting, and job brokering.

## pgvector

Chosen because semantic memory can live beside structured patient/application data instead of creating a second database too early.

## Next.js frontend + FastAPI API

Chosen instead of a single-framework full-stack implementation because AI/ML workloads, research code, background processing, and Python ecosystem integration are first-class requirements.

## Modular monolith

Chosen instead of microservices because it keeps deployment and correctness manageable while retaining clean domain boundaries.

## PWA

Chosen instead of starting with React Native because the current product is a website and PWA capabilities cover installation, offline shell, and browser push sufficiently for the core experience.

## Provider abstraction for AI

Chosen to prevent the data model/business logic from becoming dependent on a single AI vendor.

---

# 142. Current Reference / Technology Notes

The implementation should pin exact package versions at project bootstrap and keep lockfiles committed. Avoid continuously chasing “latest” packages once the stack is stable.

Relevant current official references used to inform this plan:

- Next.js documentation: https://nextjs.org/docs
- FastAPI request validation / OpenAPI: https://fastapi.tiangolo.com/tutorial/body/
- SQLAlchemy 2.x documentation: https://docs.sqlalchemy.org/en/20/
- Alembic: https://alembic.sqlalchemy.org/
- PostgreSQL Row-Level Security: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- pgvector: https://github.com/pgvector/pgvector
- Redis documentation: https://redis.io/docs/latest/
- TanStack Query: https://tanstack.com/query/latest/docs/framework/react
- OpenAI Responses API: https://developers.openai.com/api/reference/responses/overview
- OpenAI Realtime API: https://developers.openai.com/api/docs/guides/realtime
- Web Push API: https://developer.mozilla.org/en-US/docs/Web/API/Push_API
- Service Worker API: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API
- IndexedDB: https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB
- Geolocation API: https://developer.mozilla.org/en-US/docs/Web/API/Geolocation
- WCAG 2.2: https://www.w3.org/WAI/standards-guidelines/wcag/
- OWASP ASVS 5.0: https://owasp.org/www-project-application-security-verification-standard/
- OWASP Top 10:2025: https://owasp.org/www-project-top-ten/

---

# 143. Project Governance Decisions

## Decision 1

**No SIH dependency.**

The project is now an independent capstone/product and should be optimized for quality, technical depth, research contribution, and real-world usefulness rather than SIH compliance.

## Decision 2

**No fixed implementation deadline in this architecture document.**

Work proceeds by capability gates.

## Decision 3

**Website-first.**

Native mobile becomes an optional second client.

## Decision 4

**Healthcare assistance, not diagnosis.**

This wording should remain consistent across UI, report, AI prompts, research and presentation.

## Decision 5

**Structured data before AI.**

If the application can answer a question deterministically from PostgreSQL, use PostgreSQL.

## Decision 6

**AI does not own business truth.**

AI proposes language/actions; application services enforce truth and authorization.

## Decision 7

**Metrics come from code.**

LLMs summarize calculated results; they do not invent or calculate the underlying numbers.

## Decision 8

**Security is part of architecture, not a final add-on.**

Authorization, consent, audit, privacy and safe AI behavior are built into each module.

---

# 144. Final Product Blueprint

The final product should feel like:

```text
                 AI COGNITIVE CARE PLATFORM
                           │
          ┌────────────────┴────────────────┐
          │                                 │
          ▼                                 ▼
   ELDERLY EXPERIENCE                 CAREGIVER EXPERIENCE
          │                                 │
   ┌──────┼──────┐                  ┌───────┼────────┐
   │      │      │                  │       │        │
 Voice  Activities Reminders      Trends  Alerts   Reports
   │      │      │                  │       │        │
   └──────┼──────┘                  └───────┼────────┘
          │                                 │
          └──────────────┬──────────────────┘
                         ▼
                APPLICATION SERVICES
                         │
     ┌───────────────────┼────────────────────┐
     ▼                   ▼                    ▼
 Cognitive           Care Engine          Safety Engine
 Engine              & Scheduling         & Alerts
     │                   │                    │
     └───────────────────┼────────────────────┘
                         ▼
                    AI ORCHESTRATOR
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
      LLM             ML Models           Voice
       │                 │                 │
       └─────────────────┼─────────────────┘
                         ▼
                     PostgreSQL
                     + pgvector
                     + Redis
```

---

# 145. Final Product Principle

The product should pass this test:

> **Can an elderly user use it without feeling overwhelmed, can a caregiver understand what matters without reading raw data, and can every AI-generated statement be traced back to application data or clearly labeled as generated language?**

If the answer is yes, the project is solving a real problem rather than simply combining technologies.

---

# 146. Final Implementation Priority

The final priority order is:

```text
1. Correctness
2. Security / privacy
3. Core user workflows
4. Data quality
5. Accessibility
6. AI usefulness and safety
7. Analytics
8. Personalization
9. Advanced CV / location
10. Research extensions
11. Scaling optimization
```

Do not reverse this order merely because a feature looks more impressive in a demo.

---

# 147. One-Line Project Definition

**An accessibility-first, AI-assisted web platform that provides personalized cognitive activities, everyday care support, longitudinal performance insights, safe conversational assistance, and caregiver-centered monitoring for elderly people with cognitive impairment.**
