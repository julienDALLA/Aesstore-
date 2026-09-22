"""
Authentication endpoints for user registration, login, and token management.
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from pydantic import EmailStr, Field

from app.core import (
    get_db,
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    Token,
    TokenPayload,
)
from app.core.config import settings
from app.database.models import User, UserRole, UserStatus
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenRefresh,
    ForgotPassword,
    ResetPassword,
    ChangePassword,
)
from app.schemas.base import APIResponse, ErrorResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    summary="Register a new user",
    response_model=APIResponse[UserResponse],
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        409: {"model": ErrorResponse, "description": "User already exists"},
    }
)
async def register_user(
    data: UserRegister = Body(...),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[UserResponse]:
    """
    Register a new user account.
    
    This endpoint creates a new user with the provided information.
    The user will receive a verification email (if configured).
    
    Args:
        data: User registration data
        db: Database session
        
    Returns:
        APIResponse[UserResponse]: Created user information
        
    Raises:
        HTTPException 400: Validation error
        HTTPException 409: User already exists
    """
    # Check if user already exists
    existing_user = await db.scalar(
        select(User).where(
            or_(
                User.email == data.email,
                User.username == data.username
            )
        )
    )
    
    if existing_user:
        if existing_user.email == data.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Email already registered",
                    "field": "email",
                },
            )
        if existing_user.username == data.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "Username already taken",
                    "field": "username",
                },
            )
    
    # Hash password
    hashed_password = get_password_hash(data.password)
    
    # Create user
    user = User(
        email=data.email,
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name,
        hashed_password=hashed_password,
        phone=data.phone,
        role=data.role or UserRole.CUSTOMER,
        status=UserStatus.PENDING,
        company_name=data.company_name,
        company_vat=data.company_vat,
        address_line_1=data.address_line_1,
        address_line_2=data.address_line_2,
        city=data.city,
        state=data.state,
        postal_code=data.postal_code,
        country=data.country,
        language=data.language,
        currency=data.currency,
    )
    
    db.add(user)
    await db.flush()
    await db.refresh(user)
    
    # Create tokens
    access_token = create_access_token(
        subject=str(user.uuid),
        user_id=user.id,
        email=user.email,
        is_admin=user.is_admin,
        scopes=["user:read", "user:update"],
    )
    refresh_token = create_refresh_token(
        subject=str(user.uuid),
        user_id=user.id,
    )
    
    # Return response
    user_response = UserResponse.from_orm(user)
    user_response.access_token = access_token
    user_response.refresh_token = refresh_token
    
    return APIResponse(
        success=True,
        message="User registered successfully",
        data=user_response,
    )


@router.post(
    "/login",
    summary="Login user",
    response_model=APIResponse[UserResponse],
    responses={
        400: {"model": ErrorResponse, "description": "Invalid credentials"},
        401: {"model": ErrorResponse, "description": "Authentication failed"},
    }
)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()] = Body(...),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[UserResponse]:
    """
    Authenticate a user and return access tokens.
    
    Args:
        form_data: OAuth2 password request form
        db: Database session
        
    Returns:
        APIResponse[UserResponse]: User information with tokens
        
    Raises:
        HTTPException 401: Invalid credentials
    """
    # Find user
    user = await db.scalar(
        select(User).where(
            or_(
                User.email == form_data.username,
                User.username == form_data.username
            )
        )
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid credentials",
                "message": "User not found",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "Invalid credentials",
                "message": "Incorrect password",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Account inactive",
                "message": f"Your account is {user.status.value}",
            },
        )
    
    # Update last login
    user.last_login = datetime.now(timezone.utc)
    await db.flush()
    
    # Create tokens
    access_token = create_access_token(
        subject=str(user.uuid),
        user_id=user.id,
        email=user.email,
        is_admin=user.is_admin,
        scopes=[
            "user:read",
            "user:update",
            "order:read",
            "order:create",
        ] + (["admin:all"] if user.is_admin else []),
    )
    refresh_token = create_refresh_token(
        subject=str(user.uuid),
        user_id=user.id,
    )
    
    # Return response
    user_response = UserResponse.from_orm(user)
    user_response.access_token = access_token
    user_response.refresh_token = refresh_token
    
    return APIResponse(
        success=True,
        message="Login successful",
        data=user_response,
    )


@router.post(
    "/refresh",
    summary="Refresh access token",
    response_model=APIResponse[Token],
    responses={
        401: {"model": ErrorResponse, "description": "Invalid refresh token"},
    }
)
async def refresh_token(
    data: TokenRefresh = Body(...),
) -> APIResponse[Token]:
    """
    Refresh the access token using a valid refresh token.
    
    Args:
        data: Refresh token data
        
    Returns:
        APIResponse[Token]: New access and refresh tokens
        
    Raises:
        HTTPException 401: Invalid refresh token
    """
    try:
        payload = decode_token(data.refresh_token)
        
        if payload.type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid token type"},
            )
        
        # Create new tokens
        access_token = create_access_token(
            subject=payload.sub,
            user_id=payload.user_id,
            email=payload.email,
            is_admin=payload.is_admin,
            scopes=payload.scopes,
        )
        refresh_token = create_refresh_token(
            subject=payload.sub,
            user_id=payload.user_id,
        )
        
        return APIResponse(
            success=True,
            message="Token refreshed successfully",
            data=Token(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                refresh_expires_in=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            ),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid refresh token"},
        )


@router.post(
    "/logout",
    summary="Logout user",
    response_model=APIResponse[None],
)
async def logout_user(
    current_user: TokenPayload = Depends(get_current_user),
) -> APIResponse[None]:
    """
    Invalidate the current user's tokens.
    
    In a production environment, you would add the token to a blacklist.
    For this implementation, we rely on short-lived tokens.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        APIResponse[None]: Success message
    """
    # In a real implementation, add token to blacklist
    # For now, just return success
    return APIResponse(
        success=True,
        message="Logout successful",
    )


@router.post(
    "/forgot-password",
    summary="Request password reset",
    response_model=APIResponse[None],
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
    }
)
async def forgot_password(
    data: ForgotPassword = Body(...),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[None]:
    """
    Request a password reset link to be sent to the user's email.
    
    Args:
        data: Email address for password reset
        db: Database session
        
    Returns:
        APIResponse[None]: Success message
    """
    # Find user by email
    user = await db.scalar(
        select(User).where(User.email == data.email)
    )
    
    if not user:
        # Don't reveal that user doesn't exist
        return APIResponse(
            success=True,
            message="If an account exists with this email, a reset link has been sent",
        )
    
    # In a real implementation, generate and send reset token
    # For now, just return success
    return APIResponse(
        success=True,
        message="If an account exists with this email, a reset link has been sent",
    )


@router.post(
    "/reset-password",
    summary="Reset password",
    response_model=APIResponse[None],
    responses={
        400: {"model": ErrorResponse, "description": "Invalid token"},
        404: {"model": ErrorResponse, "description": "User not found"},
    }
)
async def reset_password(
    data: ResetPassword = Body(...),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[None]:
    """
    Reset the user's password using a reset token.
    
    Args:
        data: Reset password data including token
        db: Database session
        
    Returns:
        APIResponse[None]: Success message
        
    Raises:
        HTTPException 400: Invalid token
        HTTPException 404: User not found
    """
    # Find user by email
    user = await db.scalar(
        select(User).where(User.email == data.email)
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "User not found"},
        )
    
    # Verify reset token (in real implementation)
    # For now, just update password
    user.hashed_password = get_password_hash(data.password)
    user.reset_token = None
    user.reset_token_expires = None
    
    await db.flush()
    
    return APIResponse(
        success=True,
        message="Password reset successfully",
    )


@router.post(
    "/change-password",
    summary="Change password",
    response_model=APIResponse[None],
    responses={
        400: {"model": ErrorResponse, "description": "Invalid current password"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    }
)
async def change_password(
    data: ChangePassword = Body(...),
    current_user: TokenPayload = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[None]:
    """
    Change the current user's password.
    
    Args:
        data: Change password data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        APIResponse[None]: Success message
        
    Raises:
        HTTPException 400: Invalid current password
        HTTPException 401: Unauthorized
    """
    # Find user
    user = await db.get(User, current_user.user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "User not found"},
        )
    
    # Verify current password
    if not verify_password(data.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid current password"},
        )
    
    # Update password
    user.hashed_password = get_password_hash(data.new_password)
    await db.flush()
    
    return APIResponse(
        success=True,
        message="Password changed successfully",
    )


@router.get(
    "/me",
    summary="Get current user",
    response_model=APIResponse[UserResponse],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    }
)
async def get_current_user_profile(
    current_user: TokenPayload = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[UserResponse]:
    """
    Get the current authenticated user's profile.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        APIResponse[UserResponse]: Current user information
    """
    user = await db.get(User, current_user.user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "User not found"},
        )
    
    return APIResponse(
        success=True,
        data=UserResponse.from_orm(user),
    )
