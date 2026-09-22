"""
SQLAlchemy models for the Aesstore B2B platform.
"""

from datetime import datetime, date
from typing import TYPE_CHECKING, Optional, Any
from enum import Enum

from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime, Date,
    ForeignKey, JSON, Numeric, Index, CheckConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property

from app.database.base import Base, uuid


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


# Enums
class UserRole(str, Enum):
    ADMIN = "admin"
    VENDOR = "vendor"
    CUSTOMER = "customer"
    GUEST = "guest"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class ProductStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    OUT_OF_STOCK = "out_of_stock"


# Models
class User(Base):
    """User model for authentication and profile management."""
    
    __tablename__ = "users"
    
    email: str = Column(String(255), unique=True, index=True, nullable=False)
    username: str = Column(String(50), unique=True, index=True, nullable=True)
    first_name: str = Column(String(100), nullable=True)
    last_name: str = Column(String(100), nullable=True)
    hashed_password: str = Column(String(255), nullable=False)
    phone: str = Column(String(20), nullable=True)
    
    role: UserRole = Column(
        String(20),
        default=UserRole.CUSTOMER,
        nullable=False
    )
    status: UserStatus = Column(
        String(20),
        default=UserStatus.PENDING,
        nullable=False
    )
    
    # Address
    address_line_1: str = Column(Text, nullable=True)
    address_line_2: str = Column(Text, nullable=True)
    city: str = Column(String(100), nullable=True)
    state: str = Column(String(100), nullable=True)
    postal_code: str = Column(String(20), nullable=True)
    country: str = Column(String(100), default="France", nullable=True)
    
    # Company info (for B2B)
    company_name: str = Column(String(200), nullable=True)
    company_vat: str = Column(String(50), nullable=True)
    company_address: str = Column(Text, nullable=True)
    
    # Preferences
    language: str = Column(String(10), default="fr", nullable=True)
    currency: str = Column(String(3), default="EUR", nullable=True)
    timezone: str = Column(String(50), default="Europe/Paris", nullable=True)
    
    # Security
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    verification_token: str = Column(String(100), nullable=True)
    reset_token: str = Column(String(100), nullable=True)
    reset_token_expires: datetime = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    last_login: datetime = Column(DateTime(timezone=True), nullable=True)
    email_verified_at: datetime = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="vendor",
        foreign_keys="Product.vendor_id",
        cascade="all, delete-orphan"
    )
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="customer",
        foreign_keys="Order.customer_id",
        cascade="all, delete-orphan"
    )
    vendor_orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="vendor",
        foreign_keys="Order.vendor_id",
        cascade="all, delete-orphan"
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    cart: Mapped[Optional["Cart"]] = relationship(
        "Cart",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_role", "role"),
        Index("idx_user_status", "status"),
        Index("idx_user_created_at", "created_at"),
    )
    
    @hybrid_property
    def full_name(self) -> str:
        return f"{self.first_name or ''} {self.last_name or ''}".strip()
    
    @hybrid_property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
    
    @hybrid_property
    def is_vendor(self) -> bool:
        return self.role == UserRole.VENDOR
    
    @hybrid_property
    def is_customer(self) -> bool:
        return self.role == UserRole.CUSTOMER


class Category(Base):
    """Product category model."""
    
    __tablename__ = "categories"
    
    name: str = Column(String(200), nullable=False)
    slug: str = Column(String(200), unique=True, index=True, nullable=False)
    description: str = Column(Text, nullable=True)
    parent_id: Optional[int] = Column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=True
    )
    
    # SEO
    meta_title: str = Column(String(200), nullable=True)
    meta_description: str = Column(Text, nullable=True)
    
    # Display
    icon: str = Column(String(100), nullable=True)
    color: str = Column(String(20), nullable=True)
    image: str = Column(String(255), nullable=True)
    is_featured: bool = Column(Boolean, default=False, nullable=False)
    sort_order: int = Column(Integer, default=0, nullable=False)
    
    # Relationships
    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        remote_side=[id],
        back_populates="children"
    )
    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent"
    )
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        foreign_keys="Product.category_id"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_category_slug", "slug"),
        Index("idx_category_parent", "parent_id"),
        Index("idx_category_featured", "is_featured"),
    )
    
    @hybrid_property
    def path(self) -> str:
        if self.parent:
            return f"{self.parent.path}/{self.slug}"
        return self.slug


