from sqlalchemy import Column, String, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedModel


class Conversation(TimeStampedModel):
    __tablename__ = "conversations"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    started_by_user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), default="Conversation")
    status = Column(String(50), default="ACTIVE")  # ACTIVE, ARCHIVED

    patient = relationship("PatientProfile", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(TimeStampedModel):
    __tablename__ = "messages"

    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(50), nullable=False)  # USER, ASSISTANT, SYSTEM, TOOL
    content = Column(Text, nullable=False)
    content_type = Column(String(50), default="TEXT")
    tool_calls = Column(JSON, nullable=True)

    conversation = relationship("Conversation", back_populates="messages")


class MemoryItem(TimeStampedModel):
    __tablename__ = "memory_items"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    memory_type = Column(String(50), default="PREFERENCE")  # PREFERENCE, ROUTINE, PERSONAL_CONTEXT
    content = Column(Text, nullable=False)
    sensitivity = Column(String(50), default="STANDARD")
    is_active = Column(Boolean, default=True)
