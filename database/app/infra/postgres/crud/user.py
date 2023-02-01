from tortoise.transactions import in_transaction

from app.core.logging import get_logging
from app.schemas import UserCreate, UserUpdate
from app.infra.postgres.models import User
from app.helpers.loads.errors.user import user_diferent_password, user_registered
from app.helpers.loads.rules import UserRules
from .base import CRUDBase
from app.services.security import bcrypt


log = get_logging(__name__)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate, UserRules]):
    # This method is only used by the middleware for get the user with no rule
    async def get_middleware(
        self, id: int
    ) -> User | None:
        async with in_transaction() as db:
            obj_db = await User.filter(id=id).using_db(_db=db).first()
            return obj_db

    # This method help us to get an user by email
    async def get_by_email(
        self, email: str
    ) -> User:
        email = email.upper()
        async with in_transaction() as db:
            obj_db = await User.filter(email=email).using_db(_db=db).first()
            return obj_db

    # This method help us to get an user by username
    async def get_by_username(
        self, username: str
    ) -> User:
        username = username.upper()
        async with in_transaction() as db:
            obj_db = await User.filter(username=username).using_db(_db=db).first()
            return obj_db

    # This method help us to get all user in platform
    async def get_multi(
        self,
        who: User,
        *,
        skip: int = 0,
        limit: int = 100,
        active: bool = True,
    ) -> list[User]:
        async with in_transaction() as db:
            self.rules.get_multi(who=who)
            objs_db = await (
                User.all(using_db=db)
                .filter(is_active=active)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return objs_db

    async def create(
        self,
        *,
        obj_in: UserCreate
    ) -> User:
        async with in_transaction() as db:
            user: User = await self.get_by_username(username=obj_in.username) or await self.get_by_email(email=obj_in.email)
            self.rules.create(to=user)
            hashed_password = bcrypt.get_password_hash(obj_in.password)
            data = dict(obj_in)
            del data['password']
            data['hashed_password'] = hashed_password
            db_obj = await User.create(using_db=db, **data)
            return db_obj

    async def update(
        self,
        who: User,
        *,
        obj_in: UserUpdate | dict,
        id: int
    ) -> User:
        async with in_transaction() as db:
            db_obj = await self.get(who, id=id)
            user: User = await self.get_by_username(
                obj_in.username) or await self.get_by_email(obj_in.email)
            # Error
            if user and (user.id != id):
                raise user_registered
            # Handle data
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            self.rules.update(who=who, to=db_obj, obj_in=obj_in)
            # Update
            await User.filter(id=id).using_db(db).update(**update_data)
            # Return User
            return await User.get(id=id, using_db=db)

    async def update_password(
        self,
        who: User,
        *,
        password: str,
        confirmPassword: str,
        db_obj: User,
    ) -> User:
        async with in_transaction() as db:
            self.rules.update_password(
                who=who, to=db_obj, password=password, confirmpassword=confirmPassword
            )
            update_data = {
                "hashed_password": bcrypt.get_password_hash(password)
            }
            return await super().update(db=db, who=who, obj_in=update_data)

    async def authenticate(
        self,
        *,
        username: str,
        password: str
    ) -> User:
        async with in_transaction() as db:
            user: User = await self.get_by_email(
                username) or await self.get_by_username(username)
            self.rules.authenticate(who=user)
            if not bcrypt.check_password(password, user.hashed_password):
                raise user_diferent_password
            return user


rules = UserRules()
user = CRUDUser(User, rules)