class Product(Base):
    """Product model for B2B e-commerce."""
    
    __tablename__ = "products"
    
    name: str = Column(String(200), nullable=False)
    slug: str = Column(String(200), unique=True, index=True, nullable=False)
    description: str = Column(Text, nullable=True)
    short_description: str = Column(String(500), nullable=True)
    
    # Pricing
    base_price: float = Column(Numeric(10, 2), nullable=False)
    sale_price: float = Column(Numeric(10, 2), nullable=True)
    cost_price: float = Column(Numeric(10, 2), nullable=True)
    
    # Inventory
    sku: str = Column(String(100), unique=True, index=True, nullable=True)
    quantity: int = Column(Integer, default=0, nullable=False)
    low_stock_threshold: int = Column(Integer, default=5, nullable=False)
    track_inventory: bool = Column(Boolean, default=True, nullable=False)
    allow_backorders: bool = Column(Boolean, default=False, nullable=False)
    
    # Status
    status: ProductStatus = Column(
        String(20),
        default=ProductStatus.DRAFT,
        nullable=False
    )
    
    # Categories
    category_id: Optional[int] = Column(
        Integer,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Vendor
    vendor_id: Optional[int] = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Images
    featured_image: str = Column(String(255), nullable=True)
    image_gallery: JSON = Column(JSON, default=[], nullable=False)
    
    # SEO
    meta_title: str = Column(String(200), nullable=True)
    meta_description: str = Column(Text, nullable=True)
    
    # Specifications
    weight: float = Column(Float, nullable=True)
    dimensions: JSON = Column(JSON, default={}, nullable=False)
    attributes: JSON = Column(JSON, default={}, nullable=False)
    
    # Shipping
    is_shippable: bool = Column(Boolean, default=True, nullable=False)
    shipping_class: str = Column(String(50), nullable=True)
    
    # Tax
    tax_class: str = Column(String(50), default="standard", nullable=False)
    tax_rate: float = Column(Float, default=20.0, nullable=False)
    
    # Visibility
    is_featured: bool = Column(Boolean, default=False, nullable=False)
    is_visible: bool = Column(Boolean, default=True, nullable=False)
    
    # Dates
    published_at: datetime = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    category: Mapped[Optional["Category"]] = relationship(
        "Category",
        back_populates="products"
    )
    vendor: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="products",
        foreign_keys=[vendor_id]
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="product",
        cascade="all, delete-orphan"
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="product",
        cascade="all, delete-orphan"
    )
    cart_items: Mapped[list["CartItem"]] = relationship(
        "CartItem",
        back_populates="product",
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_product_slug", "slug"),
        Index("idx_product_sku", "sku"),
        Index("idx_product_vendor", "vendor_id"),
        Index("idx_product_category", "category_id"),
        Index("idx_product_status", "status"),
        Index("idx_product_price", "base_price"),
        Index("idx_product_featured", "is_featured"),
        Index("idx_product_visible", "is_visible"),
        CheckConstraint("base_price >= 0", name="check_base_price_nonnegative"),
        CheckConstraint("quantity >= 0", name="check_quantity_nonnegative"),
    )
    
    @hybrid_property
    def final_price(self) -> float:
        return self.sale_price if self.sale_price else self.base_price
    
    @hybrid_property
    def in_stock(self) -> bool:
        return self.quantity > 0
    
    @hybrid_property
    def rating(self) -> float:
        if not self.reviews:
            return 0.0
        return sum(r.rating for r in self.reviews) / len(self.reviews)
    
    @hybrid_property
    def review_count(self) -> int:
        return len(self.reviews)


