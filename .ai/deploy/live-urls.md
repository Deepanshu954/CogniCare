# CogniCare: Live & Local Deployment Endpoints

## 1. Local Deployment (Active Environment)

| Component | Target URL | Description | Health Check |
|---|---|---|---|
| **Frontend Web App** | http://localhost:3000 | Next.js 14 Responsive PWA (Elderly & Caregiver) | Browser loads 200 OK |
| **Backend REST API** | http://localhost:8000 | FastAPI REST Engine | `GET http://localhost:8000/health/live` |
| **Interactive API Docs (Swagger)** | http://localhost:8000/docs | OpenAPI 3.1 Interactive Explorer & Schema | Interactive UI loads 200 OK |
| **Alternative API Docs (ReDoc)** | http://localhost:8000/redoc | ReDoc Clean Reference Guide | UI loads 200 OK |

---

## 2. Key Web Application Routes

| Role / Context | Route | Feature |
|---|---|---|
| **Public / Auth** | `/login` | High-contrast login with 1-click Margaret / Sarah demo buttons |
| **Elderly Experience** | `/app/my-day` | Daily schedule, 1-tap confirmation, oversized interactive tiles |
| **Elderly Activities** | `/app/activities` | Cognitive game portal (Memory, Sequence, Stroop, Orientation) |
| **Elderly Assistant** | `/app/assistant` | Conversational companion with speech toggle & stop buttons |
| **Elderly Safety** | `/app/safety` | Emergency SOS trigger with 5-second cancel safeguard |
| **Caregiver Control** | `/caregiver/dashboard` | Multi-patient switcher, adherence ring, 30d Recharts, alerts |
| **Caregiver Reports** | `/caregiver/reports` | Weekly AI clinical report generator with print/PDF styling |

---

## 3. Cloud Deployment Blueprint

| Layer | Recommended Free Tier | Instructions | Expected Production URL |
|---|---|---|---|
| **Frontend (Next.js)** | **Vercel** | Import Git repository -> auto-detect Next.js -> set `NEXT_PUBLIC_API_URL` | `https://cognicare-app.vercel.app` |
| **Backend (FastAPI)** | **Railway / Render** | Connect Git repo -> deploy Dockerfile -> set environment variables | `https://cognicare-api.up.railway.app` |
| **Database (PostgreSQL)** | **Railway / Supabase** | Managed PostgreSQL 16 database | Connected via internal connection URI |
