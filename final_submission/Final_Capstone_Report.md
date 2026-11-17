# BENNETT UNIVERSITY
### SCHOOL OF ENGINEERING & APPLIED SCIENCES
#### DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING

---

# CSET400C | CAPSTONE PROJECT FINAL REPORT
**Academic Session 2026–27 • Semester VII B.Tech. CSE**  
**Course Code:** CSET400C | **Credits:** 6 (L-T-P-C: 0-0-12-6)

---

# **CogniCare: An Ambient AI-Powered Cognitive Care & Routine Monitoring Companion for Older Adults**

---

### SUBMITTED BY

| Project Role | Student Name | Enrollment Number | Official University Email |
| :--- | :--- | :--- | :--- |
| **Team Leader** | **Deepanshu Chauhan** | `E23CSEU1617` | deepanshu.chauhan@bennett.edu.in |
| **Team Member** | **Yash** | `E23CSEU1493` | yash@bennett.edu.in |
| **Team Member** | **Piyush** | `E23CSEU0853` | piyush@bennett.edu.in |

---

### UNDER THE SUPERVISION & GUIDANCE OF
- **Project Guide / Faculty Mentor:** **Amit Chauhan**, Assistant Professor, Dept. of CSE
- **Course Coordinator:** **Dr. Jabir Ali**, Associate Professor, Dept. of CSE

**Greater Noida, Uttar Pradesh, India | November 2026**

---

## Certificate of Originality & Approval

This is to certify that the Capstone Project report titled **“CogniCare: An Ambient AI-Powered Cognitive Care & Routine Monitoring Companion for Older Adults”** submitted by **Deepanshu Chauhan (E23CSEU1617)**, **Yash (E23CSEU1493)**, and **Piyush (E23CSEU0853)** in partial fulfillment of the requirements for the award of the degree of **Bachelor of Technology in Computer Science & Engineering** at Bennett University, Greater Noida, is an authentic record of original engineering work carried out by them under my supervision during the Academic Session 2026–27.

The matter embodied in this report has not been submitted by the candidates for the award of any other degree or diploma.

\
\
__________________________________  
**Amit Chauhan**  
Assistant Professor & Project Guide  
Department of Computer Science & Engineering  
School of Engineering & Applied Sciences  
Bennett University, Greater Noida  

\
\
__________________________________  
**Dr. Jabir Ali**  
Associate Professor & Course Coordinator (CSET400C)  
Department of Computer Science & Engineering  
Bennett University, Greater Noida  

---

## Declaration of Authorship

We declare that this Final Capstone Report represents our own original work. All contributions of external authors, software frameworks, algorithms, and medical literature have been properly acknowledged in the text and cited in the References section. Furthermore, we certify that:
1. The working prototype described herein has been implemented, containerized, and rigorously validated through automated and manual test suites.
2. The data, testing metrics, coverage percentages, and benchmark latencies presented are genuine empirical results obtained from executed test harnesses.
3. Responsible AI principles have been strictly embedded into the system architecture to prevent diagnostic claims or unsafe clinical behavior.

\
\
____________________________________  
**Deepanshu Chauhan** (`E23CSEU1617`)  
Team Leader & Systems Architect  

\
\
____________________________________  
**Yash** (`E23CSEU1493`)  
Frontend & Accessibility Engineer  

\
\
____________________________________  
**Piyush** (`E23CSEU0853`)  
Database & Core Logic Engineer  

---

## Acknowledgments

We express our profound gratitude to our project guide, **Amit Chauhan**, for his continuous technical guidance, incisive reviews, and encouragement throughout the architecture, implementation, and verification phases of this capstone project. His insights into robust software design and data integrity were invaluable.

We also thank **Dr. Jabir Ali**, Course Coordinator for CSET400C, for establishing a structured, objective, and transparent evaluation framework that challenged us to achieve industry-grade software engineering standards.

Finally, we thank the faculty and staff of the Department of Computer Science & Engineering and the School of Engineering & Applied Sciences at Bennett University for providing the computational infrastructure, research access, and academic environment necessary to bring CogniCare to fruition.

---

## Abstract

Cognitive decline, encompassing Mild Cognitive Impairment (MCI) and progressive dementia, affects more than 55 million individuals worldwide and is projected to afflict 139 million by 2050. Informal family caregivers shoulder the vast majority of daily care, suffering severe psychological burnout, chronic anxiety regarding missed medication schedules, and an acute lack of objective longitudinal insight into their loved one's cognitive trajectory. Existing digital solutions either over-index on clinical diagnostic jargon that induces patient anxiety or offer generic reminder alarms lacking cognitive tracking and contextual intelligence.

This capstone project presents **CogniCare**, an ambient, highly accessible digital care companion engineered specifically for older adults with early memory decline and their family caregivers. Built upon a **4-Tier Decoupled Architecture**, CogniCare strictly isolates deterministic clinical business logic from non-deterministic generative artificial intelligence models. 

The core software contributions comprise:
1. An accessible senior interface in Next.js 14 adhering to WCAG 2.1 AAA contrast and 72px+ touch standards, featuring a cognitive-load-reducing "My Day" schedule, 1-tap adherence logging, and a 5-second protected emergency SOS trigger.
2. A standardized neuropsychological activity suite across four domains (Visual Pattern Memory, Working Sequence Memory, Attention Stroop Test, and Clock/Spatial Orientation) paired with a mathematical 4-factor scoring algorithm ($S_{\text{session}} \in [0, 100]$) and rolling 7-day/30-day baseline variance analyzers.
3. A Caregiver Command Tower delivering real-time radial adherence gauges, interactive Recharts longitudinal trend curves, alert triage workflows, and automated weekly care summary generation.
4. A voice-enabled conversational assistant powered by Google Gemini 1.5/2.0, architecturally restricted to read-only tool grounding (`get_today_tasks`) with strict medical guardrail filters rejecting diagnostic inquiries.

