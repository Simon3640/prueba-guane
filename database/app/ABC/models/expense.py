from typing import Protocol
from datetime import datetime

from .expense_category import ExpenseCategory


class Expense(Protocol):
    @property
    def category(self) -> ExpenseCategory:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def value(self) -> float:
        ...

    @property
    def payment_date(self) -> datetime:
        ...
