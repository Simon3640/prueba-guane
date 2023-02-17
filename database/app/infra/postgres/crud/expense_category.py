from tortoise.transactions import in_transaction

from app.infra.postgres.models import ExpenseCategory, User
from app.helpers.loads.rules import ExpenseCategoryRules
from app.schemas import (
    ExpenseCategoryCreate,
    ExpenseCategoryUpdate,
    ExpenseCategoryResponse,
)
from .base import CRUDBase


class CRUDExpenseCategory(
    CRUDBase[
        ExpenseCategory,
        ExpenseCategoryCreate,
        ExpenseCategoryUpdate,
        ExpenseCategoryRules,
    ]
):
    async def get_prefetch(
        self, who: User, *, id: int
    ) -> ExpenseCategoryResponse | None:
        async with in_transaction() as db:
            category = await (
                ExpenseCategory.filter(id=id)
                .using_db(_db=db)
                .first()
                .prefetch_related("expenses")
            )
            self.rules.get(who=who, to=category)
            expenses = await category.expenses.all().using_db(db)
            return ExpenseCategoryResponse(**category.__dict__, expenses=expenses)

    async def get_multi(
        self, who: User, *, skip: int = 0, limit: int = 100
    ) -> list[ExpenseCategory]:
        async with in_transaction() as db:
            self.rules.get_multi(who=who)
            categories = ExpenseCategory.all().using_db(_db=db)
            if not who.is_superuser:
                categories = categories.filter(user_id=who.id)
            return await categories.offset(skip).limit(limit)


expense_category = CRUDExpenseCategory(ExpenseCategory, ExpenseCategoryRules())
