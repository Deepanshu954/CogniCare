# CogniCare: Technical Viva-Voce Defense Guide & Evaluation Q&A Bank
**Course:** CSET400C – Capstone Project | **Academic Session:** 2026–27  
**Bennett University, School of Computer Science Engineering & Technology**

---

## 🎯 Evaluation Rubric Mapping

This defense guide maps directly to the **Final Evaluation Criteria (Table 7 & Table 8)** in the Bennett University CSET400C Capstone Framework:
- **Criterion 1 (Project Understanding & Objectives - 4 Marks)**
- **Criterion 2 (Technical Contribution - 3 Marks)**
- **Criterion 5 (Project Completion & Ownership - 3 Marks)**
- **Criterion 6 (Presentation & Communication - 5 Marks)**
- **Criterion 7 (Demonstration / Implementation - 5 Marks)**
- **Criterion 8 (Results, Testing & Validation - 5 Marks)**
- **Criterion 9 (Problem Solving & Technical Reasoning - 5 Marks)**
- **Criterion 10 (Technical Viva-Voce - 5 Marks)**
- **Criterion 11 (Innovation / Research Achievement - 5 Marks)**

---

## Part 1: Core Architecture & System Understanding

### Q1: What is the core problem CogniCare solves, and why can't existing apps (like Medisafe or Lumosity) solve it?
**Model Defense Answer:**
Existing solutions fall into two isolated extremes:
1. *Medication Reminder Apps* (Medisafe, CareZone) focus solely on scheduled alarms. Their interfaces are cluttered with small buttons and multi-step drop-downs that overwhelm older adults experiencing early cognitive decline. Crucially, they lack any cognitive activity tracking, voice interaction, or caregiver escalation state machines.
2. *Brain Training Games* (Lumosity, Elevate) are commercialized gamification platforms with zero connection to routine healthcare, prescriptions, or informal family caregivers.

**CogniCare’s core innovation is strict architectural integration**: it pairs an ultra-accessible, prospective memory routine companion (WCAG AAA contrast, 72px+ touch targets, 1-tap adherence) with standardized neuropsychological activity tracking (Memory, Working Sequence, Stroop, Clock Orientation) and an analytical Caregiver Command Tower.

### Q2: Why did you separate the deterministic core from the generative AI assistant?
**Model Defense Answer:**
In healthcare software, predictability, auditability, and safety are paramount:
- *Large Language Models (LLMs)* are probabilistic and stochastic. If an LLM directly governed medication schedules, hallucination risks could result in missed doses, corrupted records, or catastrophic diagnostic advice.
- Therefore, CogniCare enforces a **Generative Firewall Rule**:
  - The deterministic core (FastAPI, PostgreSQL 16) is the absolute **System of Record**. It calculates medication adherence, executes the reminder state machine, computes mathematical cognitive scores, and triggers critical alerts.
  - The generative AI assistant (Google Gemini 1.5/2.0) acts strictly as a **read-only conversational adapter**. It can answer questions (*"What pills do I take tonight?"*) by calling the grounded tool `get_today_tasks`, but it is architecturally prevented from inserting, updating, or deleting any healthcare record.

### Q3: What happens if an older adult asks the AI assistant: "Do I have Alzheimer's?" or "Should I take 20mg instead of 10mg?"
**Model Defense Answer:**
The prompt is immediately intercepted by the **Medical Guardrail Service** (`backend/app/ai/gemini_provider.py`). The regex-based safety filter detects diagnostic keywords (*"diagnose"*, *"Alzheimer's"*, *"dosage"*, *"prescribe"*). 
Instead of sending the query to the language model, the system immediately returns a standardized, empathetic safety refusal:
> *"I cannot give medical advice, diagnostic evaluations, or alter your prescriptions. Please consult Dr. Elena Vance or your family caregiver."*
This behavior is 100% verified in automated integration tests (`backend/tests/test_assistant.py`).

---

## Part 2: State Machines, Algorithms & Scoring Logic

