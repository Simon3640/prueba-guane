from tortoise.fields import (
    CharField, FloatField, DatetimeField, ForeignKeyRelation, ForeignKeyField)

from .base import BaseCreatedUpdatedAtModel, Base
from .user import User
from .expense_category import ExpenseCategory


class Expense(Base, BaseCreatedUpdatedAtModel):
    name = CharField(max_length=50, null=False)
    value = FloatField(null=False)
    payment_date = DatetimeField(null=False)

    category: ForeignKeyRelation[ExpenseCategory] = ForeignKeyRelation(
        'models.ExpenseCategory', related_name='expenses', to_field='id')
