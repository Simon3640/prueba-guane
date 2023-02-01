from tortoise.transactions import in_transaction

from app.infra.postgres.models import Expense, User
from app.helpers.loads.rules import ExpenseRules
from app.schemas import ExpenseCreate, ExpenseUpdate
from .base import CRUDBase


class CRUDExpense(CRUDBase[Expense, ExpenseCreate, ExpenseUpdate, ExpenseRules]):
    async def get_related(self, who: User, *, id: int) -> Expense | None:
        async with in_transaction() as db:
            income = await Expense.filter(id=id).using_db(_db=db).select_related('category').first()
            self.rules.get(who=who, to=income)
            return income

    async def get_multi(
        self,
        who: User,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> list[Expense]:
        async with in_transaction() as db:
            self.rules.get_multi(who=who)
            expenses = Expense.all().using_db(_db=db)
            if not who.is_superuser:
                expenses = expenses.filter(category__user_id=who.id)
            return await expenses.offset(skip).limit(limit)


expense = CRUDExpense(Expense, ExpenseRules())