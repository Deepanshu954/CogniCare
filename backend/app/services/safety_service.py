from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.repositories.safety_repository import SafetyRepository
from app.repositories.patient_repository import PatientRepository
from app.models.user import User
from app.models.safety import Alert, Notification
from app.schemas.safety import (
    AlertResponse,
    AlertEventResponse,
    SOSTriggerRequest,
    AlertActionRequest,
    NotificationResponse,
)
from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException


class SafetyService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SafetyRepository(db)
        self.patient_repo = PatientRepository(db)

    def _check_access(self, current_user: User, patient_id: str, write: bool = False):
        perm = "MANAGE_ALERTS" if write else "VIEW_ALERTS"
        if not self.patient_repo.check_access(current_user, patient_id, required_permission=perm if current_user.role != "ELDERLY" else None):
            raise ForbiddenException(message="Access denied to safety alerts.")

    def trigger_sos(
        self,
        patient_id: str,
        current_user: User,
        data: Optional[SOSTriggerRequest] = None,
    ) -> AlertResponse:
        self._check_access(current_user, patient_id, write=False)  # Patient or Caregiver can trigger SOS

        patient = self.patient_repo.get_by_id(patient_id)
        name = patient.user.profile.display_name if patient and patient.user and patient.user.profile else "Patient"

        msg = data.message if data and data.message else "Emergency SOS button triggered"
        loc = data.location_note if data and data.location_note else "Home"

        alert = self.repo.create_alert(
            patient_id=patient_id,
            alert_type="SOS",
            severity="CRITICAL",
            summary=f"EMERGENCY SOS: {name}",
            details={"message": msg, "location": loc, "actor_id": current_user.id},
        )

        # Notify all registered caregivers immediately
        self.repo.notify_caregivers(
            patient_id=patient_id,
            title="CRITICAL: Emergency SOS Triggered",
            body=f"{name} has pressed the Emergency SOS button. Immediate check-in required.",
            priority="CRITICAL",
        )

        return self._to_alert_response(alert)

    def list_alerts(self, patient_id: str, current_user: User, open_only: bool = False) -> List[AlertResponse]:
        self._check_access(current_user, patient_id, write=False)
        alerts = self.repo.list_alerts(patient_id, open_only=open_only)
        return [self._to_alert_response(a) for a in alerts]

    def get_alert_details(self, patient_id: str, alert_id: str, current_user: User) -> AlertResponse:
        self._check_access(current_user, patient_id, write=False)
        alert = self.repo.get_alert(alert_id)
        if not alert or alert.patient_id != patient_id:
            raise NotFoundException(message="Alert not found.")
        return self._to_alert_response(alert)

    def acknowledge_alert(self, patient_id: str, alert_id: str, current_user: User) -> AlertResponse:
        self._check_access(current_user, patient_id, write=True)
        alert = self.repo.get_alert(alert_id)
        if not alert or alert.patient_id != patient_id:
            raise NotFoundException(message="Alert not found.")

        alert.status = "ACKNOWLEDGED"
        alert.acknowledged_at = datetime.now(timezone.utc)
        self.repo.record_alert_event(
            alert=alert,
            event_type="ACKNOWLEDGED",
            actor_id=current_user.id,
            note="Alert acknowledged by caregiver.",
        )
        self.db.commit()
        self.db.refresh(alert)
        return self._to_alert_response(alert)

    def resolve_alert(
        self,
        patient_id: str,
        alert_id: str,
        current_user: User,
        data: AlertActionRequest,
    ) -> AlertResponse:
        self._check_access(current_user, patient_id, write=True)
        alert = self.repo.get_alert(alert_id)
        if not alert or alert.patient_id != patient_id:
            raise NotFoundException(message="Alert not found.")

        alert.status = "RESOLVED"
        alert.resolved_at = datetime.now(timezone.utc)
        self.repo.record_alert_event(
            alert=alert,
            event_type="RESOLVED",
            actor_id=current_user.id,
            note=data.note or "Resolved by caregiver.",
        )
        self.db.commit()
        self.db.refresh(alert)
        return self._to_alert_response(alert)

    def list_notifications(self, current_user: User) -> List[NotificationResponse]:
        notifs = self.repo.list_user_notifications(current_user.id)
        return [NotificationResponse.model_validate(n) for n in notifs]

    def mark_notification_read(self, notification_id: str, current_user: User):
        notif = self.db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == current_user.id).first()
        if notif:
            notif.read_at = datetime.now(timezone.utc)
            self.db.commit()

    def _to_alert_response(self, alert: Alert) -> AlertResponse:
        return AlertResponse(
            id=alert.id,
            patient_id=alert.patient_id,
            alert_type=alert.alert_type,
            severity=alert.severity,
            status=alert.status,
            summary=alert.summary,
            details=alert.details or {},
            created_at=alert.created_at,
            acknowledged_at=alert.acknowledged_at,
            resolved_at=alert.resolved_at,
            events=[AlertEventResponse.model_validate(e) for e in alert.events],
        )
