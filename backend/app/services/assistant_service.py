from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.assignment import Assignment
from app.models.assistant import Assistant
from app.schemas.assistant_schema import (
    AssistantCreate,
    AssistantMemoUpdate,
    AssistantUpdate,
)


def _get_owned_assistant(
    db: Session, assistant_id: int, organization_id: int
) -> Assistant:
    assistant = (
        db.query(Assistant)
        .filter(
            Assistant.assistant_id == assistant_id,
            Assistant.organization_id == organization_id,
        )
        .one_or_none()
    )
    if assistant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 활동지원사를 찾을 수 없습니다.",
        )
    return assistant


def create_assistant(db: Session, assistant_in: AssistantCreate):
    # 스키마 데이터를 언패킹해서 모델 생성
    db_assistant = Assistant(**assistant_in.model_dump())
    db.add(db_assistant)
    db.commit()
    db.refresh(db_assistant)
    return db_assistant


def get_assistant(
    db: Session, assistant_id: int, organization_id: int
) -> Assistant:
    return _get_owned_assistant(db, assistant_id, organization_id)


def update_assistant(
    db: Session,
    assistant_id: int,
    organization_id: int,
    payload: AssistantUpdate,
) -> Assistant:
    assistant = _get_owned_assistant(db, assistant_id, organization_id)
    update_data = payload.model_dump(exclude_unset=True)
    if "assistant_name" in update_data and not update_data["assistant_name"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이름은 필수 입력 사항입니다.",
        )
    for field, value in update_data.items():
        setattr(assistant, field, value)
    db.commit()
    db.refresh(assistant)
    return assistant


def delete_assistant(
    db: Session, assistant_id: int, organization_id: int
) -> None:
    assistant = _get_owned_assistant(db, assistant_id, organization_id)
    has_assignment = (
        db.query(Assignment.assignment_id)
        .filter(Assignment.assistant_id == assistant_id)
        .first()
        is not None
    )
    if has_assignment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="배정 이력이 있는 활동지원사는 삭제할 수 없습니다.",
        )
    db.delete(assistant)
    db.commit()


def update_assistant_memo(
    db: Session,
    organization_id: int,
    assistant_id: int,
    payload: AssistantMemoUpdate,
) -> Assistant:
    assistant = (
        db.query(Assistant)
        .filter(
            Assistant.assistant_id == assistant_id,
            Assistant.organization_id == organization_id,
        )
        .one_or_none()
    )
    if assistant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="활동지원사를 찾을 수 없습니다.",
        )
    assistant.assistant_memo = payload.assistant_memo
    db.commit()
    db.refresh(assistant)
    return assistant
