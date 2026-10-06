# CogniCare: Capstone Evaluation & Viva Summary (2-Minute Elevator Pitch)

## 1. What is CogniCare?
**CogniCare** is an ambient, dual-interface cognitive health and daily routine companion tailored specifically for seniors living with mild cognitive impairment (MCI) or early-stage dementia, and their family caregivers. It empowers aging seniors to live independently and with dignity through an ultra-accessible, speech-enabled daily station, while equipping caregivers with longitudinal cognitive analytics, medication adherence tracking, and urgent safety alerts.

---

## 2. Why Did We Build It? (Problem Statement)
Current solutions fall into two flawed extremes:
1. **Generic Reminder Apps**: Over-complex, small fonts, cluttered interfaces that frustrate and confuse seniors.
2. **Clinical Diagnostic Tools**: Cold, anxiety-inducing tests that are administered only occasionally in doctor's offices, missing subtle day-to-day cognitive decline.

**CogniCare bridges this gap** by weaving unobtrusive cognitive games and daily routine confirmations into everyday living, capturing objective data continuously without clinical anxiety.

---

## 3. Key Technological Highlights
- **Dual Persona Architecture**: Single unified platform serving both Senior (simplified, large-format, voice-supported) and Caregiver (rich data visualization, triage feeds, PDF reports).
- **Deterministic Math Scoring**: Cognitive performance is scored using rigorous mathematical formulas (accuracy + reaction latency bonus) rather than nondeterministic LLM outputs.
- **Medical Safety Guardrails**: AI assistant strictly operates under safety filters that reject diagnostic claims or medication adjustments.
- **Enterprise Engineering**: 87% test coverage on backend, 100% Vitest pass rate on frontend, OWASP Top 10 security hardened, containerized with Docker Compose.
