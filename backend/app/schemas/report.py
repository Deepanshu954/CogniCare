from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ReportMetricsSnapshot(BaseModel):
    adherence_percentage: float
    total_reminders_scheduled: int
    reminders_acknowledged: int
    cognitive_composite_score: float
    cognitive_sessions_completed: int
    average_accuracy_percentage: float
    average_latency_ms: int
    alerts_triggered_count: int
    sos_events_count: int


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    patient_id: str
    period_start: str
    period_end: str
    metrics_snapshot: Dict[str, Any]
    ai_narrative_summary: str
    status: str
    created_at: datetime
