from app.domain.models import IncomeCategory
from app.domain.schemas import IncomeCategoryCreate, IncomeCategoryUpdate
from .base import Base

class IncomeCategoryRules(Base[IncomeCategory, IncomeCategoryCreate, IncomeCategoryUpdate]):
    pass