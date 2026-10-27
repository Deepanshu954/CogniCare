# BENNETT UNIVERSITY
### SCHOOL OF ENGINEERING & APPLIED SCIENCES
#### DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING

---

# CSET400C | CAPSTONE PROJECT REPORT
**Academic Session 2026–27 • Semester VII B.Tech. CSE**  

---

### MILESTONE 1
## PROJECT PROPOSAL, REQUIREMENTS & FEASIBILITY

# **CogniCare**
*An Accessible Routine and Cognitive-Activity Companion for Older Adults*

---

### SUBMITTED BY

| Project Role | Student Name | Enrollment Number |
| :--- | :--- | :--- |
| **Team Leader** | **Deepanshu Chauhan** | `E23CSEU1617` |
| **Team Member** | **Yash** | `E23CSEU1493` |
| **Team Member** | **Piyush** | `E23CSEU0853` |

---

### UNDER THE SUPERVISION & GUIDANCE OF
- **Project Guide / Faculty Mentor:** **Amit Chauhan**  
- **Course Coordinator:** **Dr. Jabir Ali**  

**Greater Noida, Uttar Pradesh | 19 October 2026**

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 2                                                      -->
<!-- ========================================================================= -->

## Declaration of Originality

We declare that this Milestone 1 report for “CogniCare: An Accessible Routine and Cognitive-Activity Companion for Older Adults” has been prepared by our team for CSET400C (Capstone Project) at Bennett University during the 2026–27 academic session. Sources used for background information, standards, and software technologies are acknowledged in the references. The system design and implementation status are described as proposed or completed according to the evidence available at the time of submission; planned work is not represented as tested or deployed work.

Team responsibilities for the proposed project are recorded below. Signatures may be added to the submitted copy as required by the department.

| Student | Proposed responsibility | Signature |
| :--- | :--- | :--- |
| **Deepanshu Chauhan** | System architecture, backend services, AI-provider adapter, integration and report coordination | ________________ |
| **Yash** | Frontend, accessible interaction design, PWA behavior and cognitive activities | ________________ |
| **Piyush** | Database schema, reminder state machine, scoring logic and test design | ________________ |

> **Status note**  
> This is a proposal and feasibility report. Statements about future features, targets, and tests are design commitments to be verified during implementation, not assertions of clinical validation or production readiness.

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 3                                                      -->
<!-- ========================================================================= -->

## Executive Summary

CogniCare is a proposed, low-cost Progressive Web App (PWA) intended to help older adults manage everyday routines while giving consented family caregivers a clearer view of user-reported activity. It brings together four functions: an accessible “My Day” routine view, configurable medication and daily-task reminders, short non-diagnostic cognitive activities, and a caregiver dashboard for missed reminders and longitudinal activity summaries. An optional conversational assistant may provide supportive, plain-language interaction, but it will not diagnose conditions, alter treatment, or make safety-critical state transitions.

The motivation is practical rather than diagnostic. The World Health Organization reports that 57 million people were living with dementia worldwide in 2021 and nearly 10 million new cases occur each year [1]. The WHO also identifies the substantial role of informal care in dementia support [1]. These figures describe a broad public-health context; they do not imply that every older adult has cognitive impairment or that a software companion can replace clinical or family care. CogniCare is designed as an assistive routine tool, not a medical device or clinical assessment system.

The proposed implementation uses a Next.js App Router frontend, TypeScript, an accessible component system, FastAPI for the REST API, and PostgreSQL for transactional persistence. SQLAlchemy and Alembic are proposed for data access and schema migrations. A provider adapter will integrate a currently supported Gemini Live API model after the model identifier and account availability are verified against official documentation [11]. Deterministic code, rather than generative AI, will govern reminder states and calculate activity scores. Offline behavior will be limited to cached routines and selected activities; cloud conversations, remote caregiver notifications, and delivery verification require a network connection.

The immediate milestone is to agree on requirements, architecture, data boundaries, risk controls, and a testable evaluation plan. The next milestone should produce a functional prototype and evidence from automated tests, accessibility checks, and formative usability evaluation. The report deliberately avoids claims of HIPAA/GDPR compliance, guaranteed medication adherence, clinical benefit, universal availability, or 100% test coverage unless such claims are separately substantiated.

**Keywords:** older adults, routine support, medication reminders, accessible PWA, caregiver dashboard, deterministic scoring, responsible AI

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 4                                                      -->
<!-- ========================================================================= -->

## Contents

| Chapter / Section | Page |
| :--- | :---: |
| **Executive Summary** | **3** |
| **1. Introduction and Project Definition** | **5** |
| **2. Related Work and Design Gap** | **6** |
| **3. SDG Alignment and Responsible Design** | **7** |
| **4. Stakeholders and Requirements** | **8** |
| **5. Proposed Architecture and Core Logic** | **10** |
| **6. Feasibility and Risk Management** | **13** |
| **7. Verification and Evaluation Plan** | **15** |
| **8. Project Plan, Roles and Deliverables** | **16** |
| **9. Limitations and Conclusion** | **17** |
| **References** | **18** |

