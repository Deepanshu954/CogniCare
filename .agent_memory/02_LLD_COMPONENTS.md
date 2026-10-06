# CogniCare: Low-Level Design & Component Architecture (LLD)

## 1. Design Patterns & Architectural Paradigms

CogniCare enforces strict separation of concerns via standard enterprise design patterns:

### A. Repository Pattern (`backend/app/repositories/`)
- Isolates raw database persistence logic and SQLAlchemy queries from business workflows.
- Implemented repositories:
  - `UserRepository`: User lookup, registration, role querying.
  - `PatientRepository`: Patient profiles, caregiver permissions, emergency contacts, consents.
  - `CareRepository`: Medication prescriptions, routines, scheduled reminder lifecycles.
  - `CognitionRepository`: Cognitive exercise sessions, baseline computation, longitudinal trends.
  - `SafetyRepository`: SOS alerts, severity events, resolutions, in-app notifications.

### B. Service Layer Pattern (`backend/app/services/`)
- Encapsulates domain logic, validation rules, business events, and transactions.
- Services:
  - `AuthService`: Token creation, password verification with 12 bcrypt rounds, session restoration.
  - `PatientService`: Permission enforcement (only linked caregivers or owners can access patient records).
  - `CareService`: Reminder scheduling, snooze calculations (+15 min), acknowledgment state transitions, missed medication escalation.
  - `CognitionService`: Deterministic mathematical scoring calculations:
    $$\text{Composite Score} = \min(100.0, \max(0.0, \text{Accuracy} \times 0.70 + \text{Speed Bonus} \times 0.30))$$
    $$\text{Speed Bonus} = \max(0.0, 100.0 - \frac{\text{Latency (ms)} - \text{Expected Time}}{50.0})$$
  - `AssistantService`: Retrieval-augmented context grounding combining medications, reminders, and daily state; regex-based safety guardrails preventing medical advice or dosage alteration.
  - `SafetyService`: Emergency SOS trigger, instant alert creation, caregiver notifications, resolution with required notes.
  - `ReportService`: Weekly statistical rollup and compassionate clinical summary synthesis.

### C. Strategy & Factory Pattern (`backend/app/ai/`)
- Abstract base class: `BaseAIProvider` with methods `generate_assistant_reply(context, message)` and `generate_weekly_report(metrics)`.
- Concrete implementations:
  - `MockAIProvider`: Zero-latency, deterministic, offline healthcare-safe simulation with empathetic responses and clinical disclaimers.
  - `OpenAIProvider`: Live GPT-4o-mini integration with system prompt guardrails.
- Factory: `get_ai_provider()` selects implementation based on `settings.USE_MOCK_AI` and `settings.OPENAI_API_KEY`.

---

## 2. Error Handling & Standardized Problem Details

All error responses strictly adhere to RFC 7807 Problem Details format:
```json
{
  "error": {
    "code": "PATIENT_FORBIDDEN",
    "message": "User does not have permission to access patient record.",
    "details": {}
  },
  "request_id": "req_839a2f10b74e"
}
```

- Handlers registered in `backend/app/main.py`:
  - `AppException` (400, 401, 403, 404, 409, 422)
  - `RequestValidationError` (422 with exact field path breakdowns)
  - `Exception` (500 internal server error with masked traceback and server log capture)

---

## 3. Concurrency & Concurrency Protection

- **Thread Pool Execution**: FastAPI runs SQLAlchemy synchronous I/O operations inside thread pools (`anyio`), ensuring the async event loop is never blocked.
- **Database Session Scoping**: Each HTTP request obtains an isolated SQLAlchemy `Session` from `get_db` and closes it via standard Python generator cleanup (`try ... finally db.close()`).
- **Idempotency**: Acknowledging a reminder that is already acknowledged is a safe, idempotent operation without state corruption.
