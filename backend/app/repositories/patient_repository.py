from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.patient import PatientProfile, CaregiverLink, EmergencyContact, Consent
from app.models.user import User, Profile
from app.models.care import Medication, Reminder
from app.models.safety import Alert


class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, patient_id: str) -> Optional[PatientProfile]:
        return self.db.query(PatientProfile).filter(PatientProfile.id == patient_id).first()

    def get_by_user_id(self, user_id: str) -> Optional[PatientProfile]:
        return self.db.query(PatientProfile).filter(PatientProfile.user_id == user_id).first()

    def list_by_caregiver(self, caregiver_user_id: str) -> List[PatientProfile]:
        links = (
            self.db.query(CaregiverLink)
            .filter(CaregiverLink.caregiver_user_id == caregiver_user_id, CaregiverLink.status == "ACTIVE")
            .all()
        )
        patient_ids = [link.patient_id for link in links]
        if not patient_ids:
            return []
        return self.db.query(PatientProfile).filter(PatientProfile.id.in_(patient_ids)).all()

    def list_all(self) -> List[PatientProfile]:
        return self.db.query(PatientProfile).all()

    def check_access(self, user: User, patient_id: str, required_permission: Optional[str] = None) -> bool:
        if user.role == "ADMIN":
            return True
        if user.role == "ELDERLY":
            profile = self.get_by_id(patient_id)
            return profile is not None and profile.user_id == user.id
        if user.role in ["CAREGIVER", "REVIEWER"]:
            link = (
                self.db.query(CaregiverLink)
                .filter(
                    CaregiverLink.patient_id == patient_id,
                    CaregiverLink.caregiver_user_id == user.id,
                    CaregiverLink.status == "ACTIVE",
                )
                .first()
            )
            if not link:
                return False
            if required_permission:
                perms = link.permissions or []
                return required_permission in perms
            return True
        return False

    def create_patient_with_profile(
        self,
        email: str,
        password_hash: str,
        display_name: str,
        phone_number: Optional[str],
        emergency_notes: Optional[str],
        accessibility_preferences: dict,
        care_preferences: dict,
    ) -> PatientProfile:
        user = User(
            email=email.lower().strip(),
            password_hash=password_hash,
            role="ELDERLY",
            status="ACTIVE",
        )
        self.db.add(user)
        self.db.flush()

        profile = Profile(
            user_id=user.id,
            display_name=display_name,
            phone_number=phone_number,
            preferred_language="en",
            timezone="UTC",
        )
        self.db.add(profile)

        patient = PatientProfile(
            user_id=user.id,
            emergency_notes=emergency_notes,
            accessibility_preferences=accessibility_preferences,
            care_preferences=care_preferences,
        )
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def add_caregiver_link(
        self,
        patient_id: str,
        caregiver_user_id: str,
        relationship_type: str,
        permissions: List[str],
    ) -> CaregiverLink:
        existing = (
            self.db.query(CaregiverLink)
            .filter(CaregiverLink.patient_id == patient_id, CaregiverLink.caregiver_user_id == caregiver_user_id)
            .first()
        )
        if existing:
            existing.status = "ACTIVE"
            existing.permissions = permissions
            existing.relationship_type = relationship_type
            self.db.commit()
            return existing

        link = CaregiverLink(
            patient_id=patient_id,
            caregiver_user_id=caregiver_user_id,
            relationship_type=relationship_type,
            permissions=permissions,
            status="ACTIVE",
        )
        self.db.add(link)
        self.db.commit()
        self.db.refresh(link)
        return link

    def add_emergency_contact(
        self,
        patient_id: str,
        name: str,
        relationship_type: str,
        phone: str,
        email: Optional[str],
        priority: int,
    ) -> EmergencyContact:
        contact = EmergencyContact(
            patient_id=patient_id,
            name=name,
            relationship_type=relationship_type,
            phone=phone,
            email=email,
            priority=priority,
            is_active=True,
        )
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def add_consent(self, patient_id: str, purpose: str, policy_version: str, granted: bool) -> Consent:
        consent = Consent(
            patient_id=patient_id,
            purpose=purpose,
            policy_version=policy_version,
            granted=granted,
        )
        self.db.add(consent)
        self.db.commit()
        self.db.refresh(consent)
        return consent
