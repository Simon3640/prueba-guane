from typing import Type, TypeVar, Generic, Union, Dict, Any
from pydantic import BaseModel

from app.domain.models import base

ModelType = TypeVar("ModelType", bound=base.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# Generamos una clase para crear las reglas del crud
class Base(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self) -> None:
        pass

    def get(self, to: Type[ModelType]) -> None:
        pass

    def get_multi(self) -> None:
        pass

    def create(self, to: Type[CreateSchemaType]) -> None:
        pass

    def update(
        self,
        to: Type[ModelType],
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> None:
        pass

    def delete(self, to: Type[ModelType]) -> None:
        pass
