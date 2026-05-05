from fastapi import APIRouter
from app.api.routers import client, assistant

api_router = APIRouter()
api_router.include_router(client.router, prefix="/clients", tags=["Clients"])
api_router.include_router(assistant.router, prefix="/assistants", tags=["Assistants"])