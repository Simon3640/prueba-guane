from typing import TYPE_CHECKING

from tortoise.fields import CharField, ForeignKeyRelation, ReverseRelation, FloatField

from .base import BaseCreatedUpdatedAtModel, Base
from .user import User

if TYPE_CHECKING:
    from .income import Income


class IncomeCategory(Base, BaseCreatedUpdatedAtModel):
    name = CharField(max_length=50, null=False)

    user: ForeignKeyRelation[User] = ForeignKeyRelation(
        "models.User", related_name="income_categories", to_field="id"
    )
    incomes: ReverseRelation["Income"]