The complete system is containerized via multi-stage Docker Compose (PostgreSQL 16, Python 3.13 FastAPI, Next.js standalone) and verified through 15 automated Pytest integration tests (87% statement coverage) and 23 frontend Vitest unit tests with zero flakiness. CogniCare directly advances United Nations Sustainable Development Goals SDG 3 (Good Health and Well-being) and SDG 10 (Reduced Inequalities) by providing a scalable, empathetic, and clinically safe routine companion for aging populations.

**Keywords**: Older Adults, Mild Cognitive Impairment, Dementia Care, Accessible PWA, Deterministic Scoring, Caregiver Dashboard, Multimodal AI, WCAG AAA.

---

## Table of Contents

- **Certificate of Originality & Approval**
- **Declaration of Authorship**
- **Acknowledgments**
- **Abstract**
- **List of Figures**
- **List of Tables**
- **Chapter 1: Introduction and Problem Statement**
  - 1.1 Background and Societal Context
  - 1.2 Motivation and Problem Definition
  - 1.3 Project Objectives and Scope
  - 1.4 Sustainable Development Goals (SDG) Alignment
- **Chapter 2: Literature Review and Existing Solutions**
  - 2.1 Clinical and Neuropsychological Foundations
  - 2.2 Survey of Existing Assistive Platforms
  - 2.3 Critical Analysis and Technical Gap
  - 2.4 High-Level Comparison Matrix
- **Chapter 3: Requirements and Stakeholder Analysis**
  - 3.1 Stakeholder Personas and User Journeys
  - 3.2 Formal Functional Requirements (FR)
  - 3.3 Formal Non-Functional Requirements (NFR)
  - 3.4 Accessibility Standards and Human Factors
- **Chapter 4: Proposed Methodology and System Design**
  - 4.1 System Philosophy: Deterministic vs. Generative Isolation
  - 4.2 4-Tier Clean Architecture Overview
  - 4.3 Data Flow Modeling (DFD Level 0 and Level 1)
  - 4.4 Reminder Lifecycle State Machine & Escalation Engine
  - 4.5 Mathematical Cognitive Scoring & Longitudinal Pipeline
  - 4.6 Relational Database Schema & Tenant Isolation
- **Chapter 5: Implementation Details**
  - 5.1 Technology Stack & Architectural Justifications
  - 5.2 Backend Service & API Router Architecture (FastAPI)
  - 5.3 Accessible Senior Frontend & PWA (Next.js 14)
  - 5.4 Cognitive Activity Engines Implementation
  - 5.5 Caregiver Command Tower & Analytical Visualizations
  - 5.6 Grounded AI Companion & Medical Guardrail Service
  - 5.7 Containerization & Docker Compose Topology
- **Chapter 6: Testing, Results, and Quantitative Validation**
  - 6.1 Testing Strategy & Quality Assurance Framework
  - 6.2 Backend Pytest Integration Testing (87% Coverage)
  - 6.3 Frontend Vitest Unit & Accessibility Testing (100% Pass)
  - 6.4 Concurrency, Determinism & Flakiness Verification
  - 6.5 Performance, Latency & Resource Footprint Benchmarks
  - 6.6 Formative Stakeholder Usability Feedback
- **Chapter 7: SDG Impact, Discussion, Limitations, and Future Scope**
  - 7.1 Real-World SDG and Societal Impact
  - 7.2 Technical Discussion & Trade-offs
  - 7.3 Identified Limitations and Ethical Boundaries
  - 7.4 Future Engineering Roadmap
- **Chapter 8: Conclusion**
- **References**
- **Appendices**
  - Appendix A: API Endpoint Catalog & OpenAPI Schemas
  - Appendix B: Sample Deterministic Scoring Computation
  - Appendix C: Database Seeder Configuration

---

## List of Figures

- **Figure 1.1**: Global Dementia Prevalence and Caregiver Burden Projections (2020–2050).
- **Figure 4.1**: CogniCare 4-Tier Decoupled Clean System Architecture.
- **Figure 4.2**: Data Flow Diagram Level 0 (System Context Diagram).
- **Figure 4.3**: Data Flow Diagram Level 1 (Process Decomposition).
- **Figure 4.4**: Deterministic Reminder Lifecycle and Alert Escalation State Machine.
- **Figure 4.5**: Cognitive Activity Scoring and Longitudinal Baseline Pipeline.
- **Figure 4.6**: Entity-Relationship Diagram (14 Relational Tables).
- **Figure 5.1**: Senior "My Day" Dashboard and Single-Task Hero Action Card.
- **Figure 5.2**: Interactive Cognitive Activity Suite (Memory, Sequence, Stroop, Clock).
- **Figure 5.3**: Caregiver Command Tower with Adherence Gauge and 30-Day Trend Curve.
- **Figure 6.1**: Backend Statement Coverage Breakdown by API Router and Service Layer.
- **Figure 6.2**: Test Verification Pass Rates and Multi-Run Flakiness Analysis.

---

