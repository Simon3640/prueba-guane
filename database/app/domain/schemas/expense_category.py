from typing import Any
from datetime import datetime

from pydantic import BaseModel, validator

from .expense import ExpenseInDB


class ExpenseCategoryBase(BaseModel):
    name: str
    budget: float | None


class ExpenseCategoryCreateBase(ExpenseCategoryBase):
    @validator('name')
    def convert_upper(cls, v, values):
        return v.upper()


class ExpenseCategoryCreate(ExpenseCategoryCreateBase):
    user_id: int


class ExpenseCategoryUpdate(ExpenseCategoryCreateBase):
    pass


class ExpenseCategoryInDB(ExpenseCategoryCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ExpenseCategoryResponse(ExpenseCategoryInDB):
    expenses: list[ExpenseInDB]
