from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.report import ReportResponse
from app.services.report_service import ReportService

router = APIRouter(prefix="/patients/{patient_id}/reports", tags=["Reports & Summaries"])


@router.get("", response_model=List[ReportResponse])
def list_reports(
    patient_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ReportService(db)
    return service.list_reports(patient_id, current_user)


@router.post("/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def generate_weekly_report(
    patient_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ReportService(db)
    return service.generate_weekly_report(patient_id, current_user)


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    patient_id: str,
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ReportService(db)
    return service.get_report(patient_id, report_id, current_user)
