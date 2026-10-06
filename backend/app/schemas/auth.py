from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Minimum 8 characters")
    display_name: str = Field(..., min_length=2, max_length=100)
    role: str = Field("ELDERLY", description="ELDERLY, CAREGIVER, REVIEWER, ADMIN")
    phone_number: Optional[str] = None
    preferred_language: str = "en"
    emergency_notes: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserResponse"


class RefreshRequest(BaseModel):
    refresh_token: Optional[str] = None


# Import UserResponse for reference resolution
from app.schemas.user import UserResponse
TokenResponse.model_rebuild()
