import os
import shutil
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.constants import (
    EXPIRATION_WARNING_DAYS,
    DocumentStatus,
    DocumentTargetType,
)
from app.models.document import Document
from app.models.document_requirement import DocumentRequirement
from app.schemas.document_schema import (
    DocumentChecklistItem,
    DocumentRequirementCreate,
    DocumentRequirementUpdate,
    DocumentResponse,
    DocumentUpdate,
)


UPLOAD_ROOT = Path(__file__).resolve().parents[2] / "uploads"


def compute_status(document: Document, today: date) -> DocumentStatus:
    """is_submitted + expiration_date 조합으로 3종 상태 산출."""
    if not document.is_submitted:
        return DocumentStatus.NOT_SUBMITTED
    if document.expiration_date is None:
        return DocumentStatus.SUBMITTED
    if document.expiration_date < today:
        return DocumentStatus.NOT_SUBMITTED
    if document.expiration_date <= today + timedelta(days=EXPIRATION_WARNING_DAYS):
        return DocumentStatus.EXPIRING_SOON
    return DocumentStatus.SUBMITTED


def _to_response(document: Document, today: date) -> DocumentResponse:
    return DocumentResponse(
        document_id=document.document_id,
        requirement_id=document.requirement_id,
        target_id=document.target_id,
        target_type=DocumentTargetType(document.requirement.target_type),
        document_name=document.requirement.document_name,
        file_path=document.file_path,
        created_date=document.created_date,
        expiration_date=document.expiration_date,
        is_submitted=document.is_submitted,
        needs_revision=bool(document.needs_revision),
        document_memo=document.document_memo,
        status=compute_status(document, today),
    )


def _get_requirement_or_404(db: Session, requirement_id: int) -> DocumentRequirement:
    requirement = (
        db.query(DocumentRequirement)
        .filter(DocumentRequirement.requirement_id == requirement_id)
        .one_or_none()
    )
    if requirement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 필수서류 정의입니다.",
        )
    return requirement


def _get_document_or_404(
    db: Session, organization_id: int, document_id: int
) -> Document:
    document = (
        db.query(Document)
        .filter(
            Document.document_id == document_id,
            Document.organization_id == organization_id,
        )
        .one_or_none()
    )
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="서류를 찾을 수 없습니다.",
        )
    return document


def _save_upload(
    upload: UploadFile, organization_id: int, document_id: int
) -> str:
    org_dir = UPLOAD_ROOT / str(organization_id)
    org_dir.mkdir(parents=True, exist_ok=True)
    safe_name = os.path.basename(upload.filename or "file")
    target = org_dir / f"{document_id}_{safe_name}"
    with target.open("wb") as f:
        shutil.copyfileobj(upload.file, f)
    return str(target)


def list_requirements(
    db: Session, target_type: Optional[DocumentTargetType] = None
) -> list[DocumentRequirement]:
    query = db.query(DocumentRequirement)
    if target_type is not None:
        query = query.filter(DocumentRequirement.target_type == target_type.value)
    return query.order_by(DocumentRequirement.requirement_id).all()


def create_requirement(
    db: Session, payload: DocumentRequirementCreate
) -> DocumentRequirement:
    name = payload.document_name.strip()
    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="서류명을 입력해주세요.",
        )

    duplicate = (
        db.query(DocumentRequirement)
        .filter(
            DocumentRequirement.target_type == payload.target_type.value,
            DocumentRequirement.document_name == name,
        )
        .first()
    )
    if duplicate is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 같은 대상·서류명의 정의가 존재합니다.",
        )

    requirement = DocumentRequirement(
        target_type=payload.target_type.value,
        document_name=name,
        valid_period_years=payload.valid_period_years,
    )
    db.add(requirement)
    db.commit()
    db.refresh(requirement)
    return requirement


def update_requirement(
    db: Session, requirement_id: int, payload: DocumentRequirementUpdate
) -> DocumentRequirement:
    requirement = _get_requirement_or_404(db, requirement_id)
    data = payload.model_dump(exclude_unset=True)

    new_name = data.get("document_name")
    if new_name is not None:
        new_name = new_name.strip()
        if not new_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="서류명을 입력해주세요.",
            )
        duplicate = (
            db.query(DocumentRequirement)
            .filter(
                DocumentRequirement.target_type == requirement.target_type,
                DocumentRequirement.document_name == new_name,
                DocumentRequirement.requirement_id != requirement_id,
            )
            .first()
        )
        if duplicate is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 같은 대상·서류명의 정의가 존재합니다.",
            )
        requirement.document_name = new_name

    if "valid_period_years" in data:
        requirement.valid_period_years = data["valid_period_years"]

    db.commit()
    db.refresh(requirement)
    return requirement


