from typing import Generic, TypeVar, Type

from app.ABC.crud.crud import ABCCRUD
from app.ABC.models import User

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

CrudType = TypeVar("CrudType", bound=ABCCRUD)


class ServiceBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, CrudType]):
    def __init__(self, model: Type[ModelType], crud: CrudType):
        self.crud = crud
        self.model = model

    async def get(self, who: User, *, id: int) -> ModelType | None:
        return await self.crud.get(who, id=id)

    async def get_multi(
        self, who: User, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        return await self.crud.get_multi(who, skip=skip, limit=limit)

    async def create(self, who: User, *, obj_in: CreateSchemaType) -> ModelType:
        return await self.crud.create(who, obj_in=obj_in)

    async def update(
        self, who: User, *, obj_in: UpdateSchemaType | dict, id: int
    ) -> ModelType:
        return await self.crud.update(who, obj_in=obj_in, id=id)

    async def delete(self, who: User, *, id: int) -> bool:
        return await self.crud.delete(who, id=id)
