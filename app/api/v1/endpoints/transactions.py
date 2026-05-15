from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.transactions import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter()


@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction_in: TransactionCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new transaction in the DB.
    """
    # Map the Pydantic model to the SQLAlchemy model
    db_transaction = Transaction(
        amount=transaction_in.amount,
        description=transaction_in.description,
        category=transaction_in.category,
        date=transaction_in.date,
        user_id=current_user.id,
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.get("/", response_model=List[TransactionResponse])
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    List all transaction in the DB with pagination.
    """

    return (
        db.query(Transaction)
        .filter(Transaction.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