> **How to read this report**  
> The system described here is proposed. Requirements and performance values are target acceptance criteria to test during implementation. The report does not claim that the application is clinically validated or already compliant with any healthcare regulation.

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 5                                                      -->
<!-- ========================================================================= -->

# 1. Introduction and Project Definition

### 1.1 Background and Motivation
Age-related changes in memory, attention, and task sequencing can make complex daily routines harder to manage for some older adults. Mild cognitive impairment (MCI) is a heterogeneous clinical condition and is not equivalent to dementia; diagnosis and care planning belong with qualified professionals [3]. The design problem addressed here is narrower: people may benefit from clearer reminders, simpler interfaces, and an easy way to communicate routine status to trusted supporters.

The WHO estimates that 57 million people were living with dementia globally in 2021, with nearly 10 million new cases each year [1]. It also estimates that informal carers provide an average of five hours of care and supervision per day for people living with dementia [1]. Separately, the WHO has reported that adherence to long-term treatment for chronic diseases averages around 50% in developed countries, while emphasizing that adherence problems vary across conditions and settings [2]. These figures establish a broad motivation; they are not precise estimates of medication adherence among older adults in India and are not used as a forecast of CogniCare’s impact.

Many digital experiences assume confident vision, fine motor control, and familiarity with multi-step navigation. CogniCare therefore proposes large, clearly labelled controls, predictable navigation, optional voice output, simple confirmation flows, and a caregiver view based on consent. The intent is to support autonomy without turning ordinary activity data into a clinical judgement.

### 1.2 Problem Statement

> **Problem statement**  
> Older adults who find complex daily routines difficult may need accessible reminders and low-friction ways to record task status. Family caregivers who live separately may lack a reliable, consent-based view of those self-reported events. Existing tools in separate categories may address only parts of this workflow. CogniCare proposes to integrate routine support, accessible activities, and caregiver visibility in one web-based system while preserving user choice and clearly stating the limits of monitoring.

### 1.3 Aim
To design and evaluate a secure, accessible PWA that supports daily routine management for older adults and provides consented caregivers with transparent, user-reported routine information.

### 1.4 Objectives
- • Provide a senior-facing “My Day” screen with readable labels, predictable navigation, adjustable text scale, and optional voice guidance.
- • Represent medication and non-medication reminders with a deterministic state machine and auditable timestamps.
- • Provide simple cognitive activities for engagement and practice, with repeatable scoring that is explicitly non-diagnostic.
- • Allow a user to pair with a caregiver through expiring invitations and granular, revocable permissions.
- • Offer caregivers a dashboard showing reminder states, declared acknowledgements, and descriptive activity trends without claiming clinical interpretation.
- • Add a bounded conversational assistant with explicit safety rules and a predictable offline fallback.
- • Validate the prototype using automated tests, accessibility review, security checks, offline scenarios, and formative usability evaluation.

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 6                                                      -->
<!-- ========================================================================= -->

### 1.5 Scope and Boundaries

| In scope for the prototype | Out of scope for this capstone prototype |
| :--- | :--- |
| Accounts, role-based access, consented caregiver pairing | Clinical diagnosis, prognosis, or cognitive-disorder screening |
| Routine configuration, reminder states, self-reported acknowledgement | Verification that a person physically swallowed a medicine |
| Small cognitive-activity catalogue and deterministic score calculation | Prescription recommendations, dosage changes, or treatment decisions |
| Caregiver dashboard, missed-reminder alerts and audit events | Guaranteed emergency-service dispatch or guaranteed alert delivery |
| Selected offline access to cached routines and activities | Full offline AI conversation or reliable remote alerting without connectivity |
| Supportive conversational interaction with safety constraints | Claims of clinical effectiveness or regulatory certification |

# 2. Related Work and Design Gap

### 2.1 Review of Solution Categories
This report uses a preliminary category-level comparison to clarify the proposed design. It is not a systematic literature review or a controlled product benchmark. Commercial features, accessibility, device compatibility, and pricing vary by region and subscription plan; these details must be verified from current first-party sources before a final comparative claim is made.

| Solution category | Potential value | Design opportunity for CogniCare |
| :--- | :--- | :--- |
| **Cognitive-training applications** | Offer structured games and repeated practice; may help users engage with short activities. | Use calm, untimed-by-default activities; avoid punitive feedback; keep results descriptive and non-diagnostic. |
| **Medication and routine reminder applications** | Offer scheduled prompts, confirmation flows, and medication lists. | Prioritize large controls, low-step acknowledgement, caregiver consent, and visible reminder state history. |
| **Voice assistants and companion devices** | Can provide conversational access, prompts, and social interaction. | Offer an affordable browser-based option with an explicit mute control and a clear boundary between conversation and safety logic. |
| **Caregiver monitoring tools** | Can help a caregiver receive updates or manage care-related tasks. | Use granular consent and show what is reported, when it was reported, and what remains unknown. |

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 7                                                      -->
<!-- ========================================================================= -->

