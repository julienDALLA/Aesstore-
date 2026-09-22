"""
SQLAlchemy base model with common columns and utilities.
"""

from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, Integer, DateTime, Boolean, func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker
from datetime import datetime, timezone
import uuid


class Base(AsyncAttrs, DeclarativeBase):
    """Base model with common columns and async support."""
    
    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name."""
        return cls.__name__.lower() + "s"
    
    id: int = Column(Integer, primary_key=True, index=True)
    uuid: str = Column(
        String(36),
        unique=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )
    created_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(timezone.utc),
        nullable=False
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(timezone.utc),
        onupdate=func.now(timezone.utc),
        nullable=False
    )
    is_active: bool = Column(Boolean, default=True, nullable=False)
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def to_dict_exclude(self, exclude: list[str] = None) -> dict:
        """Convert model to dictionary excluding specified fields."""
        data = self.to_dict()
        if exclude:
            for field in exclude:
                data.pop(field, None)
        return data
    
    @classmethod
    def from_dict(cls, data: dict, exclude: list[str] = None) -> "Base":
        """Create model instance from dictionary."""
        if exclude:
            data = {k: v for k, v in data.items() if k not in exclude}
        return cls(**data)


# Import SQLAlchemy types for convenience
from sqlalchemy import String, Text, Float, Numeric, JSON, ForeignKey, Date, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column

__all__ = [
    "Base",
    "String",
    "Text",
    "Float",
    "Numeric",
    "JSON",
    "ForeignKey",
    "Date",
    "Time",
    "relationship",
    "Mapped",
    "mapped_column",
]
