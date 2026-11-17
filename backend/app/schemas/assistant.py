from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MessageCreate(BaseModel):
    content: str
    mode: Optional[str] = "normal"  # "normal" (Gemini 3.8 Live) or "extended" (Gemini 3.8 Live Extended Thinking)
    attachment_url: Optional[str] = None
    attachment_name: Optional[str] = None
    attachment_type: Optional[str] = None
    attachment_data_url: Optional[str] = None


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    conversation_id: str
    role: str
    content: str
    content_type: str
    tool_calls: Optional[Dict[str, Any]] = None
    active_model: Optional[str] = None
    thinking_trace: Optional[str] = None
    attachment_url: Optional[str] = None
    attachment_name: Optional[str] = None
    attachment_type: Optional[str] = None
    attachment_data_url: Optional[str] = None
    created_at: datetime


class ApiKeyStatusResponse(BaseModel):
    is_configured: bool
    is_valid: bool
    masked_key: Optional[str] = None
    active_model: str
    status_detail: str


class ApiKeyConfigRequest(BaseModel):
    api_key: str


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    patient_id: str
    title: str
    status: str
    messages: List[MessageResponse] = []
    created_at: datetime


class MemoryItemCreate(BaseModel):
    memory_type: str = "PREFERENCE"  # PREFERENCE, ROUTINE, PERSONAL_CONTEXT
    content: str
    sensitivity: str = "STANDARD"


class MemoryItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    patient_id: str
    memory_type: str
    content: str
    sensitivity: str
    is_active: bool
    created_at: datetime
