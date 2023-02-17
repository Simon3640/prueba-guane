from typing import Generic, TypeVar

from tortoise.transactions import in_transaction

from app.schemas.general import ModelType, CreateSchemaType, UpdateSchemaType
from app.ABC.rules import ABCRule
from app.ABC.models import User

RuleType = TypeVar("RuleType", bound=ABCRule)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, RuleType]):
    def __init__(self, model: ModelType, rules: RuleType):
        """
        Factory para el crud
        """
        self.model = model
        self.rules = rules

    async def get(self, who: User, *, id: int) -> ModelType | None:
        async with in_transaction() as db:
            obj_db = await self.model.filter(id=id).using_db(_db=db).first()
            self.rules.get(who=who, to=obj_db)
            return obj_db

    async def get_multi(
        self, who: User, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        async with in_transaction() as db:
            objs_db = await self.model.all(using_db=db).offset(skip).limit(limit).all()
            self.rules.get_multi(who=who)
            return objs_db

    async def create(self, who: User, *, obj_in: CreateSchemaType) -> ModelType:
        async with in_transaction() as db:
            self.rules.create(who=who, to=obj_in)
            db_obj = await self.model.create(using_db=db, **obj_in.dict())
            return db_obj

    async def update(
        self, who: User, *, obj_in: UpdateSchemaType | dict, id: int
    ) -> ModelType:
        async with in_transaction() as db:
            db_obj = self.get(who, id=id)
            self.rules.update(who=who, to=db_obj, obj_in=obj_in)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            await self.model.filter(id=id).using_db(_db=db).update(**update_data)
            db_obj = await self.model.get(id=id)
            return db_obj

    async def delete(self, who: User, *, id: int) -> bool:
        async with in_transaction() as db:
            obj_db = await self.model.filter(id=id).using_db(_db=db).first()
            self.rules.delete(who=who, to=obj_db)
            await obj_db.delete(using_db=db)
            return True
