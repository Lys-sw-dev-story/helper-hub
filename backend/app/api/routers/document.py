from datetime import date
from typing import Optional
from urllib.parse import quote

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff
from app.core.constants import DocumentTargetType
from app.core.database import get_db
from app.models.staff import Staff
from app.schemas.document_schema import (
    DocumentChecklistItem,
    DocumentRequirementCreate,
    DocumentRequirementResponse,
    DocumentRequirementUpdate,
    DocumentResponse,
    DocumentUpdate,
)
from app.services import document_service


router = APIRouter()
requirement_router = APIRouter()


@router.get("/checklist", response_model=list[DocumentChecklistItem])
def get_checklist(
    target_type: DocumentTargetType,
    target_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return document_service.build_checklist(
        db=db,
        organization_id=current_staff.organization_id,
        target_type=target_type,
        target_id=target_id,
        today=date.today(),
    )


@router.get("", response_model=list[DocumentResponse])
def list_documents(
    target_type: Optional[DocumentTargetType] = None,
    target_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return document_service.list_documents(
        db=db,
        organization_id=current_staff.organization_id,
        target_type=target_type,
        target_id=target_id,
        today=date.today(),
    )


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return document_service.get_document(
        db=db,
        organization_id=current_staff.organization_id,
        document_id=document_id,
        today=date.today(),
    )


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(
    requirement_id: int = Form(...),
    target_id: int = Form(...),
    expiration_date: Optional[date] = Form(None),
    document_memo: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return document_service.create_document(
        db=db,
        organization_id=current_staff.organization_id,
        requirement_id=requirement_id,
        target_id=target_id,
        upload=file,
        expiration_date=expiration_date,
        document_memo=document_memo,
        today=date.today(),
    )


@router.post("/save", response_model=DocumentResponse)
def save_document(
    requirement_id: int = Form(...),
    target_id: int = Form(...),
    document_id: Optional[int] = Form(None),
    expiration_date: Optional[date] = Form(None),
    document_memo: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    """체크리스트 행 [변경사항 저장] — 파일·만료일·메모를 한 번에 upsert."""
    return document_service.save_document(
        db=db,
        organization_id=current_staff.organization_id,
        requirement_id=requirement_id,
        target_id=target_id,
        document_id=document_id,
        upload=file,
        expiration_date=expiration_date,
        document_memo=document_memo,
        today=date.today(),
    )


@router.get("/{document_id}/file")
def download_document_file(
    document_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    data, file_name, media_type = document_service.get_document_file(
        db=db,
        organization_id=current_staff.organization_id,
        document_id=document_id,
    )
    # 한글 파일명 대응 (RFC 5987)
    disposition = f"attachment; filename*=UTF-8''{quote(file_name)}"
    return Response(
        content=data,
        media_type=media_type,
        headers={"Content-Disposition": disposition},
    )


@router.patch("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: int,
    payload: DocumentUpdate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return document_service.update_document(
        db=db,
        organization_id=current_staff.organization_id,
        document_id=document_id,
        payload=payload,
        today=date.today(),
    )


@router.put("/{document_id}/file", response_model=DocumentResponse)
def replace_document_file(
    document_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return document_service.replace_document_file(
        db=db,
        organization_id=current_staff.organization_id,
        document_id=document_id,
        upload=file,
        today=date.today(),
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    document_service.delete_document(
        db=db,
        organization_id=current_staff.organization_id,
        document_id=document_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@requirement_router.get("", response_model=list[DocumentRequirementResponse])
def list_requirements(
    target_type: Optional[DocumentTargetType] = None,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return document_service.list_requirements(db=db, target_type=target_type)


@requirement_router.post(
    "",
    response_model=DocumentRequirementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_requirement(
    payload: DocumentRequirementCreate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return document_service.create_requirement(db=db, payload=payload)


@requirement_router.patch(
    "/{requirement_id}", response_model=DocumentRequirementResponse
)
def update_requirement(
    requirement_id: int,
    payload: DocumentRequirementUpdate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return document_service.update_requirement(
        db=db, requirement_id=requirement_id, payload=payload
    )


@requirement_router.delete(
    "/{requirement_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_requirement(
    requirement_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    document_service.delete_requirement(db=db, requirement_id=requirement_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
