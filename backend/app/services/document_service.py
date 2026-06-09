import mimetypes
from datetime import date, timedelta
from pathlib import Path, PurePath
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


MAX_UPLOAD_BYTES = 32 * 1024 * 1024  # 32MB (LONGBLOB 한계 내 안전선)


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
        file_name=_file_display_name(document),
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


def _read_upload(upload: UploadFile) -> tuple[bytes, str]:
    """업로드 파일을 바이트로 읽어 (데이터, 원본파일명) 으로 반환한다.

    파일은 파일시스템이 아니라 document.file_data(LONGBLOB) 에 저장한다
    (팀 결정 2026-06-02). 과도한 용량은 거부한다.
    """
    data = upload.file.read()
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="파일이 너무 큽니다. 32MB 이하만 업로드할 수 있습니다.",
        )
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="빈 파일은 업로드할 수 없습니다.",
        )
    file_name = PurePath(upload.filename or "file").name
    return data, file_name


def _guess_media_type(file_name: Optional[str]) -> str:
    if file_name:
        guessed, _ = mimetypes.guess_type(file_name)
        if guessed:
            return guessed
    return "application/octet-stream"


def _file_display_name(document: Document) -> Optional[str]:
    """표시용 파일명: DB 저장 파일명 우선, 없으면 레거시 경로 베이스네임."""
    if document.file_name:
        return document.file_name
    if document.file_path:
        return PurePath(document.file_path).name
    return None


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

    if upload is not None:
        data, file_name = _read_upload(upload)
        document.file_data = data
        document.file_name = file_name

    db.add(document)
    db.commit()
    db.refresh(document)
    return _to_response(document, today)


def save_document(
    db: Session,
    organization_id: int,
    requirement_id: int,
    target_id: int,
    document_id: Optional[int],
    upload: Optional[UploadFile],
    expiration_date: Optional[date],
    document_memo: Optional[str],
    today: date,
    created_date: Optional[date] = None,
) -> DocumentResponse:
    """체크리스트 행의 [변경사항 저장] 용 upsert.

    document_id 가 있으면 그 문서를, 없으면 새 문서를 만들어 파일·만료일·메모를
    한 번에 반영한다. 프론트에서 파일과 만료일을 모두 입력한 뒤 한 번만 호출한다.
    """
    requirement = _get_requirement_or_404(db, requirement_id)

    # 신규 제출은 반드시 파일이 있어야 한다 (만료일만 있는 빈 문서 생성 방지)
    if document_id is None and upload is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="제출할 파일을 선택해주세요.",
        )

    if document_id is not None:
        document = _get_document_or_404(db, organization_id, document_id)
    else:
        document = Document(
            target_id=target_id,
            requirement_id=requirement.requirement_id,
            organization_id=organization_id,
            is_submitted=False,
        )
        db.add(document)

    if upload is not None:
        data, file_name = _read_upload(upload)
        document.file_data = data
        document.file_name = file_name
        document.file_path = None  # DB 저장으로 전환 — 레거시 경로 무효화
        document.is_submitted = True
        if document.created_date is None:
            document.created_date = today

    # 작성일을 명시적으로 지정하면 우선 적용 (데모: 보관임박 재현용 과거 작성일)
    if created_date is not None:
        document.created_date = created_date

    document.expiration_date = expiration_date
    if document_memo is not None:
        document.document_memo = document_memo

    db.commit()
    db.refresh(document)
    return _to_response(document, today)


def get_document_file(
    db: Session, organization_id: int, document_id: int
) -> tuple[bytes, str, str]:
    """다운로드용 (바이트, 파일명, media_type). DB 저장분 우선, 없으면 레거시 파일시스템."""
    document = _get_document_or_404(db, organization_id, document_id)

    if document.file_data is not None:
        file_name = document.file_name or f"document_{document_id}"
        return bytes(document.file_data), file_name, _guess_media_type(file_name)

    # 레거시: 파일시스템에 저장된 기존 문서
    if document.file_path:
        legacy = Path(document.file_path)
        if legacy.exists():
            file_name = document.file_name or legacy.name
            return legacy.read_bytes(), file_name, _guess_media_type(file_name)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="첨부된 파일이 없습니다.",
    )


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
    data, file_name = _read_upload(upload)
    document.file_data = data
    document.file_name = file_name
    document.file_path = None  # DB 저장으로 전환 — 레거시 경로 무효화
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
                    file_name=_file_display_name(document),
                    status=compute_status(document, today),
                )
            )
    return items