def delete_requirement(db: Session, requirement_id: int) -> None:
    requirement = _get_requirement_or_404(db, requirement_id)
    in_use = (
        db.query(Document.document_id)
        .filter(Document.requirement_id == requirement_id)
        .first()
    )
    if in_use is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 등록된 서류가 있어 삭제할 수 없습니다.",
        )
    db.delete(requirement)
    db.commit()


def list_documents(
    db: Session,
    organization_id: int,
    target_type: Optional[DocumentTargetType],
    target_id: Optional[int],
    today: date,
) -> list[DocumentResponse]:
    query = (
        db.query(Document)
        .join(DocumentRequirement, Document.requirement_id == DocumentRequirement.requirement_id)
        .filter(Document.organization_id == organization_id)
    )
    if target_type is not None:
        query = query.filter(DocumentRequirement.target_type == target_type.value)
    if target_id is not None:
        query = query.filter(Document.target_id == target_id)
    documents = query.order_by(Document.document_id).all()
    return [_to_response(doc, today) for doc in documents]


def get_document(
    db: Session, organization_id: int, document_id: int, today: date
) -> DocumentResponse:
    document = _get_document_or_404(db, organization_id, document_id)
    return _to_response(document, today)


def create_document(
    db: Session,
    organization_id: int,
    requirement_id: int,
    target_id: int,
    upload: Optional[UploadFile],
    expiration_date: Optional[date],
    document_memo: Optional[str],
    today: date,
) -> DocumentResponse:
    requirement = _get_requirement_or_404(db, requirement_id)

    document = Document(
        target_id=target_id,
        requirement_id=requirement.requirement_id,
        organization_id=organization_id,
        created_date=today,
        expiration_date=expiration_date,
        is_submitted=upload is not None,
        document_memo=document_memo,
    )
    db.add(document)
    db.flush()  # document_id 확보

    if upload is not None:
        document.file_path = _save_upload(upload, organization_id, document.document_id)

    db.commit()
    db.refresh(document)
    return _to_response(document, today)


def update_document(
    db: Session,
    organization_id: int,
    document_id: int,
    payload: DocumentUpdate,
    today: date,
) -> DocumentResponse:
    document = _get_document_or_404(db, organization_id, document_id)

    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(document, field, value)

    db.commit()
    db.refresh(document)
    return _to_response(document, today)


def replace_document_file(
    db: Session,
    organization_id: int,
    document_id: int,
    upload: UploadFile,
    today: date,
) -> DocumentResponse:
    document = _get_document_or_404(db, organization_id, document_id)
    document.file_path = _save_upload(upload, organization_id, document.document_id)
    document.is_submitted = True
    if document.created_date is None:
        document.created_date = today
    db.commit()
    db.refresh(document)
    return _to_response(document, today)


def delete_document(
    db: Session, organization_id: int, document_id: int
) -> None:
    document = _get_document_or_404(db, organization_id, document_id)
    if document.file_path:
        try:
            Path(document.file_path).unlink(missing_ok=True)
        except OSError:
            pass
    db.delete(document)
    db.commit()


def build_checklist(
    db: Session,
    organization_id: int,
    target_type: DocumentTargetType,
    target_id: int,
    today: date,
) -> list[DocumentChecklistItem]:
    """target (client/assistant/organization) 별 필수서류 체크리스트.

    각 requirement 마다 실제 제출된 document 가 있는지 확인하고,
    있으면 그 document 의 상태, 없으면 NOT_SUBMITTED 를 돌려준다.
    """
    requirements = list_requirements(db, target_type)

    documents_by_req = {
        doc.requirement_id: doc
        for doc in db.query(Document)
        .filter(
            Document.organization_id == organization_id,
            Document.target_id == target_id,
        )
        .all()
    }

    items: list[DocumentChecklistItem] = []
    for req in requirements:
        document = documents_by_req.get(req.requirement_id)
        if document is None:
            items.append(
                DocumentChecklistItem(
                    requirement_id=req.requirement_id,
                    document_name=req.document_name,
                    valid_period_years=req.valid_period_years,
                    document_id=None,
                    expiration_date=None,
                    file_path=None,
                    status=DocumentStatus.NOT_SUBMITTED,
                )
            )
        else:
            items.append(
                DocumentChecklistItem(
                    requirement_id=req.requirement_id,
                    document_name=req.document_name,
                    valid_period_years=req.valid_period_years,
                    document_id=document.document_id,
                    expiration_date=document.expiration_date,
                    file_path=document.file_path,
                    status=compute_status(document, today),
                )
            )
    return items