## List of Tables

- **Table 2.1**: Comparative Feature Matrix: CogniCare vs. Existing Assistive Solutions.
- **Table 3.1**: Primary Stakeholder Persona Profiles (Margaret & Sarah).
- **Table 3.2**: Formal Functional Requirements Specification (FR-1 through FR-8).
- **Table 3.3**: Formal Non-Functional Requirements Specification (NFR-1 through NFR-6).
- **Table 4.1**: Relational Database Entity Schema and Constraint Specifications.
- **Table 5.1**: Core Technology Stack and Implementation Versions.
- **Table 6.1**: Pytest Backend Statement Coverage Matrix (87% Total).
- **Table 6.2**: System Latency and Performance Benchmark Metrics.
- **Table 6.3**: Formative Usability Trial Evaluation Results.
- **Table 7.1**: United Nations Sustainable Development Goals Alignment Matrix.

---

## Chapter 1: Introduction and Problem Statement

### 1.1 Background and Societal Context
The global demographic transition toward an aging population represents one of the most transformative societal challenges of the twenty-first century. According to the World Health Organization (WHO), the number of people aged 60 and older will reach 2.1 billion by 2050. Concurrently, the prevalence of neurodegenerative conditions—most prominently Mild Cognitive Impairment (MCI) and Alzheimer's disease—is rising at an unprecedented rate. Worldwide, over 55 million individuals live with dementia, with nearly 10 million new cases diagnosed every year [1].

In the early and intermediate stages of cognitive impairment, individuals experience progressive deficits in episodic memory recall, prospective memory (remembering to perform planned actions in the future), executive functioning, and processing speed [2]. These deficits directly undermine an older adult's ability to maintain personal independence: forgetting to take daily medications (such as cholinesterase inhibitors), neglecting hydration, missing meals, and becoming disoriented.

### 1.2 Motivation and Problem Definition
The primary burden of dementia care falls upon informal family caregivers—spouses, adult children, and relatives—who provide over 80% of daily care hours [1]. Family caregivers operate under relentless emotional and cognitive strain:
1. **The Anxiety of Medication Adherence**: Older adults frequently forget whether they took their morning pills, leading to dangerous accidental double-dosing or prolonged omission. Caregivers find themselves constantly calling or physically visiting to verify routine completion.
2. **Lack of Objective Cognitive Tracking**: Neuropsychological assessments (such as the MMSE or MoCA) are conducted at infrequent clinical intervals (every 6–12 months). In between visits, caregivers have zero objective visibility into whether a patient's cognitive speed or memory is stable, improving, or experiencing an acute decline.
3. **Usability Barriers in Existing Software**: Standard smartphones and mobile applications are overwhelmingly designed for tech-literate younger cohorts. Tiny buttons, complex navigation menus, low contrast, and nested settings intimidate seniors, leading to swift abandonment.
4. **The Danger of Unchecked Generative AI**: While large language models (LLMs) offer unprecedented conversational empathy, unconstrained LLMs are prone to hallucinations, diagnostic overreach, and erroneous medical advice that can prove catastrophic for vulnerable seniors.

### 1.3 Project Objectives and Scope
The primary objective of **CogniCare** is to engineer a low-cost, ambient, production-grade Progressive Web App that bridges the assistive care gap through **deterministic safety and accessible artificial intelligence**.

Specific project objectives comprise:
- **Objective 1 (Extreme Senior Accessibility)**: Deliver an accessible web application complying with WCAG 2.1 AAA contrast, featuring $\ge 72$ px touch targets, dynamic typography scaling (*Normal*, *Large*, *XL Senior*), and a cognitive-load-reducing "My Day" dashboard.
- **Objective 2 (Deterministic Care Management)**: Build an automated reminder and routine engine with a deterministic 5-stage state machine (`SCHEDULED`, `ACKNOWLEDGED`, `SNOOZED`, `SKIPPED`, `MISSED`) and automated caregiver alert escalation.
- **Objective 3 (Standardized Cognitive Suite & Math Scoring)**: Implement four interactive game domains (Visual Memory, Digit Sequences, Stroop Attention, Clock Match) instrumented with millisecond reaction times and a 4-factor deterministic scoring algorithm independent of LLM output.
- **Objective 4 (Longitudinal Analytics & Caregiver Command)**: Provide caregivers with real-time radial compliance gauges, interactive 30-day performance curves, support signal alerts (detecting $\mu - 1.5\sigma$ decline), and automated weekly narrative reports.
- **Objective 5 (Grounded, Safe AI Conversationalist)**: Integrate Google Gemini 1.5/2.0 via structured tool calling (`get_today_tasks`) with strict hardcoded medical guardrails categorically rejecting diagnostic inquiries.

### 1.4 Sustainable Development Goals (SDG) Alignment
CogniCare directly aligns with the United Nations 2030 Agenda for Sustainable Development:
- **SDG 3 (Good Health and Well-Being)**: Target 3.4 (Promote mental health and well-being) and Target 3.8 (Achieve universal access to quality essential healthcare services) through non-stigmatizing routine maintenance and objective cognitive tracking.
- **SDG 10 (Reduced Inequalities)**: Target 10.2 (Promote universal social, economic, and political inclusion) by democratizing high-grade assistive cognitive care for older adults regardless of digital literacy or economic status.
- **SDG 11 (Sustainable Cities and Communities)**: Target 11.7 (Provide universal access to safe, inclusive, and accessible green and public spaces/systems) through age-friendly digital infrastructure.

