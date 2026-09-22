"""Pydantic schemas for request/response validation."""

from app.schemas.base import APIResponse, ErrorResponse, PaginatedResponse
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenRefresh,
    ForgotPassword,
    ResetPassword,
    ChangePassword,
)
from app.schemas.user import UserCreate, UserUpdate, UserList
from app.schemas.product import ProductCreate, ProductUpdate, ProductList
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryList
from app.schemas.order import OrderCreate, OrderUpdate, OrderList
from app.schemas.cart import CartItemCreate, CartItemUpdate
from app.schemas.review import ReviewCreate, ReviewUpdate

__all__ = [
    # Base
    "APIResponse",
    "ErrorResponse",
    "PaginatedResponse",
    # Auth
    "UserRegister",
    "UserLogin",
    "UserResponse",
    "TokenRefresh",
    "ForgotPassword",
    "ResetPassword",
    "ChangePassword",
    # User
    "UserCreate",
    "UserUpdate",
    "UserList",
    # Product
    "ProductCreate",
    "ProductUpdate",
    "ProductList",
    # Category
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryList",
    # Order
    "OrderCreate",
    "OrderUpdate",
    "OrderList",
    # Cart
    "CartItemCreate",
    "CartItemUpdate",
    # Review
    "ReviewCreate",
    "ReviewUpdate",
]
