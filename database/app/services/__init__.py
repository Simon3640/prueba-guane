from .user import UserService
from .income import IncomeService
from .income_category import IncomeCategoryService
from .expense import ExpenseService
from .expense_category import ExpenseCategoryService
from app.infra.postgres.models import (
    User,
    Income,
    Expense,
    IncomeCategory,
    ExpenseCategory,
)
from app.infra.postgres.crud import (
    user,
    income,
    expense,
    income_category,
    expense_category,
)


user_service = UserService(User, user)
income_service = IncomeService(Income, income)
expense_service = ExpenseService(Expense, expense)
income_category_service = IncomeCategoryService(IncomeCategory, income_category)
expense_category_service = ExpenseCategoryService(ExpenseCategory, expense_category)