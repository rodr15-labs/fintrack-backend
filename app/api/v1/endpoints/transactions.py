from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.transactions import Transaction
from app.schemas.transaction import TransactionResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @router.post("/", response_model=TransactionResponse)
# def create_transaction(
#     transaction_in: TransactionCreate, db: Session = Depends(get_db)
# ):
#     """
#     Create a new transaction in the DB.
#     """
#     # Map the Pydantic model to the SQLAlchemy model
#     db_transaction = Transaction(
#         amount=transaction_in.amount,
#         description=transaction_in.description,
#         category=transaction_in.category,
#         date=transaction_in.date,
#         user_id=transaction_in.user_id,
#     )

#     db.add(db_transaction)
#     db.commit()
#     db.refresh(db_transaction)
#     return db_transaction


@router.get("/all", response_model=List[TransactionResponse])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all transaction in the DB with pagination.
    """
    return db.query(Transaction).offset(skip).limit(limit).all()
