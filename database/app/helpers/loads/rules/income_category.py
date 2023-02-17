from app.ABC.models import IncomeCategory
from app.schemas import IncomeCategoryCreate, IncomeCategoryUpdate
from .base import Base


class IncomeCategoryRules(
    Base[IncomeCategory, IncomeCategoryCreate, IncomeCategoryUpdate]
):
    pass
