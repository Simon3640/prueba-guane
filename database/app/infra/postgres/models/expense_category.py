from typing import TYPE_CHECKING

from tortoise.fields import CharField, ForeignKeyRelation, ReverseRelation, FloatField

from .base import BaseCreatedUpdatedAtModel, Base
from .user import User

if TYPE_CHECKING:
    from .expense import Expense


class ExpenseCategory(Base, BaseCreatedUpdatedAtModel):
    name = CharField(max_length=50, null=False)
    budget = FloatField(null=True)

    user: ForeignKeyRelation[User] = ForeignKeyRelation(
        "models.User", related_name="expense_categories", to_field="id"
    )
    expenses: ReverseRelation["Expense"]