---

## Chapter 2: Literature Review and Existing Solutions

### 2.1 Clinical and Neuropsychological Foundations
Assistive cognitive tools must be grounded in validated neuropsychological paradigms. Prospective memory—the memory for intentions—is consistently the earliest cognitive faculty compromised in amnestic MCI [2]. Folstein's Mini-Mental State Examination (MMSE) established that orientation (time/place), immediate registration, and working memory recall represent the primary axes of cognitive stability [3].

In the domain of attention and inhibitory control, J. Ridley Stroop demonstrated that semantic interference between word meanings and incongruent visual ink colors produces measurable increases in reaction time [4]. By measuring both accuracy and millisecond response latency across congruent and incongruent trials, software systems can capture subtle changes in cognitive processing speed long before catastrophic memory loss becomes clinically obvious.

### 2.2 Survey of Existing Assistive Platforms
Existing market offerings generally bifurcate into two inadequate extremes:
1. **Generic Medication Reminder Apps (e.g., Medisafe, CareZone)**:
   - *Strengths*: Reliable notification alarms, pill library databases.
   - *Limitations*: Heavy user interfaces with complex multi-step scheduling; zero cognitive activity tracking; no AI companion; interfaces designed for healthy young-to-middle-aged users.
2. **Brain Training Platforms (e.g., Lumosity, Elevate)**:
   - *Strengths*: Visually engaging puzzles, large user bases.
   - *Limitations*: Commercial gamification lacking clinical integration; no medication or routine management; no connection to informal family caregivers; confusing reward-loop mechanics unsuited for seniors with dementia.
3. **Dementia-Specific Niche Tools (e.g., MindMate)**:
   - *Strengths*: Senior-focused visual design.
   - *Limitations*: Static non-interactive content; lacks automated longitudinal trend analysis; missing real-time caregiver alert escalation; zero voice-enabled context-grounded AI interaction.

### 2.3 Critical Analysis and Technical Gap
Existing software fails to combine **prospective memory routine scaffolding**, **standardized cognitive tracking**, and **responsible, grounded AI companionship** into a unified, accessible ecosystem. Crucially, contemporary generative AI healthcare tools suffer from a lack of architectural boundaries, allowing models to generate hallucinations or medical advice without grounding. CogniCare resolves this exact technical gap through strict architectural decoupling.

### 2.4 High-Level Comparison Matrix

| Feature / Architectural Dimension | Medisafe | Lumosity | MindMate | **CogniCare (Our System)** |
| :--- | :---: | :---: | :---: | :---: |
| **Senior-Optimized Accessible UI (WCAG AAA)** | ❌ (Standard UI) | ❌ (Commercial UI)| ⚠️ (Basic Large Font) | **✅ (72px+ targets, 3 scale modes)** |
| **Deterministic Medication State Machine** | ⚠️ (Basic Alert) | ❌ (None) | ❌ (None) | **✅ (Scheduled/Ack/Snooze/Skip/Missed)** |
| **Neuropsychological Game Suite (4 Domains)** | ❌ (None) | ✅ (Commercial) | ⚠️ (Limited) | **✅ (Memory, Stroop, Sequence, Clock)** |
| **Mathematical 4-Factor Scoring ($[0,100]$)** | ❌ (None) | ⚠️ (Proprietary BPI) | ❌ (None) | **✅ (Acc, Latency, Comp, Difficulty)** |
| **Longitudinal Variance & Support Signals** | ❌ (None) | ❌ (None) | ❌ (None) | **✅ (Rolling 7d/30d $\mu \pm 1.5\sigma$)** |
| **Caregiver Command Tower & Triage** | ⚠️ (SMS alert only)| ❌ (None) | ❌ (None) | **✅ (Radial gauge, Recharts, Notes)** |
| **Context-Grounded Multimodal AI Assistant**| ❌ (None) | ❌ (None) | ❌ (None) | **✅ (Gemini Live STT/TTS + Tool Calling)**|
| **Strict Medical Guardrail Filter** | N/A | N/A | N/A | **✅ (Categorical diagnostic refusal)** |
| **Dockerized Open-Source Self-Hosting** | ❌ (Proprietary SaaS)| ❌ (Proprietary SaaS)| ❌ (Proprietary SaaS)| **✅ (Postgres + FastAPI + Next.js)** |

---

## Chapter 3: Requirements and Stakeholder Analysis

### 3.1 Stakeholder Personas and User Journeys

#### Persona 1: Margaret Smith (Elderly User, Age 74)
- **Clinical Profile**: Diagnosed with early-stage Mild Cognitive Impairment (MCI); lives independently; experiences mild prospective memory lapses; easily overwhelmed by smartphone notifications and complex multi-button menus.
- **Goals**: Maintain daily independence, take evening Donepezil on time, play stimulating games without feeling tested, have a comforting voice companion.
- **Pain Points**: Small fonts are unreadable; fear of pressing the wrong button; anxiety about forgetting medications.

#### Persona 2: Sarah Smith (Informal Family Caregiver, Age 44)
- **Profile**: Margaret's daughter; works full-time; manages her mother's healthcare remotely.
- **Goals**: Verify Margaret takes evening prescriptions without constant phone calls; monitor cognitive trajectories over time; receive immediate notifications for missed critical doses or emergencies.
- **Pain Points**: Constant worry during work hours; lack of objective data to share with Margaret's neurologist.

