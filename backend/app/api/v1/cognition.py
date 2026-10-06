from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.cognition import (
    CognitiveActivityResponse,
    ActivitySessionResponse,
    StartSessionRequest,
    SessionAnswerRequest,
    SessionAnswerResponse,
    CognitiveOverviewResponse,
    CognitiveTrendPoint,
    SupportSignalResponse,
)
from app.services.cognition_service import CognitionService

activities_router = APIRouter(prefix="/activities", tags=["Cognitive Activities Catalog"])
cognition_router = APIRouter(prefix="/patients/{patient_id}", tags=["Cognitive Health & Sessions"])


@activities_router.get("", response_model=List[CognitiveActivityResponse])
def list_activities(
    db: Session = Depends(get_db),
):
    service = CognitionService(db)
    return service.list_activities()


@cognition_router.post("/activity-sessions", response_model=ActivitySessionResponse, status_code=status.HTTP_201_CREATED)
def start_session(
    patient_id: str,
    data: StartSessionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CognitionService(db)
    return service.start_session(
        patient_id=patient_id,
        activity_id=data.activity_id,
        difficulty=data.difficulty or 1,
        current_user=current_user,
    )


@cognition_router.post("/activity-sessions/{session_id}/answers", response_model=SessionAnswerResponse)
def submit_session_answer(
    patient_id: str,
    session_id: str,
    data: SessionAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CognitionService(db)
    return service.submit_answer(session_id=session_id, data=data, current_user=current_user)


@cognition_router.post("/activity-sessions/{session_id}/complete", response_model=ActivitySessionResponse)
def complete_session(
    patient_id: str,
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CognitionService(db)
    return service.complete_session(session_id=session_id, current_user=current_user)


@cognition_router.get("/cognition/overview", response_model=CognitiveOverviewResponse)
def get_cognitive_overview(
    patient_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CognitionService(db)
    return service.get_overview(patient_id=patient_id, current_user=current_user)


@cognition_router.get("/cognition/trends", response_model=List[CognitiveTrendPoint])
def get_cognitive_trends(
    patient_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CognitionService(db)
    return service.get_trends(patient_id=patient_id, current_user=current_user)


@cognition_router.get("/cognition/signals", response_model=List[SupportSignalResponse])
def get_support_signals(
    patient_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = CognitionService(db)
    return service.get_signals(patient_id=patient_id, current_user=current_user)
