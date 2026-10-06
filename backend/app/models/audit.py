from sqlalchemy import Column, String, Text, JSON
from app.models.base import TimeStampedModel


class AuditLog(TimeStampedModel):
    __tablename__ = "audit_logs"

    actor_user_id = Column(String(36), nullable=True)
    patient_id = Column(String(36), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(36), nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    details = Column(JSON, default=dict)
