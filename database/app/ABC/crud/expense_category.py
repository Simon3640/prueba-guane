from app.schemas import ExpenseCategoryCreate, ExpenseCategoryUpdate
from app.ABC.models import ExpenseCategory, User
from .crud import ABCCRUD


class ABCCRUDExpenseCategory(
    ABCCRUD[ExpenseCategory, ExpenseCategoryCreate, ExpenseCategoryUpdate]
):
    async def get_prefetch(self, who: User, *, id: int) -> ExpenseCategory | None:
        ...
