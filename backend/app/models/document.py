from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship as orm_relationship
from app.models.base import TimeStampedModel


class MedicalDocument(TimeStampedModel):
    __tablename__ = "medical_documents"

    patient_id = Column(
        String(36),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    uploader_user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    title = Column(String(255), nullable=False)
    document_type = Column(
        String(50),
        nullable=False,
        default="PRESCRIPTION",
    )  # PRESCRIPTION, MEDICAL_CONDITION, LAB_REPORT, CLINICAL_NOTE, EMERGENCY_PLAN, OTHER
    doctor_name = Column(String(255), nullable=True)
    document_date = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(100), nullable=False)  # application/pdf, image/png, image/jpeg, etc.
    file_size_bytes = Column(Integer, default=0)
    file_path = Column(String(500), nullable=True)
    file_data_url = Column(Text, nullable=True)  # base64 data URI for instant standalone preview
    is_archived = Column(Boolean, default=False)

    patient = orm_relationship("PatientProfile", back_populates="documents")
    uploader = orm_relationship("User", foreign_keys=[uploader_user_id])
