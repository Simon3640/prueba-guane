from app.domain.models import ExpenseCategory
from app.domain.schemas import ExpenseCategoryCreate, ExpenseCategoryUpdate
from .base import Base

class ExpenseCategoryRules(Base[ExpenseCategory, ExpenseCategoryCreate, ExpenseCategoryUpdate]):
    pass