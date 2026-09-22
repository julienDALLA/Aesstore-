"""
Base Pydantic schemas for API responses and common models.
"""

from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any
from datetime import datetime


T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response format."""
    
    success: bool = Field(default=True, description="Whether the request was successful")
    message: Optional[str] = Field(default=None, description="Success message")
    data: Optional[T] = Field(default=None, description="Response data")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Request successful",
                "data": None,
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response format."""
    
    success: bool = Field(default=False, description="Whether the request was successful")
    error: str = Field(..., description="Error code")
    message: Optional[str] = Field(default=None, description="Error message")
    field: Optional[str] = Field(default=None, description="Field with error")
    details: Optional[dict[str, Any]] = Field(default=None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "validation_error",
                "message": "Invalid input data",
                "field": "email",
                "details": {"email": "Invalid email format"},
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response format."""
    
    items: list[T] = Field(default_factory=list, description="List of items")
    total: int = Field(default=0, description="Total number of items")
    page: int = Field(default=1, description="Current page number")
    page_size: int = Field(default=20, description="Number of items per page")
    total_pages: int = Field(default=0, description="Total number of pages")
    has_next: bool = Field(default=False, description="Whether there is a next page")
    has_previous: bool = Field(default=False, description="Whether there is a previous page")
    
    @classmethod
    def from_data(
        cls,
        items: list[T],
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedResponse[T]":
        total_pages = (total + page_size - 1) // page_size
        has_next = page < total_pages
        has_previous = page > 1
        
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=has_next,
            has_previous=has_previous,
        )


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""
    
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class UUIDMixin(BaseModel):
    """Mixin for UUID field."""
    
    uuid: str = Field(..., description="Unique identifier")


class BaseModelWithID(BaseModel):
    """Base model with ID field."""
    
    id: int = Field(..., description="Database ID")
