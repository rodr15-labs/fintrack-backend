from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    pass


class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="The amount must be greater than zero")
    description: Optional[str] = Field(None, max_length=255)
    category: str = Field(..., min_length=1, max_length=50)
    date: Optional[datetime] = Field(default_factory=datetime.utcnow)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None


class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