### 2.2 Design Gap
The proposed contribution is an integrated workflow rather than a claim that no comparable product exists. CogniCare aims to combine accessible routine management, user-reported reminder history, simple cognitive activities, caregiver visibility, and a safety-constrained conversational interface in one open-web implementation. The integration hypothesis should be assessed through a product-specific comparison and user evaluation during later milestones.

### 2.3 Design Principles Derived from the Review
- • **Make the next action obvious:** show a small number of primary choices and use direct language.
- • **Keep care events deterministic:** reminders, acknowledgements, missed states, and alert records must not depend on AI output.
- • **Treat caregiver access as a permissioned relationship,** not an automatic entitlement.
- • **Separate engagement scores from clinical conclusions;** show context and uncertainty.
- • **Design for poor connectivity** and make limitations visible instead of implying that every feature remains available offline.

# 3. SDG Alignment and Responsible Design

### 3.1 Sustainable Development Goal 3: Good Health and Well-Being
SDG 3 seeks to ensure healthy lives and promote well-being for people of all ages [4], [5]. CogniCare aligns with this goal at the level of design intent by supporting routine organization, accessible engagement, and communication between an older adult and a chosen caregiver. The project cannot claim reduced mortality, improved clinical outcomes, or a medication-adherence rate before a suitable evaluation has been conducted.

### 3.2 Sustainable Development Goal 10: Reduced Inequalities
SDG Target 10.2 calls for promoting social, economic, and political inclusion regardless of age, disability, or other status [4], [6]. CogniCare contributes to this aim by prioritizing accessibility and avoiding proprietary hardware as a prerequisite. A browser-based application does not by itself eliminate affordability, device, language, connectivity, or digital-literacy barriers; these must be considered in design and evaluation.

### 3.3 Accessibility Approach
The target is WCAG 2.2 Level AA, supported by automated checks and manual testing with keyboard and screen-reader workflows [7]. For normal text, WCAG AA generally requires a contrast ratio of at least 4.5:1; large text generally requires 3:1. The enhanced 7:1 ratio is an AAA criterion for normal text, so 7:1 is retained as a preferred design target where practical, not incorrectly presented as the AA minimum [7].
- • Use plain-language labels, a consistent page structure, visible focus states, and semantic form labels.
- • Adopt 76-by-76 CSS-pixel primary controls as a proposed senior-friendly design target, not as a WCAG requirement; ensure the layout remains usable on smaller screens.
- • Allow text scaling up to 200% without loss of content or functionality.
- • Do not rely on color, sound, animation, or time limits alone to convey important information.
- • Provide optional voice output with an always-visible stop or mute control; voice output should default to off unless the user enables it.

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 8                                                      -->
<!-- ========================================================================= -->

### 3.4 Privacy, Consent, and Security Principles
The prototype should follow privacy-by-design principles: collect only the data needed for the stated feature, explain the purpose in plain language, grant caregiver access only after explicit pairing, support permission revocation, protect sessions, and define retention and deletion behavior before collecting real users’ data. The design should be reviewed against applicable Indian data-protection requirements, including the Digital Personal Data Protection Act, 2023 and notified Rules, with their provisions and commencement timelines checked at implementation time [12].

The report does not claim HIPAA or GDPR compliance. Applicability depends on jurisdiction, organizational role, data flows, service providers, and operational controls; compliance requires more than authentication or audit logging. Student testing should use synthetic data unless faculty approval, informed consent, and appropriate safeguards are in place for any study involving people or health-related information.

### 3.5 AI Safety Policy
- • **Non-diagnostic use:** the assistant may help with general conversation and app navigation but must not diagnose, prognose, recommend prescription changes, or override professional advice.
- • **Deterministic control:** AI output must never create or modify reminder states, caregiver permissions, SOS state, or numeric activity scores.
- • **Constrained fallback:** if the provider is unavailable, use a small set of tested, pre-approved local messages; do not simulate a live model or fabricate personal context.
- • **Transparency:** identify AI-generated interaction where appropriate and give the user a simple way to stop the conversation.
- • **Data minimization:** do not send medication details, identifiers, or activity histories to the AI provider unless the feature requires it, consent and security review allow it, and the request is minimized.

# 4. Stakeholders and Requirements

### 4.1 Stakeholder Personas
The following personas are illustrative design aids, not real participants or clinical profiles.

| Persona | Context | Primary needs |
| :--- | :--- | :--- |
| **Margaret — older adult** | Illustrative 76-year-old living independently; may have low vision or reduced dexterity and sometimes forgets routine tasks. | One clear “My Day” view, large controls, calm prompts, opt-in voice, easy correction and a visible SOS option. |
| **Sarah — family caregiver** | Illustrative adult daughter who lives separately and wants to support her parent without constant check-ins. | Consented access, missed-reminder notifications, trustworthy timestamps, understandable trends and revocable permissions. |
| **Clinician / administrator** | Secondary stakeholder; not the primary operator of the prototype. | Clear statement that outputs are not clinical measurements, role separation, and traceable access logs. |

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 9                                                      -->
<!-- ========================================================================= -->

