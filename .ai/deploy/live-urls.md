# CogniCare: Live & Cloud Deployment Endpoints

## 1. Public Live Cloud Deployment

| Component | Cloud Platform | Live Production URL | Status | Health / Verification |
|---|---|---|---|---|
| **Frontend Web App (PWA)** | **Vercel** | **https://cognicare-frontend-xi.vercel.app** | 🟢 **LIVE** | 200 OK • WCAG 2.2 AA Aligned |
| **Frontend Custom Domain** | **Vercel** | **https://cognicare-frontend-deepanshus-projects-13620ecc.vercel.app** | 🟢 **LIVE** | 200 OK • CDN Edge Cached |
| **GitHub Repository** | **GitHub** | **https://github.com/Deepanshu954/CogniCare** | 🟢 **LIVE** | Clean git history, zero secrets, CI ready |

---

## 2. Local Stack (Docker Compose Topology)

| Component | Target URL | Description | Health Check |
|---|---|---|---|
| **Frontend Web App** | http://localhost:3000 | Next.js 14 Responsive PWA (Elderly & Caregiver) | Browser loads 200 OK |
| **Backend REST API** | http://localhost:8000 | FastAPI REST Engine (Python 3.13) | `GET http://localhost:8000/health/live` -> 200 OK |
| **Database Readiness** | http://localhost:8000/health/ready | PostgreSQL 16 & Auto-Seeded Database | `GET http://localhost:8000/health/ready` -> 200 OK |
| **Interactive API Docs (Swagger)** | http://localhost:8000/docs | OpenAPI 3.1 Interactive Explorer & Schema | Interactive UI loads 200 OK |
| **Alternative API Docs (ReDoc)** | http://localhost:8000/redoc | ReDoc Clean Reference Guide | UI loads 200 OK |

---

## 3. Web Application Routes & Features

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

## 4. 1-Click Cloud Backend Blueprints

The repository includes ready-to-run blueprints to deploy the FastAPI backend and PostgreSQL database to free-tier cloud platforms:

- **Render Blueprint (`render.yaml`)**:
  - Automatically provisions `cognicare-backend` (Docker web service) and `cognicare-db` (PostgreSQL 16).
  - Configures CORS for `https://cognicare-frontend-xi.vercel.app`.
  - To deploy: Go to Render Dashboard -> New -> Blueprint -> Select `Deepanshu954/CogniCare`.

- **Railway Configuration (`railway.json`)**:
  - Ready for 1-click Docker build and healthcheck at `/health/live`.
  - Add PostgreSQL plugin in Railway dashboard for managed persistence.
