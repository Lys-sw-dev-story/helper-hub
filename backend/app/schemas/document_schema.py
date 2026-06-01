from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.core.constants import DocumentStatus, DocumentTargetType


class DocumentRequirementResponse(BaseModel):
    requirement_id: int
    target_type: DocumentTargetType
    document_name: str
    valid_period_years: Optional[int] = None

    class Config:
        from_attributes = True


class DocumentRequirementCreate(BaseModel):
    target_type: DocumentTargetType
    document_name: str
    valid_period_years: Optional[int] = None


class DocumentRequirementUpdate(BaseModel):
    document_name: Optional[str] = None
    valid_period_years: Optional[int] = None


class DocumentResponse(BaseModel):
    document_id: int
    requirement_id: int
    target_id: int
    target_type: DocumentTargetType
    document_name: str
    file_path: Optional[str] = None
    created_date: Optional[date] = None
    expiration_date: Optional[date] = None
    is_submitted: bool
    needs_revision: bool = False
    document_memo: Optional[str] = None
    status: DocumentStatus

    class Config:
        from_attributes = True


class DocumentUpdate(BaseModel):
    document_memo: Optional[str] = None
    expiration_date: Optional[date] = None
    is_submitted: Optional[bool] = None
    needs_revision: Optional[bool] = None


class DocumentChecklistItem(BaseModel):
    requirement_id: int
    document_name: str
    valid_period_years: Optional[int] = None
    document_id: Optional[int] = None
    expiration_date: Optional[date] = None
    file_path: Optional[str] = None
    status: DocumentStatus
