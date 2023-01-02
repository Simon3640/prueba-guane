from typing import Union, Dict, Any

from app.domain.models import User
from app.domain.errors.user import *
from app.domain.schemas import UserUpdate, UserCreate
from .base import Base


# We create the rules for handle users
class UserPolicy(Base[User, UserCreate, UserUpdate]):
    def __init__(self) -> None:
        pass
    
    # rule for know if an user exists
    def get_by_email_id(self, to: User):
        if not to:
            raise user_404

    # This rule filter who can see another user
    def get(self, who: User, to: User) -> None:
        if not (who.is_superuser < 9) and not (who.id == to.id):
            raise user_401
        return None

    # This rule decide who can see the list of users
    def get_multi(self, who: User) -> None:
        if not (who.is_superuser):
            raise user_401
        return None

    def create(self, to: User) -> None:
        if to:
            raise user_registered

    # This rule handle who can update a user and if himself is trying to deactive
    def update(self, who: User, obj_in: Union[UserUpdate, Dict[str, Any]], to: User) -> None:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if not (who.is_superuser) and not (who.id == to.id):
            raise user_401
        if 'active' in update_data:
            if who.id == to.id and update_data['active'] != to.is_active:
                raise user_401
        return None

    # This rule handle update password, maybe it will be removed
    def update_password(self, who: User, to: User, password, confirmpassword) -> None:
        if not (who.is_superuser < 9) and not (who.id == to.id):
            raise user_401
        if not password == confirmpassword:
            raise user_diferent_password
        return None

    # This rule handle who can delete an user, it will be removed
    def delete(self, who: User, to: User | None) -> None:
        if not (who.is_superuser < 9):
            raise user_401
        return None

    # rule for authenticate user, if is inactive raise error
    def authenticate(self, who: User):
        if not who:
            raise user_404
        if not who.is_active:
            raise user_inactive
        
        