from .base import ServiceBase
from app.ABC.models import User
from app.ABC.crud import ABCCRUDUser
from app.schemas import UserCreate, UserUpdate


class UserService(ServiceBase[User, UserCreate, UserUpdate, ABCCRUDUser]):
    async def get_middleware(
        self, id: int
    ) -> User | None:
        return await self.crud.get_middleware(id)

    async def get_by_email(
        self, email: str
    ) -> User:
        return await self.crud.get_by_email(email)

    async def get_by_username(
        self, username: str
    ) -> User:
        return await self.crud.get_by_username(username)

    async def get_multi(
        self,
        who: User,
        *,
        skip: int = 0,
        limit: int = 100,
        active: bool = True,
    ) -> list[User]:
        return await self.crud.get_multi(who, skip=skip, limit=limit, active=active)

    async def create(
        self,
        *,
        obj_in: UserCreate
    ) -> User:
        return await self.crud.create(obj_in=obj_in)

    async def update(
        self,
        who: User,
        *,
        obj_in: UserUpdate,
        id: int
    ) -> User:
        return await self.crud.update(who, obj_in=obj_in, id=id)

    async def update_password(
        self,
        who: User,
        *,
        password: str,
        confirmPassword: str,
        db_obj: User,
    ) -> User:
        return await self.crud.update_password(who, password=password, confirmPassword=confirmPassword, db_obj=db_obj)

    async def authenticate(
        self,
        *,
        username: str,
        password: str
    ) -> User:
        return await self.crud.authenticate(username=username, password=password)