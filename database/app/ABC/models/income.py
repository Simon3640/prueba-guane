from typing import Protocol

from .income_category import IncomeCategory
from .base import Base, BaseCreatedUpdatedAtModel


class Income(Base, BaseCreatedUpdatedAtModel, Protocol):
    @property
    def category(self) -> IncomeCategory:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> float:
        ...
