"""Marketplace models: products, reviews and orders."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    seller_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str] = Column(Text, nullable=False)
    category: Mapped[str] = Column(String(64), default="template", index=True)
    price: Mapped[float] = Column(Float, nullable=False, default=0)
    currency: Mapped[str] = Column(String(16), default="USD")
    cover_url: Mapped[str | None] = Column(String(512), nullable=True)
    demo_url: Mapped[str | None] = Column(String(512), nullable=True)
    tags: Mapped[str] = Column(Text, default="", nullable=False)
    rating: Mapped[float] = Column(Float, default=0, nullable=False)
    sales: Mapped[int] = Column(Integer, default=0, nullable=False)
    is_published: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    seller = relationship("User", back_populates="products")
    reviews = relationship("ProductReview", back_populates="product", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="product")


class ProductReview(Base):
    __tablename__ = "product_reviews"
    __table_args__ = (UniqueConstraint("product_id", "user_id", name="uq_review_product_user"),)

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    rating: Mapped[int] = Column(Integer, nullable=False, default=5)
    comment: Mapped[str | None] = Column(Text, nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="reviews")
    user = relationship("User")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), index=True)
    buyer_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    amount: Mapped[float] = Column(Float, nullable=False)
    currency: Mapped[str] = Column(String(16), default="USD")
    status: Mapped[str] = Column(String(32), default="pending")  # pending, paid, cancelled, refunded
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="orders")
    buyer = relationship("User", back_populates="orders")
