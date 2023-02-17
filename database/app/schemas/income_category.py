from typing import Any
from datetime import datetime

from pydantic import BaseModel, validator

from .income import IncomeInDB


class IncomeCategoryBase(BaseModel):
    name: str


class IncomeCategoryCreateBase(IncomeCategoryBase):
    @validator("name")
    def convert_upper(cls, v, values):
        return v.upper()


class IncomeCategoryCreate(IncomeCategoryCreateBase):
    user_id: int


class IncomeCategoryUpdate(IncomeCategoryCreateBase):
    pass


class IncomeCategoryInDB(IncomeCategoryCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class IncomeCategoryResponse(IncomeCategoryInDB):
    incomes: list[IncomeInDB]