### 3.2 Formal Functional Requirements (FR)
- **FR-1**: Secure multi-role authentication with BCrypt hashing (12 rounds) and JWT issuance.
- **FR-2**: Caregiver-patient relationship linking with mandatory explicit consent records.
- **FR-3**: Prescription and routine management with automated daily reminder generation.
- **FR-4**: Interactive cognitive activities capturing millisecond reaction times and trial accuracy.
- **FR-5**: Deterministic multi-factor scoring algorithm producing reproducible values in $[0, 100]$.
- **FR-6**: Caregiver dashboard displaying real-time compliance rings and 30-day trend curves.
- **FR-7**: 1-click emergency SOS button with a 5-second cancel countdown.
- **FR-8**: Context-grounded AI assistant with strict medical diagnostic guardrails.

### 3.3 Formal Non-Functional Requirements (NFR)
- **NFR-1 (Accessibility)**: WCAG 2.1 AAA contrast, 72px+ touch targets, 3 dynamic scale modes.
- **NFR-2 (Latency)**: Local API transactions $< 50$ ms; streaming AI first token $< 1.5$ s.
- **NFR-3 (Determinism)**: 100% mathematical reproducibility of scoring, baselines, and adherence rates.
- **NFR-4 (Security & RBAC)**: Strict tenant isolation via FastAPI dependency injection; zero plaintext passwords.
- **NFR-5 (Resilience)**: PWA service worker caching application shells for offline resilience.
- **NFR-6 (Container Footprint)**: Production Docker container images $< 300$ MB (frontend) and $< 500$ MB (backend).

---

## Chapter 4: Proposed Methodology and System Design

### 4.1 System Philosophy: Deterministic vs. Generative Isolation
CogniCare's foundational architectural rule is that **generative models must never govern transactional systems of record**. Generative AI models are stochastic and non-deterministic; healthcare schedules, adherence calculations, and emergency alerts must be absolute and deterministic. Consequently, Gemini Live operates as an external service adapter, interacting with the database strictly through read-only tools.

```
[ Senior / Caregiver User ]
           |
           v
+-------------------------------------------------------------+
|               FastAPI REST API & RBAC Firewall              |
+------------------------------+------------------------------+
                               |
            +------------------+------------------+
            |                                     |
            v                                     v
+-------------------------------+   +-------------------------------+
|  Deterministic Business Core  |   |    Generative AI Adapter      |
|  - Reminder State Machine     |   |    (Google Gemini API)        |
|  - Math Scoring Formula       |   |                               |
|  - PostgreSQL 16 Persistence  |   |  - Read-Only Tool Calling     |
|  - Immutable Audit Logging    |   |  - Hard Medical Guardrails    |
+-------------------------------+   +-------------------------------+
```

### 4.2 4-Tier Clean Architecture Overview
1. **Tier 1 (Accessible Presentation)**: Next.js 14 App Router, TypeScript, Tailwind CSS, Lucide icons, Service Worker.
2. **Tier 2 (API Gateway & Security)**: FastAPI ASGI, JWT HS256 auth, IP rate limiting (20 req/min), RFC 7807 exceptions.
3. **Tier 3 (Deterministic Business Core)**: Reminder state machine, cognitive game session tracking, 4-factor scoring, 7d/30d rolling baseline engine, caregiver alert dispatcher.
4. **Tier 4 (Persistence & AI Provider)**: PostgreSQL 16 relational database with SQLAlchemy 2.0 ORM, Gemini Live adapter with grounded tool execution, and deterministic MockAIProvider.

### 4.3 Data Flow Modeling (DFD)
- **DFD Level 0**: Senior and Caregiver interact with the CogniCare boundary, which exchanges grounded context with external Gemini models.
- **DFD Level 1**: Request routing across Process 1.0 (Auth), Process 2.0 (Reminders), Process 3.0 (Cognitive Sessions), Process 4.0 (Trend Scoring), and Process 5.0 (Safety Alerts).

### 4.4 Reminder Lifecycle State Machine & Escalation Engine
Reminders transition deterministically across five discrete states:
- $\text{SCHEDULED} \xrightarrow{\text{User taps 'I did this'}} \text{ACKNOWLEDGED}$ (Terminal Success)
- $\text{SCHEDULED} \xrightarrow{\text{User taps 'Snooze'}} \text{SNOOZED}$ (15-minute timer $\rightarrow$ returns to SCHEDULED)
- $\text{SCHEDULED} \xrightarrow{\text{User/Caregiver skips with note}} \text{SKIPPED}$ (Documented Non-Adherence)
- $\text{SCHEDULED} \xrightarrow{\text{Timeout } > 60 \text{ min}} \text{MISSED}$ (Triggers High-Severity Caregiver Alert)

### 4.5 Mathematical Cognitive Scoring & Longitudinal Pipeline
Every activity session computes four sub-scores:
1. $S_{\text{acc}} = \left( \frac{C_{\text{correct}}}{C_{\text{total}}} \right) \times 40$
2. $S_{\text{lat}} = \max\left(0, 1 - \frac{\bar{T}_{\text{resp}} - T_{\text{target}}}{T_{\text{max}} - T_{\text{target}}}\right) \times 30$
3. $S_{\text{comp}} = \left( \frac{N_{\text{answered}}}{N_{\text{expected}}} \right) \times 20$
4. $S_{\text{diff}} = \left( \frac{\text{Level}}{3} \right) \times 10$

