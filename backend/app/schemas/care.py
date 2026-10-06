from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MedicationScheduleCreate(BaseModel):
    schedule_type: str = "DAILY"  # DAILY, WEEKLY, AS_NEEDED
    time_of_day: str  # HH:MM e.g. "09:00"
    days_of_week: List[str] = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    criticality: str = "HIGH"  # NORMAL, HIGH, CRITICAL


class MedicationScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    schedule_type: str
    time_of_day: str
    days_of_week: List[str]
    criticality: str
    active: bool


class MedicationCreate(BaseModel):
    name: str
    dosage_text: str
    instructions: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    schedules: List[MedicationScheduleCreate] = []


class MedicationUpdate(BaseModel):
    name: Optional[str] = None
    dosage_text: Optional[str] = None
    instructions: Optional[str] = None
    active: Optional[bool] = None


class MedicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    patient_id: str
    name: str
    dosage_text: str
    instructions: Optional[str] = None
    active: bool
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    schedules: List[MedicationScheduleResponse] = []
    created_at: datetime


class RoutineCreate(BaseModel):
    routine_type: str  # MEAL, HYDRATION, EXERCISE, APPOINTMENT, SLEEP, CUSTOM
    title: str
    description: Optional[str] = None
    scheduled_time: str  # HH:MM
    recurrence_pattern: str = "DAILY"


class RoutineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    patient_id: str
    routine_type: str
    title: str
    description: Optional[str] = None
    scheduled_time: str
    recurrence_pattern: str
    active: bool
    created_at: datetime


class ReminderCreate(BaseModel):
    source_type: str = "CUSTOM"
    title: str
    description: Optional[str] = None
    scheduled_for: datetime
    priority: str = "NORMAL"


class ReminderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    patient_id: str
    source_type: str
    source_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    scheduled_for: datetime
    status: str
    priority: str
    snooze_until: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    created_at: datetime


class ReminderActionRequest(BaseModel):
    reason: Optional[str] = None
    snooze_minutes: Optional[int] = 15
