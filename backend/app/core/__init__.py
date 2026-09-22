"""Core application configuration and utilities."""

from app.core.config import settings
from app.core.security import (
    pwd_context,
    oauth2_scheme,
    TokenData,
    Token,
    TokenPayload,
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    get_current_admin_user,
    RequireScope,
)
from app.core.dependencies import (
    get_db,
    get_sync_db,
    Pagination,
    PaginationDep,
    SearchFilter,
    SearchFilterDep,
    PaginatedResponse,
    HealthCheckResponse,
)

__all__ = [
    "settings",
    "pwd_context",
    "oauth2_scheme",
    "TokenData",
    "Token",
    "TokenPayload",
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "get_current_user",
    "get_current_admin_user",
    "RequireScope",
    "get_db",
    "get_sync_db",
    "Pagination",
    "PaginationDep",
    "SearchFilter",
    "SearchFilterDep",
    "PaginatedResponse",
    "HealthCheckResponse",
]
