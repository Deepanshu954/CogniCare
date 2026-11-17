# CogniCare: Live Project Demonstration Script
**Course:** CSET400C – Capstone Project | **Bennett University**  
**Estimated Demo Time:** 10–12 Minutes | **Panel Target:** 30 Marks

---

## 🛠️ Step 0: Pre-Flight Environment Setup

Open two terminal windows or boot the verified Docker Compose stack:

```bash
# Option A: Multi-Container Docker Stack
docker compose up -d

# Verify healthy containers:
docker compose ps
```

*Open Browser Tabs:*
1. Tab 1: **Frontend**: `http://localhost:3000`
2. Tab 2: **Backend Swagger API**: `http://localhost:8000/docs`
3. Tab 3: **Caregiver Portal**: `http://localhost:3000/caregiver/dashboard`

---

## 🎭 Step 1: Senior Persona Walkthrough (Margaret Smith)

### 1.1 One-Click Elderly Authentication
1. Navigate to `http://localhost:3000/login`.
2. Point out the **Accessible 1-Click Demo Buttons** designed for senior accessibility.
3. Click: **"Login as Margaret (Elderly)"**.
4. The system issues a JWT token and automatically routes Margaret to her personalized `/app/my-day` portal.

### 1.2 "My Day" Dashboard & Cognitive-Load-Reducing Hero Card
1. Direct the evaluators' attention to the **Oversized Greeting & Digital Clock**:
   - High-contrast, reassuring greeting with date and time.
2. Demonstrate the **Display Scale Switcher** in the top navigation bar:
   - Click **"XL Senior"** mode. Observe all text, cards, and buttons scale smoothly for low-vision seniors.
3. Demonstrate the **"Next Up" Hero Action Card**:
   - The card isolates Margaret's most immediate care item: *"Take Evening Donepezil (10mg)"*.
   - Point out that isolating the single next task eliminates anxiety and decision paralysis.
4. **Log Adherence**:
   - Click the massive 72px green button: **"I did this!"**.
   - The card transitions to a muted completed state with a prominent checkmark.
   - *Technical Note for Evaluators*: This action triggered a `POST /api/v1/patients/{id}/reminders/{id}/acknowledge` API call, updating the database state machine and recording an immutable `AuditLog` entry.

---

## 🧠 Step 2: Interactive Cognitive Activity Session

1. Navigate to **"Brain Games"** (`/app/activities`).
2. Show the catalog of 4 standardized neuropsychological games:
   - *Visual Memory Recall* (Home & Hearth Items)
   - *Number Sequence Recall* (Working Memory)
   - *Color Stroop Test* (Inhibitory Attention & Speed)
   - *Spatial Clock Match* (Orientation)
3. Click **"Play Visual Memory"**.
4. **Study Phase**:
   - A 5-second countdown prompts Margaret to study two vintage household items (*"Vintage Teapot"*, *"Golden Sunflower"*).
5. **Recall Phase**:
   - Margaret is prompted: *"Which item was in your study collection?"*.
   - Select *"Vintage Teapot"*.
   - Point out the instant auditory and visual celebratory modal.
6. **Scoring Explanation**:
   - Explain to the panel: *"The backend captured the 1,240 ms response time and trial accuracy, calculating a composite session score of 94/100 using our mathematical 4-factor formula."*

---

## 🎙️ Step 3: Conversational Voice Companion & Safety Guardrails

1. Navigate to **"Assistant"** (`/app/assistant`).
2. Demonstrate the **Voice Microphone Interface**:
   - Click the pulsing microphone (or click the quick preset prompt: *"What's my schedule for today?"*).
3. **Context Grounding in Action**:
   - The assistant calls the tool `get_today_tasks` and replies:
     > *"Good evening, Margaret! You've already taken your evening Donepezil. Next, remember to drink a glass of water before bed at 9:00 PM."*
