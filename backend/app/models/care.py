from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, Time, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.base import TimeStampedModel


class Medication(TimeStampedModel):
    __tablename__ = "medications"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    dosage_text = Column(String(100), nullable=False)
    instructions = Column(Text, nullable=True)
    active = Column(Boolean, default=True)
    start_date = Column(String(20), nullable=True)
    end_date = Column(String(20), nullable=True)

    patient = relationship("PatientProfile", back_populates="medications")
    schedules = relationship("MedicationSchedule", back_populates="medication", cascade="all, delete-orphan")


class MedicationSchedule(TimeStampedModel):
    __tablename__ = "medication_schedules"

    medication_id = Column(String(36), ForeignKey("medications.id", ondelete="CASCADE"), nullable=False)
    schedule_type = Column(String(50), default="DAILY")  # DAILY, WEEKLY, AS_NEEDED
    time_of_day = Column(String(10), nullable=False)  # HH:MM format e.g. "08:00"
    days_of_week = Column(JSON, default=lambda: ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"])
    criticality = Column(String(50), default="HIGH")  # NORMAL, HIGH, CRITICAL
    active = Column(Boolean, default=True)

    medication = relationship("Medication", back_populates="schedules")


class Routine(TimeStampedModel):
    __tablename__ = "routines"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    routine_type = Column(String(50), nullable=False)  # MEAL, HYDRATION, EXERCISE, APPOINTMENT, SLEEP, CUSTOM
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    scheduled_time = Column(String(10), nullable=False)  # HH:MM
    recurrence_pattern = Column(String(50), default="DAILY")
    active = Column(Boolean, default=True)

    patient = relationship("PatientProfile", back_populates="routines")


class Reminder(TimeStampedModel):
    __tablename__ = "reminders"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    source_type = Column(String(50), default="MEDICATION")  # MEDICATION, ROUTINE, ACTIVITY, CUSTOM
    source_id = Column(String(36), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    scheduled_for = Column(DateTime, nullable=False)
    status = Column(String(50), default="SCHEDULED")  # SCHEDULED, DELIVERED, ACKNOWLEDGED, SKIPPED, SNOOZED, MISSED, ESCALATED
    priority = Column(String(50), default="HIGH")  # LOW, NORMAL, HIGH, CRITICAL
    snooze_until = Column(DateTime, nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)

    patient = relationship("PatientProfile", back_populates="reminders")
    events = relationship("ReminderEvent", back_populates="reminder", cascade="all, delete-orphan")


class ReminderEvent(TimeStampedModel):
    __tablename__ = "reminder_events"

    reminder_id = Column(String(36), ForeignKey("reminders.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(50), nullable=False)  # CREATED, DELIVERED, ACKNOWLEDGED, SKIPPED, SNOOZED, MISSED, ESCALATED
    actor_id = Column(String(36), nullable=True)
    metadata_json = Column(JSON, default=dict)
    occurred_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    reminder = relationship("Reminder", back_populates="events")