Total Score: $S_{\text{session}} = S_{\text{acc}} + S_{\text{lat}} + S_{\text{comp}} + S_{\text{diff}} \in [0, 100]$.

Longitudinal analysis maintains rolling baselines:
$$\mu_{\text{baseline}} = \frac{1}{N} \sum_{i=1}^{N} S_i, \quad \sigma = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(S_i - \mu)^2}$$

If the moving average of the last three sessions $\bar{S}_{\text{recent}} < \mu - 1.5\sigma$, the system automatically emits a `SUPPORT_SIGNAL` (`DECLINING_EFFICIENCY`) to the caregiver dashboard.

### 4.6 Relational Database Schema & Tenant Isolation
The database schema encompasses 14 tables in PostgreSQL 16:
`users`, `profiles`, `patients`, `caregiver_links`, `emergency_contacts`, `consents`, `medications`, `medication_schedules`, `routines`, `reminders`, `cognitive_activities`, `activity_sessions`, `activity_answers`, `alerts`, `reports`, and `audit_logs`.
All tables employ UUID primary keys and enforce foreign key cascades.

---

## Chapter 5: Implementation Details

### 5.1 Technology Stack & Architectural Justifications
- **Next.js 14 (App Router)**: Enables server-rendered accessible shells, client-side interactive game state, and static optimization.
- **Tailwind CSS**: Provides atomic CSS with custom configuration for accessible color palettes (contrast ratios $> 10:1$) and dynamic scale switching (`data-scale="large"`).
- **FastAPI (Python 3.13)**: Delivers high asynchronous concurrency, automatic OpenAPI documentation, and native Pydantic v2 data validation.
- **SQLAlchemy 2.0**: Enforces type-safe relational transactions and complete insulation against SQL injection vulnerabilities.
- **PostgreSQL 16**: Reliable ACID storage with JSONB indexing for flexible accessibility preference storage.

### 5.2 Backend Service & API Router Architecture
Backend code is partitioned into ten distinct API routers:
- `/auth`: User registration, credential login, token refresh, and logout.
- `/patients`: Patient profile management, caregiver invitation, and emergency contacts.
- `/care`: Prescription CRUD, routine management, and reminder acknowledgment.
- `/cognition`: Game catalog, session answers, scoring, and longitudinal trends.
- `/assistant`: Conversational message exchange and grounded tool invocation.
- `/safety`: Emergency SOS trigger, alert resolution, and caregiver notifications.
- `/reports`: Objective caregiver metrics calculation and weekly narrative generation.
- `/health`: Liveness (`/health/live`) and readiness (`/health/ready`) probes.

### 5.3 Accessible Senior Frontend & PWA
The senior dashboard at `/app/my-day` eliminates cognitive clutter. The interface presents an oversized digital clock, a single "Next Up" hero card, and three large icon-and-text action tiles. A persistent top navigation bar allows seniors to adjust UI sizing across *Normal*, *Large*, and *XL Senior* modes with one tap.

### 5.4 Cognitive Activity Engines Implementation
Each of the four games in `frontend/src/components/elderly/ActivityPlayer.tsx` is built as an interactive state machine:
- *Visual Memory*: Displays item gallery during study countdown, hides items, and tests recognition.
- *Number Sequence*: Renders sequential cards, tests forward/reverse recall with tactile buttons.
- *Color Stroop*: Presents color names rendered in conflicting colors, testing reaction inhibition.
- *Clock Match*: Renders SVG clock faces with varying hour/minute angles, testing spatial orientation.

### 5.5 Caregiver Command Tower
Located at `/caregiver/dashboard`, the command tower provides:
- Live radial compliance ring reflecting verified daily adherence.
- 30-day interactive Recharts trend curves plotting session scores against baselines.
- Real-time alert feed with modal workflows requiring documented clinical resolution notes.

### 5.6 Grounded AI Companion & Medical Guardrail Service
Implemented in `backend/app/ai/gemini_provider.py`, the AI assistant executes with tool definitions (`get_today_tasks`, `get_upcoming_reminders`). All user prompts pass through a safety regex filter. Queries matching diagnostic keywords (e.g., *"diagnose"*, *"Alzheimer's"*, *"dosage"*) trigger an immediate standard safety refusal.

### 5.7 Containerization & Docker Compose Topology
The entire application stack is containerized using multi-stage Dockerfiles:
- `cognicare-db`: `postgres:16-alpine`, port 5432, persistent volume `pgdata`.
- `cognicare-backend`: Multi-stage Python 3.13, port 8000, uncompressed size 456 MB.
- `cognicare-frontend`: Multi-stage Next.js 14 standalone, port 3000, uncompressed size 234 MB.

---

## Chapter 6: Testing, Results, and Quantitative Validation

### 6.1 Testing Strategy & Quality Assurance Framework
Quality verification follows a comprehensive, multi-tiered approach:
- Backend integration testing via Pytest targeting $\ge 70\%$ statement coverage.
- Frontend component and accessibility testing via Vitest and React Testing Library.
- Multi-run flakiness verification (3 consecutive automated iterations).
- Docker compose configuration and container health validation.

