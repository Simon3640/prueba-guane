from typing import Protocol, Type

from .models.user import User


class Object(Protocol):
    @property
    def id(self) -> int:
        ...

    @property
    def created_at(self) -> str:
        ...

    @property
    def updated_at(self) -> str:
        ...


class ABCRule(Protocol):
    def get(self, *, who: User, to: Type[Object]) -> None:
        """Rule to get a object from db"""

    def get_multi(self, *, who: User) -> None:
        """Rule to get multiple objects from db"""

    def create(self, *, who: User, to: Type[Object]) -> None:
        """Rule to create a object in db"""

    def update(self, *, who: User, to: Type[Object], obj_in: Type[Object]) -> None:
        """Rule to update a object from db"""

    def delete(self, *, who: User, to: Type[Object]) -> None:
        """Rule to delete a object in db"""
