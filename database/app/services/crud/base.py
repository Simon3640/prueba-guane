from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from tortoise.backends.base.client import BaseDBAsyncClient

from app.domain.models.base import Base
from app.domain.rules import base
from app.domain.models import User

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
Rules = TypeVar("Rules", bound=base.Base)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, Rules]):
    def __init__(self, model: Type[ModelType], rules: Type[Rules]):
        """
        Factory para el crud
        """
        self.model = model
        self.rules = rules

    async def get(self, db: BaseDBAsyncClient, who: User, *, id: int) -> ModelType | None:
        obj_db = await self.model.filter(id=id).using_db(_db=db).first()
        self.rules.get(who=who, to=obj_db)
        return obj_db

    async def get_multi(
        self,
        db: BaseDBAsyncClient,
        who: User,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> list[ModelType]:
        objs_db = await self.model.all(using_db=db).offset(skip).limit(limit).all()
        self.rules.get_multi(who=who)
        return objs_db

    async def create(
        self,
        db: BaseDBAsyncClient,
        who: User,
        *,
        obj_in: CreateSchemaType
    ) -> ModelType:
        self.rules.create(who=who, to=obj_in)
        # We ignore types
        obj_in_data = dict(obj_in)
        db_obj = await self.model.create(using_db=db, **obj_in_data)
        return db_obj

    async def update(
        self,
        db: BaseDBAsyncClient,
        who: User,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType
    ) -> ModelType:
        self.rules.update(who=who, to=db_obj, obj_in=obj_in)
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        await self.model.filter(id=db_obj.id).using_db(
            _db=db).update(**update_data)
        db_obj = await self.model.get(id=db_obj.id)
        return db_obj

    async def delete(self, db: BaseDBAsyncClient, who: User, *, id: int) -> bool:
        obj_db = await self.model.filter(id=id).using_db(_db=db).first()
        self.rules.delete(who=who, to=obj_db)
        await obj_db.delete(using_db=db)
        return True
