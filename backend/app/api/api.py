from fastapi import APIRouter
from app.api.endpoints import login, strategy, reports, projects, subscriptions, payments, admin

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(strategy.router, prefix="/strategy", tags=["strategy"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
