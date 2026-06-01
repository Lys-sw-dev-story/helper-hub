from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.core.constants import DocumentStatus, DocumentTargetType


class AuditDocumentItem(BaseModel):
    document_id: Optional[int] = None
    requirement_id: int
    document_name: str
    target_type: DocumentTargetType
    target_id: int
    target_name: str
    created_date: Optional[date] = None
    expiration_date: Optional[date] = None
    retention_until: Optional[date] = None
    status: DocumentStatus
    days_until_expire: Optional[int] = None
    days_until_retention_end: Optional[int] = None


class AuditOverview(BaseModel):
    missing: list[AuditDocumentItem]
    expiring_soon: list[AuditDocumentItem]
    retention_ending_soon: list[AuditDocumentItem]


class AuditRecentClient(BaseModel):
    client_id: int
    client_name: str
    client_status: Optional[str] = None
    organization_id: int


class AuditRecentAssistant(BaseModel):
    assistant_id: int
    assistant_name: str
    work_start_date: Optional[date] = None
    organization_id: int


class AuditRecentServiceLog(BaseModel):
    service_log_id: int
    assignment_id: int
    service_date: date
    service_hours: Decimal
    service_count: Optional[int] = None
    service_content: Optional[str] = None
    client_id: int
    client_name: str
    assistant_id: int
    assistant_name: str


class AuditRecentResponse(BaseModel):
    window_years: int
    cutoff_date: date
    retention_years: int
    clients: list[AuditRecentClient]
    assistants: list[AuditRecentAssistant]
    documents: list[AuditDocumentItem]
    service_logs: list[AuditRecentServiceLog]
