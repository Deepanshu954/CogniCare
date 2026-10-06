from sqlalchemy import Column, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedModel


class Report(TimeStampedModel):
    __tablename__ = "reports"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    period_start = Column(String(20), nullable=False)
    period_end = Column(String(20), nullable=False)
    metrics_snapshot = Column(JSON, default=dict)
    ai_narrative_summary = Column(Text, nullable=False)
    status = Column(String(50), default="FINAL")  # DRAFT, FINAL

    patient = relationship("PatientProfile", back_populates="reports")
