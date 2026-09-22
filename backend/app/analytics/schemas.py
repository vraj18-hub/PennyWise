from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TransactionOut(BaseModel):
    id: int
    date: datetime
    description: str
    amount: float
    category: str

    model_config = ConfigDict(from_attributes=True)


class UploadResult(BaseModel):
    inserted: int
    skipped: int

class CategoryTotal(BaseModel):
    category: str
    total: float


class SpendingSummary(BaseModel):
    total_income: float
    total_expenses: float
    savings_rate: float
    by_category: list[CategoryTotal]