from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.cognition import (
    CognitiveActivity,
    CognitiveActivityVersion,
    ActivitySession,
    ActivityAnswer,
    CognitiveBaseline,
    CognitiveTrendSnapshot,
    SupportSignal,
)


class CognitionRepository:
    def __init__(self, db: Session):
        self.db = db
        self._ensure_default_catalog()

    def _ensure_default_catalog(self):
        """Seed default 4 cognitive activities if catalog is empty."""
        count = self.db.query(CognitiveActivity).count()
        if count > 0:
            return

        catalog_defs = [
            {
                "activity_type": "MEMORY_RECALL",
                "title": "Visual Memory Pairs",
                "category": "Memory Recall",
                "description": "Find and remember matching pairs of everyday household items and nature photos.",
                "difficulty": 1,
                "content": {
                    "cards": [
                        {"id": "c1", "label": "Sunflower", "icon": "flower"},
                        {"id": "c2", "label": "Robin", "icon": "bird"},
                        {"id": "c3", "label": "Teacup", "icon": "cup"},
                        {"id": "c4", "label": "Apple", "icon": "apple"},
                    ],
                    "rounds": 4,
                },
            },
            {
                "activity_type": "WORD_SEQUENCE",
                "title": "Sequence & Number Recall",
                "category": "Working Memory",
                "description": "Remember the sequence of numbers shown on the screen and repeat them in order.",
                "difficulty": 1,
                "content": {
                    "sequences": [
                        {"sequence": [2, 5, 8], "length": 3},
                        {"sequence": [1, 4, 7, 9], "length": 4},
                    ]
                },
            },
            {
                "activity_type": "ATTENTION_STROOP",
                "title": "Color Word Attention",
                "category": "Executive Function & Attention",
                "description": "Select the color of the ink rather than the word written. Sharpens focus and inhibitory control.",
                "difficulty": 1,
                "content": {
                    "trials": [
                        {"word": "RED", "ink": "blue", "options": ["red", "blue", "green"]},
                        {"word": "GREEN", "ink": "red", "options": ["red", "blue", "green"]},
                        {"word": "BLUE", "ink": "green", "options": ["red", "blue", "green"]},
                    ]
                },
            },
            {
                "activity_type": "ORIENTATION_MATCH",
                "title": "Clock & Daily Orientation",
                "category": "Orientation & Spatial",
                "description": "Identify clock times and morning/afternoon routines. Supports temporal grounding.",
                "difficulty": 1,
                "content": {
                    "questions": [
                        {"prompt": "What meal is usually eaten at 8:00 AM?", "options": ["Breakfast", "Dinner", "Midnight snack"], "correct": "Breakfast"},
                        {"prompt": "If the sun is setting, is it morning or evening?", "options": ["Morning", "Evening", "Noon"], "correct": "Evening"},
                    ]
                },
            },
        ]

        for item in catalog_defs:
            activity = CognitiveActivity(
                activity_type=item["activity_type"],
                title=item["title"],
                category=item["category"],
                description=item["description"],
                is_active=True,
            )
            self.db.add(activity)
            self.db.flush()

            version = CognitiveActivityVersion(
                activity_id=activity.id,
                version_number=1,
                difficulty=item["difficulty"],
                content_data=item["content"],
                scoring_config={"base_points": 100, "latency_penalty": True},
            )
            self.db.add(version)

        self.db.commit()

    def list_activities(self) -> List[CognitiveActivity]:
        return self.db.query(CognitiveActivity).filter(CognitiveActivity.is_active == True).all()

    def get_activity(self, activity_id: str) -> Optional[CognitiveActivity]:
        return self.db.query(CognitiveActivity).filter(CognitiveActivity.id == activity_id).first()

    def create_session(
        self,
        patient_id: str,
        activity_id: str,
        version_id: Optional[str],
        difficulty: int = 1,
    ) -> ActivitySession:
        session = ActivitySession(
            patient_id=patient_id,
            activity_id=activity_id,
            activity_version_id=version_id,
            status="IN_PROGRESS",
            difficulty=difficulty,
            started_at=datetime.now(timezone.utc),
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session(self, session_id: str) -> Optional[ActivitySession]:
        return self.db.query(ActivitySession).filter(ActivitySession.id == session_id).first()

    def add_answer(
        self,
        session_id: str,
        question_id: str,
        user_answer: any,
        is_correct: bool,
        response_time_ms: int,
        attempt_number: int = 1,
        difficulty: int = 1,
    ) -> ActivityAnswer:
        answer = ActivityAnswer(
            session_id=session_id,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=is_correct,
            response_time_ms=response_time_ms,
            attempt_number=attempt_number,
            difficulty=difficulty,
        )
        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return answer

    def list_patient_sessions(self, patient_id: str) -> List[ActivitySession]:
        return (
            self.db.query(ActivitySession)
            .filter(ActivitySession.patient_id == patient_id)
            .order_by(ActivitySession.started_at.desc())
            .all()
        )

    def get_baseline(self, patient_id: str, metric_name: str = "OVERALL_SCORE") -> Optional[CognitiveBaseline]:
        return (
            self.db.query(CognitiveBaseline)
            .filter(CognitiveBaseline.patient_id == patient_id, CognitiveBaseline.metric_name == metric_name)
            .first()
        )

    def set_baseline(self, patient_id: str, metric_name: str, value: float, sample_count: int) -> CognitiveBaseline:
        baseline = self.get_baseline(patient_id, metric_name)
        if baseline:
            baseline.baseline_value = value
            baseline.sample_count = sample_count
            baseline.calculated_at = datetime.now(timezone.utc)
        else:
            baseline = CognitiveBaseline(
                patient_id=patient_id,
                metric_name=metric_name,
                baseline_value=value,
                sample_count=sample_count,
            )
            self.db.add(baseline)
        self.db.commit()
        self.db.refresh(baseline)
        return baseline

    def list_signals(self, patient_id: str) -> List[SupportSignal]:
        return (
            self.db.query(SupportSignal)
            .filter(SupportSignal.patient_id == patient_id)
            .order_by(SupportSignal.created_at.desc())
            .all()
        )

    def create_signal(
        self,
        patient_id: str,
        signal_type: str,
        severity: str,
        description: str,
        evidence: dict,
    ) -> SupportSignal:
        signal = SupportSignal(
            patient_id=patient_id,
            signal_type=signal_type,
            severity=severity,
            description=description,
            evidence=evidence,
            status="ACTIVE",
        )
        self.db.add(signal)
        self.db.commit()
        self.db.refresh(signal)
        return signal
