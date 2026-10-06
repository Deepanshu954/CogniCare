from typing import List, Optional
from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.repositories.user_repository import UserRepository
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    token = None
    # 1. Check Bearer Authorization header
    if credentials:
        token = credentials.credentials
    # 2. Check HTTP-only cookie as fallback
    if not token and "cognicare_access_token" in request.cookies:
        token = request.cookies.get("cognicare_access_token")

    if not token:
        raise UnauthorizedException(message="Not authenticated. Bearer token or session cookie required.")

    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise UnauthorizedException(message="Invalid or expired access token.")

    user_id = payload.get("sub")
    user = UserRepository(db).get_by_id(user_id)
    if not user or user.status != "ACTIVE":
        raise UnauthorizedException(message="User not found or account is deactivated.")

    return user


def require_roles(*allowed_roles: str):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenException(
                message=f"Access denied. Role '{current_user.role}' does not have required permissions."
            )
        return current_user

    return role_checker
