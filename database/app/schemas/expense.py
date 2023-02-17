from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, validator


class ExpenseBase(BaseModel):
    name: str = Field(max_length=50)
    value: float = Field(lt=2**1023 * (2**53 - 1) / 2**52)
    payment_date: datetime
    category_id: int


class ExpenseCreate(ExpenseBase):
    @validator("name")
    def convert_upper(cls, v, values):
        return v.upper()


class ExpenseUpdate(ExpenseCreate):
    pass


class ExpenseInDB(ExpenseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
