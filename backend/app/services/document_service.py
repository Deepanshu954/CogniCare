import os
import base64
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.repositories.patient_repository import PatientRepository
from app.models.document import MedicalDocument
from app.models.user import User
from app.models.audit import AuditLog
from app.schemas.document import DocumentCreateRequest, DocumentUpdateRequest, DocumentResponse
from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException


# Allowed MIME types for PDF and images
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/webp",
}

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads", "documents")


class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = DocumentRepository(db)
        self.patient_repo = PatientRepository(db)
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    def _check_access(self, current_user: User, patient_id: str, write: bool = False):
        if not self.patient_repo.check_access(current_user, patient_id):
            raise ForbiddenException(message="Access denied to patient medical documents.")

    def list_documents(
        self, patient_id: str, current_user: User, document_type: Optional[str] = None
    ) -> List[DocumentResponse]:
        self._check_access(current_user, patient_id, write=False)
        docs = self.repo.list_by_patient(patient_id, document_type)
        return [DocumentResponse.model_validate(d) for d in docs]

    def create_document(
        self, patient_id: str, current_user: User, data: DocumentCreateRequest
    ) -> DocumentResponse:
        self._check_access(current_user, patient_id, write=True)

        # Validate file type
        file_type_lower = data.file_type.lower()
        if file_type_lower not in ALLOWED_MIME_TYPES and not file_type_lower.startswith("image/"):
            raise BadRequestException(
                message=f"Unsupported file type: {data.file_type}. Only PDFs and images are accepted."
            )

        # If data URI is supplied, save to local disk file as well
        saved_file_path = None
        if data.file_data_url and "," in data.file_data_url:
            try:
                header, encoded = data.file_data_url.split(",", 1)
                file_bytes = base64.b64decode(encoded)
                safe_name = f"{patient_id}_{int(data.file_size_bytes or 0)}_{data.file_name.replace('/', '_')}"
                saved_file_path = os.path.join(UPLOAD_DIR, safe_name)
                with open(saved_file_path, "wb") as f:
                    f.write(file_bytes)
            except Exception as e:
                # Log and fallback to storing in data_url
                pass

        doc = MedicalDocument(
            patient_id=patient_id,
            uploader_user_id=current_user.id,
            title=data.title.strip(),
            document_type=data.document_type.upper(),
            doctor_name=data.doctor_name.strip() if data.doctor_name else None,
            document_date=data.document_date.strip() if data.document_date else None,
            notes=data.notes.strip() if data.notes else None,
            file_name=data.file_name,
            file_type=data.file_type,
            file_size_bytes=data.file_size_bytes,
            file_path=saved_file_path,
            file_data_url=data.file_data_url,
        )
        saved_doc = self.repo.create(doc)

        # Record Audit Log
        audit = AuditLog(
            actor_user_id=current_user.id,
            patient_id=patient_id,
            action="UPLOAD_MEDICAL_DOCUMENT",
            resource_type="MEDICAL_DOCUMENT",
            resource_id=saved_doc.id,
            details={
                "title": saved_doc.title,
                "document_type": saved_doc.document_type,
                "file_name": saved_doc.file_name,
                "file_size": saved_doc.file_size_bytes,
            },
        )
        self.db.add(audit)
        self.db.commit()

        return DocumentResponse.model_validate(saved_doc)

    def get_document(
        self, patient_id: str, document_id: str, current_user: User
    ) -> DocumentResponse:
        self._check_access(current_user, patient_id, write=False)
        doc = self.repo.get_by_id(document_id)
        if not doc or doc.patient_id != patient_id:
            raise NotFoundException(message="Medical document not found.")
        return DocumentResponse.model_validate(doc)

    def get_document_file_payload(
        self, patient_id: str, document_id: str, current_user: User
    ) -> Tuple[bytes, str, str]:
        """Returns (file_bytes, mime_type, filename)"""
        self._check_access(current_user, patient_id, write=False)
        doc = self.repo.get_by_id(document_id)
        if not doc or doc.patient_id != patient_id:
            raise NotFoundException(message="Medical document not found.")

        # If on disk
        if doc.file_path and os.path.exists(doc.file_path):
            with open(doc.file_path, "rb") as f:
                return f.read(), doc.file_type, doc.file_name

        # If stored as data URL
        if doc.file_data_url and "," in doc.file_data_url:
            _, encoded = doc.file_data_url.split(",", 1)
            return base64.b64decode(encoded), doc.file_type, doc.file_name

        raise NotFoundException(message="Document file content not found.")

    def delete_document(
        self, patient_id: str, document_id: str, current_user: User
    ) -> None:
        self._check_access(current_user, patient_id, write=True)
        doc = self.repo.get_by_id(document_id)
        if not doc or doc.patient_id != patient_id:
            raise NotFoundException(message="Medical document not found.")

        self.repo.delete(doc)

        audit = AuditLog(
            actor_user_id=current_user.id,
            patient_id=patient_id,
            action="DELETE_MEDICAL_DOCUMENT",
            resource_type="MEDICAL_DOCUMENT",
            resource_id=doc.id,
            details={"title": doc.title, "document_type": doc.document_type},
        )
        self.db.add(audit)
        self.db.commit()
