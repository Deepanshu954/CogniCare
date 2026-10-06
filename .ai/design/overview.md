# CogniCare: System Overview

## 1. System Philosophy
CogniCare decouples deterministic system of record (PostgreSQL, FastAPI business logic) from generative AI capabilities (LLM summaries, voice conversation). The AI proposes language and navigates users, but application services strictly enforce authorization, consent, and transaction validity.

## 2. Core Capabilities
1. **Identity & Multi-Role Access Control**:
   - Elderly, Caregiver, Reviewer, Admin roles with granular permissions (`VIEW_COGNITION`, `MANAGE_REMINDERS`, `VIEW_ALERTS`, etc.).
2. **Care Management**:
   - Medication scheduling, daily routines (meals, hydration, exercise), reminder dispatching, user acknowledgment, snooze, skip, and automated escalation upon missed critical reminders.
3. **Cognitive Activity Engine**:
   - Interactive games across 4 domains:
     - Memory Recall (pattern & word recall)
     - Sequence & Working Memory (forward/reverse digit & item sequences)
     - Attention & Reaction (Stroop color/word test, target selection)
     - Orientation & Spatial Matching (clock orientation, matching pairs)
   - Real-time answer capture: `response_time_ms`, attempts, accuracy, difficulty level.
4. **Scoring & Longitudinal Trend Engine**:
   - Mathematical, reproducible scoring formula based on accuracy, reaction efficiency, completion, and task difficulty.
   - Rolling baseline calculation (7-day and 30-day windows), statistical variance, and trend classification (stable, improving, variable, declining signal).
5. **Caregiver Dashboard**:
   - Real-time status cards, adherence percentage gauges, interactive Recharts trend graphs, alert notification center, and weekly summary generator.
6. **AI Assistant with Tool Calling**:
   - Natural language companion grounded in user's schedule, memories, and today's routine.
   - Structured tool execution (`get_today_tasks`, `get_upcoming_reminders`, `start_activity`).
   - Medical guardrail policy: rejects diagnostic inquiries and medication alterations.
7. **Safety & Alerts**:
   - 1-click SOS button trigger, missed medication alarms, and inactivity threshold checks.
8. **PWA & Offline Capability**:
   - Service worker caching, Web App Manifest, IndexedDB storage for offline activity play with background sync upon reconnect.
