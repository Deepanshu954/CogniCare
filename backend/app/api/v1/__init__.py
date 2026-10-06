from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.patients import router as patients_router
from app.api.v1.care import router as care_router
from app.api.v1.cognition import activities_router, cognition_router
from app.api.v1.assistant import router as assistant_router
from app.api.v1.safety import safety_router, notifications_router
from app.api.v1.reports import router as reports_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(patients_router)
api_v1_router.include_router(care_router)
api_v1_router.include_router(activities_router)
api_v1_router.include_router(cognition_router)
api_v1_router.include_router(assistant_router)
api_v1_router.include_router(safety_router)
api_v1_router.include_router(notifications_router)
api_v1_router.include_router(reports_router)
