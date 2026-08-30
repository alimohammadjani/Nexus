"""Marketplace schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    category: str = "template"
    price: float = Field(..., ge=0)
    currency: str = "USD"
    cover_url: str | None = None
    demo_url: str | None = None
    tags: str = ""


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    price: float | None = None
    currency: str | None = None
    cover_url: str | None = None
    demo_url: str | None = None
    tags: str | None = None
    is_published: bool | None = None


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    seller_id: int
    rating: float
    sales: int
    is_published: bool
    created_at: datetime
    updated_at: datetime


class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    user_id: int
    rating: int
    comment: str | None = None
    created_at: datetime


class OrderCreate(BaseModel):
    product_id: int


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    buyer_id: int
    amount: float
    currency: str
    status: str
    created_at: datetime
