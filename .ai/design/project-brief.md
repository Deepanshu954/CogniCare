# CogniCare: Project Brief

## 1. Executive Summary
**CogniCare** is an accessibility-first, AI-assisted web platform (responsive PWA) that provides personalized cognitive activities, everyday care support, longitudinal performance insights, safe conversational assistance, and caregiver-centered monitoring for elderly people experiencing cognitive impairment or early memory challenges.

## 2. Core Problem Statement
Elderly individuals coping with mild cognitive decline struggle with fragmented daily routines, medication adherence, and feelings of isolation, while caregivers carry immense cognitive burden trying to monitor safety, track adherence, and understand subtle longitudinal trends without clinically overwhelming data.

## 3. Product Vision & Non-Goals
### What CogniCare Is:
- A compassionate, large-touch/voice-friendly daily companion for the elderly.
- A single pane of glass for caregivers to manage care routines, medications, and track objective cognitive performance signals.
- A deterministic, safe AI assistant that grounds every response in structured application data.

### What CogniCare Is NOT:
- Not a clinical diagnostic tool or dementia diagnosis instrument.
- Not an autonomous medical decision maker.
- Not an emergency 911 dispatch replacement.

## 4. Key User Personas
1. **Elderly User ("Margaret", 76)**: Needs very high contrast, large buttons, minimal clutter, speech input/output, clear reminders, enjoyable low-stress cognitive games, and a 1-tap SOS button.
2. **Caregiver ("Sarah", 48, daughter)**: Needs real-time visibility into whether Margaret took her medicine, access to cognitive performance trends over 14-30 days, instant alert notifications, and AI-generated weekly plain-language summaries.
3. **Reviewer / Clinician**: Needs read-only exportable timeline data, activity completion rates, and longitudinal trend charts with confidence intervals.
4. **Platform Admin**: System health, activity catalog management, audit log inspection.

## 5. Success Criteria & KPIs
- Zero-confusion elderly UI (tested with WCAG 2.2 AA accessibility standards).
- 100% reproducible cognitive scoring engine (no hallucinated AI scores).
- Sub-second API response times for interactive activities.
- Full offline capability for daily cognitive routines via PWA IndexedDB caching.
- End-to-end security compliance with OWASP Top 10 guidelines and strict data isolation.
