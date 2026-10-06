from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User, Profile
from app.models.patient import PatientProfile


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email.lower().strip()).first()

    def create(
        self,
        email: str,
        password_hash: str,
        role: str,
        display_name: str,
        phone_number: Optional[str] = None,
        preferred_language: str = "en",
        emergency_notes: Optional[str] = None,
    ) -> User:
        user = User(
            email=email.lower().strip(),
            password_hash=password_hash,
            role=role,
            status="ACTIVE",
        )
        self.db.add(user)
        self.db.flush()

        profile = Profile(
            user_id=user.id,
            display_name=display_name,
            phone_number=phone_number,
            preferred_language=preferred_language,
            timezone="UTC",
        )
        self.db.add(profile)

        # If user is elderly, automatically create PatientProfile
        if role == "ELDERLY":
            patient_profile = PatientProfile(
                user_id=user.id,
                emergency_notes=emergency_notes,
                accessibility_preferences={
                    "high_contrast": True,
                    "large_text": True,
                    "speech_speed": 1.0,
                    "voice_guidance": True,
                },
                care_preferences={
                    "preferred_wake_time": "08:00",
                    "preferred_sleep_time": "21:30",
                },
            )
            self.db.add(patient_profile)

        self.db.commit()
        self.db.refresh(user)
        return user