### Q4: Explain the mathematical formula used to score cognitive activities. Why not just measure accuracy?
**Model Defense Answer:**
Measuring accuracy alone in cognitive assessment is insufficient because an individual with progressive Mild Cognitive Impairment may maintain high accuracy by taking ten times longer to complete a simple task (compensatory processing).
CogniCare implements a **4-Factor Multi-Dimensional Scoring Formula**:
$$S_{\text{session}} = S_{\text{acc}} + S_{\text{lat}} + S_{\text{comp}} + S_{\text{diff}} \quad (S_{\text{session}} \in [0, 100])$$
1. **Accuracy ($S_{\text{acc}}$, 40% weight)**: $(C_{\text{correct}} / C_{\text{total}}) \times 40$.
2. **Latency Efficiency ($S_{\text{lat}}$, 30% weight)**: $\max(0, 1 - (\bar{T}_{\text{resp}} - T_{\text{target}}) / (T_{\text{max}} - T_{\text{target}})) \times 30$. Rewards responses closer to target reaction speed.
3. **Completion Rate ($S_{\text{comp}}$, 20% weight)**: $(N_{\text{answered}} / N_{\text{expected}}) \times 20$. Penalizes early abandonment.
4. **Difficulty Weight ($S_{\text{diff}}$, 10% weight)**: $(\text{Level} / 3) \times 10$. Accounts for trial complexity.

This formula is completely deterministic, transparent, and reproducible across test harnesses.

### Q5: How does the system detect cognitive decline over time without inducing patient alarm?
**Model Defense Answer:**
The system maintains **rolling 7-day and 30-day baseline distributions** ($\mu_{\text{baseline}}$ and $\sigma$). 
When a senior completes a session, the score is compared against their personal baseline. 
If the moving average of the last three sessions falls below $\mu - 1.5\sigma$, the system automatically emits a `SUPPORT_SIGNAL` (`DECLINING_EFFICIENCY`) directly to the **Caregiver Command Tower**. 
Crucially, the senior is *not* greeted with an alarming failure message—their UI remains celebratory and supportive—while the caregiver receives empirical data to share with the attending physician.

### Q6: Walk us through the Reminder Lifecycle State Machine. How are missed doses handled?
**Model Defense Answer:**
1. At midnight, the scheduler instantiates reminders in the `SCHEDULED` state.
2. The senior can transition the reminder to `ACKNOWLEDGED` by tapping the massive *"I did this!"* button, or request a 15-minute delay by tapping `SNOOZED`.
3. If the senior or caregiver explicitly marks `SKIPPED`, a mandatory justification note is recorded.
4. **Escalation**: If a high-criticality medication reminder remains in `SCHEDULED` or `SNOOZED` 60 minutes after the scheduled time, the state machine automatically transitions it to `MISSED`. This immediately generates a `CRITICAL` alert row in the `alerts` table and pushes notifications to linked caregivers.

---

## Part 3: Engineering, Security & Testing Rigor

### Q7: How did you verify the quality and reliability of your software?
**Model Defense Answer:**
Our testing and verification strategy spans multiple dimensions:
1. **Backend Integration Suite (Pytest)**: 16 automated integration tests verifying authentication, tenant isolation, reminder lifecycles, cognitive scoring, safety alerts, report generation, and medical document uploads. We achieved **88% overall statement coverage** (surpassing the 70% threshold).
2. **Frontend Unit Suite (Vitest)**: 12 test files with 26 individual test cases verifying accessible components (`TodayCard`, `SosButton`, `TrendChart`, `AdherenceGauge`, `Navbar`, `uiScaleContext`, `MedicalDocuments`). 100% pass rate.
3. **Flakiness Verification**: We ran both suites across **three consecutive iterations** with zero failures, proving complete test determinism.
4. **Build & Lint Verification**: Next.js 14 production build compiled all 12 routes with zero TypeScript or ESLint errors.

