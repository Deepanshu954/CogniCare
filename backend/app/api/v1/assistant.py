from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.assistant import (
    ConversationResponse,
    MessageCreate,
    MessageResponse,
    MemoryItemCreate,
    MemoryItemResponse,
)
from app.services.assistant_service import AssistantService

router = APIRouter(prefix="/patients/{patient_id}", tags=["AI Assistant & Memory"])


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def get_or_create_conversation(
    patient_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AssistantService(db)
    return service.get_or_create_conversation(patient_id, current_user)


@router.get("/conversations", response_model=List[ConversationResponse])
def list_conversations(
    patient_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AssistantService(db)
    return service.list_conversations(patient_id, current_user)


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
def send_assistant_message(
    patient_id: str,
    conversation_id: str,
    data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AssistantService(db)
    return service.send_message(
        patient_id=patient_id,
        conversation_id=conversation_id,
        user_content=data.content,
        mode=data.mode or "normal",
        current_user=current_user,
    )


@router.get("/memory", response_model=List[MemoryItemResponse])
def list_memory_items(
    patient_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AssistantService(db)
    return service.list_memory_items(patient_id, current_user)


@router.post("/memory", response_model=MemoryItemResponse, status_code=status.HTTP_201_CREATED)
def create_memory_item(
    patient_id: str,
    data: MemoryItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AssistantService(db)
    return service.create_memory_item(patient_id, data, current_user)
