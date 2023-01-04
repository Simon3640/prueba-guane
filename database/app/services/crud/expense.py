from tortoise.backends.base.client import BaseDBAsyncClient

from app.domain.models import Expense, User
from app.domain.rules import ExpenseRules
from app.domain.schemas import ExpenseCreate, ExpenseUpdate
from .base import CRUDBase


class CRUDExpense(CRUDBase[Expense, ExpenseCreate, ExpenseUpdate, ExpenseRules]):
    async def get_multi(
        self,
        db: BaseDBAsyncClient,
        who: User,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> list[Expense]:
        expenses = Expense.all().using_db(_db=db)
        if not who.is_superuser:
            expenses = expenses.filter(user_id=who.id)
        return await expenses.offset(skip).limit(limit)


expense = CRUDExpense(Expense, ExpenseRules())
