from typing import Protocol

from app.schemas import UserCreate, UserUpdate
from app.ABC.models import User
from .crud import ABCCRUD


class ABCCRUDUser(ABCCRUD[User, UserCreate, UserUpdate], Protocol):
    async def get_middleware(self, id: int) -> User | None:
        ...

    async def get_by_email(self, email: str) -> User:
        ...

    async def get_by_username(self, username: str) -> User:
        ...

    async def get_multi(
        self,
        who: User,
        *,
        skip: int = 0,
        limit: int = 100,
        active: bool = True,
    ) -> list[User]:
        ...

    async def create(self, *, obj_in: UserCreate) -> User:
        ...

    async def update(self, who: User, *, obj_in: UserUpdate, id: int) -> User:
        ...

    async def update_password(
        self,
        who: User,
        *,
        password: str,
        confirmPassword: str,
        db_obj: User,
    ) -> User:
        ...

    async def authenticate(self, *, username: str, password: str) -> User:
        ...
