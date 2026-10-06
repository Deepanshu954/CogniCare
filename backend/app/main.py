import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine, Base
from app.core.exceptions import AppException
from app.core.logging import setup_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Initializing CogniCare Backend...")
    # Resilient DB connection retry for container cold-starts
    import time
    for attempt in range(1, 11):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database schemas verified.")
            break
        except Exception as e:
            if attempt == 10:
                logger.error(f"Database initialization failed after 10 attempts: {e}")
                raise e
            logger.warning(f"Database not ready yet (attempt {attempt}/10): {e}. Retrying in 2s...")
            time.sleep(2)
    yield
    logger.info("CogniCare Backend shutting down.")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Cognitive Health & Care Assistant Backend API",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app.core.rate_limit import rate_limit_middleware

app.middleware("http")(rate_limit_middleware)


@app.middleware("http")
async def security_headers_and_request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", f"req_{uuid.uuid4().hex[:12]}")
    request.state.request_id = request_id
    response = await call_next(request)
    
    # Traceability
    response.headers["X-Request-ID"] = request_id
    
    # OWASP Category 12: HTTP Security Hardening Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(self), geolocation=()"
    
    return response


# Global Exception Handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    req_id = getattr(request.state, "request_id", "req_unknown")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
            "request_id": req_id,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    req_id = getattr(request.state, "request_id", "req_unknown")
    errors = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Input validation failed.",
                "details": {"fields": errors},
            },
            "request_id": req_id,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    req_id = getattr(request.state, "request_id", "req_unknown")
    logger.exception(f"Unhandled server error on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again later.",
                "details": {},
            },
            "request_id": req_id,
        },
    )


from app.api.v1 import api_v1_router
app.include_router(api_v1_router)


# System Health Endpoints
@app.get("/health/live", tags=["System"])
def liveness_check(request: Request):
    req_id = getattr(request.state, "request_id", "req_unknown")
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
        "request_id": req_id,
    }


@app.get("/health/ready", tags=["System"])
def readiness_check(request: Request):
    req_id = getattr(request.state, "request_id", "req_unknown")
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database readiness check failed: {e}")
        db_status = "error"

    return {
        "status": "ready" if db_status == "connected" else "degraded",
        "database": db_status,
        "request_id": req_id,
    }
