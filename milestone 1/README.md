# Milestone 1 Deliverables Package
**Course:** CSET400C Capstone Project (Academic Session 2026–27)  
**Institution:** Bennett University, Greater Noida  
**Project:** CogniCare — Ambient Elderly Cognitive & Routine Care Companion  

---

## 👥 Student & Faculty Metadata

- **Team Leader:** Deepanshu Chauhan (`E23CSEU1617`) — System Architecture, AI Orchestration & Backend Infrastructure
- **Team Member 1:** Yash (`E23CSEU1493`) — Frontend Architecture, Accessibility Engineering & Cognitive Games
- **Team Member 2:** Piyush (`E23CSEU0853`) — Relational Schemas, Deterministic State Machines & Quality Verification
- **Course Coordinator:** Dr. Jabir Ali
- **Project Guide / Faculty Mentor:** Amit Chauhan

---

## 📁 Artifacts Inventory

| File | Format | Description | Page / Slide Count |
| :--- | :--- | :--- | :--- |
| **`report_content_blocks.txt`** | Plain Text (.txt) | 23 calibrated text blocks (strictly 160–180 words each) ready for humanized user edits | 23 Verified Blocks |
| **`Milestone_1_Report.docx`** | Microsoft Word (.docx) | Primary academic report with official Bennett University logo, complete IEEE references, formatted tables, and humanized text | **Exactly 11 Pages** (Conforms to 10–12 page specification) |
| **`Milestone_1_Report.md`** | Markdown (.md) | GitHub-readable Markdown version of the report matching the exact 11-page structure | 11 Chapters / Sections |
| **`CogniCare_Milestone_1_Presentation.pptx`** | PowerPoint (.pptx) | Official 10-slide oral evaluation deck adhering to Bennett University white/academic theme with zero crowding and speaker scripts | **10 Slides** (16:9 Widescreen) |
| **`presentation_slides.md`** | Markdown (.md) | Markdown companion containing full slide visual layout specifications and verbal scripts | 10 Slides |
| **`bennett_university_logo.png`** | PNG (876×1024) | High-resolution official Bennett University seal with transparent alpha background | Institutional Asset |

---

## 🚀 Live Docker Stack Verification

The application is fully containerized and currently running via Docker Compose:

```bash
docker compose ps
```
- **Frontend Container (`cognicare-frontend`):** Up & Healthy at `http://localhost:3000`
- **Backend Container (`cognicare-backend`):** Up & Healthy at `http://localhost:8000` (`http://localhost:8000/docs`)
- **Database Container (`cognicare-db`):** Up & Healthy on port 5432 (PostgreSQL 16)
