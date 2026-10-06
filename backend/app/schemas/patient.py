from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class EmergencyContactCreate(BaseModel):
    name: str
    relationship_type: str
    phone: str
    email: Optional[EmailStr] = None
    priority: int = 1


class EmergencyContactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    relationship_type: str
    phone: str
    email: Optional[str] = None
    priority: int
    is_active: bool


class ConsentCreate(BaseModel):
    purpose: str
    policy_version: str = "v1.0"
    granted: bool = True


class ConsentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    purpose: str
    policy_version: str
    granted: bool
    granted_at: datetime
    revoked_at: Optional[datetime] = None


class CaregiverInviteRequest(BaseModel):
    caregiver_email: EmailStr
    relationship_type: str
    permissions: List[str] = ["VIEW_PROFILE", "VIEW_COGNITION", "VIEW_REMINDERS", "MANAGE_REMINDERS", "VIEW_ALERTS", "MANAGE_ALERTS"]


class CaregiverLinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    caregiver_user_id: str
    caregiver_email: Optional[str] = None
    caregiver_name: Optional[str] = None
    relationship_type: str
    permissions: List[str]
    status: str
    created_at: datetime


class PatientCreateRequest(BaseModel):
    display_name: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    emergency_notes: Optional[str] = None
    accessibility_preferences: Dict[str, Any] = {}
    care_preferences: Dict[str, Any] = {}


class PatientUpdateRequest(BaseModel):
    display_name: Optional[str] = None
    emergency_notes: Optional[str] = None
    accessibility_preferences: Optional[Dict[str, Any]] = None
    care_preferences: Optional[Dict[str, Any]] = None


class PatientDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    display_name: str
    email: str
    phone_number: Optional[str] = None
    emergency_notes: Optional[str] = None
    accessibility_preferences: Dict[str, Any] = {}
    care_preferences: Dict[str, Any] = {}
    emergency_contacts: List[EmergencyContactResponse] = []
    consents: List[ConsentResponse] = []
    caregivers: List[CaregiverLinkResponse] = []
    created_at: datetime


class PatientSummaryResponse(BaseModel):
    id: str
    display_name: str
    total_medications: int
    today_reminders_count: int
    today_completed_reminders: int
    adherence_percentage: float
    open_alerts_count: int
    last_activity_date: Optional[str] = None
    status: str  # EXCELLENT, ATTENTION_NEEDED, CRITICAL_ALERT
