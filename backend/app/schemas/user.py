from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    display_name: str
    phone_number: Optional[str] = None
    preferred_language: str
    timezone: str
    avatar_url: Optional[str] = None


class PatientProfileSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    emergency_notes: Optional[str] = None
    accessibility_preferences: Dict[str, Any] = {}
    care_preferences: Dict[str, Any] = {}


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    role: str
    status: str
    profile: Optional[ProfileResponse] = None
    patient_profile: Optional[PatientProfileSummary] = None
    created_at: datetime

