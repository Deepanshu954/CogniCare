from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DocumentCreateRequest(BaseModel):
    title: str
    document_type: str = "PRESCRIPTION"  # PRESCRIPTION, MEDICAL_CONDITION, LAB_REPORT, CLINICAL_NOTE, EMERGENCY_PLAN, OTHER
    doctor_name: Optional[str] = None
    document_date: Optional[str] = None
    notes: Optional[str] = None
    file_name: str
    file_type: str  # application/pdf, image/png, image/jpeg, etc.
    file_size_bytes: int = 0
    file_data_url: Optional[str] = None  # base64 data URI (data:image/png;base64,... or data:application/pdf;base64,...)


class DocumentUpdateRequest(BaseModel):
    title: Optional[str] = None
    document_type: Optional[str] = None
    doctor_name: Optional[str] = None
    document_date: Optional[str] = None
    notes: Optional[str] = None


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    patient_id: str
    uploader_user_id: Optional[str] = None
    title: str
    document_type: str
    doctor_name: Optional[str] = None
    document_date: Optional[str] = None
    notes: Optional[str] = None
    file_name: str
    file_type: str
    file_size_bytes: int
    file_data_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