class Order(Base):
    """Order model for customer purchases."""
    
    __tablename__ = "orders"
    
    # Order info
    order_number: str = Column(String(50), unique=True, index=True, nullable=False)
    status: OrderStatus = Column(
        String(20),
        default=OrderStatus.PENDING,
        nullable=False
    )
    
    # Customer
    customer_id: int = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Vendor (for marketplace)
    vendor_id: Optional[int] = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Shipping
    shipping_first_name: str = Column(String(100), nullable=False)
    shipping_last_name: str = Column(String(100), nullable=False)
    shipping_email: str = Column(String(255), nullable=False)
    shipping_phone: str = Column(String(20), nullable=True)
    shipping_address_line_1: str = Column(Text, nullable=False)
    shipping_address_line_2: str = Column(Text, nullable=True)
    shipping_city: str = Column(String(100), nullable=False)
    shipping_state: str = Column(String(100), nullable=True)
    shipping_postal_code: str = Column(String(20), nullable=False)
    shipping_country: str = Column(String(100), nullable=False)
    
    # Billing
    billing_first_name: str = Column(String(100), nullable=True)
    billing_last_name: str = Column(String(100), nullable=True)
    billing_email: str = Column(String(255), nullable=True)
    billing_phone: str = Column(String(20), nullable=True)
    billing_address_line_1: str = Column(Text, nullable=True)
    billing_address_line_2: str = Column(Text, nullable=True)
    billing_city: str = Column(String(100), nullable=True)
    billing_state: str = Column(String(100), nullable=True)
    billing_postal_code: str = Column(String(20), nullable=True)
    billing_country: str = Column(String(100), nullable=True)
    
    # Payment
    payment_status: PaymentStatus = Column(
        String(20),
        default=PaymentStatus.PENDING,
        nullable=False
    )
    payment_method: str = Column(String(50), nullable=True)
    payment_gateway: str = Column(String(50), nullable=True)
    transaction_id: str = Column(String(100), nullable=True)
    
    # Pricing
    subtotal: float = Column(Numeric(10, 2), default=0.0, nullable=False)
    tax: float = Column(Numeric(10, 2), default=0.0, nullable=False)
    shipping_cost: float = Column(Numeric(10, 2), default=0.0, nullable=False)
    discount: float = Column(Numeric(10, 2), default=0.0, nullable=False)
    total: float = Column(Numeric(10, 2), default=0.0, nullable=False)
    
    # Currency
    currency: str = Column(String(3), default="EUR", nullable=False)
    
    # Notes
    customer_notes: str = Column(Text, nullable=True)
    admin_notes: str = Column(Text, nullable=True)
    
    # Tracking
    tracking_number: str = Column(String(100), nullable=True)
    tracking_url: str = Column(String(255), nullable=True)
    
    # Dates
    paid_at: datetime = Column(DateTime(timezone=True), nullable=True)
    shipped_at: datetime = Column(DateTime(timezone=True), nullable=True)
    delivered_at: datetime = Column(DateTime(timezone=True), nullable=True)
    cancelled_at: datetime = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    customer: Mapped["User"] = relationship(
        "User",
        back_populates="orders",
        foreign_keys=[customer_id]
    )
    vendor: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="vendor_orders",
        foreign_keys=[vendor_id]
    )
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_order_number", "order_number"),
        Index("idx_order_customer", "customer_id"),
        Index("idx_order_vendor", "vendor_id"),
        Index("idx_order_status", "status"),
        Index("idx_order_payment_status", "payment_status"),
        Index("idx_order_created_at", "created_at"),
        CheckConstraint("subtotal >= 0", name="check_subtotal_nonnegative"),
        CheckConstraint("tax >= 0", name="check_tax_nonnegative"),
        CheckConstraint("total >= 0", name="check_total_nonnegative"),
    )
    
    @hybrid_property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)


