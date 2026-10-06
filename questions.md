# Project Questions & Selected Defaults

All defaults have been selected in alignment with [`plan.md`](file:///Users/deepanshu954/GitHub/Capstone/plan.md) and the user's preference to proceed autonomously.

### 1. Project Name & Branding
- **Question**: What should the project name and branding be?
- **Selected Default**: **CogniCare** (AI-Powered Cognitive Health & Care Assistant).

### 2. Backend Stack
- **Question**: Python FastAPI vs Java Spring Boot?
- **Selected Default**: **Python 3.13 + FastAPI + SQLAlchemy 2.x + Alembic + Pydantic v2 + PostgreSQL + Redis**, as explicitly specified in [`plan.md`](file:///Users/deepanshu954/GitHub/Capstone/plan.md) Section 0 ("Final primary stack") and Section 141 ("FastAPI chosen because the project has strong Python AI/ML requirements").

### 3. Frontend Stack
- **Question**: Frontend framework and UI system?
- **Selected Default**: **Next.js 14+ (App Router) + TypeScript + Tailwind CSS + Lucide Icons + TanStack Query + Zod + Vitest**, supporting dual experience (Elderly accessible UI + Caregiver Dashboard) and PWA manifest.

### 4. Database & Storage
- **Question**: Database engine and vector storage?
- **Selected Default**: **PostgreSQL 16** with schema migrations via Alembic. Vector search using pgvector / semantic embeddings fallback.

### 5. AI Services & Provider
- **Question**: LLM and speech provider?
- **Selected Default**: Provider abstraction (`LLMProvider`, `SpeechToTextProvider`, `TextToSpeechProvider`) with a pluggable OpenAI adapter and mock/local deterministic fallback adapter for testing and offline development without requiring an active paid API key.

### 6. Authentication Mechanism
- **Question**: Session vs JWT?
- **Selected Default**: Secure HTTP-only cookies + short-lived Bearer tokens, Argon2id/bcrypt password hashing, multi-role RBAC (`ELDERLY`, `CAREGIVER`, `REVIEWER`, `ADMIN`).

### 7. Seed Data
- **Question**: Realistic demo accounts and cognitive exercises?
- **Selected Default**: Built-in comprehensive seed data with 2 elderly users, 2 caregivers, 4+ cognitive games (Memory Recall, Word Sequence, Attention Stroop, Spatial Orientation), medication schedules, daily routines, alerts, and historical trends.
