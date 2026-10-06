from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SOSTriggerRequest(BaseModel):
    message: Optional[str] = "Elderly user pressed SOS emergency button."
    location_note: Optional[str] = "Living room / home"


class AlertEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    event_type: str
    actor_id: Optional[str] = None
    note: Optional[str] = None
    created_at: datetime


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    patient_id: str
    alert_type: str
    severity: str
    status: str
    summary: str
    details: Dict[str, Any] = {}
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    events: List[AlertEventResponse] = []


class AlertActionRequest(BaseModel):
    note: Optional[str] = None


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    body: str
    channel: str
    priority: str
    read_at: Optional[datetime] = None
    created_at: datetime
