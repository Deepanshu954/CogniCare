# CogniCare: High-Level Architecture (HLD)

## 1. System Vision & Purpose
CogniCare is an ambient, dual-interface cognitive health and routine care companion designed specifically for aging seniors experiencing mild cognitive impairment (MCI) or early-stage dementia, and their family/professional caregivers.

The system combines:
1. **Senior Ambient Interface**: Ultra-accessible, high-contrast, speech-enabled daily routine and cognitive stimulation station.
2. **Caregiver Control Tower**: Observability dashboard tracking longitudinal cognitive decline, medication adherence, real-time safety alerts, and AI-synthesized clinical reports.
3. **Deterministic Mathematical Scoring Engine**: Zero hallucinations for cognitive performance metrics — strict scoring formulas with baseline drift tracking.
4. **Safety & Policy Guardrails**: Medical policy enforcement strictly prohibiting autonomous clinical diagnoses or prescription alterations.

---

## 2. High-Level Architecture Diagram

```mermaid
graph TD
    subgraph Clients["Presentation Layer"]
        ElderlyUI["Senior Portal (Next.js 14)<br/>- 72px+ touch targets<br/>- Big Action Tiles<br/>- Speech STT/TTS<br/>- Emergency SOS Screen"]
        CaregiverUI["Caregiver Tower (Next.js 14)<br/>- Adherence Gauge<br/>- Cognitive Trend Curves<br/>- Alert Triage Feed<br/>- PDF/Print Reports"]
    end

    subgraph API_GW["API & Security Boundary"]
        ReverseProxy["Next.js Rewrite / CORS"]
        FastAPIGateway["FastAPI Gateway (Port 8000)<br/>- JWT Bearer Auth<br/>- RFC 7807 Exception Handlers<br/>- Security Headers Middleware<br/>- Sliding Window Rate Limiter"]
    end

    subgraph CoreServices["Backend Application Layer"]
        AuthSvc["AuthService<br/>(Argon2/BCrypt, JWT)"]
        PatientSvc["PatientService<br/>(Isolation, Consent, Contacts)"]
        CareSvc["CareService<br/>(Medications, Reminders, Escalations)"]
        CognitionSvc["CognitionService<br/>(Games Engine, Scoring, Baselines)"]
        AssistantSvc["AssistantService<br/>(Context Grounding, Guardrails)"]
        SafetySvc["SafetyService<br/>(SOS Trigger, Notifications, Triage)"]
        ReportSvc["ReportService<br/>(Metrics Aggregation, AI Narrative)"]
    end

    subgraph Persistence["Storage & External Layer"]
        PostgresDB[("PostgreSQL 16 / SQLite<br/>- Users, Patients, Caregivers<br/>- Medications, Reminders<br/>- Cognitive Sessions, Signals<br/>- Alerts, Audit Logs")]
        AIProvider["Pluggable AI Provider<br/>- MockAIProvider (Offline)<br/>- OpenAI GPT-4o-mini"]
    end

    ElderlyUI --> ReverseProxy
    CaregiverUI --> ReverseProxy
    ReverseProxy --> FastAPIGateway

    FastAPIGateway --> AuthSvc
    FastAPIGateway --> PatientSvc
    FastAPIGateway --> CareSvc
    FastAPIGateway --> CognitionSvc
    FastAPIGateway --> AssistantSvc
    FastAPIGateway --> SafetySvc
    FastAPIGateway --> ReportSvc

    AuthSvc --> PostgresDB
    PatientSvc --> PostgresDB
    CareSvc --> PostgresDB
    CognitionSvc --> PostgresDB
    AssistantSvc --> PostgresDB
    AssistantSvc --> AIProvider
    SafetySvc --> PostgresDB
    ReportSvc --> PostgresDB
    ReportSvc --> AIProvider
```

---

## 3. Entity-Relationship Data Model

```mermaid
erDiagram
    USER ||--o{ PATIENT_PROFILE : "owns / created"
    USER ||--o{ CAREGIVER_LINK : "has caregiver access"
    PATIENT_PROFILE ||--o{ CAREGIVER_LINK : "associated caregivers"
    PATIENT_PROFILE ||--o{ EMERGENCY_CONTACT : "has emergency contacts"
    PATIENT_PROFILE ||--o{ CAREGIVER_CONSENT : "grants data consent"
    PATIENT_PROFILE ||--o{ MEDICATION_PRESCRIPTION : "prescribed"
    PATIENT_PROFILE ||--o{ DAILY_ROUTINE : "has routines"
    PATIENT_PROFILE ||--o{ SCHEDULED_REMINDER : "receives reminders"
    PATIENT_PROFILE ||--o{ COGNITIVE_SESSION : "performs exercises"
    PATIENT_PROFILE ||--o{ COGNITIVE_BASELINE : "tracked baseline"
    PATIENT_PROFILE ||--o{ SUPPORT_SIGNAL : "generated signals"
    PATIENT_PROFILE ||--o{ CONVERSATION_SESSION : "holds AI chats"
    PATIENT_PROFILE ||--o{ ALERT_EVENT : "safety events"
    PATIENT_PROFILE ||--o{ CAREGIVER_REPORT : "weekly reports"

    USER {
        string id PK
        string email UK
        string password_hash
        string role
        boolean is_active
        datetime created_at
    }

    PATIENT_PROFILE {
        string id PK
        string user_id FK
        string display_name
        string care_level
        string notes
    }

    MEDICATION_PRESCRIPTION {
        string id PK
        string patient_id FK
        string medication_name
        string dosage
        string schedule_time
        boolean is_active
    }

    SCHEDULED_REMINDER {
        string id PK
        string patient_id FK
        string title
        datetime scheduled_for
        string status
        datetime acknowledged_at
    }

    COGNITIVE_SESSION {
        string id PK
        string patient_id FK
        string activity_type
        float composite_score
        float accuracy_percentage
        int average_latency_ms
    }

    ALERT_EVENT {
        string id PK
        string patient_id FK
        string alert_type
        string severity
        string status
        string summary
    }
```

---

## 4. Deployment Topology

Containerized multi-service Docker Compose topology with custom isolated bridge network `cognicare-net`:
1. `cognicare-db`: PostgreSQL 16 Alpine container with health probe.
2. `cognicare-backend`: Multi-stage Python 3.13 image running Uvicorn ASGI server with non-root security.
3. `cognicare-frontend`: Multi-stage Next.js 14 standalone Node.js server.
