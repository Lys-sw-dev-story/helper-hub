from fastapi import APIRouter
from app.api.routers import (
    assignment,
    assistant,
    audit,
    auth,
    client,
    dashboard,
    document,
    service_log,
)

api_router = APIRouter()
api_router.include_router(client.router, prefix="/clients", tags=["Clients"])
api_router.include_router(assistant.router, prefix="/assistants", tags=["Assistants"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(document.router, prefix="/documents", tags=["Documents"])
api_router.include_router(
    document.requirement_router,
    prefix="/document-requirements",
    tags=["Document Requirements"],
)
api_router.include_router(
    assignment.router, prefix="/assignments", tags=["Assignments"]
)
api_router.include_router(
    service_log.router, prefix="/service-logs", tags=["Service Logs"]
)
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit"])
