from app.ABC.models import User
from ..errors.user import *
from app.schemas import UserUpdate, UserCreate
from .base import Base


# We create the rules for handle users
class UserRules(Base[User, UserCreate, UserUpdate]):
    def __init__(self):
        ...

    def get(self, *, who: User, to: User) -> None:
        if not to:
            raise user_404
        if (not who.is_superuser) and not (who.id == to.id):
            raise user_401
        return None

    def get_multi(self, *, who: User) -> None:
        if not who.is_superuser:
            raise user_401
        return None

    # rule for know if an user exists
    def get_by_email_id(self, *, to: User):
        if not to:
            raise user_404
        return None

    def create(self, *, to: User) -> None:
        if to:
            raise user_registered

    # This rule handle update password, maybe it will be removed
    def update_password(self, *, who: User, to: User,
                        password: str, confirmpassword: str) -> None:
        if not (who.is_superuser) and not (who.id == to.id):
            raise user_401
        if not password == confirmpassword:
            raise user_diferent_password
        return None

    def delete(self, *, who: User, to: User) -> None:
        if not who.is_superuser:
            raise user_401

    # rule for authenticate user, if is inactive raise error
    def authenticate(self, *, who: User) -> None:
        if not who:
            raise user_diferent_password
        if not who.is_active:
            raise user_inactive
        return None
