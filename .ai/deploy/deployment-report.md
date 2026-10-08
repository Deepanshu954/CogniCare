# CogniCare Deployment & Containerization Report

## 1. Executive Summary
- **Target Topology**: Multi-tier isolated container network (`cognicare-net`)
- **Containers & Built Images**:
  - `cognicare-db`: PostgreSQL 16 Alpine (`postgres:16-alpine`), internal health check (`pg_isready`), persistent volume `pgdata`.
  - `cognicare-backend`: Multi-stage Python 3.13 image (`capstone-backend`), non-root `appuser`, automated PostgreSQL URL normalization, startup auto-seed bootstrap, and liveness health check (`/health/live`). Image size: **100MB compressed / 456MB uncompressed**.
  - `cognicare-frontend`: Multi-stage Next.js 14 standalone image (`capstone-frontend`), non-root `nextjs` user, embedded curl health check (`http://localhost:3000/`). Image size: **56MB compressed / 234MB uncompressed** (well under 300MB target).
- **CI/CD Automation**: GitHub Actions workflow at `.github/workflows/ci.yml` running backend pytest coverage, frontend ESLint + Vitest, Next.js build, and Docker compose config validation.
- **Docker Compose Status**: 100% healthy across all 3 containers (`cognicare-db`, `cognicare-backend`, `cognicare-frontend`).

---

## 2. Container Topology Matrix

| Container Name | Service | Image | Host Port | Status | Health Check |
|---|---|---|---|---|---|
| `cognicare-db` | `db` | `postgres:16-alpine` | `5432` (Internal) | **Healthy** | `pg_isready -U cognicare -d cognicare_db` |
| `cognicare-backend` | `backend` | `capstone-backend:latest` | `8000:8000` | **Healthy** | `curl -f http://localhost:8000/health/live` |
| `cognicare-frontend` | `frontend` | `capstone-frontend:latest` | `3000:3000` | **Healthy** | `curl -f http://localhost:3000/` |

---

## 3. How to Run Locally

### Option A: Running via Docker Compose (Recommended)
```bash
# 1. Start all services in detached mode
docker compose up -d

# 2. View running containers and health status
docker compose ps

# 3. View live aggregated logs
docker compose logs -f

# 4. Stop all services
docker compose down
```

### Option B: Running Bare-Metal Development (No Docker)
1. **Backend Server**:
```bash
cd backend
source .venv/bin/activate
python -m app.db.seed
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API runs on: `http://localhost:8000` | Swagger UI: `http://localhost:8000/docs`

2. **Frontend Application**:
```bash
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:3000`

---

## 4. Verification & Smoke Testing Checklist
- [x] Multi-stage `backend/Dockerfile` with non-root user, PostgreSQL driver normalization, and health check.
- [x] Multi-stage `frontend/Dockerfile` with Next.js standalone runner, non-root user, and health check.
- [x] `docker-compose.yml` validated via `docker compose config` (exit 0).
- [x] Automatic database schema bootstrap and demo seed (Margaret & Sarah) upon first boot.
- [x] Smoke test verified: Backend liveness (HTTP 200), Database readiness (HTTP 200), Frontend rendering (HTTP 200), Margaret senior login, Sarah caregiver login, activities catalog (4 games).
- [x] Both images successfully built, tagged, and tested locally.
