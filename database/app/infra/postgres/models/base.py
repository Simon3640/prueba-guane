from tortoise.models import Model
from tortoise.fields import DatetimeField, BigIntField


class Base(Model):
    id = BigIntField(pk=True, index=True)

    class Meta:
        abstract = True


class BaseCreatedUpdatedAtModel:
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)
