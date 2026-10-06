from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CognitiveActivityVersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    version_number: int
    difficulty: int
    content_data: Dict[str, Any]
    scoring_config: Dict[str, Any]


class CognitiveActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    activity_type: str
    title: str
    category: str
    description: str
    is_active: bool
    current_version: Optional[CognitiveActivityVersionResponse] = None


class StartSessionRequest(BaseModel):
    activity_id: str
    difficulty: Optional[int] = 1


class SessionAnswerRequest(BaseModel):
    question_id: str
    user_answer: Any
    is_correct: bool
    response_time_ms: int
    attempt_number: int = 1


class SessionAnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    question_id: str
    is_correct: bool
    response_time_ms: int
    created_at: datetime


class ActivitySessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    patient_id: str
    activity_id: str
    activity_title: Optional[str] = None
    status: str
    difficulty: int
    total_score: float
    accuracy_rate: float
    avg_response_time_ms: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    answers_count: int = 0
    feedback_message: Optional[str] = None


class CognitiveTrendPoint(BaseModel):
    date: str
    score: float
    accuracy: float
    avg_latency_ms: int
    baseline_score: float


class CognitiveOverviewResponse(BaseModel):
    current_composite_score: float
    baseline_score: float
    total_sessions_completed: int
    recent_accuracy_rate: float
    recent_avg_latency_ms: int
    trend_direction: str  # STABLE, IMPROVING, VARIABLE, DECLINING
    category_scores: Dict[str, float]


class SupportSignalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    signal_type: str
    severity: str
    description: str
    evidence: Dict[str, Any]
    status: str
    created_at: datetime
