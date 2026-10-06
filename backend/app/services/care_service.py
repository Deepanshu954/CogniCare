from typing import List, Optional
from datetime import datetime, timezone, timedelta, date, time
from sqlalchemy.orm import Session

from app.repositories.care_repository import CareRepository
from app.repositories.patient_repository import PatientRepository
from app.models.user import User
from app.models.care import Medication, Routine, Reminder
from app.models.safety import Alert, AlertEvent
from app.schemas.care import (
    MedicationCreate,
    MedicationUpdate,
    MedicationResponse,
    MedicationScheduleResponse,
    RoutineCreate,
    RoutineResponse,
    ReminderCreate,
    ReminderResponse,
)
from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException


class CareService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CareRepository(db)
        self.patient_repo = PatientRepository(db)

    def _check_access(self, current_user: User, patient_id: str, write: bool = False):
        perm = "MANAGE_REMINDERS" if write else "VIEW_REMINDERS"
        if not self.patient_repo.check_access(current_user, patient_id, required_permission=perm if current_user.role != "ELDERLY" else None):
            raise ForbiddenException(message="Access denied to patient care records.")

    # --- Medications ---
    def list_medications(self, patient_id: str, current_user: User) -> List[MedicationResponse]:
        self._check_access(current_user, patient_id, write=False)
        meds = self.repo.list_medications(patient_id)
        return [self._to_medication_response(m) for m in meds]

    def create_medication(self, patient_id: str, current_user: User, data: MedicationCreate) -> MedicationResponse:
        self._check_access(current_user, patient_id, write=True)
        med = self.repo.create_medication(
            patient_id=patient_id,
            name=data.name,
            dosage_text=data.dosage_text,
            instructions=data.instructions,
            start_date=data.start_date,
            end_date=data.end_date,
        )

        for sched_data in data.schedules:
            self.repo.add_medication_schedule(
                medication_id=med.id,
                time_of_day=sched_data.time_of_day,
                schedule_type=sched_data.schedule_type,
                days_of_week=sched_data.days_of_week,
                criticality=sched_data.criticality,
            )

        self.db.refresh(med)
        # Generate today's reminders immediately for this medication
        self.generate_today_reminders_for_patient(patient_id)
        return self._to_medication_response(med)

    def update_medication(self, patient_id: str, med_id: str, current_user: User, data: MedicationUpdate) -> MedicationResponse:
        self._check_access(current_user, patient_id, write=True)
        med = self.repo.get_medication(med_id)
        if not med or med.patient_id != patient_id:
            raise NotFoundException(message="Medication not found.")

        if data.name is not None:
            med.name = data.name
        if data.dosage_text is not None:
            med.dosage_text = data.dosage_text
        if data.instructions is not None:
            med.instructions = data.instructions
        if data.active is not None:
            med.active = data.active

        self.db.commit()
        self.db.refresh(med)
        return self._to_medication_response(med)

    def deactivate_medication(self, patient_id: str, med_id: str, current_user: User):
        self._check_access(current_user, patient_id, write=True)
        med = self.repo.get_medication(med_id)
        if not med or med.patient_id != patient_id:
            raise NotFoundException(message="Medication not found.")
        med.active = False
        self.db.commit()

    # --- Routines ---
    def list_routines(self, patient_id: str, current_user: User) -> List[RoutineResponse]:
        self._check_access(current_user, patient_id, write=False)
        routines = self.repo.list_routines(patient_id)
        return [RoutineResponse.model_validate(r) for r in routines]

    def create_routine(self, patient_id: str, current_user: User, data: RoutineCreate) -> RoutineResponse:
        self._check_access(current_user, patient_id, write=True)
        routine = self.repo.create_routine(
            patient_id=patient_id,
            routine_type=data.routine_type,
            title=data.title,
            scheduled_time=data.scheduled_time,
            description=data.description,
            recurrence_pattern=data.recurrence_pattern,
        )
        self.generate_today_reminders_for_patient(patient_id)
        return RoutineResponse.model_validate(routine)

    # --- Reminders ---
    def generate_today_reminders_for_patient(self, patient_id: str):
        """Idempotently generates today's reminders from active medications and routines."""
        now = datetime.now(timezone.utc)
        today_date = now.date()

        # 1. From Medications
        meds = self.repo.list_medications(patient_id, active_only=True)
        for med in meds:
            for sched in med.schedules:
                if not sched.active:
                    continue
                # Parse HH:MM
                hour, minute = map(int, sched.time_of_day.split(":"))
                sched_dt = datetime.combine(today_date, time(hour, minute)).replace(tzinfo=timezone.utc)

                # Check if reminder already created today for this medication schedule
                existing = (
                    self.db.query(Reminder)
                    .filter(
                        Reminder.patient_id == patient_id,
                        Reminder.source_type == "MEDICATION",
                        Reminder.source_id == sched.id,
                        Reminder.scheduled_for >= datetime.combine(today_date, time.min).replace(tzinfo=timezone.utc),
                        Reminder.scheduled_for <= datetime.combine(today_date, time.max).replace(tzinfo=timezone.utc),
                    )
                    .first()
                )
                if not existing:
                    self.repo.create_reminder(
                        patient_id=patient_id,
                        title=f"Take {med.name} ({med.dosage_text})",
                        description=med.instructions or "Take with water as prescribed.",
                        scheduled_for=sched_dt,
                        source_type="MEDICATION",
                        source_id=sched.id,
                        priority=sched.criticality,
                    )

        # 2. From Routines
        routines = self.repo.list_routines(patient_id, active_only=True)
        for routine in routines:
            hour, minute = map(int, routine.scheduled_time.split(":"))
            sched_dt = datetime.combine(today_date, time(hour, minute)).replace(tzinfo=timezone.utc)

            existing = (
                self.db.query(Reminder)
                .filter(
                    Reminder.patient_id == patient_id,
                    Reminder.source_type == "ROUTINE",
                    Reminder.source_id == routine.id,
                    Reminder.scheduled_for >= datetime.combine(today_date, time.min).replace(tzinfo=timezone.utc),
                    Reminder.scheduled_for <= datetime.combine(today_date, time.max).replace(tzinfo=timezone.utc),
                )
                .first()
            )
            if not existing:
                self.repo.create_reminder(
                    patient_id=patient_id,
                    title=routine.title,
                    description=routine.description or "Scheduled daily routine.",
                    scheduled_for=sched_dt,
                    source_type="ROUTINE",
                    source_id=routine.id,
                    priority="NORMAL",
                )

    def get_today_reminders(self, patient_id: str, current_user: User) -> List[ReminderResponse]:
        self._check_access(current_user, patient_id, write=False)
        self.generate_today_reminders_for_patient(patient_id)

        now = datetime.now(timezone.utc)
        start_of_day = datetime.combine(now.date(), time.min).replace(tzinfo=timezone.utc)
        end_of_day = datetime.combine(now.date(), time.max).replace(tzinfo=timezone.utc)

        reminders = self.repo.list_reminders(patient_id, start_time=start_of_day, end_time=end_of_day)
        return [ReminderResponse.model_validate(r) for r in reminders]

    def create_custom_reminder(self, patient_id: str, current_user: User, data: ReminderCreate) -> ReminderResponse:
        self._check_access(current_user, patient_id, write=True)
        reminder = self.repo.create_reminder(
            patient_id=patient_id,
            title=data.title,
            description=data.description,
            scheduled_for=data.scheduled_for,
            source_type=data.source_type,
            priority=data.priority,
        )
        return ReminderResponse.model_validate(reminder)

    def acknowledge_reminder(self, patient_id: str, reminder_id: str, current_user: User) -> ReminderResponse:
        self._check_access(current_user, patient_id, write=False)
        reminder = self.repo.get_reminder(reminder_id)
        if not reminder or reminder.patient_id != patient_id:
            raise NotFoundException(message="Reminder not found.")

        reminder.status = "ACKNOWLEDGED"
        reminder.acknowledged_at = datetime.now(timezone.utc)
        self.repo.record_reminder_event(
            reminder=reminder,
            event_type="ACKNOWLEDGED",
            actor_id=current_user.id,
            metadata={"role": current_user.role},
        )
        self.db.commit()
        self.db.refresh(reminder)
        return ReminderResponse.model_validate(reminder)

    def snooze_reminder(self, patient_id: str, reminder_id: str, snooze_minutes: int, current_user: User) -> ReminderResponse:
        self._check_access(current_user, patient_id, write=False)
        reminder = self.repo.get_reminder(reminder_id)
        if not reminder or reminder.patient_id != patient_id:
            raise NotFoundException(message="Reminder not found.")

        snooze_until = datetime.now(timezone.utc) + timedelta(minutes=snooze_minutes)
        reminder.status = "SNOOZED"
        reminder.snooze_until = snooze_until

        self.repo.record_reminder_event(
            reminder=reminder,
            event_type="SNOOZED",
            actor_id=current_user.id,
            metadata={"snooze_minutes": snooze_minutes, "snooze_until": snooze_until.isoformat()},
        )
        self.db.commit()
        self.db.refresh(reminder)
        return ReminderResponse.model_validate(reminder)

    def skip_reminder(self, patient_id: str, reminder_id: str, reason: Optional[str], current_user: User) -> ReminderResponse:
        self._check_access(current_user, patient_id, write=False)
        reminder = self.repo.get_reminder(reminder_id)
        if not reminder or reminder.patient_id != patient_id:
            raise NotFoundException(message="Reminder not found.")

        reminder.status = "SKIPPED"
        self.repo.record_reminder_event(
            reminder=reminder,
            event_type="SKIPPED",
            actor_id=current_user.id,
            metadata={"reason": reason or "User skipped"},
        )
        self.db.commit()
        self.db.refresh(reminder)
        return ReminderResponse.model_validate(reminder)

    def trigger_escalation_for_missed(self, patient_id: str, reminder_id: str) -> Alert:
        """Escalates a missed critical reminder into an open alert."""
        reminder = self.repo.get_reminder(reminder_id)
        if not reminder or reminder.patient_id != patient_id:
            raise NotFoundException(message="Reminder not found.")

        reminder.status = "ESCALATED"
        self.repo.record_reminder_event(reminder=reminder, event_type="ESCALATED", metadata={"reason": "Overdue threshold reached"})

        # Create alert
        alert = Alert(
            patient_id=patient_id,
            alert_type="MISSED_MEDICATION" if reminder.source_type == "MEDICATION" else "INACTIVITY",
            severity="CRITICAL" if reminder.priority == "CRITICAL" else "HIGH",
            status="OPEN",
            summary=f"Missed Care Event: {reminder.title}",
            details={"reminder_id": reminder.id, "scheduled_for": reminder.scheduled_for.isoformat()},
        )
        self.db.add(alert)
        self.db.flush()

        event = AlertEvent(
            alert_id=alert.id,
            event_type="CREATED",
            note="Escalated automatically by system reminder scheduler.",
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def _to_medication_response(self, med: Medication) -> MedicationResponse:
        return MedicationResponse(
            id=med.id,
            patient_id=med.patient_id,
            name=med.name,
            dosage_text=med.dosage_text,
            instructions=med.instructions,
            active=med.active,
            start_date=med.start_date,
            end_date=med.end_date,
            schedules=[MedicationScheduleResponse.model_validate(s) for s in med.schedules if s.active],
            created_at=med.created_at,
        )
