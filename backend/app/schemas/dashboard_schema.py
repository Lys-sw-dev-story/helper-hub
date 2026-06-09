from pydantic import BaseModel

from app.core.constants import DocumentStatus


class DashboardCounts(BaseModel):
    client_count: int
    assistant_count: int
    active_assignment_count: int
    not_submitted_document_count: int
    submitted_document_count: int


class DocumentStatusBarItem(BaseModel):
    status: DocumentStatus
    count: int


class DashboardSummary(BaseModel):
    counts: DashboardCounts
    document_status_chart: list[DocumentStatusBarItem]
