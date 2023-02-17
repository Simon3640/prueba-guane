from typing import Protocol


class ExpenseCategory(Protocol):
    @property
    def user_id(self) -> int:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def budget(self) -> float:
        ...