### 4.2 Functional Requirements

| ID / requirement | Description | Acceptance criterion |
| :--- | :--- | :--- |
| **FR-01 Identity and roles** | Users can sign in and access only the screens and records permitted by their role. | Unauthorized cross-user access tests fail closed. |
| **FR-02 Caregiver pairing and consent** | A user can create or accept a time-limited invitation, choose a permission tier, and revoke access. | Expired/revoked invitations cannot create or retain access. |
| **FR-03 Routine configuration** | Authorized users can define reminder name, schedule, time zone, instructions, and urgency. | A saved routine persists and is rendered consistently in the senior view. |
| **FR-04 Reminder lifecycle** | The system manages SCHEDULED, TRIGGERED, SNOOZED, ACKNOWLEDGED, and MISSED states. | Every defined transition has a unit test and an audit event. |
| **FR-05 Self-reported acknowledgement** | The user can record that a reminder was acknowledged or snoozed. | Interface labels this as user-reported status, not proof of ingestion. |
| **FR-06 Cognitive activities** | The prototype includes memory, sequence, and attention activities with adjustable difficulty. | Activities are keyboard-operable, have clear instructions, and can be exited. |
| **FR-07 Deterministic scoring** | Scoring is computed in application code from accuracy and normalized response time. | Identical valid inputs always return the same score. |
| **FR-08 Caregiver dashboard** | Permitted caregivers can view routine history, missed events, and descriptive activity trends. | Dashboard displays time range, event status, and limitations of the data. |
| **FR-09 Conversational assistant** | Users can request supportive conversation or simple app guidance through a provider adapter. | Safety tests reject diagnostic, prescription, and treatment-change requests. |
| **FR-10 SOS interaction** | The user can trigger an emergency-contact alert workflow for linked caregivers. | The system records attempt/delivery status where available and states if offline. |
| **FR-11 PWA/offline behavior** | Cached core routine information and selected activities can open without connectivity. | Offline status is visible; queued events synchronize idempotently when reconnected. |
| **FR-12 Audit and user controls** | Security-sensitive events, permission changes, and reminder transitions are recorded; data export/deletion rules are defined. | Logs avoid unnecessary sensitive content and access is role-restricted. |

### 4.3 Non-Functional Requirements

| ID | Requirement / target |
| :--- | :--- |
| **NFR-01 Accessibility** | Target WCAG 2.2 AA; use 76-by-76 CSS-pixel primary targets as the product design target; support visible focus, screen readers, and 200% text resize. |

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 10                                                     -->
<!-- ========================================================================= -->

| ID | Requirement / target |
| :--- | :--- |
| **NFR-02 Performance** | Target p95 under 500 ms for non-AI API requests in a documented local/staging test profile. AI provider time is measured separately. |
| **NFR-03 Local fallback** | Target under 100 ms for a template/rule-based fallback response on the test environment; fallback scope must remain deliberately limited. |
| **NFR-04 Reliability** | Reminder transitions and event writes are idempotent; critical events use explicit deadlines, retries, and recorded delivery attempts. |
| **NFR-05 Security and privacy** | HTTPS in deployment, secure session cookies, input validation, least privilege, rate limiting, consent revocation, retention policy, and security tests. |
| **NFR-06 Offline behavior** | Core cached screens and selected activities remain usable offline; cloud AI, remote alerts, and live synchronization clearly require connectivity. |
| **NFR-07 Maintainability** | Versioned database migrations, documented API schemas, modular service boundaries, automated tests, and reproducible container setup. |
| **NFR-08 Observability** | Record operational errors and state transitions with timestamps and correlation identifiers, while excluding secrets and unnecessary personal data. |

### 4.4 Requirement Prioritization
For Milestone 2, prioritize the end-to-end path for one senior and one consented caregiver: sign-in, caregiver pairing, routine creation, reminder state transition, acknowledgement, missed-event alert, and dashboard display. Add cognitive activities and deterministic scoring next. Conversational AI and advanced trend visualization should not delay safe completion of the core routine workflow.

# 5. Proposed Architecture and Core Logic

### 5.1 Architecture Choice
CogniCare is proposed as a modular monolith with explicit internal boundaries. This is appropriate for a small capstone team because it reduces operational complexity while allowing modules to be tested independently. A modular monolith does not remove the need for transaction design, locking, idempotency, or failure handling; these are defined at the service and database boundary. PostgreSQL transactions will be used for atomic multi-step writes where required [9].

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 11                                                     -->
<!-- ========================================================================= -->

