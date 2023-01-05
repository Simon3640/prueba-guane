from fastapi import APIRouter

from .routes import user, auth, expense, expense_category, income

api_route = APIRouter()

api_route.include_router(user.router, prefix='/user', tags=['user'])
api_route.include_router(auth.router, prefix='/auth', tags=['auth'])
api_route.include_router(expense.router, prefix='/expense', tags=['expense'])
api_route.include_router(expense_category.router, prefix='/expense-category', tags=['expense-category'])
api_route.include_router(income.router, prefix='/income', tags=['income'])