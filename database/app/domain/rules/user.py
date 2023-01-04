from typing import Any

from app.domain.models import User
from app.domain.errors.user import *
from app.domain.schemas import UserUpdate, UserCreate
from .base import Base


# We create the rules for handle users
class UserRules(Base[User, UserCreate, UserUpdate]):
    def __init__(self) -> None:
        pass

    # rule for know if an user exists
    def get_by_email_id(self, to: User):
        if not to:
            raise user_404
        return None

    def create(self, to: User) -> None:
        if to:
            raise user_registered

    # This rule handle update password, maybe it will be removed
    def update_password(self, password, confirmpassword) -> None:
        if not password == confirmpassword:
            raise user_diferent_password
        return None

    # rule for authenticate user, if is inactive raise error
    def authenticate(self, who: User) -> None:
        if not who:
            raise user_404
        if not who.is_active:
            raise user_inactive
        return None
