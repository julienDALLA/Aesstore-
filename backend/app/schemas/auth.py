"""
Pydantic schemas for authentication endpoints.
"""

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

from app.schemas.base import BaseModelWithID, TimestampMixin, UUIDMixin
from app.database.models import UserRole, UserStatus


class UserBase(BaseModel):
    """Base user model."""
    
    email: EmailStr = Field(..., description="User email address")
    username: Optional[str] = Field(default=None, description="Username")
    first_name: Optional[str] = Field(default=None, description="First name")
    last_name: Optional[str] = Field(default=None, description="Last name")
    phone: Optional[str] = Field(default=None, description="Phone number")


class UserRegister(UserBase):
    """User registration schema."""
    
    password: str = Field(..., min_length=8, description="Password")
    
    # Company info (B2B)
    company_name: Optional[str] = Field(default=None, description="Company name")
    company_vat: Optional[str] = Field(default=None, description="Company VAT number")
    
    # Address
    address_line_1: Optional[str] = Field(default=None, description="Address line 1")
    address_line_2: Optional[str] = Field(default=None, description="Address line 2")
    city: Optional[str] = Field(default=None, description="City")
    state: Optional[str] = Field(default=None, description="State/Province")
    postal_code: Optional[str] = Field(default=None, description="Postal code")
    country: Optional[str] = Field(default="France", description="Country")
    
    # Preferences
    language: Optional[str] = Field(default="fr", description="Preferred language")
    currency: Optional[str] = Field(default="EUR", description="Preferred currency")
    
    # Role (optional, defaults to CUSTOMER)
    role: Optional[UserRole] = Field(default=UserRole.CUSTOMER, description="User role")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "password123",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+33123456789",
                "company_name": "Acme Corp",
                "company_vat": "FR123456789",
                "address_line_1": "123 Main St",
                "city": "Paris",
                "postal_code": "75000",
                "country": "France",
                "language": "fr",
                "currency": "EUR",
            }
        }


class UserLogin(BaseModel):
    """User login schema."""
    
    username: str = Field(..., description="Email or username")
    password: str = Field(..., description="Password")
    remember_me: Optional[bool] = Field(default=False, description="Remember me")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "user@example.com",
                "password": "password123",
                "remember_me": True,
            }
        }


class UserResponse(BaseModelWithID, UUIDMixin, TimestampMixin, UserBase):
    """User response schema with additional fields."""
    
    role: UserRole = Field(..., description="User role")
    status: UserStatus = Field(..., description="User status")
    
    # Company info
    company_name: Optional[str] = Field(default=None, description="Company name")
    company_vat: Optional[str] = Field(default=None, description="Company VAT")
    
    # Address
    address_line_1: Optional[str] = Field(default=None, description="Address line 1")
    address_line_2: Optional[str] = Field(default=None, description="Address line 2")
    city: Optional[str] = Field(default=None, description="City")
    state: Optional[str] = Field(default=None, description="State")
    postal_code: Optional[str] = Field(default=None, description="Postal code")
    country: Optional[str] = Field(default=None, description="Country")
    
    # Preferences
    language: Optional[str] = Field(default=None, description="Language")
    currency: Optional[str] = Field(default=None, description="Currency")
    
    # Security
    is_verified: bool = Field(default=False, description="Email verified")
    
    # Timestamps
    last_login: Optional[datetime] = Field(default=None, description="Last login timestamp")
    email_verified_at: Optional[datetime] = Field(default=None, description="Email verification timestamp")
    
    # Tokens (only for registration/login responses)
    access_token: Optional[str] = Field(default=None, description="JWT access token")
    refresh_token: Optional[str] = Field(default=None, description="JWT refresh token")
    
    @classmethod
    def from_orm(cls, user: any) -> "UserResponse":
        """Create UserResponse from ORM model."""
        return cls(
            id=user.id,
            uuid=user.uuid,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            role=user.role,
            status=user.status,
            company_name=user.company_name,
            company_vat=user.company_vat,
            address_line_1=user.address_line_1,
            address_line_2=user.address_line_2,
            city=user.city,
            state=user.state,
            postal_code=user.postal_code,
            country=user.country,
            language=user.language,
            currency=user.currency,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
            email_verified_at=user.email_verified_at,
        )


class TokenRefresh(BaseModel):
    """Token refresh schema."""
    
    refresh_token: str = Field(..., description="Refresh token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        }


class ForgotPassword(BaseModel):
    """Forgot password schema."""
    
    email: EmailStr = Field(..., description="Email address")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
            }
        }


class ResetPassword(BaseModel):
    """Reset password schema."""
    
    email: EmailStr = Field(..., description="Email address")
    token: str = Field(..., description="Reset token")
    password: str = Field(..., min_length=8, description="New password")
    password_confirmation: str = Field(..., description="Password confirmation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "token": "reset-token-123",
                "password": "newpassword123",
                "password_confirmation": "newpassword123",
            }
        }


class ChangePassword(BaseModel):
    """Change password schema."""
    
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
    new_password_confirmation: str = Field(..., description="New password confirmation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "oldpassword123",
                "new_password": "newpassword123",
                "new_password_confirmation": "newpassword123",
            }
        }
