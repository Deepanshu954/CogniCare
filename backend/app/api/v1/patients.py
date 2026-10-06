from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.patient import (
    PatientCreateRequest,
    PatientUpdateRequest,
    PatientDetailResponse,
    PatientSummaryResponse,
    EmergencyContactCreate,
    EmergencyContactResponse,
    ConsentCreate,
    ConsentResponse,
    CaregiverInviteRequest,
    CaregiverLinkResponse,
)
from app.services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["Patients & Caregivers"])


@router.get("", response_model=List[PatientDetailResponse])
def list_patients(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PatientService(db)
    return service.list_accessible_patients(current_user)


@router.post("", response_model=PatientDetailResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    data: PatientCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PatientService(db)
    return service.create_patient_by_caregiver(current_user, data)


@router.get("/{patient_id}", response_model=PatientDetailResponse)
def get_patient_details(
    patient_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PatientService(db)
    return service.get_patient(patient_id, current_user)


@router.patch("/{patient_id}", response_model=PatientDetailResponse)
def update_patient_preferences(
    patient_id: str,
    data: PatientUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PatientService(db)
    return service.update_patient(patient_id, current_user, data)


@router.post("/{patient_id}/caregivers/invite", response_model=CaregiverLinkResponse)
def invite_caregiver(
    patient_id: str,
    data: CaregiverInviteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PatientService(db)
    return service.invite_caregiver(patient_id, current_user, data)


@router.post("/{patient_id}/emergency-contacts", response_model=EmergencyContactResponse)
def add_emergency_contact(
    patient_id: str,
    data: EmergencyContactCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PatientService(db)
    return service.add_emergency_contact(patient_id, current_user, data)


@router.post("/{patient_id}/consents", response_model=ConsentResponse)
def add_consent(
    patient_id: str,
    data: ConsentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PatientService(db)
    return service.add_consent(patient_id, current_user, data)


@router.get("/{patient_id}/summary", response_model=PatientSummaryResponse)
def get_patient_summary(
    patient_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PatientService(db)
    return service.get_patient_summary(patient_id, current_user)
