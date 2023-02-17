from fastapi import APIRouter

from app.api.v1.routes import (
    user,
    expense,
    expense_category,
    income,
    income_category,
    auth,
)

api_route = APIRouter()

api_route.include_router(user.router, prefix="/user", tags=["user"])
api_route.include_router(expense.router, prefix="/expense", tags=["expense"])
api_route.include_router(
    expense_category.router, prefix="/expense-category", tags=["expense-category"]
)
api_route.include_router(income.router, prefix="/income", tags=["income"])
api_route.include_router(
    income_category.router, prefix="/income-category", tags=["income-category"]
)
api_route.include_router(auth.router, prefix="/auth", tags=["auth"])
