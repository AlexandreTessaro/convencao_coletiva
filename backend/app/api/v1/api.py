from fastapi import APIRouter
from app.api.v1.endpoints import auth, companies, convencoes, notifications, dashboard, collector, mediador_search

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(convencoes.router, prefix="/convencoes", tags=["convencoes"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(collector.router, prefix="/collector", tags=["collector"])
api_router.include_router(mediador_search.router, prefix="/mediador", tags=["mediador"])

