from typing import Protocol
from datetime import datetime


class Base(Protocol):
    @property
    def id(self) -> int:
        ...


class BaseCreatedUpdatedAtModel(Protocol):
    @property
    def created_at(self) -> datetime:
        ...

    @property
    def updated_at(self) -> datetime:
        ...
