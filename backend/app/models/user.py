from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedModel


class User(TimeStampedModel):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="ELDERLY")  # ELDERLY, CAREGIVER, REVIEWER, ADMIN
    status = Column(String(50), nullable=False, default="ACTIVE")  # ACTIVE, SUSPENDED, DELETED
    email_verified_at = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)

    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    patient_profile = relationship("PatientProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    caregiver_links = relationship("CaregiverLink", back_populates="caregiver", foreign_keys="CaregiverLink.caregiver_user_id")


class Profile(TimeStampedModel):
    __tablename__ = "profiles"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    display_name = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=True)
    date_of_birth = Column(String(20), nullable=True)
    preferred_language = Column(String(10), default="en", nullable=False)
    timezone = Column(String(50), default="UTC", nullable=False)
    avatar_url = Column(String(500), nullable=True)

    user = relationship("User", back_populates="profile")
