from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship as orm_relationship
from datetime import datetime, timezone
from app.models.base import TimeStampedModel


class PatientProfile(TimeStampedModel):
    __tablename__ = "patient_profiles"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    emergency_notes = Column(Text, nullable=True)
    accessibility_preferences = Column(JSON, default=dict)
    care_preferences = Column(JSON, default=dict)

    user = orm_relationship("User", back_populates="patient_profile")
    caregiver_links = orm_relationship("CaregiverLink", back_populates="patient", cascade="all, delete-orphan")
    emergency_contacts = orm_relationship("EmergencyContact", back_populates="patient", cascade="all, delete-orphan")
    consents = orm_relationship("Consent", back_populates="patient", cascade="all, delete-orphan")
    medications = orm_relationship("Medication", back_populates="patient", cascade="all, delete-orphan")
    routines = orm_relationship("Routine", back_populates="patient", cascade="all, delete-orphan")
    reminders = orm_relationship("Reminder", back_populates="patient", cascade="all, delete-orphan")
    activity_sessions = orm_relationship("ActivitySession", back_populates="patient", cascade="all, delete-orphan")
    alerts = orm_relationship("Alert", back_populates="patient", cascade="all, delete-orphan")
    reports = orm_relationship("Report", back_populates="patient", cascade="all, delete-orphan")
    conversations = orm_relationship("Conversation", back_populates="patient", cascade="all, delete-orphan")


class CaregiverLink(TimeStampedModel):
    __tablename__ = "caregiver_links"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    caregiver_user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column("relationship", String(100), nullable=False)  # Daughter, Son, Spouse, Nurse, etc.
    permissions = Column(JSON, default=lambda: ["VIEW_PROFILE", "VIEW_COGNITION", "VIEW_REMINDERS", "MANAGE_REMINDERS", "VIEW_ALERTS", "MANAGE_ALERTS"])
    status = Column(String(50), default="ACTIVE")  # ACTIVE, PENDING, REVOKED
    revoked_at = Column(DateTime, nullable=True)

    patient = orm_relationship("PatientProfile", back_populates="caregiver_links")
    caregiver = orm_relationship("User", back_populates="caregiver_links", foreign_keys=[caregiver_user_id])


class EmergencyContact(TimeStampedModel):
    __tablename__ = "emergency_contacts"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    relationship_type = Column("relationship", String(100), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=True)
    priority = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)

    patient = orm_relationship("PatientProfile", back_populates="emergency_contacts")


class Consent(TimeStampedModel):
    __tablename__ = "consents"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    purpose = Column(String(100), nullable=False)  # VOICE_PROCESSING, AI_ASSISTANT, ANALYTICS, CAREGIVER_ACCESS
    policy_version = Column(String(50), default="v1.0")
    granted = Column(Boolean, default=True)
    granted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    revoked_at = Column(DateTime, nullable=True)

    patient = orm_relationship("PatientProfile", back_populates="consents")
