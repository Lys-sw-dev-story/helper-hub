from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.assistant import Assistant
from app.schemas.assistant_schema import AssistantCreate, AssistantMemoUpdate


def create_assistant(db: Session, assistant_in: AssistantCreate):
    # 스키마 데이터를 언패킹해서 모델 생성
    db_assistant = Assistant(**assistant_in.model_dump())
    db.add(db_assistant)
    db.commit()
    db.refresh(db_assistant)
    return db_assistant


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
