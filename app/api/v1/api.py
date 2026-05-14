from fastapi import APIRouter

from app.api.v1.endpoints import health, login, transactions

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(
    transactions.router, prefix="/transactions", tags=["transactions"]
)
api_router.include_router(login.router, prefix="/login", tags=["login"])
