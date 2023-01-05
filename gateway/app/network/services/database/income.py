from .base import ServiceBase
from app.schemas import IncomeCreate, IncomeUpdate
from app.core.config import get_app_settings

settings = get_app_settings()


class incomeService(ServiceBase[IncomeCreate, IncomeUpdate]):
    pass

income_service = incomeService(settings.database_svc + 'income/')