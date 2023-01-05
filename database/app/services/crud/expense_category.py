from tortoise.backends.base.client import BaseDBAsyncClient

from app.domain.models import ExpenseCategory, User
from app.domain.schemas import ExpenseCategoryCreate, ExpenseCategoryUpdate, ExpenseCategoryResponse
from app.domain.rules import ExpenseCategoryRules
from .base import CRUDBase


class CRUDExpenseCategory(CRUDBase[ExpenseCategory, ExpenseCategoryCreate, ExpenseCategoryUpdate, ExpenseCategoryRules]):
    async def get(self, db: BaseDBAsyncClient, who: User, *, id: int) -> ExpenseCategoryResponse | None:
        category = await ExpenseCategory.filter(id=id).using_db(_db=db).first().prefetch_related('expenses')
        self.rules.get(who=who, to=category)
        expenses = await category.expenses.all().using_db(db)
        return ExpenseCategoryResponse(**category.__dict__, expenses=expenses)


expense_category = CRUDExpenseCategory(ExpenseCategory, ExpenseCategoryRules())