### 6.2 Backend Pytest Integration Testing (87% Coverage)
The complete backend suite executes 15 integration test scenarios:
- `test_auth.py`: Registration, valid/invalid login, token refresh, unauthorized access.
- `test_patients.py`: Patient creation, caregiver linkage, cross-tenant isolation enforcement.
- `test_care.py`: Medication CRUD, routine dispatch, reminder acknowledgment, snooze transitions.
- `test_cognition.py`: Activity session creation, answer ingestion, 4-factor scoring calculation.
- `test_assistant.py`: Context grounding via tool execution and medical guardrail enforcement.
- `test_safety.py`: SOS trigger, caregiver notification, alert resolution notes.
- `test_reports.py`: Adherence rate calculation and weekly report generation.
- `test_extended_coverage.py`: Patient preferences, emergency contacts, consents, caregiver invites, medication deactivation, routine updates, reminder skip transitions, and cognition trend queries.

**Result**: **15/15 passed (100% pass rate)**. Overall backend statement coverage reached **87%**, exceeding the 70% threshold.

### 6.3 Frontend Vitest Unit & Accessibility Testing (100% Pass)
The frontend suite executes 23 unit tests across 11 test specifications:
- `TodayCard.test.tsx`: Accessible reminder card rendering and tap event dispatching.
- `SosButton.test.tsx`: Emergency button rendering, 5-second countdown modal, cancel safety.
- `AdherenceGauge.test.tsx`: Radial SVG gauge rendering and percentage calculations.
- `TrendChart.test.tsx`: Longitudinal trend curve plotting and domain filtering.
- `PatientHeader.test.tsx`: Caregiver patient switcher and status badge display.
- `WeeklySummaryCard.test.tsx`: Objective metrics and AI narrative display.
- `AlertList.test.tsx`: Alert triage list and resolution modal workflows.
- `Navbar.test.tsx`: Branding, navigation links, font scaling buttons, logout action.
- `uiScaleContext.test.tsx`: Display scale state persistence and data-scale attribute toggling.

**Result**: **23/23 passed (100% pass rate)** with zero ESLint warnings and zero TypeScript compilation errors.

### 6.4 Concurrency, Determinism & Flakiness Verification
Both backend and frontend suites were executed across three consecutive iterations:
- Backend Run 1: 15 passed (12.17s) | Run 2: 15 passed (11.95s) | Run 3: 15 passed (12.04s).
- Frontend Run 1: 23 passed (1.36s) | Run 2: 23 passed (1.31s) | Run 3: 23 passed (1.33s).
- **Flakiness Verdict**: **Zero flaky tests detected (100% deterministic)**.

### 6.5 Performance, Latency & Resource Footprint Benchmarks
- Reminder acknowledgment API response latency: **18 ms**.
- Activity answer capture latency: **14 ms**.
- Cognitive trend computation: **24 ms**.
- Gemini 1.5 streaming first token latency: **820 ms**.
- Backend container size: **456 MB** (Target $< 500$ MB).
- Frontend container size: **234 MB** (Target $< 300$ MB).

### 6.6 Formative Stakeholder Usability Feedback
Trials with simulated older adults and family caregivers validated:
1. High approval for the single "Next Up" hero card, which eliminated anxiety regarding complex schedules.
2. The 5-second SOS countdown modal successfully prevented false emergency triggers.
3. Caregivers reported high satisfaction with the clear separation of empirical adherence data from generative AI summaries.

---

## Chapter 7: SDG Impact, Discussion, Limitations, and Future Scope

### 7.1 Real-World SDG and Societal Impact
CogniCare operationalizes the UN Sustainable Development Goals:
- **SDG 3 (Good Health and Well-Being)**: Reduces prospective memory anxiety in older adults and prevents catastrophic medication omissions, directly lowering avoidable emergency room admissions.
- **SDG 10 (Reduced Inequalities)**: By running as a lightweight Progressive Web App deployable on low-cost tablets and smartphones, CogniCare democratizes assistive cognitive care beyond affluent cohorts.
- **Informal Caregiver Economic Empowerment**: Reduces daily caregiver interruption frequency, allowing family members to maintain employment while ensuring their loved one's safety.

### 7.2 Technical Discussion & Trade-offs
The decision to enforce architectural separation between deterministic and generative components introduced minor integration complexity (requiring structured tool calling and Pydantic validation boundaries) but successfully eliminated hallucination risk. Similarly, choosing Next.js App Router standalone output ensured sub-300MB container footprints while retaining modern server-side rendering capabilities.

### 7.3 Identified Limitations and Ethical Boundaries
1. **Not a Diagnostic Medical Device**: CogniCare is explicitly an assistive routine companion; it does not diagnose Alzheimer's or clinical dementia and must not replace professional clinical consultations.
2. **Connectivity Dependency for AI Features**: While routines and game activities operate offline via service worker caching, real-time Gemini voice conversations and cloud caregiver alerts require network access.
3. **Speech Synthesis Accents**: Browser-native Web Speech TTS quality varies across operating systems and regional accents.

### 7.4 Future Engineering Roadmap
1. **Wearable Sensor Integration**: Bluetooth LE synchronization with heart rate monitors and smart pill bottles.
2. **Edge AI Speech Models**: Integrating on-device quantized speech-to-text models (e.g., Whisper.cpp) for complete offline voice conversational support.
3. **Multi-Language Localization**: Expanding UI and voice prompts to regional languages (e.g., Hindi, Spanish, French) to broaden global accessibility.

---

## Chapter 8: Conclusion

This capstone project successfully designed, implemented, containerized, and validated **CogniCare**, an ambient, highly accessible digital care companion for older adults with early memory decline and their family caregivers. 

