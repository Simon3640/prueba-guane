from app.schemas import ExpenseCreate, ExpenseUpdate
from app.ABC.models import Expense, User
from .crud import ABCCRUD


class ABCCRUDExpense(ABCCRUD[Expense, ExpenseCreate, ExpenseUpdate]):
    async def get_related(self, who: User, *, id: int) -> Expense | None:
        ...
