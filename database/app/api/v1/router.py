from fastapi import APIRouter

from app.api.v1.routes import user, expense, expense_category

api_route = APIRouter()

api_route.include_router(user.router, prefix='/user', tags=['user'])
api_route.include_router(expense.router, prefix='/expense', tags=['expense'])
api_route.include_router(expense_category.router, prefix='/expense-category', tags=['expense-category'])