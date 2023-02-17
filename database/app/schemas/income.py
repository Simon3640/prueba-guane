from datetime import datetime

from pydantic import BaseModel, Field, validator


class IncomeBase(BaseModel):
    name: str = Field(max_length=50)
    value: float = Field(lt=2**1023 * (2**53 - 1) / 2**52)
    category_id: int


class IncomeCreate(IncomeBase):
    @validator("name")
    def convert_upper(cls, v, values):
        return v.upper()


class IncomeUpdate(IncomeCreate):
    pass


class IncomeInDB(IncomeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
