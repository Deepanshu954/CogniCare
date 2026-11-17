import os
import re
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.core.config import settings
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
    ApiKeyStatusResponse,
)
from app.ai.factory import get_ai_provider
from app.ai.gemini_provider import GeminiProvider
from app.ai.context_builder import build_system_prompt
from app.core.exceptions import NotFoundException, ForbiddenException

logger = logging.getLogger(__name__)


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
        attachment: Optional[Dict[str, Any]] = None,
    ) -> MessageResponse:
        self._check_access(current_user, patient_id)

        conv = self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv or conv.patient_id != patient_id:
            raise NotFoundException(message="Conversation not found.")

        user_tool_calls = {}
        if attachment and (attachment.get("attachment_url") or attachment.get("attachment_data_url") or attachment.get("attachment_name")):
            user_tool_calls["attachment"] = {
                "url": attachment.get("attachment_url"),
                "name": attachment.get("attachment_name"),
                "type": attachment.get("attachment_type"),
                "data_url": attachment.get("attachment_data_url"),
            }

        # 1. Save user message
        display_content = user_content.strip() if user_content else ""
        if not display_content and attachment and attachment.get("attachment_name"):
            display_content = f"Uploaded {attachment['attachment_name']}"

        user_msg = Message(
            conversation_id=conv.id,
            role="USER",
            content=display_content or "Hello",
            content_type="ATTACHMENT" if user_tool_calls.get("attachment") else "TEXT",
            tool_calls=user_tool_calls if user_tool_calls else None,
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
            attachment=attachment,
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

        return self._to_message_response(assist_msg)

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

    def _to_message_response(self, m: Message) -> MessageResponse:
        res = MessageResponse.model_validate(m)
        if m.tool_calls and isinstance(m.tool_calls, dict):
            res.active_model = m.tool_calls.get("active_model")
            res.thinking_trace = m.tool_calls.get("thinking_trace")
            att = m.tool_calls.get("attachment")
            if att and isinstance(att, dict):
                res.attachment_url = att.get("url")
                res.attachment_name = att.get("name")
                res.attachment_type = att.get("type")
                res.attachment_data_url = att.get("data_url")
        return res

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
            messages=[self._to_message_response(m) for m in messages],
            created_at=conv.created_at,
        )

    def get_api_key_status(self) -> ApiKeyStatusResponse:
        key = self.gemini_provider.api_key or settings.GEMINI_API_KEY
        if not key or not key.strip():
            return ApiKeyStatusResponse(
                is_configured=False,
                is_valid=False,
                masked_key=None,
                active_model="CogniCare Resilient Healthcare Engine (Local Mode)",
                status_detail="No Gemini API key configured. Operating in local resilient offline mode.",
            )
        clean = key.strip()
        masked = f"{clean[:4]}...{clean[-4:]}" if len(clean) > 8 else "***"
        is_valid, msg = self.gemini_provider.validate_key(clean)
        return ApiKeyStatusResponse(
            is_configured=True,
            is_valid=is_valid,
            masked_key=masked,
            active_model="Gemini 2.0 Flash (Live AI Connected)" if is_valid else "CogniCare Local Engine (Key Invalid)",
            status_detail=msg,
        )

    def configure_api_key(self, new_key: str) -> ApiKeyStatusResponse:
        clean = new_key.strip()
        is_valid, msg = self.gemini_provider.validate_key(clean)

        self.gemini_provider.api_key = clean
        settings.GEMINI_API_KEY = clean

        try:
            env_path = ".env"
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    content = f.read()
                if "GEMINI_API_KEY=" in content:
                    content = re.sub(r"GEMINI_API_KEY=.*", f"GEMINI_API_KEY={clean}", content)
                else:
                    content += f"\nGEMINI_API_KEY={clean}\n"
                with open(env_path, "w", encoding="utf-8") as f:
                    f.write(content)
        except Exception as e:
            logger.warning(f"Could not persist GEMINI_API_KEY to .env: {e}")

        masked = f"{clean[:4]}...{clean[-4:]}" if len(clean) > 8 else "***"
        return ApiKeyStatusResponse(
            is_configured=bool(clean),
            is_valid=is_valid,
            masked_key=masked,
            active_model="Gemini 2.0 Flash (Live AI Connected)" if is_valid else "CogniCare Local Engine (Key Rejected)",
            status_detail=msg,
        )
