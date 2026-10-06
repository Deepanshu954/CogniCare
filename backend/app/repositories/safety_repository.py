from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.safety import Alert, AlertEvent, Notification
from app.models.patient import CaregiverLink


class SafetyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_alert(
        self,
        patient_id: str,
        alert_type: str,
        severity: str,
        summary: str,
        details: Optional[dict] = None,
    ) -> Alert:
        alert = Alert(
            patient_id=patient_id,
            alert_type=alert_type,
            severity=severity,
            status="OPEN",
            summary=summary,
            details=details or {},
        )
        self.db.add(alert)
        self.db.flush()

        event = AlertEvent(
            alert_id=alert.id,
            event_type="CREATED",
            note=f"Alert triggered: {summary}",
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def get_alert(self, alert_id: str) -> Optional[Alert]:
        return self.db.query(Alert).filter(Alert.id == alert_id).first()

    def list_alerts(self, patient_id: str, open_only: bool = False) -> List[Alert]:
        query = self.db.query(Alert).filter(Alert.patient_id == patient_id)
        if open_only:
            query = query.filter(Alert.status.in_(["OPEN", "ACKNOWLEDGED", "ESCALATED"]))
        return query.order_by(Alert.created_at.desc()).all()

    def record_alert_event(
        self,
        alert: Alert,
        event_type: str,
        actor_id: Optional[str] = None,
        note: Optional[str] = None,
    ) -> AlertEvent:
        event = AlertEvent(
            alert_id=alert.id,
            event_type=event_type,
            actor_id=actor_id,
            note=note,
        )
        self.db.add(event)
        self.db.commit()
        return event

    def notify_caregivers(self, patient_id: str, title: str, body: str, priority: str = "HIGH"):
        links = self.db.query(CaregiverLink).filter(CaregiverLink.patient_id == patient_id, CaregiverLink.status == "ACTIVE").all()
        for link in links:
            notif = Notification(
                user_id=link.caregiver_user_id,
                title=title,
                body=body,
                channel="IN_APP",
                priority=priority,
            )
            self.db.add(notif)
        self.db.commit()

    def list_user_notifications(self, user_id: str) -> List[Notification]:
        return (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(50)
            .all()
        )