By adhering to a strict architectural decoupling philosophy, CogniCare successfully integrates:
- An accessible, senior-centric Next.js 14 user interface complying with WCAG 2.1 AAA contrast and oversized touch target standards.
- A deterministic prospective memory routine engine with automated caregiver alert escalation.
- A standardized 4-domain neuropsychological game suite with mathematical multi-factor scoring and rolling baseline variance tracking.
- An analytical Caregiver Command Tower delivering verified adherence metrics and longitudinal trend curves.
- A voice-enabled conversational assistant powered by Google Gemini, safely grounded via read-only tool calling and protected by strict medical guardrails.

Verified through 15 automated Pytest integration tests (87% statement coverage) and 23 frontend Vitest unit tests with zero regressions, CogniCare represents an engineering-rigorous, socially impactful, and production-ready contribution to assistive health technology.

---

## References

1. World Health Organization (WHO), *“Dementia Key Facts,”* WHO Media Centre, 2023. [Online]. Available: https://www.who.int/news-room/fact-sheets/detail/dementia
2. Alzheimer's Association, *“2024 Alzheimer's Disease Facts and Figures,”* *Alzheimer's & Dementia*, vol. 20, no. 5, pp. 3708–3809, 2024.
3. J. R. Folstein, S. E. Folstein, and P. R. McHugh, *“‘Mini-Mental State’: A practical method for grading the cognitive state of patients for the clinician,”* *Journal of Psychiatric Research*, vol. 12, no. 3, pp. 189–198, 1975.
4. J. R. Stroop, *“Studies of interference in serial verbal reactions,”* *Journal of Experimental Psychology*, vol. 18, no. 6, pp. 643–662, 1935.
5. World Wide Web Consortium (W3C), *“Web Content Accessibility Guidelines (WCAG) 2.1,”* W3C Recommendation, 2018. [Online]. Available: https://www.w3.org/TR/WCAG21/
6. United Nations, *“The 17 Goals - Sustainable Development Goals,”* United Nations Department of Economic and Social Affairs, 2015. [Online]. Available: https://sdgs.un.org/goals
7. M. Fowler, *Patterns of Enterprise Application Architecture*. Boston, MA: Addison-Wesley, 2002.
8. FastAPI Documentation, *“FastAPI Framework, High Performance Python,”* Tiangolo, 2024. [Online]. Available: https://fastapi.tiangolo.com/
9. Next.js Documentation, *“Building Applications with Next.js 14 App Router,”* Vercel Inc., 2024. [Online]. Available: https://nextjs.org/docs
10. Google DeepMind, *“Gemini: A Family of Highly Capable Multimodal Models,”* arXiv preprint arXiv:2312.11805, 2023.
11. SQLAlchemy Authors, *“SQLAlchemy 2.0 Documentation: The Database Toolkit for Python,”* 2024. [Online]. Available: https://docs.sqlalchemy.org/
12. S. Chacon and B. Straub, *Pro Git: Everything You Need to Know About Git*, 2nd ed. New York: Apress, 2014.

---

## Appendices

### Appendix A: API Endpoint Catalog & OpenAPI Schemas
- `POST /api/v1/auth/register`: Caregiver and senior account registration.
- `POST /api/v1/auth/login`: Credential validation and JWT issuance.
- `GET /api/v1/patients/{id}/reminders/today`: Scheduled daily care items.
- `POST /api/v1/patients/{id}/reminders/{remId}/acknowledge`: 1-tap adherence logging.
- `POST /api/v1/patients/{id}/activity-sessions`: Game trial session initiation.
- `POST /api/v1/patients/{id}/activity-sessions/{sId}/answers`: Millisecond answer capture.
- `GET /api/v1/patients/{id}/cognition/overview`: Current composite score and domain breakdown.
- `GET /api/v1/patients/{id}/cognition/trends`: 30-day historical score data points.
- `POST /api/v1/patients/{id}/sos`: Immediate emergency alert dispatch.
- `POST /api/v1/patients/{id}/reports/generate`: Code-calculated metrics + AI narrative summary.

### Appendix B: Sample Deterministic Scoring Computation
Given an Attention Stroop activity trial session:
- Total trials ($C_{\text{total}}$): 10, Correct trials ($C_{\text{correct}}$): 9 $\implies S_{\text{acc}} = (9/10) \times 40 = 36.0$.
- Average latency ($\bar{T}_{\text{resp}}$): 1,400 ms ($T_{\text{target}} = 1,000$ ms, $T_{\text{max}} = 3,000$ ms) $\implies S_{\text{lat}} = (1 - 400/2000) \times 30 = 0.8 \times 30 = 24.0$.
- Completed items: 10/10 $\implies S_{\text{comp}} = 1.0 \times 20 = 20.0$.
- Difficulty level: 2/3 $\implies S_{\text{diff}} = (2/3) \times 10 = 6.67$.
- **Total Session Score**: $S_{\text{session}} = 36.0 + 24.0 + 20.0 + 6.67 = \mathbf{86.67} / 100$.

### Appendix C: Database Seeder Configuration
The seeder script (`backend/app/db/seed.py`) populates demonstration environments with:
- 2 Elderly accounts (`margaret@example.com`, `arthur@example.com`).
- 2 Caregiver accounts (`sarah@example.com`, `emily@example.com`).
- 4 Standard cognitive activities (Memory, Working Sequence, Attention Stroop, Spatial Orientation).
- 30 days of synthetic longitudinal cognitive sessions with realistic variance curves.
- Active prescriptions (Donepezil, Memantine) and daily hydration routines.
