from .base import ServiceBase
from app.ABC.models import ExpenseCategory, User
from app.ABC.crud import ABCCRUDExpenseCategory
from app.schemas import ExpenseCategoryCreate, ExpenseCategoryUpdate, ExpenseCategoryResponse


class ExpenseCategoryService(ServiceBase[ExpenseCategory, ExpenseCategoryCreate, ExpenseCategoryUpdate, ABCCRUDExpenseCategory]):
    async def get_prefetch(self, who: User, *, id: int) -> ExpenseCategoryResponse | None:
        return await self.crud.get_prefetch(who, id=id)