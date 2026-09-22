"""
FastAPI dependencies for database session, pagination, and common utilities.
"""

from typing import AsyncGenerator, Optional, Annotated
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.database.session import async_session_maker, sync_session_maker
from app.core.config import settings


# Database session dependencies
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get an async database session."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db() -> AsyncGenerator[Session, None]:
    """Get a sync database session (for migrations, scripts)."""
    with sync_session_maker() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


# Pagination dependency
class Pagination:
    """Pagination model for API responses."""
    page: int = Query(
        default=settings.DEFAULT_PAGE,
        ge=1,
        description="Page number"
    )
    page_size: int = Query(
        default=settings.DEFAULT_PAGE_SIZE,
        le=settings.MAX_PAGE_SIZE,
        ge=1,
        description="Items per page"
    )
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        return self.page_size


PaginationDep = Annotated[Pagination, Depends()]


# Search and filter dependencies
class SearchFilter:
    """Search and filter parameters."""
    search: Optional[str] = Query(
        default=None,
        description="Search term for filtering results"
    )
    sort_by: Optional[str] = Query(
        default=None,
        description="Field to sort by"
    )
    sort_order: str = Query(
        default="desc",
        description="Sort order (asc or desc)"
    )
    
    @property
    def is_ascending(self) -> bool:
        return self.sort_order.lower() == "asc"


SearchFilterDep = Annotated[SearchFilter, Depends()]


# Common response models
class PaginatedResponse:
    """Standard paginated response format."""
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int
    
    @classmethod
    def from_data(
        cls,
        data: list,
        total: int,
        page: int,
        page_size: int
    ) -> "PaginatedResponse":
        total_pages = (total + page_size - 1) // page_size
        return cls(
            items=data,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )


class HealthCheckResponse:
    """Health check response model."""
    status: str = "healthy"
    version: str
    debug: bool
    
    @classmethod
    def default(cls) -> "HealthCheckResponse":
        return cls(
            status="healthy",
            version=settings.APP_VERSION,
            debug=settings.DEBUG
        )
