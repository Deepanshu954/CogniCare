from sqlalchemy import Column, String, Text, Boolean, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.base import TimeStampedModel


class CognitiveActivity(TimeStampedModel):
    __tablename__ = "cognitive_activities"

    activity_type = Column(String(50), nullable=False)  # MEMORY_RECALL, WORD_SEQUENCE, ATTENTION_STROOP, ORIENTATION_MATCH
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)

    versions = relationship("CognitiveActivityVersion", back_populates="activity", cascade="all, delete-orphan")
    sessions = relationship("ActivitySession", back_populates="activity")


class CognitiveActivityVersion(TimeStampedModel):
    __tablename__ = "cognitive_activity_versions"

    activity_id = Column(String(36), ForeignKey("cognitive_activities.id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, default=1)
    difficulty = Column(Integer, default=1)  # 1 to 5
    content_data = Column(JSON, default=dict)
    scoring_config = Column(JSON, default=dict)
    published_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    activity = relationship("CognitiveActivity", back_populates="versions")
    sessions = relationship("ActivitySession", back_populates="activity_version")


class ActivitySession(TimeStampedModel):
    __tablename__ = "activity_sessions"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    activity_id = Column(String(36), ForeignKey("cognitive_activities.id"), nullable=False)
    activity_version_id = Column(String(36), ForeignKey("cognitive_activity_versions.id"), nullable=True)
    status = Column(String(50), default="IN_PROGRESS")  # IN_PROGRESS, COMPLETED, ABANDONED
    difficulty = Column(Integer, default=1)
    total_score = Column(Float, default=0.0)
    accuracy_rate = Column(Float, default=0.0)
    avg_response_time_ms = Column(Integer, default=0)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    patient = relationship("PatientProfile", back_populates="activity_sessions")
    activity = relationship("CognitiveActivity", back_populates="sessions")
    activity_version = relationship("CognitiveActivityVersion", back_populates="sessions")
    answers = relationship("ActivityAnswer", back_populates="session", cascade="all, delete-orphan")


class ActivityAnswer(TimeStampedModel):
    __tablename__ = "activity_answers"

    session_id = Column(String(36), ForeignKey("activity_sessions.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(String(100), nullable=False)
    user_answer = Column(JSON, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    response_time_ms = Column(Integer, nullable=False)
    attempt_number = Column(Integer, default=1)
    difficulty = Column(Integer, default=1)

    session = relationship("ActivitySession", back_populates="answers")


class CognitiveBaseline(TimeStampedModel):
    __tablename__ = "cognitive_baselines"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    metric_name = Column(String(100), nullable=False)  # OVERALL_SCORE, ACCURACY, SPEED_MS, MEMORY, ATTENTION
    baseline_value = Column(Float, nullable=False)
    sample_count = Column(Integer, default=1)
    window_days = Column(Integer, default=30)
    calculated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CognitiveTrendSnapshot(TimeStampedModel):
    __tablename__ = "cognitive_trend_snapshots"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    metric_name = Column(String(100), nullable=False)
    period_start = Column(String(20), nullable=False)
    period_end = Column(String(20), nullable=False)
    current_value = Column(Float, nullable=False)
    baseline_value = Column(Float, nullable=False)
    delta_percent = Column(Float, default=0.0)
    trend_direction = Column(String(50), default="STABLE")  # STABLE, IMPROVING, VARIABLE, DECLINING
    sample_count = Column(Integer, default=0)


class SupportSignal(TimeStampedModel):
    __tablename__ = "support_signals"

    patient_id = Column(String(36), ForeignKey("patient_profiles.id", ondelete="CASCADE"), nullable=False)
    signal_type = Column(String(100), nullable=False)
    severity = Column(String(50), default="INFO")  # INFO, ATTENTION, CONCERN
    description = Column(Text, nullable=False)
    evidence = Column(JSON, default=dict)
    status = Column(String(50), default="ACTIVE")  # ACTIVE, REVIEWED, DISMISSED
