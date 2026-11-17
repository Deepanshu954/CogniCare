from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.models.document import MedicalDocument


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, document: MedicalDocument) -> MedicalDocument:
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_by_id(self, document_id: str) -> Optional[MedicalDocument]:
        return self.db.execute(
            select(MedicalDocument).where(
                MedicalDocument.id == document_id,
                MedicalDocument.is_archived.is_(False),
            )
        ).scalar_one_or_none()

    def list_by_patient(
        self, patient_id: str, document_type: Optional[str] = None
    ) -> List[MedicalDocument]:
        stmt = select(MedicalDocument).where(
            MedicalDocument.patient_id == patient_id,
            MedicalDocument.is_archived.is_(False),
        )
        if document_type:
            stmt = stmt.where(MedicalDocument.document_type == document_type.upper())
        stmt = stmt.order_by(desc(MedicalDocument.created_at))
        return list(self.db.execute(stmt).scalars().all())

    def update(self, document: MedicalDocument) -> MedicalDocument:
        self.db.commit()
        self.db.refresh(document)
        return document

    def delete(self, document: MedicalDocument) -> None:
        document.is_archived = True
        self.db.commit()
