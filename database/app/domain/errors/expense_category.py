from tortoise.fields import CharField, ForeignKeyRelation, ForeignKeyField

from .base import BaseCreatedUpdatedAtModel, Base
from .user import User


class ExpenseCategory(Base, BaseCreatedUpdatedAtModel):
    name = CharField(max_length=50, null=False)

    user: ForeignKeyRelation[User] = ForeignKeyRelation(
        'models.User', related_name='expense_categories', to_field='id')
