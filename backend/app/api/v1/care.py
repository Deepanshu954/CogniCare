from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.care import (
    MedicationCreate,
    MedicationUpdate,
    MedicationResponse,
    RoutineCreate,
    RoutineResponse,
    ReminderCreate,
    ReminderResponse,
    ReminderActionRequest,
)
from app.services.care_service import CareService

router = APIRouter(prefix="/patients/{patient_id}", tags=["Care & Reminders"])


# --- Medications ---
@router.get("/medications", response_model=List[MedicationResponse])
def list_medications(
    patient_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CareService(db)
    return service.list_medications(patient_id, current_user)


@router.post("/medications", response_model=MedicationResponse, status_code=status.HTTP_201_CREATED)
def create_medication(
    patient_id: str,
    data: MedicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CareService(db)
    return service.create_medication(patient_id, current_user, data)


@router.patch("/medications/{med_id}", response_model=MedicationResponse)
def update_medication(
    patient_id: str,
    med_id: str,
    data: MedicationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CareService(db)
    return service.update_medication(patient_id, med_id, current_user, data)


@router.delete("/medications/{med_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_medication(
    patient_id: str,
    med_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CareService(db)
    service.deactivate_medication(patient_id, med_id, current_user)
    return None


# --- Routines ---
@router.get("/routines", response_model=List[RoutineResponse])
def list_routines(
    patient_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CareService(db)
    return service.list_routines(patient_id, current_user)


@router.post("/routines", response_model=RoutineResponse, status_code=status.HTTP_201_CREATED)
def create_routine(
    patient_id: str,
    data: RoutineCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CareService(db)
    return service.create_routine(patient_id, current_user, data)


# --- Reminders ---
@router.get("/reminders/today", response_model=List[ReminderResponse])
def get_today_reminders(
    patient_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CareService(db)
    return service.get_today_reminders(patient_id, current_user)


@router.post("/reminders", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
def create_custom_reminder(
    patient_id: str,
    data: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CareService(db)
    return service.create_custom_reminder(patient_id, current_user, data)


@router.post("/reminders/{reminder_id}/acknowledge", response_model=ReminderResponse)
def acknowledge_reminder(
    patient_id: str,
    reminder_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CareService(db)
    return service.acknowledge_reminder(patient_id, reminder_id, current_user)


@router.post("/reminders/{reminder_id}/snooze", response_model=ReminderResponse)
def snooze_reminder(
    patient_id: str,
    reminder_id: str,
    data: ReminderActionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CareService(db)
    return service.snooze_reminder(patient_id, reminder_id, data.snooze_minutes or 15, current_user)


@router.post("/reminders/{reminder_id}/skip", response_model=ReminderResponse)
def skip_reminder(
    patient_id: str,
    reminder_id: str,
    data: ReminderActionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CareService(db)
    return service.skip_reminder(patient_id, reminder_id, data.reason, current_user)
