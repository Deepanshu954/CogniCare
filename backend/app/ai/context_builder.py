from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.patient import PatientProfile, EmergencyContact, CaregiverLink
from app.models.care import Medication, Routine, Reminder
from app.models.cognition import CognitiveBaseline, ActivitySession


PUBLIC_GERIATRIC_KNOWLEDGE = """
=== PUBLIC MEDICAL & GERIATRIC CARE KNOWLEDGE BASE ===
1. Condition Overview:
   - Mild Cognitive Impairment (MCI) and early-stage dementia involve gradual deficits in short-term episodic memory, word-finding hesitations, mild executive dysfunction, and disorientation to time/dates.
   - Seniors retain long-term memories, emotional intuition, and dignity. They may experience anxiety or frustration when forgetting daily tasks.

2. Evidence-Based Communication Principles (Validation & Grounding):
   - Validation Therapy (Naomi Feil Methodology): Never argue, debate, or bluntly correct an elderly person. If they misplace an item or express anxiety, validate the emotion first: "I understand you are looking for your glasses, let's check your favorite table together."
   - Cognitive Load Reduction: Keep sentences short, warm, and focused on one thought or single action at a time.
   - Gentle Orientation Cues: Naturally weave comforting time references into greetings ("Good morning Margaret! It is Tuesday morning, a lovely sunny day.").
   - Patience & Repetition without Judgment: NEVER say "I already told you that" or "You asked this 5 minutes ago." Answer each question as if it is the first time with gentle reassurance.
   - Respect & Dignity: Avoid infantilizing baby-talk or condescension. Treat the senior as a respected elder.

3. Strict Medical & Safety Boundaries:
   - You are an ambient supportive companion station, NOT a licensed physician.
   - You MUST NEVER diagnose conditions (e.g. do not say "You have stage 2 Alzheimer's").
   - You MUST NEVER alter prescription dosages (e.g. if asked "Should I take 2 pills?", advise them to check with their doctor or daughter Sarah).
   - In case of physical fall, severe confusion, chest pain, or panic, immediately advise pressing the red Emergency SOS button or contacting their designated caregiver.
======================================================
"""


def get_private_patient_context(patient_id: str, db: Session) -> Dict[str, Any]:
    """Retrieve authorized private clinical and daily schedule context for a patient."""
    patient = db.query(PatientProfile).filter(PatientProfile.id == patient_id).first()
    if not patient:
        return {"error": "Patient record not found"}

    # 1. Identity & Care Level
    user = patient.user
    display_name = user.profile.display_name if (user and user.profile) else (user.email if user else "Senior User")
    care_level = patient.care_preferences.get("care_level", "STANDARD") if patient.care_preferences else "STANDARD"
    
    # 2. Caregiver Links
    caregivers = (
        db.query(CaregiverLink)
        .filter(CaregiverLink.patient_id == patient_id, CaregiverLink.status == "ACTIVE")
        .all()
    )
    caregiver_info = [
        f"{c.caregiver.profile.display_name if c.caregiver and c.caregiver.profile else c.caregiver.email} ({c.relationship_type})"
        for c in caregivers
    ]

    # 3. Emergency Contacts
    contacts = (
        db.query(EmergencyContact)
        .filter(EmergencyContact.patient_id == patient_id)
        .all()
    )
    contact_list = [
        f"{c.name} ({c.relationship}, Phone: {c.phone_number})"
        for c in contacts
    ]

    # 4. Active Prescriptions
    meds = (
        db.query(Medication)
        .filter(Medication.patient_id == patient_id, Medication.active == True)
        .all()
    )
    medication_list = [
        f"{m.name} ({m.dosage_text}, Instructions: {m.instructions or 'Take with water'})"
        for m in meds
    ]

    # 5. Daily Routines
    routines = (
        db.query(Routine)
        .filter(Routine.patient_id == patient_id, Routine.active == True)
        .all()
    )
    routine_list = [
        f"{r.title} ({r.routine_type}, Scheduled: {r.scheduled_time})"
        for r in routines
    ]

    # 6. Today's Reminders & Adherence Status
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    reminders = (
        db.query(Reminder)
        .filter(Reminder.patient_id == patient_id, Reminder.scheduled_for >= today_start)
        .order_by(Reminder.scheduled_for.asc())
        .all()
    )
    reminders_status = [
        f"{r.title} at {r.scheduled_for.strftime('%I:%M %p')}: [{r.status}]"
        for r in reminders
    ]

    # 7. Cognitive Baseline & Recent Trend
    baselines = (
        db.query(CognitiveBaseline)
        .filter(CognitiveBaseline.patient_id == patient_id)
        .all()
    )
    baseline_summary = [
        f"Domain {b.domain}: Mean Score {b.baseline_score}/100, Latency {b.baseline_latency_ms}ms"
        for b in baselines
    ]

    return {
        "display_name": display_name,
        "care_level": care_level,
        "emergency_notes": patient.emergency_notes,
        "caregivers": caregiver_info,
        "emergency_contacts": contact_list,
        "medications": medication_list,
        "daily_routines": routine_list,
        "today_schedule": reminders_status,
        "cognitive_baselines": baseline_summary,
    }


