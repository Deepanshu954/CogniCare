from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.base import TimeStampedModel


class Alert(TimeStampedModel):
    __tablename__ = "alerts"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    alert_type = Column(String(50), nullable=False)  # SOS, MISSED_MEDICATION, INACTIVITY, HIGH_RISK_DECLINE
    severity = Column(String(50), default="HIGH")  # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(50), default="OPEN")  # OPEN, ACKNOWLEDGED, ESCALATED, RESOLVED, FALSE_POSITIVE
    summary = Column(String(255), nullable=False)
    details = Column(JSON, default=dict)
    acknowledged_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)

    patient = relationship("PatientProfile", back_populates="alerts")
    events = relationship("AlertEvent", back_populates="alert", cascade="all, delete-orphan")


class AlertEvent(TimeStampedModel):
    __tablename__ = "alert_events"

    alert_id = Column(String(36), ForeignKey("alerts.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(50), nullable=False)  # CREATED, ACKNOWLEDGED, ESCALATED, RESOLVED
    actor_id = Column(String(36), nullable=True)
    note = Column(Text, nullable=True)

    alert = relationship("Alert", back_populates="events")


class Notification(TimeStampedModel):
    __tablename__ = "notifications"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    channel = Column(String(50), default="IN_APP")  # IN_APP, PUSH, EMAIL
    priority = Column(String(50), default="NORMAL")  # LOW, NORMAL, HIGH, CRITICAL
    read_at = Column(DateTime, nullable=True)
