from tortoise.fields import (
    CharField, FloatField, DatetimeField, ForeignKeyRelation, ForeignKeyField, CASCADE)

from .base import BaseCreatedUpdatedAtModel, Base
from .user import User


class Expense(Base, BaseCreatedUpdatedAtModel):
    name = CharField(max_length=50, null=False)
    value = FloatField(null=False)
    payment_date = DatetimeField(null=False)

    user: ForeignKeyRelation[User] = ForeignKeyField(
        'models.User', on_delete=CASCADE, related_name='expenses', to_field='id')