class OrderItem(Base):
    """Individual items within an order."""
    
    __tablename__ = "order_items"
    
    order_id: int = Column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )
    product_id: int = Column(
        Integer,
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Product info (snapshot at time of order)
    product_name: str = Column(String(200), nullable=False)
    product_sku: str = Column(String(100), nullable=True)
    product_slug: str = Column(String(200), nullable=True)
    
    # Pricing
    unit_price: float = Column(Numeric(10, 2), nullable=False)
    quantity: int = Column(Integer, nullable=False)
    tax: float = Column(Numeric(10, 2), default=0.0, nullable=False)
    discount: float = Column(Numeric(10, 2), default=0.0, nullable=False)
    subtotal: float = Column(Numeric(10, 2), nullable=False)
    total: float = Column(Numeric(10, 2), nullable=False)
    
    # Product attributes (snapshot)
    product_attributes: JSON = Column(JSON, default={}, nullable=False)
    
    # Relationships
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="items"
    )
    product: Mapped[Optional["Product"]] = relationship(
        "Product",
        back_populates="order_items"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_order_item_order", "order_id"),
        Index("idx_order_item_product", "product_id"),
    )


class Review(Base):
    """Product review model."""
    
    __tablename__ = "reviews"
    
    user_id: int = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    product_id: int = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )
    
    rating: int = Column(Integer, nullable=False)
    title: str = Column(String(200), nullable=True)
    comment: str = Column(Text, nullable=True)
    
    # Status
    is_approved: bool = Column(Boolean, default=True, nullable=False)
    is_recommended: bool = Column(Boolean, default=False, nullable=False)
    
    # Media
    images: JSON = Column(JSON, default=[], nullable=False)
    videos: JSON = Column(JSON, default=[], nullable=False)
    
    # Helpfulness
    helpful_count: int = Column(Integer, default=0, nullable=False)
    unhelpful_count: int = Column(Integer, default=0, nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="reviews"
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="reviews"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_review_user", "user_id"),
        Index("idx_review_product", "product_id"),
        Index("idx_review_rating", "rating"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range"),
    )


class Cart(Base):
    """Shopping cart model."""
    
    __tablename__ = "carts"
    
    user_id: int = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    
    # Currency
    currency: str = Column(String(3), default="EUR", nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="cart"
    )
    items: Mapped[list["CartItem"]] = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_cart_user", "user_id", unique=True),
    )
    
    @hybrid_property
    def subtotal(self) -> float:
        return sum(item.subtotal for item in self.items)
    
    @hybrid_property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)


class CartItem(Base):
    """Individual items within a shopping cart."""
    
    __tablename__ = "cart_items"
    
    cart_id: int = Column(
        Integer,
        ForeignKey("carts.id", ondelete="CASCADE"),
        nullable=False
    )
    product_id: int = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )
    
    quantity: int = Column(Integer, default=1, nullable=False)
    
    # Product attributes (selected options)
    attributes: JSON = Column(JSON, default={}, nullable=False)
    
    # Relationships
    cart: Mapped["Cart"] = relationship(
        "Cart",
        back_populates="items"
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="cart_items"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_cart_item_cart", "cart_id"),
        Index("idx_cart_item_product", "product_id"),
        Index("idx_cart_item_cart_product", "cart_id", "product_id", unique=True),
    )
    
    @hybrid_property
    def unit_price(self) -> float:
        return self.product.final_price if self.product else 0.0
    
    @hybrid_property
    def subtotal(self) -> float:
        return self.unit_price * self.quantity


__all__ = [
    "UserRole",
    "UserStatus",
    "OrderStatus",
    "PaymentStatus",
    "ProductStatus",
    "User",
    "Category",
    "Product",
    "Order",
    "OrderItem",
    "Review",
    "Cart",
    "CartItem",
]
