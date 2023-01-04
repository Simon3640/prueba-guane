from datetime import datetime

from pydantic import BaseModel, Field, validator


class ExpenseBase(BaseModel):
    name: str = Field(max_length=50)
    value: float = Field(lt=2**1023 * (2**53 - 1) / 2**52)
    payment_date: datetime


class ExpenseCreateBase(ExpenseBase):
    pass

class ExpenseCreate(ExpenseBase):
    user_id: int
    @validator('name')
    def convert_upper(cls, v, values):
        return v.upper()

class ExpenseUpdate(ExpenseCreateBase):
    pass

class ExpenseInDB(ExpenseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode=True
