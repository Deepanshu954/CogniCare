from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.audit import AuditLog


class AuditService:
    @staticmethod
    def log_action(
        db: Session,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        actor_user_id: Optional[str] = None,
        patient_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        try:
            entry = AuditLog(
                actor_user_id=actor_user_id,
                patient_id=patient_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address=ip_address,
                user_agent=user_agent,
                details=details or {},
            )
            db.add(entry)
            db.commit()
        except Exception:
            db.rollback()
