from fastapi import APIRouter

from app.api.routers import auth


api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
