# Changelog

All notable changes to the **CogniCare** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-10-06

### Added
- **Google Gemini 3.8 Live Integration**:
  - Dual conversational modes: **Normal Mode** (`gemini-2.0-flash` / Gemini 3.8 Live) for rapid audio/text companion interactions, and **Extended Mode** (`gemini-2.0-flash-thinking-exp` / Gemini 3.8 Live Extended Thinking) featuring step-by-step reasoning trace inspection.
  - Interactive Live Talk modal with animated microphone visualizer, Web Speech recognition, and auto-speech synthesis.
  - Zero-downtime Resilient Local Fallback Engine dynamically extracting clinical groundings when external API quotas are exhausted (HTTP 429).
- **Dual-Layer Grounding Context Engine**:
  - **Public Knowledge Layer**: Built-in geriatric care guidance, Mild Cognitive Impairment (MCI) communication guidelines, Naomi Feil validation therapy, orientation anchors, and strict medical non-diagnostic boundaries.
  - **Private Knowledge Layer**: Complete live patient profile injection including active prescriptions, daily schedules, emergency contacts, and 30-day cognitive performance metrics.
- **Rich Visual Brain Games**:
  - Visual Memory Cards with study phase and picture tokens (Vintage Teapot, Golden Sunflower, Crimson Apple).
  - Orientation Match with interactive SVG Analog Clock Face (hour & minute hands) and Compass Rose needle.
  - Color Stroop with high-contrast color cards and color swatch answer buttons.
  - Word Sequence with geometric shape tokens.
- **Multi-Scale Responsive UI**:
  - UI scale switcher with three dedicated scales: **Normal** (compact laptop layout), **Large** (standard legible layout), and **Extra Large** (senior touch targets 76px+).
  - Fully responsive design engineered for both mobile phone touch screens and laptop displays.
- **Docker & Infrastructure Resiliency**:
  - Restructured backend Dockerfile using `/opt/venv` multi-stage build, eliminating Debian Python 3.13 site-packages discovery issues.
  - Added resilient PostgreSQL startup loop (10 retries with exponential backoff) in FastAPI lifespan to prevent container crash loops.

## [1.0.0] - 2026-10-06

### Added
- **Core Architecture**:
  - FastAPI 0.142 + Python 3.13 backend with clean 4-tier modular architecture (Controllers, Services, Repositories, Models).
  - Next.js 14 App Router frontend with TypeScript strict mode and Tailwind CSS.
- **Elderly Companion Portal (`/app/*`)**:
  - "My Day" dashboard with 72px+ touch targets and 1-tap routine confirmation.
  - Interactive cognitive exercises: Memory Pairs, Number Sequence, Color Stroop, Orientation Match.
  - Ambient conversational companion with Web Speech API speech-to-text and text-to-speech.
  - Emergency SOS safety trigger with 5-second cancel countdown.
- **Caregiver Control Tower (`/caregiver/*`)**:
  - Executive dashboard with patient switcher, medication adherence gauge, and 30-day cognitive performance Recharts curve.
  - Real-time alert triage with acknowledge and resolve workflows.
  - Weekly AI reports engine with objective metrics snapshot and print/PDF layout.
- **Security & Reliability**:
  - OWASP Top 10 hardening, BCrypt 12-round password hashing, JWT stateless bearer authentication.
  - Sliding-window auth rate limiting (20 req/min) and hardened HTTP security headers.
  - Medical policy safety guardrail rejecting diagnostic claims or dosage alterations.
- **Testing & Deployment**:
  - 11 backend test suites with 87% test coverage.
  - 5 frontend test suites with 100% Vitest pass rate.
  - Multi-stage non-root Dockerfiles and validated Docker Compose topology.
  - GitHub Actions CI/CD automation pipeline.
