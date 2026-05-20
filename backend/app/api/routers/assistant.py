from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff
from app.core.database import get_db
from app.models.staff import Staff
from app.schemas.assistant_schema import (
    AssistantCreate,
    AssistantDetail,
    AssistantMemoResponse,
    AssistantMemoUpdate,
    AssistantResponse,
    AssistantUpdate,
)
from app.services import assistant_service

router = APIRouter()


@router.post("/", response_model=AssistantResponse)
def register_assistant(
    assistant_in: AssistantCreate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return assistant_service.create_assistant(
        db, assistant_in, current_staff.organization_id
    )


@router.get("/", response_model=list[AssistantDetail])
def read_assistants(
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return assistant_service.list_assistants(db, current_staff.organization_id)


@router.get("/{assistant_id}", response_model=AssistantDetail)
def read_assistant(
    assistant_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    db_assistant = assistant_service.get_assistant(
        db, assistant_id, current_staff.organization_id
    )
    if db_assistant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 활동지원사를 찾을 수 없습니다.",
        )
    return db_assistant


@router.patch("/{assistant_id}", response_model=AssistantDetail)
def update_assistant(
    assistant_id: int,
    assistant_in: AssistantUpdate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    db_assistant = assistant_service.update_assistant(
        db, assistant_id, assistant_in, current_staff.organization_id
    )
    if db_assistant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 활동지원사를 찾을 수 없습니다.",
        )
    return db_assistant


@router.delete("/{assistant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assistant(
    assistant_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    deleted = assistant_service.delete_assistant(
        db, assistant_id, current_staff.organization_id
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 활동지원사를 찾을 수 없습니다.",
        )
    return None


@router.patch("/{assistant_id}/memo", response_model=AssistantMemoResponse)
def update_assistant_memo(
    assistant_id: int,
    payload: AssistantMemoUpdate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return assistant_service.update_assistant_memo(
        db=db,
        organization_id=current_staff.organization_id,
        assistant_id=assistant_id,
        payload=payload,
    )
