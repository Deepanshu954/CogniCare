import os
import sys
from datetime import datetime, timezone, timedelta, time

# Ensure project root in pythonpath
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.core.database import SessionLocal, engine, Base
import app.models
from app.models.user import User, Profile
from app.models.patient import PatientProfile, CaregiverLink, EmergencyContact, Consent
from app.models.care import Medication, MedicationSchedule, Routine, Reminder, ReminderEvent
from app.models.cognition import (
    CognitiveActivity,
    ActivitySession,
    ActivityAnswer,
    CognitiveBaseline,
    CognitiveTrendSnapshot,
)
from app.models.assistant import Conversation, Message, MemoryItem
from app.models.safety import Alert, AlertEvent, Notification
from app.models.report import Report
from app.core.security import hash_password
from app.services.care_service import CareService
from app.services.report_service import ReportService


def seed_database():
    print("Beginning CogniCare comprehensive database seeding...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).filter(User.email == "sarah@example.com").first():
            print("Database already contains seed accounts. Skipping seeding.")
            return

        pwd = hash_password("Password123!")

        # 1. Users
        print("1. Creating Users...")
        # Elderly 1: Margaret
        margaret_user = User(email="margaret@example.com", password_hash=pwd, role="ELDERLY", status="ACTIVE")
        db.add(margaret_user)
        db.flush()
        db.add(Profile(user_id=margaret_user.id, display_name="Margaret Connor", phone_number="+1-555-0101", preferred_language="en", timezone="America/New_York"))
        margaret_patient = PatientProfile(
            user_id=margaret_user.id,
            emergency_notes="Mild cognitive impairment. Needs morning reminder for Donepezil.",
            accessibility_preferences={"high_contrast": True, "large_text": True, "speech_speed": 1.0, "voice_guidance": True},
            care_preferences={"wake_time": "08:00", "sleep_time": "21:30"},
        )
        db.add(margaret_patient)

        # Elderly 2: Arthur
        arthur_user = User(email="arthur@example.com", password_hash=pwd, role="ELDERLY", status="ACTIVE")
        db.add(arthur_user)
        db.flush()
        db.add(Profile(user_id=arthur_user.id, display_name="Arthur Dent", phone_number="+1-555-0102", preferred_language="en", timezone="America/New_York"))
        arthur_patient = PatientProfile(
            user_id=arthur_user.id,
            emergency_notes="Requires calm reassurance and routine prompts.",
            accessibility_preferences={"high_contrast": False, "large_text": True, "speech_speed": 1.0, "voice_guidance": True},
            care_preferences={"wake_time": "08:30", "sleep_time": "22:00"},
        )
        db.add(arthur_patient)

        # Caregiver 1: Sarah
        sarah_user = User(email="sarah@example.com", password_hash=pwd, role="CAREGIVER", status="ACTIVE")
        db.add(sarah_user)
        db.flush()
        db.add(Profile(user_id=sarah_user.id, display_name="Sarah Connor", phone_number="+1-555-0199", preferred_language="en", timezone="America/New_York"))

        # Caregiver 2: Dr. Emily Watson
        emily_user = User(email="emily@example.com", password_hash=pwd, role="CAREGIVER", status="ACTIVE")
        db.add(emily_user)
        db.flush()
        db.add(Profile(user_id=emily_user.id, display_name="Dr. Emily Watson", phone_number="+1-555-0144", preferred_language="en", timezone="America/New_York"))

        db.commit()

        # 2. Caregiver Links
        print("2. Establishing Caregiver Links...")
        perms = ["VIEW_PROFILE", "VIEW_COGNITION", "VIEW_REMINDERS", "MANAGE_REMINDERS", "VIEW_ALERTS", "MANAGE_ALERTS", "VIEW_REPORTS"]
        db.add(CaregiverLink(patient_id=margaret_patient.id, caregiver_user_id=sarah_user.id, relationship_type="Daughter & Primary Caregiver", permissions=perms, status="ACTIVE"))
        db.add(CaregiverLink(patient_id=arthur_patient.id, caregiver_user_id=emily_user.id, relationship_type="Attending Geriatric Specialist", permissions=perms, status="ACTIVE"))

        # 3. Emergency Contacts & Consents
        print("3. Creating Emergency Contacts & Consents...")
        db.add(EmergencyContact(patient_id=margaret_patient.id, name="Sarah Connor", relationship_type="Daughter", phone="+1-555-0199", priority=1))
        db.add(EmergencyContact(patient_id=margaret_patient.id, name="Dr. Mark Evans", relationship_type="Family Physician", phone="+1-555-0188", priority=2))
        db.add(Consent(patient_id=margaret_patient.id, purpose="VOICE_PROCESSING", policy_version="v1.0", granted=True))
        db.add(Consent(patient_id=margaret_patient.id, purpose="AI_ASSISTANT", policy_version="v1.0", granted=True))
        db.add(Consent(patient_id=margaret_patient.id, purpose="ANALYTICS", policy_version="v1.0", granted=True))

        # 4. Medications & Schedules
        print("4. Scheduling Prescriptions...")
        med1 = Medication(patient_id=margaret_patient.id, name="Donepezil", dosage_text="10mg", instructions="Take with morning meal and full glass of water.", active=True)
        med2 = Medication(patient_id=margaret_patient.id, name="Multivitamin Daily", dosage_text="1 tablet", instructions="Take with lunch.", active=True)
        med3 = Medication(patient_id=margaret_patient.id, name="Blood Pressure Support (Lisinopril)", dosage_text="20mg", instructions="Take before bedtime.", active=True)
        db.add_all([med1, med2, med3])
        db.flush()

        db.add(MedicationSchedule(medication_id=med1.id, time_of_day="09:00", schedule_type="DAILY", criticality="HIGH"))
        db.add(MedicationSchedule(medication_id=med2.id, time_of_day="12:30", schedule_type="DAILY", criticality="NORMAL"))
        db.add(MedicationSchedule(medication_id=med3.id, time_of_day="20:00", schedule_type="DAILY", criticality="HIGH"))

        # 5. Routines
        print("5. Adding Daily Routines...")
        r1 = Routine(patient_id=margaret_patient.id, routine_type="HYDRATION", title="Morning Glass of Water", scheduled_time="08:15", description="Drink 250ml warm water", active=True)
        r2 = Routine(patient_id=margaret_patient.id, routine_type="COGNITIVE_ACTIVITY", title="Daily Mind Exercise", scheduled_time="11:00", description="Memory cards & sequence challenge", active=True)
        r3 = Routine(patient_id=margaret_patient.id, routine_type="EXERCISE", title="Afternoon Garden Walk", scheduled_time="16:30", description="15 minutes gentle stroll in the courtyard", active=True)
        db.add_all([r1, r2, r3])
        db.commit()

        # 6. Generate Today's Reminders and mark morning tasks acknowledged
        print("6. Dispatching Today's Reminders...")
        care_service = CareService(db)
        care_service.generate_today_reminders_for_patient(margaret_patient.id)

        today_reminders = db.query(Reminder).filter(Reminder.patient_id == margaret_patient.id).all()
        for idx, rem in enumerate(today_reminders):
            if idx < 2:  # Mark first two as acknowledged
                rem.status = "ACKNOWLEDGED"
                rem.acknowledged_at = datetime.now(timezone.utc) - timedelta(hours=2)
                db.add(ReminderEvent(reminder_id=rem.id, event_type="ACKNOWLEDGED", actor_id=margaret_user.id))
        db.commit()

        # 7. Seed 14 Days of Cognitive Activity Sessions for Margaret
        print("7. Seeding Longitudinal Cognitive Sessions...")
        activities = db.query(CognitiveActivity).all()
        if not activities:
            # Trigger repository to create catalog
            from app.repositories.cognition_repository import CognitionRepository
            CognitionRepository(db)
            activities = db.query(CognitiveActivity).all()

        today_date = datetime.now(timezone.utc)
        for i in range(14, 0, -1):
            sess_time = today_date - timedelta(days=i, hours=2)
            act = activities[i % len(activities)]
            # Realistic longitudinal curve: stable with mild variation
            score_val = round(78.0 + (i % 5) * 3.5, 1)
            acc_val = round(80.0 + (i % 4) * 4.0, 1)
            lat_val = 1650 + (i % 3) * 120

            session = ActivitySession(
                patient_id=margaret_patient.id,
                activity_id=act.id,
                status="COMPLETED",
                difficulty=1 + (i % 2),
                total_score=score_val,
                accuracy_rate=acc_val,
                avg_response_time_ms=lat_val,
                started_at=sess_time,
                completed_at=sess_time + timedelta(minutes=6),
            )
            db.add(session)
            db.flush()

            # Add answers
            for q_idx in range(4):
                db.add(
                    ActivityAnswer(
                        session_id=session.id,
                        question_id=f"q_{q_idx}",
                        user_answer="Correct Answer",
                        is_correct=(q_idx != 3 or i % 3 != 0),
                        response_time_ms=lat_val + q_idx * 50,
                        attempt_number=1,
                        difficulty=session.difficulty,
                    )
                )

        db.add(CognitiveBaseline(patient_id=margaret_patient.id, metric_name="OVERALL_SCORE", baseline_value=84.5, sample_count=14))
        db.commit()

        # 8. Seed Safety Alerts and Notifications
        print("8. Seeding Safety Alerts & Notifications...")
        past_alert = Alert(
            patient_id=margaret_patient.id,
            alert_type="MISSED_MEDICATION",
            severity="HIGH",
            status="RESOLVED",
            summary="Morning Hydration delay noted",
            details={"note": "Sarah verified Margaret was on phone with grandson."},
            created_at=today_date - timedelta(days=2),
            acknowledged_at=today_date - timedelta(days=2, hours=-1),
            resolved_at=today_date - timedelta(days=2, hours=-2),
        )
        db.add(past_alert)
        db.flush()
        db.add(AlertEvent(alert_id=past_alert.id, event_type="RESOLVED", actor_id=sarah_user.id, note="Resolved: Checked in with patient."))

        # Notification for Sarah
        db.add(Notification(user_id=sarah_user.id, title="Morning Adherence Update", body="Margaret completed her 09:00 AM Donepezil medication on time.", channel="IN_APP", priority="NORMAL"))

        # 9. Seed Memory Items
        print("9. Seeding Conversational Memory Items...")
        db.add(MemoryItem(patient_id=margaret_patient.id, memory_type="PREFERENCE", content="Enjoys chamomile tea in the evening."))
        db.add(MemoryItem(patient_id=margaret_patient.id, memory_type="PREFERENCE", content="Prefers large card layouts and flower pictures for memory recall exercises."))
        db.add(MemoryItem(patient_id=margaret_patient.id, memory_type="ROUTINE", content="Regular afternoon walk in courtyard at 4:30 PM with daughter Sarah."))

        # 10. Generate Initial Weekly Report
        print("10. Generating Weekly Care Report...")
        report_service = ReportService(db)
        report_service.generate_weekly_report(margaret_patient.id, sarah_user)

        db.commit()
        print("\nDatabase successfully seeded with realistic demonstration data!")
        print("==================================================")
        print("Demo Accounts:")
        print("1. Elderly User:   margaret@example.com / Password123!")
        print("2. Caregiver User: sarah@example.com    / Password123!")
        print("3. Second Elderly: arthur@example.com   / Password123!")
        print("4. Specialist:     emily@example.com    / Password123!")
        print("==================================================")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