4. **Demonstrating Medical Guardrails**:
   - Click or speak: *"Do I have Alzheimer's disease?"* or *"Should I double my dosage?"*.
   - Point out the immediate safety intercept:
     > *"I cannot give medical advice or alter prescriptions. Please consult Dr. Elena Vance or your caregiver."*
   - Highlight that the model has zero write access to medical schedules.

---

## 🚨 Step 4: Emergency SOS & False-Alarm Prevention

1. Navigate to **"Call for Help"** (`/app/safety`).
2. Point out the prominent crimson **"PRESS FOR HELP"** emergency trigger.
3. Click the button.
4. An interactive **5-Second Countdown Modal** appears with a prominent **"Cancel (False Alarm)"** button.
5. Click **"Cancel"**:
   - Explain that formative usability trials revealed seniors fear accidental calls; the 5-second cancel buffer provides complete peace of mind.
6. Click the button again and click **"Send Now"**:
   - An urgent `CRITICAL` alert is dispatched instantly to linked caregivers.

---

## 📊 Step 5: Caregiver Command Tower (Sarah Smith)

1. Open the Caregiver Dashboard at `http://localhost:3000/caregiver/dashboard`.
2. Point out the **Live Adherence Radial Gauge**:
   - Shows Margaret's real-time daily adherence percentage (e.g., $100\%$).
3. Point out the **30-Day Cognitive Trajectory Curve**:
   - Interactive Recharts SVG curve plotting Margaret's session scores against her baseline ($\mu \pm 1.5\sigma$).
   - Filter by domain (*Memory*, *Attention*, *Speed*).
4. Direct attention to the **Urgent Alerts Feed**:
   - The SOS alert triggered in Step 4 is visible with a crimson badge.
   - Click **"Acknowledge"** $\rightarrow$ Status changes to `ACKNOWLEDGED`.
   - Click **"Resolve"** $\rightarrow$ A modal requires clinical notes (*"Called Margaret, verified she is safe."*) before resolving.
5. Navigate to **"Weekly Reports"** (`/caregiver/reports`):
   - Click **"Generate Weekly Report"**.
   - Show the side-by-side display of code-calculated objective metrics (Adherence %, average latency, session counts) and the plain-language AI narrative summary.

### 5.2 Medical Documents & Prescription Drag-and-Drop Ingestion
1. Scroll down to the **"Medical Documents & Prescriptions"** section on the Caregiver Dashboard.
2. Demonstrate the **Drag-and-Drop Upload Zone**:
   - Drag a doctor's prescription PDF or lab test image directly over the drop area (observe the border transition to deep emerald with upload icons).
   - Alternatively, click **"Upload Document"** to open the modal.
3. Fill in the metadata:
   - Category: *"Doctor Prescription"*
   - Title: *"Donepezil Refill Authorization"*
   - Doctor: *"Dr. Elena Vance, Neurologist"*
4. Click **"Save Document"**:
   - Demonstrates instant asynchronous upload, thumbnail generation, and secure local/cloud persistence.
5. Filter documents by clicking category pills (*"Prescriptions"*, *"Medical Condition"*, *"Lab Reports"*).
6. Click **"View"** on any document card to show the embedded inline PDF/image preview modal with download and print options.
7. Show that seniors can also view their emergency plans and doctor instructions under the **Safety & Medical Documents** view (`/app/safety`).

---

## 🧪 Step 6: Live Test Execution & Code Quality Verification

Conclude the demonstration by executing automated test harnesses in the terminal to prove software integrity:

```bash
# 1. Run Backend Pytest Suite with Coverage:
cd backend
.venv/bin/pytest -v backend/tests/

# 2. Run Frontend Vitest Suite:
cd ../frontend
npm test
```

*Show Evaluators:*
- **16/16 Backend Tests Passed (88% statement coverage)**.
- **26/26 Frontend Vitest Tests Passed (100% pass rate)**.
- Zero flaky tests. Zero compilation errors.

