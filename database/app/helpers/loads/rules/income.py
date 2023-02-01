from app.ABC.models import Income, User
from app.schemas import IncomeCreate, IncomeUpdate
from .base import Base
from ..errors.income import *


class IncomeRules(Base[Income, IncomeCreate, IncomeUpdate]):
    def get(self, *, who: User, to: Income) -> None:
        if to is None:
            raise income_404
        if not (who.is_superuser) and not (to.category.user_id == who.id):
            raise income_401
        return None

    def delete(self, *, who: User, to: Income) -> None:
        return self.get(who=who, to=to)