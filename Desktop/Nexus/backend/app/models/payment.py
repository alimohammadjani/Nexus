"""Payment and transaction models."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    amount: Mapped[float] = Column(Float, nullable=False)
    currency: Mapped[str] = Column(String(16), default="USD")
    status: Mapped[str] = Column(String(32), default="pending")  # pending, succeeded, failed, refunded
    provider: Mapped[str] = Column(String(64), default="stripe")
    reference: Mapped[str | None] = Column(String(255), nullable=True, index=True)
    description: Mapped[str | None] = Column(Text, nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    transaction_id: Mapped[int] = Column(
        Integer, ForeignKey("transactions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    method: Mapped[str] = Column(String(64), default="card")
    paid_at: Mapped[datetime | None] = Column(DateTime, nullable=True)
    receipt_url: Mapped[str | None] = Column(String(512), nullable=True)
    meta: Mapped[str | None] = Column("metadata", Text, nullable=True)
