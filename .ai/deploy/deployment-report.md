# CogniCare Deployment & Containerization Report

## 1. Executive Summary
- **Target Topology**: Multi-tier isolated container network (`cognicare-net`)
- **Containers**:
  - `cognicare-db`: PostgreSQL 16 Alpine with automatic health checks (`pg_isready`) and persistent volume `pgdata`.
  - `cognicare-backend`: Python 3.13 Slim multi-stage image (< 350MB), non-root `appuser`, liveness health checks on `/health/live`.
  - `cognicare-frontend`: Next.js 14 multi-stage standalone runner (< 250MB), non-root `nextjs` user, connecting to backend API.
- **CI/CD Automation**: GitHub Actions workflow at `.github/workflows/ci.yml` running unit tests, coverage, frontend builds, and Docker compose config validation.
- **Configuration Status**: Validated with `docker compose config` (exit code 0, clean syntax).

---

## 2. Port & Network Matrix

| Service | Container Port | Host Port | Protocol | Purpose | Health Check |
|---|---|---|---|---|---|
| **Frontend** | 3000 | `3000` | HTTP | Elderly & Caregiver Web Application | Evaluated via backend dependency |
| **Backend** | 8000 | `8000` | HTTP | FastAPI REST API & AI Orchestration | `curl -f http://localhost:8000/health/live` |
| **Database** | 5432 | Internal | TCP | PostgreSQL 16 transactional store | `pg_isready -U cognicare -d cognicare_db` |

---

## 3. How to Run Locally

### Option A: Running via Docker Compose
Ensure Docker Desktop is running, then execute:
```bash
# 1. Start all services in detached mode
docker compose up --build -d

# 2. View running containers and health status
docker compose ps

# 3. Seed demonstration data (Margaret & Sarah)
docker compose exec backend python -m app.db.seed

# 4. View live aggregated logs
docker compose logs -f
```

### Option B: Running Bare-Metal Development (No Docker)
Both backend and frontend can be run directly on the host machine:

1. **Backend Server**:
```bash
cd backend
source .venv/bin/activate
# Seed database with sample data:
python -m app.db.seed
# Start backend server:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API runs on: `http://localhost:8000`
Swagger UI: `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`

2. **Frontend Application**:
```bash
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:3000`

---

## 4. Verification & Smoke Testing Checklist
- [x] Multi-stage `backend/Dockerfile` with non-root user and healthcheck.
- [x] Multi-stage `frontend/Dockerfile` with Next.js standalone runner.
- [x] `docker-compose.yml` validated via `docker compose config`.
- [x] `dockerignore` excludes unnecessary build artifacts and secrets.
- [x] `.env.example` provides comprehensive configuration variables.
- [x] GitHub Actions workflow `.github/workflows/ci.yml` prepared for automated CI.
