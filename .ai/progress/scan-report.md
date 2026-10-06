# Codebase Scan Report: CogniCare

## 1. Project Root & Environment
- **Workspace Directory**: `/Users/deepanshu954/GitHub/Capstone`
- **Detected Operating System**: macOS Darwin (Python 3.13.15, Node.js v20.12+)
- **Git Repository**: Initialized, active branch `main`, tracking commits and history.

---

## 2. Tech Stack Detection

| Component | Technology | Version | Purpose |
|---|---|---|---|
| **Backend Framework** | FastAPI | 0.115.0 | Async REST API, OpenAPI docs, dependency injection |
| **Backend Language** | Python | 3.13.15 | Core server logic, AI provider integration |
| **ORM / Data Access** | SQLAlchemy | 2.0.35 | Relational domain modeling, session management |
| **Database** | SQLite / PostgreSQL | 16 (Compose) | Local dev SQLite (`backend/cognicare.db`), Prod Postgres |
| **AI Integration** | Google GenAI SDK | `google-genai` | Gemini 3.8 Live & Extended Thinking with fallback engine |
| **Backend Testing** | Pytest + pytest-cov | 9.1.1 / 7.1.0 | Unit, service, and endpoint integration testing |
| **Frontend Framework** | Next.js (App Router) | 14.2.35 | React 18 server and client components, static export |
| **Frontend Language** | TypeScript | 5.6.3 | Strict type safety, schemas, and API contracts |
| **Styling System** | Tailwind CSS | 3.4.13 | High-contrast WCAG AAA theme, multi-scale responsive styling |
| **Data Fetching** | TanStack React Query | 5.59.0 | Client-side cache management, query invalidation |
| **Frontend Testing** | Vitest + React Testing Library | 2.1.9 / 16.0.1 | Component rendering, user interaction, accessibility specs |
| **Containerization** | Docker & Docker Compose | Compose v2 | Multi-stage Dockerfiles, non-root users, healthchecks |
| **CI / CD** | GitHub Actions | `.github/workflows/ci.yml` | Automated linting, testing, and container build pipeline |

---

## 3. Build & Compilation Verification

| Layer | Command | Status | Details |
|---|---|---|---|
| **Backend** | `pytest backend/tests/` | **PASSED (Exit 0)** | All modules load cleanly without syntax or import errors |
| **Frontend Build** | `npm --prefix frontend run build` | **PASSED (Exit 0)** | 12/12 static & dynamic routes compiled into production standalone bundle |
| **Frontend Lint** | `npm --prefix frontend run lint` | **PASSED (Exit 0)** | 0 errors, 0 warnings across all TypeScript & TSX files |

---

## 4. Test Suite Execution & Flakiness Verification

| Suite | Tests | Passed | Failed | Skipped | Pass Rate | Flakiness (3x Runs) |
|---|---|---|---|---|---|---|
| **Backend (Pytest)** | 11 | 11 | 0 | 0 | **100%** | **0 Flaky (3/3 Passed)** |
| **Frontend (Vitest)** | 8 | 8 | 0 | 0 | **100%** | **0 Flaky (3/3 Passed)** |
| **Total** | **19** | **19** | **0** | **0** | **100%** | **0 Flaky** |

---

## 5. Directory Structure Overview
```
/Users/deepanshu954/GitHub/Capstone
├── .ai/                    # Design specifications, progress logs, test results, deploy plans
├── .github/workflows/      # Automated CI/CD pipeline definition
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── ai/             # AI provider abstraction, Gemini live/thinking, context builder
│   │   ├── api/v1/         # REST Controllers: auth, patients, care, cognition, safety, reports
│   │   ├── core/           # Security, config, database, rate limiting, exception handling
│   │   ├── db/             # Seed data and migration scripts
│   │   ├── models/         # SQLAlchemy 2.0 ORM domain entities
│   │   ├── repositories/   # Clean repository pattern database access
│   │   ├── schemas/        # Pydantic v2 validation DTOs
│   │   └── services/       # Core business logic and transaction boundaries
│   ├── tests/              # Pytest comprehensive test suite
│   ├── Dockerfile          # Multi-stage production container definition
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js 14 App Router application
│   ├── public/             # Static icons, manifest.json, sw.js
│   ├── src/
│   │   ├── app/            # Next.js App Router pages (auth, elderly, caregiver)
│   │   ├── components/     # UI primitives, accessible widgets, SVG games, visual tokens
│   │   ├── context/        # Auth context, user sessions
│   │   ├── lib/            # Axios API client, UI scale context
│   │   └── __tests__/      # Vitest component test suites
│   ├── Dockerfile          # Multi-stage production container definition
│   ├── package.json        # Node.js dependencies and scripts
│   └── tailwind.config.js  # Theme and responsive design configuration
├── docker-compose.yml      # Local container orchestration topology
├── .env.example            # Environment variable template
└── README.md               # Complete architecture, setup, and viva guide
```
