from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.safety import (
    AlertResponse,
    SOSTriggerRequest,
    AlertActionRequest,
    NotificationResponse,
)
from app.services.safety_service import SafetyService

safety_router = APIRouter(prefix="/patients/{patient_id}", tags=["Safety & Alerts"])
notifications_router = APIRouter(prefix="/notifications", tags=["Notifications"])


@safety_router.post("/sos", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def trigger_sos(
    patient_id: str,
    data: Optional[SOSTriggerRequest] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SafetyService(db)
    return service.trigger_sos(patient_id, current_user, data)


@safety_router.get("/alerts", response_model=List[AlertResponse])
def list_alerts(
    patient_id: str,
    open_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SafetyService(db)
    return service.list_alerts(patient_id, current_user, open_only=open_only)


@safety_router.get("/alerts/{alert_id}", response_model=AlertResponse)
def get_alert_details(
    patient_id: str,
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SafetyService(db)
    return service.get_alert_details(patient_id, alert_id, current_user)


@safety_router.post("/alerts/{alert_id}/acknowledge", response_model=AlertResponse)
def acknowledge_alert(
    patient_id: str,
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SafetyService(db)
    return service.acknowledge_alert(patient_id, alert_id, current_user)


@safety_router.post("/alerts/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(
    patient_id: str,
    alert_id: str,
    data: AlertActionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SafetyService(db)
    return service.resolve_alert(patient_id, alert_id, current_user, data)


# --- Notifications ---
@notifications_router.get("", response_model=List[NotificationResponse])
def list_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SafetyService(db)
    return service.list_notifications(current_user)


@notifications_router.post("/{notification_id}/read")
def mark_notification_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SafetyService(db)
    service.mark_notification_read(notification_id, current_user)
    return {"message": "Notification marked as read"}
