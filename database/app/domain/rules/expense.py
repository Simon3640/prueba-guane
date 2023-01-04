from app.domain.models import Expense, User
from app.domain.errors.expenses import *
from app.domain.schemas import ExpenseCreate, ExpenseUpdate
from .base import Base


class ExpenseRules(Base[Expense, ExpenseCreate, ExpenseUpdate]):
    def get(self, *, who: User, to: Expense) -> None:
        if not (who.is_superuser) and not (to.user_id == who.id):
            raise expense_401
        return None
    
    def delete(self, *, who: User, to: Expense) -> None:
        if not (who.is_superuser) and not (to.user_id == who.id):
            raise expense_401
        return None
    
    def update(self, *, who: User, to: Expense, obj_in: ExpenseUpdate | dict) -> None:
        if not (who.is_superuser) and not (to.user_id == who.id):
            raise expense_401
        return None