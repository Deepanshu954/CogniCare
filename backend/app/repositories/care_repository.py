from typing import List, Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.models.care import Medication, MedicationSchedule, Routine, Reminder, ReminderEvent


class CareRepository:
    def __init__(self, db: Session):
        self.db = db

    # --- Medications ---
    def list_medications(self, patient_id: str, active_only: bool = True) -> List[Medication]:
        query = self.db.query(Medication).filter(Medication.patient_id == patient_id)
        if active_only:
            query = query.filter(Medication.active == True)
        return query.all()

    def get_medication(self, med_id: str) -> Optional[Medication]:
        return self.db.query(Medication).filter(Medication.id == med_id).first()

    def create_medication(
        self,
        patient_id: str,
        name: str,
        dosage_text: str,
        instructions: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Medication:
        med = Medication(
            patient_id=patient_id,
            name=name,
            dosage_text=dosage_text,
            instructions=instructions,
            start_date=start_date,
            end_date=end_date,
            active=True,
        )
        self.db.add(med)
        self.db.commit()
        self.db.refresh(med)
        return med

    def add_medication_schedule(
        self,
        medication_id: str,
        time_of_day: str,
        schedule_type: str = "DAILY",
        days_of_week: Optional[List[str]] = None,
        criticality: str = "HIGH",
    ) -> MedicationSchedule:
        schedule = MedicationSchedule(
            medication_id=medication_id,
            time_of_day=time_of_day,
            schedule_type=schedule_type,
            days_of_week=days_of_week or ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"],
            criticality=criticality,
            active=True,
        )
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)
        return schedule

    # --- Routines ---
    def list_routines(self, patient_id: str, active_only: bool = True) -> List[Routine]:
        query = self.db.query(Routine).filter(Routine.patient_id == patient_id)
        if active_only:
            query = query.filter(Routine.active == True)
        return query.all()

    def get_routine(self, routine_id: str) -> Optional[Routine]:
        return self.db.query(Routine).filter(Routine.id == routine_id).first()

    def create_routine(
        self,
        patient_id: str,
        routine_type: str,
        title: str,
        scheduled_time: str,
        description: Optional[str] = None,
        recurrence_pattern: str = "DAILY",
    ) -> Routine:
        routine = Routine(
            patient_id=patient_id,
            routine_type=routine_type,
            title=title,
            description=description,
            scheduled_time=scheduled_time,
            recurrence_pattern=recurrence_pattern,
            active=True,
        )
        self.db.add(routine)
        self.db.commit()
        self.db.refresh(routine)
        return routine

    # --- Reminders ---
    def list_reminders(
        self,
        patient_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> List[Reminder]:
        query = self.db.query(Reminder).filter(Reminder.patient_id == patient_id)
        if start_time:
            query = query.filter(Reminder.scheduled_for >= start_time)
        if end_time:
            query = query.filter(Reminder.scheduled_for <= end_time)
        return query.order_by(Reminder.scheduled_for.asc()).all()

    def get_reminder(self, reminder_id: str) -> Optional[Reminder]:
        return self.db.query(Reminder).filter(Reminder.id == reminder_id).first()

    def create_reminder(
        self,
        patient_id: str,
        title: str,
        scheduled_for: datetime,
        source_type: str = "CUSTOM",
        source_id: Optional[str] = None,
        description: Optional[str] = None,
        priority: str = "NORMAL",
    ) -> Reminder:
        reminder = Reminder(
            patient_id=patient_id,
            title=title,
            scheduled_for=scheduled_for,
            source_type=source_type,
            source_id=source_id,
            description=description,
            priority=priority,
            status="SCHEDULED",
        )
        self.db.add(reminder)
        self.db.flush()

        event = ReminderEvent(
            reminder_id=reminder.id,
            event_type="CREATED",
            occurred_at=datetime.now(timezone.utc),
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(reminder)
        return reminder

    def record_reminder_event(
        self,
        reminder: Reminder,
        event_type: str,
        actor_id: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> ReminderEvent:
        event = ReminderEvent(
            reminder_id=reminder.id,
            event_type=event_type,
            actor_id=actor_id,
            metadata_json=metadata or {},
            occurred_at=datetime.now(timezone.utc),
        )
        self.db.add(event)
        self.db.commit()
        return event
