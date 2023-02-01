from app.ABC.models import ExpenseCategory
from app.schemas import ExpenseCategoryCreate, ExpenseCategoryUpdate
from .base import Base

class ExpenseCategoryRules(Base[ExpenseCategory, ExpenseCategoryCreate, ExpenseCategoryUpdate]):
    pass