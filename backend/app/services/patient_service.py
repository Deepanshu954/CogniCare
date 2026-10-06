import uuid
from typing import List
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.repositories.patient_repository import PatientRepository
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.patient import PatientProfile
from app.models.care import Medication, Reminder
from app.models.safety import Alert
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
from app.core.security import hash_password
from app.core.exceptions import NotFoundException, ForbiddenException, ConflictException, BadRequestException


class PatientService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PatientRepository(db)
        self.user_repo = UserRepository(db)

    def list_accessible_patients(self, current_user: User) -> List[PatientDetailResponse]:
        if current_user.role == "ELDERLY":
            profile = self.repo.get_by_user_id(current_user.id)
            return [self._to_detail_response(profile)] if profile else []
        elif current_user.role in ["CAREGIVER", "REVIEWER"]:
            profiles = self.repo.list_by_caregiver(current_user.id)
            return [self._to_detail_response(p) for p in profiles]
        elif current_user.role == "ADMIN":
            profiles = self.repo.list_all()
            return [self._to_detail_response(p) for p in profiles]
        return []

    def get_patient(self, patient_id: str, current_user: User) -> PatientDetailResponse:
        if not self.repo.check_access(current_user, patient_id):
            raise ForbiddenException(message="Access denied to this patient profile.")

        patient = self.repo.get_by_id(patient_id)
        if not patient:
            raise NotFoundException(message="Patient profile not found.")

        return self._to_detail_response(patient)

    def create_patient_by_caregiver(self, current_user: User, data: PatientCreateRequest) -> PatientDetailResponse:
        email = data.email or f"patient_{uuid.uuid4().hex[:8]}@cognicare.local"
        existing = self.user_repo.get_by_email(email)
        if existing:
            raise ConflictException(message="An account with this email already exists.")

        pwd_hash = hash_password("ElderlyTempPassword123!")
        patient = self.repo.create_patient_with_profile(
            email=email,
            password_hash=pwd_hash,
            display_name=data.display_name,
            phone_number=data.phone_number,
            emergency_notes=data.emergency_notes,
            accessibility_preferences=data.accessibility_preferences or {
                "high_contrast": True,
                "large_text": True,
                "speech_speed": 1.0,
                "voice_guidance": True,
            },
            care_preferences=data.care_preferences or {},
        )

        # Link caregiver automatically
        self.repo.add_caregiver_link(
            patient_id=patient.id,
            caregiver_user_id=current_user.id,
            relationship_type="Primary Caregiver",
            permissions=["VIEW_PROFILE", "VIEW_COGNITION", "VIEW_REMINDERS", "MANAGE_REMINDERS", "VIEW_ALERTS", "MANAGE_ALERTS", "VIEW_REPORTS"],
        )

        return self._to_detail_response(patient)

    def update_patient(self, patient_id: str, current_user: User, data: PatientUpdateRequest) -> PatientDetailResponse:
        if not self.repo.check_access(current_user, patient_id, required_permission="MANAGE_REMINDERS"):
            raise ForbiddenException(message="Access denied to update patient settings.")

        patient = self.repo.get_by_id(patient_id)
        if not patient:
            raise NotFoundException(message="Patient not found.")

        if data.display_name and patient.user and patient.user.profile:
            patient.user.profile.display_name = data.display_name

        if data.emergency_notes is not None:
            patient.emergency_notes = data.emergency_notes

        if data.accessibility_preferences is not None:
            patient.accessibility_preferences = {
                **(patient.accessibility_preferences or {}),
                **data.accessibility_preferences,
            }

        if data.care_preferences is not None:
            patient.care_preferences = {
                **(patient.care_preferences or {}),
                **data.care_preferences,
            }

        self.db.commit()
        self.db.refresh(patient)
        return self._to_detail_response(patient)

    def invite_caregiver(self, patient_id: str, current_user: User, data: CaregiverInviteRequest) -> CaregiverLinkResponse:
        if not self.repo.check_access(current_user, patient_id):
            raise ForbiddenException(message="Access denied to invite caregivers for this patient.")

        caregiver = self.user_repo.get_by_email(data.caregiver_email)
        if not caregiver:
            # Create caregiver user placeholder if not exists
            pwd_hash = hash_password("CaregiverTemp123!")
            caregiver = self.user_repo.create(
                email=data.caregiver_email,
                password_hash=pwd_hash,
                role="CAREGIVER",
                display_name=data.caregiver_email.split("@")[0].capitalize(),
            )

        link = self.repo.add_caregiver_link(
            patient_id=patient_id,
            caregiver_user_id=caregiver.id,
            relationship_type=data.relationship_type,
            permissions=data.permissions,
        )

        return CaregiverLinkResponse(
            id=link.id,
            caregiver_user_id=caregiver.id,
            caregiver_email=caregiver.email,
            caregiver_name=caregiver.profile.display_name if caregiver.profile else None,
            relationship_type=link.relationship_type,
            permissions=link.permissions or [],
            status=link.status,
            created_at=link.created_at,
        )

    def add_emergency_contact(self, patient_id: str, current_user: User, data: EmergencyContactCreate) -> EmergencyContactResponse:
        if not self.repo.check_access(current_user, patient_id):
            raise ForbiddenException(message="Access denied to manage emergency contacts.")

        contact = self.repo.add_emergency_contact(
            patient_id=patient_id,
            name=data.name,
            relationship_type=data.relationship_type,
            phone=data.phone,
            email=data.email,
            priority=data.priority,
        )
        return EmergencyContactResponse.model_validate(contact)

    def add_consent(self, patient_id: str, current_user: User, data: ConsentCreate) -> ConsentResponse:
        if not self.repo.check_access(current_user, patient_id):
            raise ForbiddenException(message="Access denied to modify consent.")

        consent = self.repo.add_consent(
            patient_id=patient_id,
            purpose=data.purpose,
            policy_version=data.policy_version,
            granted=data.granted,
        )
        return ConsentResponse.model_validate(consent)

    def get_patient_summary(self, patient_id: str, current_user: User) -> PatientSummaryResponse:
        if not self.repo.check_access(current_user, patient_id):
            raise ForbiddenException(message="Access denied to patient summary.")

        patient = self.repo.get_by_id(patient_id)
        if not patient:
            raise NotFoundException(message="Patient profile not found.")

        total_meds = self.db.query(Medication).filter(Medication.patient_id == patient_id, Medication.active == True).count()
        today_reminders = self.db.query(Reminder).filter(Reminder.patient_id == patient_id).all()
        today_count = len(today_reminders)
        completed_count = sum(1 for r in today_reminders if r.status in ["ACKNOWLEDGED"])
        adherence_pct = (completed_count / today_count * 100.0) if today_count > 0 else 100.0

        open_alerts = self.db.query(Alert).filter(Alert.patient_id == patient_id, Alert.status.in_(["OPEN", "ESCALATED"])).count()

        status_str = "EXCELLENT"
        if open_alerts > 0:
            status_str = "CRITICAL_ALERT"
        elif adherence_pct < 80.0:
            status_str = "ATTENTION_NEEDED"

        name = patient.user.profile.display_name if patient.user and patient.user.profile else "Patient"

        return PatientSummaryResponse(
            id=patient.id,
            display_name=name,
            total_medications=total_meds,
            today_reminders_count=today_count,
            today_completed_reminders=completed_count,
            adherence_percentage=round(adherence_pct, 1),
            open_alerts_count=open_alerts,
            status=status_str,
        )

    def _to_detail_response(self, patient: PatientProfile) -> PatientDetailResponse:
        display_name = patient.user.profile.display_name if patient.user and patient.user.profile else "Patient"
        email = patient.user.email if patient.user else ""
        phone = patient.user.profile.phone_number if patient.user and patient.user.profile else None

        caregiver_responses = []
        for link in patient.caregiver_links:
            cg_user = self.user_repo.get_by_id(link.caregiver_user_id)
            caregiver_responses.append(
                CaregiverLinkResponse(
                    id=link.id,
                    caregiver_user_id=link.caregiver_user_id,
                    caregiver_email=cg_user.email if cg_user else None,
                    caregiver_name=cg_user.profile.display_name if cg_user and cg_user.profile else None,
                    relationship_type=link.relationship_type,
                    permissions=link.permissions or [],
                    status=link.status,
                    created_at=link.created_at,
                )
            )

        return PatientDetailResponse(
            id=patient.id,
            user_id=patient.user_id,
            display_name=display_name,
            email=email,
            phone_number=phone,
            emergency_notes=patient.emergency_notes,
            accessibility_preferences=patient.accessibility_preferences or {},
            care_preferences=patient.care_preferences or {},
            emergency_contacts=[EmergencyContactResponse.model_validate(c) for c in patient.emergency_contacts if c.is_active],
            consents=[ConsentResponse.model_validate(c) for c in patient.consents],
            caregivers=caregiver_responses,
            created_at=patient.created_at,
        )
