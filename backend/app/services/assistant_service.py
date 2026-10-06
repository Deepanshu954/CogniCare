from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.models.assistant import Conversation, Message, MemoryItem
from app.models.patient import PatientProfile
from app.models.user import User
from app.repositories.patient_repository import PatientRepository
from app.services.care_service import CareService
from app.schemas.assistant import (
    ConversationResponse,
    MessageResponse,
    MemoryItemCreate,
    MemoryItemResponse,
)
from app.ai.factory import get_ai_provider
from app.ai.gemini_provider import GeminiProvider
from app.ai.context_builder import build_system_prompt
from app.core.exceptions import NotFoundException, ForbiddenException


class AssistantService:
    def __init__(self, db: Session):
        self.db = db
        self.patient_repo = PatientRepository(db)
        self.care_service = CareService(db)
        self.ai_provider = get_ai_provider()
        self.gemini_provider = GeminiProvider()

    def _check_access(self, current_user: User, patient_id: str):
        if not self.patient_repo.check_access(current_user, patient_id):
            raise ForbiddenException(message="Access denied to patient assistant.")

    def get_or_create_conversation(self, patient_id: str, current_user: User) -> ConversationResponse:
        self._check_access(current_user, patient_id)

        conv = (
            self.db.query(Conversation)
            .filter(Conversation.patient_id == patient_id, Conversation.status == "ACTIVE")
            .order_by(Conversation.created_at.desc())
            .first()
        )
        if not conv:
            conv = Conversation(
                patient_id=patient_id,
                started_by_user_id=current_user.id,
                title="Daily Care Companion",
                status="ACTIVE",
            )
            self.db.add(conv)
            self.db.commit()
            self.db.refresh(conv)

        return self._to_conversation_response(conv)

    def list_conversations(self, patient_id: str, current_user: User) -> List[ConversationResponse]:
        self._check_access(current_user, patient_id)
        convs = (
            self.db.query(Conversation)
            .filter(Conversation.patient_id == patient_id)
            .order_by(Conversation.created_at.desc())
            .all()
        )
        return [self._to_conversation_response(c) for c in convs]

    def send_message(
        self,
        patient_id: str,
        conversation_id: str,
        user_content: str,
        current_user: User,
        mode: str = "normal",
    ) -> MessageResponse:
        self._check_access(current_user, patient_id)

        conv = self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv or conv.patient_id != patient_id:
            raise NotFoundException(message="Conversation not found.")

        # 1. Save user message
        user_msg = Message(
            conversation_id=conv.id,
            role="USER",
            content=user_content,
            content_type="TEXT",
        )
        self.db.add(user_msg)
        self.db.commit()

        # 2. Build Rich Dual Context (Public Geriatric + Private Patient Data)
        system_prompt = build_system_prompt(patient_id, self.db, mode=mode)

        # 3. Call Multi-Mode Gemini Provider
        ai_res = self.gemini_provider.generate_assistant_reply(
            system_prompt=system_prompt,
            user_message=user_content,
            mode=mode,
        )

        metadata = {
            "active_model": ai_res.get("active_model"),
            "mode": mode,
            "thinking_trace": ai_res.get("thinking_trace"),
            "provider": ai_res.get("provider"),
        }

        # 4. Save assistant reply
        assist_msg = Message(
            conversation_id=conv.id,
            role="ASSISTANT",
            content=ai_res["reply"],
            content_type="TEXT",
            tool_calls=metadata,
        )
        self.db.add(assist_msg)
        self.db.commit()
        self.db.refresh(assist_msg)

        res = MessageResponse.model_validate(assist_msg)
        res.active_model = ai_res.get("active_model")
        res.thinking_trace = ai_res.get("thinking_trace")
        return res

    def list_memory_items(self, patient_id: str, current_user: User) -> List[MemoryItemResponse]:
        self._check_access(current_user, patient_id)
        items = (
            self.db.query(MemoryItem)
            .filter(MemoryItem.patient_id == patient_id, MemoryItem.is_active == True)
            .all()
        )
        return [MemoryItemResponse.model_validate(i) for i in items]

    def create_memory_item(self, patient_id: str, data: MemoryItemCreate, current_user: User) -> MemoryItemResponse:
        self._check_access(current_user, patient_id)
        item = MemoryItem(
            patient_id=patient_id,
            memory_type=data.memory_type,
            content=data.content,
            sensitivity=data.sensitivity,
            is_active=True,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return MemoryItemResponse.model_validate(item)

    def _build_context(self, patient_id: str, current_user: User) -> Dict[str, Any]:
        patient = self.patient_repo.get_by_id(patient_id)
        name = patient.user.profile.display_name if patient and patient.user and patient.user.profile else "Friend"

        today_reminders = self.care_service.get_today_reminders(patient_id, current_user)
        formatted_reminders = [
            {
                "id": r.id,
                "title": r.title,
                "status": r.status,
                "priority": r.priority,
                "time": r.scheduled_for.strftime("%I:%M %p"),
                "source_type": r.source_type,
            }
            for r in today_reminders
        ]

        memories = (
            self.db.query(MemoryItem)
            .filter(MemoryItem.patient_id == patient_id, MemoryItem.is_active == True)
            .all()
        )
        memory_texts = [m.content for m in memories]

        return {
            "patient_name": name,
            "today_reminders": formatted_reminders,
            "memories": memory_texts,
            "accessibility_preferences": patient.accessibility_preferences if patient else {},
        }

    def _to_conversation_response(self, conv: Conversation) -> ConversationResponse:
        messages = (
            self.db.query(Message)
            .filter(Message.conversation_id == conv.id)
            .order_by(Message.created_at.asc())
            .all()
        )
        return ConversationResponse(
            id=conv.id,
            patient_id=conv.patient_id,
            title=conv.title,
            status=conv.status,
            messages=[MessageResponse.model_validate(m) for m in messages],
            created_at=conv.created_at,
        )
