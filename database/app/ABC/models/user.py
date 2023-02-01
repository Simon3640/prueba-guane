from typing import Protocol

from .base import Base, BaseCreatedUpdatedAtModel


class User(Base, BaseCreatedUpdatedAtModel, Protocol):
    @property
    def username(self) -> str:
        ...

    @property
    def email(self) -> str:
        ...

    @property
    def names(self) -> str:
        ...

    @property
    def last_names(self) -> str:
        ...
    
    @property
    def is_superuser(self) -> bool:
        ...
    
    @property
    def is_active(self) -> bool:
        ...

    @property
    def hashed_password(self) -> bool:
        ...