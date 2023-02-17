from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    email: str
    names: str
    last_names: str
    is_active: bool
    is_superuser: bool
    hashed_password: str | None = "hashed_password"


@dataclass
class Income:
    id: int
    name: str
    value: str
    category_id: int


@dataclass
class IncomeCategory:
    id: int
    name: str
    incomes: list[Income]