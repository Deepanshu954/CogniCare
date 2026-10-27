# CogniCare: Live & Cloud Deployment Endpoints

## 1. Public Cloud Deployment (Production Ready)

| Component | Platform | Live Production URL | Status | Health / Verification |
|---|---|---|---|---|
| **Frontend Web App (PWA)** | **Vercel** | **[https://cognicare-frontend-xi.vercel.app](https://cognicare-frontend-xi.vercel.app)** | 🟢 **LIVE** | 200 OK • WCAG 2.2 AA Aligned |
| **Backend REST API** | **Vercel** | **[https://cognicare-backend-three.vercel.app](https://cognicare-backend-three.vercel.app)** | 🟢 **LIVE** | `GET /health/live` -> 200 OK |
| **Interactive API Docs (Swagger)** | **Vercel** | **[https://cognicare-backend-three.vercel.app/docs](https://cognicare-backend-three.vercel.app/docs)** | 🟢 **LIVE** | OpenAPI 3.1 Interactive Explorer |
| **Alternative Docs (ReDoc)** | **Vercel** | **[https://cognicare-backend-three.vercel.app/redoc](https://cognicare-backend-three.vercel.app/redoc)** | 🟢 **LIVE** | ReDoc Reference Guide |
| **GitHub Repository** | **GitHub** | **[https://github.com/Deepanshu954/CogniCare](https://github.com/Deepanshu954/CogniCare)** | 🟢 **LIVE** | Fully pushed, clean history, CI ready |

---

## 2. Web Application Routes & Key Features

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

## 3. Demo Credentials (For Testing Both Roles)

| Role | Name | Email | Password | Pre-loaded Data |
|---|---|---|---|---|
| **Senior User** | Margaret Vance | `margaret@example.com` | `Password123!` | 4 activities, 3 daily meds, hydration routines |
| **Caregiver** | Sarah Vance | `sarah@example.com` | `Password123!` | 30-day compliance, multi-patient switcher, weekly report |

*(You can also click the **1-Click Demo Buttons** on the `/login` page to sign in instantly without typing).*

---

## 4. Local Multi-Container Stack (Docker Compose)

| Component | Target URL | Description | Health Status |
|---|---|---|---|
| **Frontend Web App** | http://localhost:3000 | Next.js 14 Responsive PWA (Elderly & Caregiver) | 🟢 200 OK |
| **Backend REST API** | http://localhost:8000 | FastAPI REST Engine (Python 3.13) | 🟢 `GET /health/live` (200 OK) |
| **PostgreSQL 16 Engine** | http://localhost:8000/health/ready | Auto-migrated & pre-seeded with demo records | 🟢 `GET /health/ready` (200 OK) |
