from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserResponse
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app.core.exceptions import ConflictException, UnauthorizedException, BadRequestException


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def register(self, data: RegisterRequest) -> TokenResponse:
        existing = self.repo.get_by_email(data.email)
        if existing:
            raise ConflictException(message="An account with this email already exists.")

        pwd_hash = hash_password(data.password)
        user = self.repo.create(
            email=data.email,
            password_hash=pwd_hash,
            role=data.role.upper(),
            display_name=data.display_name,
            phone_number=data.phone_number,
            preferred_language=data.preferred_language,
            emergency_notes=data.emergency_notes,
        )

        return self._build_token_response(user)

    def login(self, email: str, password: str) -> TokenResponse:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedException(message="Invalid email or password.")

        if user.status != "ACTIVE":
            raise UnauthorizedException(message="This account has been deactivated.")

        # Update last login timestamp
        user.last_login_at = datetime.now(timezone.utc)
        self.db.commit()

        return self._build_token_response(user)

    def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedException(message="Invalid or expired refresh token.")

        user_id = payload.get("sub")
        user = self.repo.get_by_id(user_id)
        if not user or user.status != "ACTIVE":
            raise UnauthorizedException(message="User not found or inactive.")

        return self._build_token_response(user)

    def _build_token_response(self, user) -> TokenResponse:
        access_token = create_access_token(subject=user.id, role=user.role)
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user),
        )
