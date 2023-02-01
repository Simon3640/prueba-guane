from typing import Protocol, Any, Generic

from ..models import User
from app.schemas.general import ModelType, UpdateSchemaType, CreateSchemaType


class ABCCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType], Protocol):
    async def get(self, who: User, *, id: int) -> ModelType:
        """Method to get a object from db"""

    async def get_multi(
        self,
        who: User,
        *,
        skip: int,
        limit: int
    ) -> list[ModelType]:
        """Method to get multiple objects"""

    async def create(
        self,
        who: User,
        *,
        obj_in: CreateSchemaType
    ) -> ModelType:
        """Method to create a object"""
    
    async def update(
        self,
        who: User,
        *,
        obj_in: UpdateSchemaType,
        id: int
    ) -> ModelType:
        """Method to update a object"""
    
    async def delete(
        self,
        who: User,
        *,
        id: int
    ) -> bool:
        """Method to delete a object"""
