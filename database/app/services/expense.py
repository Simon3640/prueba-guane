from .base import ServiceBase
from app.ABC.models import Expense, User
from app.ABC.crud import ABCCRUDExpense
from app.schemas import ExpenseCreate, ExpenseUpdate


class ExpenseService(
    ServiceBase[Expense, ExpenseCreate, ExpenseUpdate, ABCCRUDExpense]
):
    async def get_related(self, who: User, *, id: int) -> Expense | None:
        return await self.crud.get_related(who, id=id)
