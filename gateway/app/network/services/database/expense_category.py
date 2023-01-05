from .base import ServiceBase
from app.schemas import ExpenseCategoryCreate, ExpenseCategoryUpdate
from app.core.config import get_app_settings

settings = get_app_settings()


class ExpenseCategoryService(ServiceBase[ExpenseCategoryCreate, ExpenseCategoryUpdate]):
    pass

expense_category_service = ExpenseCategoryService(settings.database_svc + 'expense-category/')