### Q8: How is Multi-Tenant Data Isolation enforced in the database?
**Model Defense Answer:**
We enforce tenant isolation at the service and repository layers through FastAPI dependency injection:
- Every protected endpoint requires the `get_current_user` dependency.
- In `PatientService`, `CareService`, and `DocumentService`, every query explicitly filters by the authenticated user ID or checks for an active row in `caregiver_links`.
- If an authenticated user attempts to access or mutate a patient record that they do not own and have no consented caregiver link for, the service immediately raises an `HTTP 403 Forbidden` exception. This is verified in `test_patients.py:test_caregiver_patient_lifecycle_and_isolation` and `test_documents.py:test_document_access_control_forbidden`.

### Q9: How does the Medical Document & Prescription Upload system work, and how are files stored?
**Model Defense Answer:**
The document management subsystem addresses a critical clinical need—preserving and sharing prescriptions, condition summaries, and diagnostic scans between doctors, caregivers, and seniors:
- **Interactive UI**: Supports drag-and-drop file targets with visual drag feedback and file pickers restricted to `.pdf,image/*` under a 15 MB threshold.
- **Categorization**: Classifies assets into `PRESCRIPTION`, `MEDICAL_CONDITION`, `LAB_REPORT`, `CLINICAL_NOTE`, `EMERGENCY_PLAN`, and `OTHER`.
- **Hybrid Storage Architecture**: Ingested files are stored on disk under `uploads/documents/{uuid}_{filename}` with access controlled via FastAPI streaming endpoints (`GET /api/v1/patients/{id}/documents/{doc_id}/file`). Simultaneously, a base64 data URL is retained in SQLite/PostgreSQL to enable instantaneous zero-latency client previews in both desktop and mobile viewports.
- **Audit Logging**: Every document creation or deletion generates an immutable row in the `audit_logs` table for clinical compliance.

### Q10: How is the application deployed, and what are its resource constraints?
**Model Defense Answer:**
The application is deployed using a production-ready **Docker Compose** topology:
- `cognicare-db`: `postgres:16-alpine`, persistent volume `pgdata`, internal healthcheck `pg_isready`.
- `cognicare-backend`: Multi-stage Python 3.13 image, non-root `appuser`, automated startup seeding, uncompressed size **456 MB** (well under the 500 MB budget).
- `cognicare-frontend`: Multi-stage Next.js 14 standalone image, non-root `nextjs` user, uncompressed size **234 MB** (well under the 300 MB budget).
- Both containers run with health probes (`/health/live` and `http://localhost:3000/`) and communicate over an isolated bridge network `cognicare-net`.

---

## Part 4: Individual Contributions (Defense by Member)

### Deepanshu Chauhan (Team Leader & Systems Architect - E23CSEU1617)
- **Primary Ownership**: System architecture design, FastAPI REST backend services, RBAC security dependencies, Google Gemini Live provider adapter with safety filters, Docker Compose topology, and documentation synthesis.
- **Key Technical Defense Defense**: Responsible for enforcing the Generative Firewall Rule, ensuring that all AI interactions pass through read-only tools and Pydantic schemas without write access to clinical tables.

### Yash (Frontend & Accessibility Engineer - E23CSEU1493)
- **Primary Ownership**: Next.js 14 App Router frontend architecture, accessible design system (72px+ touch targets, WCAG AAA contrast, dynamic font scaling), 4 interactive cognitive games (`ActivityPlayer.tsx`), and Vitest unit testing.
- **Key Technical Defense Defense**: Implemented the client-side state machine in `ActivityPlayer.tsx` capturing microsecond timestamp intervals between visual stimulus presentation and senior touch input.

### Piyush (Database & Core Logic Engineer - E23CSEU0853)
- **Primary Ownership**: PostgreSQL relational database schema (14 tables), SQLAlchemy 2.0 ORM mappings, reminder state machine with alert escalation, mathematical 4-factor scoring algorithm, and synthetic seeder engine.
- **Key Technical Defense Defense**: Engineered the rolling baseline variance analyzer calculating $\mu \pm 1.5\sigma$ z-scores to trigger automated caregiver support signals.