```
                             Proposed CogniCare Architecture

                              ┌─────────────────────────────┐
                              │     PRESENTATION LAYER      │
                              │ Senior PWA: My Day, games   │
                              │ Caregiver dashboard, trends │
                              │ Next.js App Router • TS     │
                              └──────────────┬──────────────┘
                                             │ HTTPS / JSON
                                             ▼
                              ┌─────────────────────────────┐
                              │     API & ROUTING LAYER     │
                              │ FastAPI • REST /api/v1      │
                              │ Pydantic • Auth & Limits    │
                              └──────────────┬──────────────┘
                                             │ validated requests
                                             ▼
                              ┌─────────────────────────────┐
                              │ DOMAIN/APPLICATION SERVICES │
                              │ Routine & Reminder States   │
                              │ Consent • Deterministic Math│
                              │ Alerts • AI Orchestration   │
                              └───────┬──────────────▲──────┘
             transactions / adapters  │              │  results / provider status
                                      ▼              │
         ┌───────────────────────────────┐   ┌───────────────────────────────┐
         │  DATA & INTEGRATION BOUNDARY  │   │        SAFETY BOUNDARY        │
         │ PostgreSQL • SQLAlchemy • Alem│   │ AI does not decide medication │
         │ Notification & Gemini Adapters│   │ states, scores, or diagnosis. │
         │ Rule-based local fallback     │   │ Local fallback only bounded.  │
         └───────────────────────────────┘   └───────────────────────────────┘
```
*Figure 1. Proposed four-layer architecture and safety boundary. External AI and notification providers are accessed through adapters; deterministic care logic remains internal.*

### 5.2 Technology Responsibilities

| Component | Responsibility | Implementation note |
| :--- | :--- | :--- |
| **Next.js App Router + TypeScript** | Senior PWA, caregiver dashboard, accessible components, and navigation. | Pin a supported version at implementation start; official documentation describes the App Router model [8]. |
| **FastAPI + Pydantic** | REST API, request validation, authentication/authorization dependencies, and OpenAPI documentation. | Keep route handlers thin; put business rules in domain/application services [10]. |
| **PostgreSQL** | Persistent users, consent links, routines, reminder instances, activity results, alert events, and audit metadata. | Use transactions for related state changes; add foreign keys, indexes, and constraints. |
| **SQLAlchemy + Alembic** | Database mapping and versioned migrations. | Migrations must be reviewable and repeatable; do not change production schema manually. |
| **PWA service worker + IndexedDB** | Cache approved static assets and selected routine/activity data; queue limited offline events. | Do not imply that IndexedDB content is inherently secure; minimize data stored locally. |
| **Gemini Live API adapter** | Optional conversational interaction; provider/model identifiers are configured and verified at implementation time. | Use the current official model catalog [11]; do not hard-code a retired identifier. |
| **Local fallback module** | Return only tested, pre-approved prompts or basic app guidance when cloud service is unavailable. | No open-ended local reasoning is assumed; AI is not required for reminders or scoring. |

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 12                                                     -->
<!-- ========================================================================= -->

### 5.3 Principal Data Entities
The first relational schema should keep identity, care relationships, operational events, and optional conversation metadata separate. Proposed entities are:
- • **User:** identity, role, authentication metadata, preferences, and account status.
- • **CareRelationship and ConsentGrant:** pairing status, permission tier, invitation expiry, consent time, and revocation time.
- • **Routine and ReminderInstance:** schedule definition, time zone, due time, current state, deadline, and event history.
- • **ActivitySession and ActivityResponse:** activity version, difficulty, response data needed for scoring, score version, and completion time.
- • **CaregiverAlert:** alert type, target, attempt status, delivery result if available, and relevant event identifier.
- • **AuditEvent:** actor, action, affected record identifier, timestamp, and outcome; omit unnecessary secrets and message content.
- • **AIConversationMetadata:** provider/model version, interaction time, safety outcome, and minimal operational metadata. Avoid storing full transcripts by default unless a justified, consented need is established.

### 5.4 Reminder State Machine
Reminder processing must be predictable and auditable. A scheduled reminder transitions to TRIGGERED at its due time. The senior can acknowledge it or snooze it. If the configured deadline expires without acknowledgement, the reminder becomes MISSED and may create a caregiver alert according to the routine urgency and consented alert policy.

```
                      [SNOOZED]
                     ▲         │
              snooze │         │ snooze ends
                     │         ▼
[SCHEDULED] ─────────► [TRIGGERED] ─────────► [ACKNOWLEDGED (user-reported)]
  due time                  │      confirm
                            │ deadline expires
                            ▼
                         [MISSED] ──────────► [CAREGIVER ALERT (delivery status logged)]
                                   critical policy
```
*Figure 2. Proposed reminder state machine. “Acknowledged” means the user reported a status; it does not independently verify medication ingestion.*

**Implementation rules:** (1) store timestamps in a consistent server-side format and render them in the user’s time zone; (2) make event processing idempotent so retries do not create duplicate acknowledgements or alerts; (3) define what happens when a snooze would cross the final deadline; (4) record alert attempts and delivery feedback where the provider exposes it; and (5) display network or delivery uncertainty clearly. Emergency alerts must never depend on a generative AI decision.

