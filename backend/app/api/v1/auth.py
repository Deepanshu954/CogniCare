from fastapi import APIRouter, Depends, Response, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_refresh_token
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _set_auth_cookies(response: Response, token_resp: TokenResponse, user: User):
    refresh_token = create_refresh_token(subject=user.id, role=user.role)
    response.set_cookie(
        key="cognicare_access_token",
        value=token_resp.access_token,
        httponly=True,
        samesite="lax",
        secure=False if settings.DEBUG else True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="cognicare_refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=False if settings.DEBUG else True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    token_resp = service.register(data)
    user = db.query(User).filter(User.id == token_resp.user.id).first()
    _set_auth_cookies(response, token_resp, user)
    return token_resp


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    token_resp = service.login(email=data.email, password=data.password)
    user = db.query(User).filter(User.id == token_resp.user.id).first()
    _set_auth_cookies(response, token_resp, user)
    return token_resp


@router.post("/refresh", response_model=TokenResponse)
def refresh_session(
    request: Request,
    response: Response,
    body: RefreshRequest = None,
    db: Session = Depends(get_db),
):
    token = None
    if body and body.refresh_token:
        token = body.refresh_token
    elif "cognicare_refresh_token" in request.cookies:
        token = request.cookies.get("cognicare_refresh_token")

    service = AuthService(db)
    token_resp = service.refresh(token)
    user = db.query(User).filter(User.id == token_resp.user.id).first()
    _set_auth_cookies(response, token_resp, user)
    return token_resp


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("cognicare_access_token")
    response.delete_cookie("cognicare_refresh_token")
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    return UserResponse.model_validate(current_user)