def build_system_prompt(
    patient_id: str,
    db: Session,
    mode: str = "normal",
) -> str:
    """Build complete dual-layer context prompt combining Public Geriatric Knowledge and Private Patient Records."""
    private_data = get_private_patient_context(patient_id, db)
    now_str = datetime.now(timezone.utc).strftime("%A, %B %d, %Y at %I:%M %p UTC")

    mode_instruction = ""
    if mode == "extended":
        mode_instruction = """
=== MODE: GEMINI 3.8 LIVE EXTENDED THINKING ===
You are operating in Extended Thinking mode.
1. Perform deep reasoning on the patient's physical state, emotional comfort, and cognitive trends.
2. Cross-reference their recent medication adherence with their scheduled routine.
3. Formulate empathetic, reassuring responses tailored to their specific historical cognitive baseline.
4. Provide structured, transparent thought steps before producing your final compassionate response.
"""
    else:
        mode_instruction = """
=== MODE: GEMINI 3.8 LIVE CONVERSATIONAL ===
You are operating in Live Conversational mode.
1. Keep replies conversational, warm, concise (2-4 sentences max), and easy to read or listen to aloud.
2. Directly answer their immediate concern (e.g. medications, daily tasks, orientation).
3. Offer comfort and one clear next step.
"""

    prompt = f"""You are CogniCare, a compassionate, context-grounded AI assistant for elderly care.
Current Time: {now_str}

{PUBLIC_GERIATRIC_KNOWLEDGE}

=== PRIVATE PATIENT CLINICAL & ROUTINE PROFILE ===
Patient Name: {private_data.get('display_name')}
Care Level: {private_data.get('care_level')}
Personal Notes / Preferences: {private_data.get('emergency_notes')}

Caregiver Team:
{chr(10).join(f"- {c}" for c in private_data.get('caregivers', [])) or "- None designated"}

Emergency Contacts:
{chr(10).join(f"- {c}" for c in private_data.get('emergency_contacts', [])) or "- None designated"}

Prescribed Active Medications:
{chr(10).join(f"- {m}" for m in private_data.get('medications', [])) or "- No active prescriptions"}

Daily Routines:
{chr(10).join(f"- {r}" for r in private_data.get('daily_routines', [])) or "- No daily routines"}

Today's Schedule & Reminders Status:
{chr(10).join(f"- {s}" for s in private_data.get('today_schedule', [])) or "- All clear for today"}

30-Day Cognitive Health Baseline:
{chr(10).join(f"- {b}" for b in private_data.get('cognitive_baselines', [])) or "- Baseline establishing"}
==================================================

{mode_instruction}

Answer the patient respectfully, empathetically, and factually based on the private records provided.
"""
    return prompt.strip()
