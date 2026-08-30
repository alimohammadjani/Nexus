"""Payment endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.payment import Payment, Transaction
from app.models.user import User
from app.schemas.payment import PaymentOut, TransactionCreate, TransactionOut

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/transactions", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Transaction:
    tx = Transaction(
        user_id=current_user.id,
        amount=payload.amount,
        currency=payload.currency,
        provider=payload.provider,
        description=payload.description,
        status="succeeded",
        reference=f"devhub_{current_user.id}_{tx_hash(payload)}",
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


@router.get("/transactions", response_model=list[TransactionOut])
def list_transactions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return list(
        db.scalars(
            select(Transaction).where(Transaction.user_id == current_user.id).order_by(Transaction.created_at.desc())
        )
    )


@router.get("/transactions/{transaction_id}", response_model=TransactionOut)
def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Transaction:
    tx = db.get(Transaction, transaction_id)
    if not tx or (tx.user_id != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return tx


@router.post("/transactions/{transaction_id}/pay", response_model=PaymentOut, status_code=status.HTTP_201_CREATED)
def pay_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Payment:
    tx = db.get(Transaction, transaction_id)
    if not tx or (tx.user_id != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    payment = Payment(transaction_id=tx.id, paid_at=__import__("datetime").datetime.utcnow())
    tx.status = "succeeded"
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def tx_hash(payload: TransactionCreate) -> str:
    """Small deterministic suffix for reference generation."""
    data = f"{payload.amount}{payload.currency}{payload.description or ''}"
    return __import__("hashlib").sha1(data.encode()).hexdigest()[:12]
