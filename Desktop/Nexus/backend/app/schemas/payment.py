"""Payment schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=16)
    provider: str = Field(default="stripe", max_length=64)
    description: str | None = None


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    amount: float
    currency: str
    status: str
    provider: str
    reference: str | None = None
    description: str | None = None
    created_at: datetime


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    transaction_id: int
    method: str
    paid_at: datetime | None = None
    receipt_url: str | None = None
