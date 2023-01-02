from tortoise.models import Model
from tortoise.fields import DatetimeField, BigIntField


class Base(Model):
    id = BigIntField(pk=True, index=True)

    async def to_dict(self):
        d = {}
        for field in self._meta.db_fields:
            d[field] = getattr(self, field)
        for field in self._meta.backward_fk_fields:
            d[field] = await getattr(self, field).all().values()
        return d

    class Meta:
        abstract = True


class BaseCreatedUpdatedAtModel:
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)