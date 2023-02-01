from typing import Generic, Any


from app.schemas.general import ModelType, CreateSchemaType, UpdateSchemaType
from app.ABC.models import User
from ..errors.base import _404


# Generamos una clase para crear las reglas del crud
class Base(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self) -> None:
        pass

    def get(self, *, who: User, to: ModelType) -> None:
        if to is None:
            raise _404

    def get_multi(self, *, who: User) -> None:
        pass

    def create(self, *, who: User, to: CreateSchemaType) -> None:
        pass

    def update(
        self,
        *,
        who: User,
        to: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> None:
        pass

    def delete(self, *, who: User, to: ModelType) -> None:
        pass
