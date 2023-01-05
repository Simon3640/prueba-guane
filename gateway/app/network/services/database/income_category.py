from .base import ServiceBase
from app.schemas import IncomeCategoryCreate, IncomeCategoryUpdate
from app.core.config import get_app_settings

settings = get_app_settings()


class IncomeCategoryService(ServiceBase[IncomeCategoryCreate, IncomeCategoryUpdate]):
    pass

income_category_service = IncomeCategoryService(settings.database_svc + 'income-category/')