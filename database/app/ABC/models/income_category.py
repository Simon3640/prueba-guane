from typing import Protocol


class IncomeCategory(Protocol):
    @property
    def user_id(self) -> int:
        ...

    @property
    def name(self) -> str:
        ...