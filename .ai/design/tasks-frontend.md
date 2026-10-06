# Frontend Task List: CogniCare

- [x] Task 1: Next.js Project Scaffold & Core Setup
  - Initialize Next.js 14+ App Router project with TypeScript and Tailwind CSS.
  - Set up Lucide React, TanStack Query provider, Axios instance with credentials and error handling.
  - Set up Auth Context and session state management.
  - Configure Tailwind with accessible high-contrast colors and large typography presets.

- [x] Task 2: Authentication & Role Gatekeeper
  - Build `/login` and `/register` pages with form validation.
  - Implement role-based redirecting: Elderly -> `/app/my-day`, Caregiver -> `/caregiver/dashboard`.
  - Add demo 1-click login quick-fill buttons ("Login as Margaret (Elderly)", "Login as Sarah (Caregiver)").

- [x] Task 3: Elderly Experience — "My Day" Dashboard
  - Screen: `/app/my-day`.
  - Big greeting card with time and date.
  - "Next Up" hero card with 1-tap "I did this!" button.
  - Big icon-and-text action tiles: Brain Games, Talk with Assistant, Call for Help.
  - Accessible today's reminder list with large badges.

- [x] Task 4: Elderly Experience — Interactive Cognitive Games
  - Screen: `/app/activities` and `/app/activities/[id]`.
  - Game 1: Memory Pairs (Visual pattern recall).
  - Game 2: Number Sequence (Working memory forward/reverse).
  - Game 3: Color Stroop (Attention & reaction test).
  - Game 4: Clock & Spatial Match (Orientation test).
  - High-touch accessible cards, step-by-step guidance, calm celebratory completion modal.

- [x] Task 5: Elderly Experience — Reminders Screen
  - Screen: `/app/my-day` and integrated reminder actions.
  - Oversized cards for scheduled medications and routines.
  - Massive high-contrast buttons: "Take Now", "Remind in 15 Min", "Skip Today".

- [x] Task 6: Elderly Experience — Conversational Voice Assistant
  - Screen: `/app/assistant`.
  - Giant pulsing microphone button with interactive listening/speaking states.
  - High-legibility speech bubbles with Web Speech API TTS toggle.
  - Preset quick prompts: "What's next?", "Did I take morning pills?", "Help me navigate".

- [x] Task 7: Elderly Experience — Emergency SOS Screen
  - Screen: `/app/safety`.
  - Massive crimson "PRESS FOR HELP" emergency button.
  - 5-second countdown with immediate cancel button to prevent false triggers.
  - Contact cards for designated family and doctors with direct dial.

- [x] Task 8: Caregiver Experience — Executive Dashboard
  - Screen: `/caregiver/dashboard`.
  - Patient switcher for multi-patient support.
  - Live status indicator (Activity, Medications, Alert status).
  - Adherence progress ring and 30-day cognitive performance Recharts curve.
  - Urgent alerts notification feed with 1-click Acknowledge.

- [x] Task 9: Caregiver Experience — Cognitive Health Analytics
  - Screen: Integrated in `/caregiver/dashboard` & `/caregiver/reports`.
  - Breakdown by cognitive domain (Memory, Attention, Speed, Orientation).
  - Historical session stats with accuracy rate and response time latency.
  - Clinical observation signals list (e.g. "Response latency stable over last 14 days").

- [x] Task 10: Caregiver Experience — Care & Medication Manager
  - Screen: Integrated in `/caregiver/dashboard`.
  - Active prescription cards with dosage, schedule, and recurrence.
  - "Add Medication" modal form with schedule and dose inputs.

- [x] Task 11: Caregiver Experience — Alert Management Center
  - Screen: Integrated in `/caregiver/dashboard`.
  - Real-time alerts feed categorized by severity (Critical, High, Medium, Info).
  - Modal workflows to Acknowledge alerts and Resolve with mandatory clinical notes.

- [x] Task 12: Caregiver Experience — Weekly AI Reports
  - Screen: `/caregiver/reports`.
  - "Generate Weekly Report" action with instant preview.
  - Side-by-side display of objective computed metrics and plain-language AI narrative.
  - Clean print/PDF export styling.

- [x] Task 13: PWA Configuration & Offline Support
  - Web App Manifest (`manifest.json`) with high-resolution icons.
  - Service Worker registration for offline asset caching.

- [x] Task 14: Frontend Build, Lint & Vitest Verification
  - Write Vitest tests for key components (BigActionButton, TrendChart, AdherenceGauge, TodayCard).
  - Execute `npm run build` and `npm test` verifying 0 errors.
