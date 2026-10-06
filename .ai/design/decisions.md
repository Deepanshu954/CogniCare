# CogniCare: Architectural & Technical Decisions Log

| Decision ID | Area | Choice | Rationale | Alternatives Considered |
|---|---|---|---|---|
| **DEC-001** | Backend Framework | Python 3.13 + FastAPI | Aligns with Plan.md, enables native Python AI/ML integration, async performance, and automatic OpenAPI schema generation. | Spring Boot 3.x, Express.js |
| **DEC-002** | Frontend Architecture | Next.js 14+ App Router + TypeScript | Provides unified responsive web PWA, SSR/hydration performance, and rich client state with React primitives. | React SPA (Vite), Mobile Native (React Native) |
| **DEC-003** | Database & Persistence | PostgreSQL 16 + SQLAlchemy 2.x + Alembic | Strong ACID compliance, relational integrity for care plans and audit trails, and native JSONB + pgvector support. | MongoDB, MySQL, DynamoDB |
| **DEC-004** | AI Provider Strategy | Pluggable Provider Abstraction (`GeminiProvider` & `MockAIProvider`) | Allows plug-and-play AI model routing while ensuring CI, offline testing, and grading evaluation succeed deterministically. | Direct OpenAI SDK coupling |
| **DEC-005** | Cognitive Scoring | Closed-form mathematical formula combining accuracy, latency, and difficulty | Guarantees reproducible, audit-friendly scores and prevents hallucinated clinical evaluations. | Pure LLM subjective grading |
| **DEC-006** | Authentication | JWT (HMAC-SHA256) with secure HTTP-only cookies & Bearer fallback | Safe against XSS in browser PWA while allowing easy API client testing. | Stateful session table only, OAuth only |
| **DEC-007** | Safety Escalation | Deterministic server-side state machine | Emergency alarms and missed medication escalations must never depend on non-deterministic AI decisions. | LLM-based alert triage |
| **DEC-008** | Accessibility Standard | WCAG 2.2 AA target with AAA considerations for elderly UI | Essential for elderly users experiencing cognitive or visual decline; prevents abandonment. | Standard generic dashboard design |
| **DEC-009** | Google Gemini Live & Thinking Modes | Gemini 3.8 Live (`gemini-2.0-flash`) & Gemini 3.8 Live Extended Thinking (`gemini-2.0-flash-thinking-exp`) | Provides zero-lag conversational assistance for live senior interactions and transparent reasoning traces for clinical inquiries. | Single generic model |
| **DEC-010** | Quota Fallback Engine | Local Resilient Fallback Engine on HTTP 429 | Senior companions must never display cryptic API errors or fail in emergencies when consumer quota is exhausted. | Raising unhandled HTTP 500 error |
| **DEC-011** | Speech Audio Output | Opt-in "Talk Aloud" toggle (default OFF) & Instant Stop Speaking controls | Prevents unsolicited audio babbling that confuses elderly users; gives immediate agency to mute audio at any moment. | Autoplay speech on every response |
| **DEC-012** | Multi-Scale Viewports | Triple UI density switcher (Normal, Large, Extra Large) | Adapts interface seamlessly from compact laptop displays to giant 76px+ touch targets for motor-impaired seniors on tablets. | Single fixed-size UI |
