from tortoise.fields import CharField, BooleanField

from .base import BaseCreatedUpdatedAtModel, BaseDBModel


class User(BaseDBModel, BaseCreatedUpdatedAtModel):

    username = CharField(max_length=20, unique=True, null=False)
    email = CharField(max_length=255, unique=True, null=False)
    names = CharField(max_length=50, null=False)
    last_names = CharField(max_length=50, null=False)
    hashed_password = CharField(max_length=128, null=False)
    is_active = BooleanField(default=True)
    is_superuser = BooleanField(default=False)
