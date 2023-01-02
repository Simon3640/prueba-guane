from typing import Any

from tortoise.backends.base.client import BaseDBAsyncClient

from app.core.logging import get_logging
from app.domain.schemas import UserCreate, UserUpdate
from app.domain.models import User
from app.domain.errors.user import user_diferent_password
from app.domain.rules import UserRules
from .base import CRUDBase
from app.services.security import bcrypt


log = get_logging(__name__)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate, UserRules]):
    # This method is only used by the middleware for get the user with no rule
    async def get_middleware(
        self, db: BaseDBAsyncClient, id: int
    ) -> User | None:
        obj_db = await User.filter(id=id).using_db(_db=db).first()
        return obj_db

    # This method help us to get an user by email
    async def get_by_email(
        self, db: BaseDBAsyncClient, email: str
    ) -> User:
        email = email.upper()
        obj_db = await User.filter(email=email).using_db(_db=db).first()
        return obj_db

    # This method help us to get an user by username
    async def get_by_username(
        self, db: BaseDBAsyncClient, username: str
    ) -> User:
        username = username.upper()
        obj_db = User.filter(username=username).using_db(_db=db).first()
        return obj_db

    # This method help us to get all user in platform
    async def get_multi(
        self,
        db: BaseDBAsyncClient,
        who: User,
        *,
        skip: int = 0,
        limit: int = 100,
        active: bool = True,
    ) -> list[User]:
        self.rules.get_multi(who=who)
        objs_db = await (
            User.all(using_db=db)
            .filter(is_active=active)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return objs_db

    # No debe ser expuesta en ningún momento, se hace para uso interno de la aplicación

    async def create(
        self,
        db: BaseDBAsyncClient,
        obj_in: UserCreate
    ) -> User:
        user: User = self.get_by_username(
            db, username=obj_in.username) or self.get_by_email(db=db, email=obj_in.email)
        self.rules.create(to=user)
        hashed_password = bcrypt.get_password_hash(obj_in.password)
        data = dict(obj_in)
        del data['password']
        data['hashed_password'] = hashed_password
        db_obj = User.create(using_db=db, **data)
        return db_obj

    async def update(
        self,
        db: BaseDBAsyncClient,
        who: User,
        *,
        db_obj: User,
        obj_in: UserUpdate | dict[str, Any]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return await super().update(db, db_obj=db_obj, who=who, obj_in=update_data)

    async def update_password(
        self,
        db: BaseDBAsyncClient,
        password: str,
        confirmPassword: str,
        db_obj: User,
        who: User
    ) -> User:
        self.rules.update_password(
            who=who, to=db_obj, password=password, confirmpassword=confirmPassword
        )
        update_data = {
            "hashed_password": bcrypt.get_password_hash(password)
        }
        return await super().update(db=db, who=who, db_obj=db_obj, obj_in=update_data)

    async def authenticate(
        self,
        db: BaseDBAsyncClient,
        *,
        username: str = None,
        password: str
    ) -> User:
        user: User = await self.get_by_email(db, username) or await self.get_by_username(
            db, username)
        if not bcrypt.check_password(password, user.hashed_password):
            raise user_diferent_password
        self.rules.authenticate(who=user)
        return user


user = CRUDUser(User, UserRules)
