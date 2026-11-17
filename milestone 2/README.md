# CogniCare: Milestone 2 Deliverables Package
**Course:** CSET400C – Capstone Project | **Academic Session:** 2026–27 (Semester VII)  
**Institution:** Bennett University, School of Computer Science Engineering & Technology  
**Milestone:** Milestone 2 – Design, MVP/Prototype & Initial Validation (30 Marks)

---

## 👥 Project Team & Supervision

| Role | Name | Enrollment No. | Email |
| :--- | :--- | :--- | :--- |
| **Team Leader** | **Deepanshu Chauhan** | `E23CSEU1617` | deepanshu.chauhan@bennett.edu.in |
| **Team Member** | **Yash** | `E23CSEU1493` | yash@bennett.edu.in |
| **Team Member** | **Piyush** | `E23CSEU0853` | piyush@bennett.edu.in |
| **Project Guide** | **Amit Chauhan** | Faculty Mentor | amit.chauhan@bennett.edu.in |
| **Course Coordinator** | **Dr. Jabir Ali** | Associate Professor | jabir.ali@bennett.edu.in |

---

## 📂 Deliverables Index

1. **Milestone 2 Written Report**:
   - `Milestone_2_Report.md`: Full 14-section comprehensive technical report adhering to syllabus Section 8.1.
   - `Milestone_2_Report.docx`: Formatted Microsoft Word document following official Bennett University layout standards (Times New Roman, 12pt, 1.5 spacing, table borders, embedded figures).
2. **Milestone 2 Presentation**:
   - `CogniCare_Milestone_2_Presentation.pptx`: 13-slide high-definition widescreen slide deck for the 10-15 minute group evaluation.
3. **Architectural & Flow Figures** (`figures/`):
   - `figure1_system_architecture.png`: 4-Tier Decoupled System Architecture.
   - `figure2_cognitive_scoring_pipeline.png`: Cognitive Activity Scoring & Longitudinal Trend Pipeline.
   - `figure3_reminder_state_machine.png`: Reminder Lifecycle & Escalation State Machine.
   - `figure4_test_verification_matrix.png`: Automated Test Verification & Statement Coverage Breakdown.
4. **Working Software MVP**:
   - Backend: FastAPI (Python 3.13) under `backend/` with 11 API routers and 16 automated integration tests (88% statement coverage).
   - Frontend: Next.js 14 App Router under `frontend/` with 12 routes, accessible senior UI, drag-and-drop medical documents & prescription repository, 4 cognitive games, and 26 unit tests (100% pass).
   - Containerization: `docker-compose.yml` supporting multi-stage non-root container deployment.

---

## 🚀 How to Run & Verify the MVP

### Option 1: Docker Compose (Recommended)
```bash
# In the project root:
docker compose up -d

# Verify container health:
docker compose ps

# Access applications:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Swagger API Docs: http://localhost:8000/docs
```

### Option 2: Running Automated Tests
```bash
# Run Backend Integration Tests & Coverage:
cd backend
.venv/bin/pytest --cov=app --cov-report=term-missing backend/tests/

# Run Frontend Vitest Unit Tests:
cd ../frontend
npm test
```

