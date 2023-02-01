from tortoise.fields import (CharField,
                             FloatField, DatetimeField, ForeignKeyRelation)

from .base import BaseCreatedUpdatedAtModel, Base
from .income_category import IncomeCategory


class Income(Base, BaseCreatedUpdatedAtModel):
    name = CharField(max_length=50, null=False)
    value = FloatField(null=False)

    category: ForeignKeyRelation[IncomeCategory] = ForeignKeyRelation(
        'models.IncomeCategory', related_name='incomes', to_field='id')
