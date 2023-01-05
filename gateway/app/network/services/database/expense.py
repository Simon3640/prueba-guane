from .base import ServiceBase
from app.schemas import ExpenseCreate, ExpenseUpdate
from app.core.config import get_app_settings

settings = get_app_settings()


class ExpenseService(ServiceBase[ExpenseCreate, ExpenseUpdate]):
    pass

expense_service = ExpenseService(settings.database_svc + 'expense/')