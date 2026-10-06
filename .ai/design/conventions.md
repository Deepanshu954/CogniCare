# CogniCare: Coding Conventions & Standards (The Golden File)

This document is the absolute authoritative source of conventions for all backend and frontend code across the repository.

---

## 1. Backend Conventions (Python 3.13 + FastAPI)

### 1.1 Architecture & Layering
Strict unidirectional dependency flow:
```text
Router (api/v1/) -> Service Layer (services/) -> Repository Layer (repositories/) -> Database Models (models/)
```
- **Routers**: Thin controllers. Responsible ONLY for HTTP concerns, parsing query/path parameters, validating request bodies via Pydantic schemas, and returning responses with appropriate status codes.
- **Services**: All business logic, transaction coordination, AI model invocation, and validation.
- **Repositories**: Direct SQLAlchemy queries and database persistence.
- **Models**: Pure SQLAlchemy declarative models with explicit column types, constraints, and relationships.
- **Schemas**: Pure Pydantic v2 schemas for request validation and response serialization.

### 1.2 Naming Standards
- Modules & Files: `snake_case.py` (e.g. `patient_service.py`, `cognitive_models.py`)
- Classes: `PascalCase` (e.g. `PatientService`, `ReminderRepository`, `UserResponse`)
- Functions & Methods: `snake_case` (e.g. `calculate_baseline_score()`, `get_today_reminders()`)
- Constants: `UPPER_SNAKE_CASE` (e.g. `DEFAULT_TOKEN_EXPIRE_MINUTES = 60`)
- Database Tables & Columns: `snake_case` (e.g. `activity_sessions`, `response_time_ms`)

### 1.3 Error Format & Handling
All exceptions must inherit from a custom `AppException` and return the standard JSON error structure:
```json
{
  "error": {
    "code": "ENTITY_NOT_FOUND",
    "message": "The requested patient profile was not found.",
    "details": {}
  },
  "request_id": "req_123456"
}
```

### 1.4 Imports Ordering
1. Python standard library (`sys`, `os`, `uuid`, `datetime`, `typing`)
2. Third-party packages (`fastapi`, `pydantic`, `sqlalchemy`, `jose`)
3. Local application imports with absolute paths (`app.core.*`, `app.models.*`, `app.schemas.*`, `app.services.*`)

---

## 2. Frontend Conventions (Next.js 14+ & TypeScript)

### 2.1 Directory Structure & Organization
```text
src/
├── app/                  # Next.js App Router (page.tsx, layout.tsx, loading.tsx, error.tsx)
├── components/
│   ├── ui/               # Reusable atom primitives (Button, Card, Input, Modal)
│   ├── elderly/          # Elderly accessible widgets (BigActionButton, VoiceButton, SosButton)
│   ├── caregiver/        # Caregiver dashboard components (TrendChart, AlertBanner, MetricCard)
│   └── shared/           # Navigation bars, Shell layouts, Theme toggle
├── hooks/                # Custom React & TanStack Query hooks
├── lib/                  # Axios API client, auth token management, date utilities
├── types/                # Domain TypeScript interfaces
```

### 2.2 Naming Standards
- Component Files: `PascalCase.tsx` (e.g. `BigActionButton.tsx`, `TrendChart.tsx`)
- Hooks: `camelCase.ts` starting with `use` (e.g. `usePatientSummary.ts`, `useAuth.ts`)
- Utility & Library Files: `camelCase.ts` (e.g. `apiClient.ts`, `formatDate.ts`)
- TypeScript Types & Interfaces: `PascalCase` (e.g. `PatientSummary`, `ReminderItem`)

### 2.3 Component Patterns
- Server Components by default; mark with `'use client'` only when using hooks, browser state, or interactivity.
- Accessible HTML semantics: explicit `<button>`, `<dialog>`, `aria-label`, `role="alert"`.
- Loading & Error States: Every data-fetching screen must render clean skeleton placeholders during load and explicit error states with a retry button.

### 2.4 State & Data Fetching
- Server state handled exclusively with TanStack Query (`useQuery`, `useMutation`).
- Client session stored via secure HTTP cookies and managed in React Auth Context.
- Form validation implemented using Zod schemas with React Hook Form.

---

## 3. Testing Conventions
- Backend: Pytest test files named `test_<module>.py` in `backend/tests/`. Must test happy paths, validation errors (400), not found (404), and permission violations (403).
- Frontend: Vitest test files named `<Component>.test.tsx` in `frontend/src/__tests__/`. Must verify rendering, user interaction, and accessible labels.
