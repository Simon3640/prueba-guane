from app.domain.models import Income, User
from app.domain.errors.income import *
from app.domain.schemas import IncomeCreate, IncomeUpdate
from .base import Base


class IncomeRules(Base[Income, IncomeCreate, IncomeUpdate]):
    def get(self, *, who: User, to: Income) -> None:
        if to is None:
            raise income_404
        if not (who.is_superuser) and not (to.category.user_id == who.id):
            raise income_401
        return None
    