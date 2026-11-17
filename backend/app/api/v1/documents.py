import base64
from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query, UploadFile, File, Form, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.document import DocumentCreateRequest, DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/patients/{patient_id}/documents", tags=["Medical Documents & Prescriptions"])


@router.get("", response_model=List[DocumentResponse])
def list_patient_documents(
    patient_id: str,
    document_type: Optional[str] = Query(None, description="Filter by type: PRESCRIPTION, MEDICAL_CONDITION, LAB_REPORT, CLINICAL_NOTE, etc."),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    return service.list_documents(patient_id, current_user, document_type)


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_patient_document(
    patient_id: str,
    data: DocumentCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    return service.create_document(patient_id, current_user, data)


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_patient_document_file(
    patient_id: str,
    file: UploadFile = File(...),
    title: str = Form(...),
    document_type: str = Form("PRESCRIPTION"),
    doctor_name: Optional[str] = Form(None),
    document_date: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_bytes = await file.read()
    file_mime = file.content_type or "application/octet-stream"
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    data_url = f"data:{file_mime};base64,{encoded}"

    data = DocumentCreateRequest(
        title=title,
        document_type=document_type,
        doctor_name=doctor_name,
        document_date=document_date,
        notes=notes,
        file_name=file.filename or "document.pdf",
        file_type=file_mime,
        file_size_bytes=len(file_bytes),
        file_data_url=data_url,
    )
    service = DocumentService(db)
    return service.create_document(patient_id, current_user, data)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_patient_document(
    patient_id: str,
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    return service.get_document(patient_id, document_id, current_user)


@router.get("/{document_id}/file")
def download_patient_document_file(
    patient_id: str,
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    file_bytes, mime_type, file_name = service.get_document_file_payload(
        patient_id, document_id, current_user
    )
    return Response(
        content=file_bytes,
        media_type=mime_type,
        headers={"Content-Disposition": f'inline; filename="{file_name}"'},
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient_document(
    patient_id: str,
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    service.delete_document(patient_id, document_id, current_user)
    return None