### 5.5 Deterministic Activity Scoring
Activity scores are intended as descriptive engagement summaries, not clinical metrics. The score should remain within 0–100, be reproducible for identical inputs, and be versioned so later formula changes do not silently rewrite prior results.

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 13                                                     -->
<!-- ========================================================================= -->

> **Proposed baseline formula**  
> $$\text{Score} = \text{round}(100 \times (0.60 \times A + 0.40 \times L))$$  
> **A** = correct valid responses / total valid responses.  
> For each valid response $i$, $L_i = \text{clamp}(T_{\text{target}} / \max(T_i, \varepsilon), 0.20, 1.00)$; $L$ is the mean of $L_i$ across the session.  
> $T_{\text{target}}$ is an activity-specific reference time, $T_i$ is the observed response time, and $\varepsilon$ prevents division by zero. If no valid responses exist, the session is unscored rather than assigned zero.

Difficulty is stored as context and used to compare sessions of similar activity and difficulty; it is not multiplied into the score. That avoids the previous design problem in which a difficulty multiplier could produce scores above 100. The response-time target must be tested for each activity and can be adjusted to reduce unnecessary time pressure. Trend views should preferably compare a person with their own prior sessions of comparable activity; no clinical threshold, diagnosis, or population ranking will be displayed.

### 5.6 AI Orchestration and Fallback
The conversational assistant should be accessed through a provider interface so model versions can change without changing care logic. The preferred voice model and endpoint must be selected from the provider’s current documentation at implementation time [11]. The assistant can use a short system policy, minimal context, output limits, and safety filters. It must not schedule medication, determine that an event is missed, interpret activity scores as a diagnosis, or invent whether an alert reached a caregiver.

On timeout, quota exhaustion, or loss of connectivity, the fallback should provide one of a small number of tested messages such as “I can still show your saved routine, but conversation is unavailable right now.” If the application is offline, the interface should clearly distinguish a locally saved event from an event successfully synchronized to the server. The local fallback is a graceful degradation mechanism, not a claim of full offline AI functionality or 100% availability.

# 6. Feasibility and Risk Management

### 6.1 Feasibility Assessment

| Dimension | Assessment | Condition / evidence needed |
| :--- | :--- | :--- |
| **Technical** | Feasible for a student team using mainstream web, API, and relational database technologies. | Validate the complete flow in Docker Compose, including scheduled jobs, timezone handling, migrations, and notification failures. |
| **Economic** | A software-first PWA avoids requiring dedicated companion hardware. | Estimate hosting, database, notification, and AI-provider costs from actual traffic and usage; no fixed cost is promised in this report. |
| **Operational** | The core workflow can be designed around a few primary actions and a caregiver view. | Usability must be assessed with representative users; “zero training required” is not assumed. |
| **Ethical / legal** | Consent, role separation, minimal collection, and non-diagnostic limits are design requirements. | Review applicable Indian data-protection requirements, accessibility, consent materials, retention, and any research-ethics needs before user testing. |

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 14                                                     -->
<!-- ========================================================================= -->

### 6.2 Risk Register

| Risk | Impact | Likelihood | Mitigation |
| :--- | :---: | :---: | :--- |
| **Missed/duplicate reminders** | **High** | Medium | Use deterministic transitions, idempotency keys, scheduler monitoring, deadline tests, and event logs. |
| **AI gives medical or misleading advice** | **High** | Medium | Constrain scope, block diagnosis/dosage changes, minimize sent context, test adversarial prompts, and provide safe escalation language. |
| **Caregiver gets access without valid consent** | **High** | Low–Medium | Expiring invitation tokens, explicit permission selection, server-side authorization on every request, and revocation tests. |
| **Network outage hides alert delivery status** | **High** | Medium | Distinguish queued/sent/delivered/unknown where supported; show offline state and never promise remote delivery without confirmation. |
| **Scores are interpreted as diagnosis** | **High** | Medium | Label results non-diagnostic, avoid clinical thresholds, contextualize trends, and prohibit AI-generated score interpretation as medical judgement. |
| **Accessibility needs are missed** | Medium–High | Medium | Use WCAG 2.2 AA review, keyboard/screen-reader testing, text scaling, and formative usability tests. |
| **Personal data exposure** | **High** | Medium | Minimize retention, secure sessions, validate authorization, avoid secrets in logs, define deletion, and test data isolation. |
| **AI provider quota/model changes** | Medium | Medium | Provider adapter, configurable model ID, quota/error handling, versioned tests, and rule-based fallback. |
| **Offline synchronization conflict** | Medium | Medium | Record event IDs/timestamps, use idempotent synchronization, define conflict rules, and display unsynchronized changes. |
| **Project scope exceeds timeline** | Medium | **High** | Deliver the core routine lifecycle first; make advanced trends and extended conversation optional after the safety-critical path works. |

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 15                                                     -->
<!-- ========================================================================= -->

### 6.3 Assumptions and Dependencies
- • The prototype will use synthetic or explicitly approved test data, not real patient records by default.
- • Caregiver alert delivery depends on the configured notification channel and network connectivity; delivery guarantees are not assumed.
- • Voice features depend on browser/device support and user permission; text interaction remains available as an alternative.
- • Cloud AI model availability, latency, quotas, and pricing may change and must be checked near deployment.
- • The capstone will not claim a regulated medical-device status, clinical validation, or legal certification.

# 7. Verification and Evaluation Plan

Quality will be demonstrated by test evidence and documented acceptance criteria, not by an unsupported blanket statement that the system has “100% automated testing” or “100% coverage.” Each test result should name the code revision, environment, number of tests, failures, and coverage method where relevant.

| Test area | Planned checks | Acceptance evidence |
| :--- | :--- | :--- |
| **Unit tests** | Reminder transition table, scheduling/time-zone rules, scoring formula, consent/token expiry, and authorization policy. | All defined state/edge cases have expected results; same inputs yield same scores. |
| **API integration** | Create routine, trigger reminder, acknowledge/snooze, expire into MISSED, generate alert, and retrieve caregiver view. | End-to-end API tests pass; transactions remain consistent under retries. |
| **Security and privacy** | Cross-user IDOR checks, role bypass, expired/revoked invitation, session handling, rate limits, validation, and log inspection. | Negative authorization tests fail closed; no secrets or unnecessary sensitive content appears in logs. |
| **Accessibility** | Automated WCAG checks plus keyboard-only, focus, text resize, contrast, screen-reader labels, error recovery, and target-size review. | Findings are recorded and high-impact blockers are fixed before user evaluation. |
| **Performance** | Measure non-AI endpoint latency and local fallback latency under a documented test setup. | Report p50/p95 and environment; assess the 500 ms / 100 ms targets separately. |
| **Offline and synchronization** | Open cached routines, complete a supported activity, queue a permitted event, reconnect, and retry synchronization. | No duplicate event is created; unsynchronized status and conflicts are visible. |
| **AI safety and provider failure** | Test diagnosis/dosage requests, hallucination prompts, timeouts, quota errors, provider/model change, and fallback messaging. | Safety cases return safe constrained behavior; failure paths remain understandable to users. |
| **Usability** | Formative task-based evaluation of routine setup, acknowledgement, caregiver pairing, and understanding of status labels. | Document task completion, observed friction, feedback, and resulting design changes. |

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 16                                                     -->
<!-- ========================================================================= -->

### 7.1 Evaluation Safeguards
Usability testing involving older adults should proceed only after faculty approval, informed consent, accessible study materials, and a clear process for stopping participation. Do not ask participants to rely on CogniCare for actual medication safety, emergency response, or clinical decisions. Early evaluation should focus on comprehension, navigation, accessibility, and task flow using a non-clinical scenario.

### 7.2 Metrics to Report
- • **Reminder correctness:** expected versus actual state transitions across scheduled, snoozed, acknowledged, and missed scenarios.
- • **Authorization correctness:** successful and rejected access attempts across roles and consent states.
- • **Latency:** p50 and p95 for non-AI endpoints and local fallback responses, with environment stated.
- • **Accessibility:** issues found, severity, remediation status, and manual checks completed against WCAG 2.2 AA.
- • **Usability:** task completion, observed errors, time on task where appropriate, and qualitative feedback.
- • **AI safety:** pass/fail outcomes for a predefined policy test set and behavior under provider errors.
- • **Offline reliability:** synchronization success, duplicate-event rate, and visibility of pending events after reconnect.

# 8. Project Plan, Roles and Deliverables

### 8.1 Milestone Schedule

| Milestone | Target period | Planned scope / output | Status for this report |
| :--- | :--- | :--- | :--- |
| **Milestone 0** | August 2026 | Problem selection, initial team charter, background exploration, and project scope. | Reported as completed by the team; supporting artefacts should be retained. |
| **Milestone 1** | October 2026 | Proposal, requirements, feasibility, risk register, architecture, and presentation. | Current milestone; this document defines the proposal baseline. |
| **Milestone 2** | November 2026 | Functional prototype of core routine workflow, caregiver pairing, activity catalogue, AI adapter, and initial test evidence. | Planned; do not claim complete until evidence exists. |
| **Final evaluation** | December 2026 | Integrated demonstration, final report, evaluation findings, code and deployment documentation, technical viva. | Planned. |

### 8.2 Work Breakdown Structure

| Team member | Primary ownership | Shared responsibilities |
| :--- | :--- | :--- |
| **Deepanshu Chauhan — Team Leader** | API/domain architecture, backend integration, AI provider adapter, container setup, and report coordination. | Integration planning, safety policy, end-to-end testing, final demo. |

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 17                                                     -->
<!-- ========================================================================= -->

| Team member | Primary ownership | Shared responsibilities |
| :--- | :--- | :--- |
| **Yash — Frontend** | Senior/caregiver interfaces, responsive layout, accessible controls, PWA interaction, and cognitive activity UI. | Manual accessibility checks, usability feedback, frontend test suite. |
| **Piyush — Data and verification** | Relational schema, ORM/migrations, reminder state machine, scoring implementation, and backend test design. | Requirement traceability, risk-based tests, consistency checks. |

### 8.3 Expected Deliverables
- • Runnable full-stack prototype with documented environment configuration and reproducible startup instructions.
- • Senior-facing routine view and caregiver dashboard with consented pairing and role-separated access.
- • Deterministic reminder lifecycle, event history, and configurable caregiver-alert policy.
- • Non-diagnostic activity catalogue with versioned scoring implementation and descriptive trend view.
- • Optional conversational assistant behind a provider adapter and bounded local fallback.
- • Automated test report, accessibility findings, security test checklist, and basic performance measurements.
- • Architecture diagram, data model, API documentation, user guide, final report, and presentation deck.

### 8.4 Definition of Done for Milestone 2
The prototype is ready for review when the core routine lifecycle can be demonstrated end to end; consent and authorization controls pass negative tests; the reminder state machine and scoring are covered by explicit tests; offline behavior is correctly labelled; major accessibility blockers are resolved; and the team can reproduce the demo from the documented setup. Any incomplete feature or known defect should be listed openly.

# 9. Limitations and Conclusion

### 9.1 Limitations
- • Routine acknowledgement is self-reported and does not verify medicine ingestion or other real-world actions.
- • Cognitive activity results can be influenced by device, language, fatigue, sensory needs, task difficulty, and familiarity; they are not clinical assessments.
- • Caregiver dashboards depend on consent, network access, and accurate recording; absence of data should not be interpreted as proof that an event did not occur.
- • Offline access is intentionally limited. Real-time caregiver alerting and cloud AI interactions cannot be guaranteed without connectivity.
- • A student prototype cannot establish clinical efficacy, regulatory compliance, or a broad market research gap without further evidence.

---

<!-- ========================================================================= -->
<!-- PAGE BREAK -> PAGE 18                                                     -->
<!-- ========================================================================= -->

### 9.2 Conclusion
CogniCare is framed as an accessible routine-support system that connects a senior-facing interface with consent-based caregiver visibility. Its strongest technical principle is separation of concerns: the application’s routine and scoring logic remains deterministic, while AI is limited to optional conversation. The design is feasible as a modular web application, but its success will depend on reliable reminder behavior, meaningful consent, accessible interaction, clear offline limitations, and evidence from testing. The next milestone should focus on a small end-to-end workflow and prove it with tests before expanding the feature set.

# References

- [1] World Health Organization, “Dementia,” Fact sheet, 3 July 2026. [Online]. Available: https://www.who.int/en/news-room/fact-sheets/detail/dementia/. Accessed: 19 Oct. 2026.
- [2] World Health Organization, *Adherence to Long-Term Therapies: Evidence for Action*. Geneva, Switzerland: WHO, 2003. [Online]. Available: https://www.who.int/publications/i/item/9241545992.
- [3] R. C. Petersen et al., “Practice guideline update summary: Mild cognitive impairment,” *Neurology*, vol. 90, no. 3, pp. 126–135, 2018, doi: 10.1212/WNL.0000000000004826.
- [4] United Nations General Assembly, “Transforming our world: the 2030 Agenda for Sustainable Development,” A/RES/70/1, 2015. [Online]. Available: https://sdgs.un.org/2030agenda.
- [5] United Nations, “Goal 3: Ensure healthy lives and promote well-being for all at all ages.” [Online]. Available: https://sdgs.un.org/goals/goal3. Accessed: 19 Oct. 2026.
- [6] United Nations, “Goal 10: Reduce inequality within and among countries.” [Online]. Available: https://sdgs.un.org/goals/goal10. Accessed: 19 Oct. 2026.
- [7] World Wide Web Consortium (W3C), “Web Content Accessibility Guidelines (WCAG) 2.2,” W3C Recommendation, 5 Oct. 2023. [Online]. Available: https://www.w3.org/TR/WCAG22/.
- [8] Vercel, “Next.js Documentation: App Router.” [Online]. Available: https://nextjs.org/docs/app. Accessed: 19 Oct. 2026.
- [9] PostgreSQL Global Development Group, “Transaction Processing,” *PostgreSQL Documentation*. [Online]. Available: https://www.postgresql.org/docs/current/transactions.html. Accessed: 19 Oct. 2026.
- [10] FastAPI, “FastAPI Documentation.” [Online]. Available: https://fastapi.tiangolo.com/. Accessed: 19 Oct. 2026.
- [11] Google, “Gemini API Models,” *Google AI for Developers*. [Online]. Available: https://ai.google.dev/gemini-api/docs/models. Accessed: 19 Oct. 2026.
- [12] Government of India, “The Digital Personal Data Protection Act, 2023,” Act No. 22 of 2023; Ministry of Electronics and Information Technology, “Digital Personal Data Protection Rules, 2025,” notified 14 Nov. 2025. [Online]. Available: https://www.indiacode.nic.in/indiacode/handle/123456789/22037?view_type=browse and https://www.meity.gov.in/documents/act-and-policies. Accessed: 19 Oct. 2026.
