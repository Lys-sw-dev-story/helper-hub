from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff
from app.core.database import get_db
from app.models.staff import Staff
from app.schemas.assistant_schema import (
    AssistantCreate,
    AssistantMemoResponse,
    AssistantMemoUpdate,
    AssistantResponse,
)
from app.services import assistant_service

router = APIRouter()

@router.post("/", response_model=AssistantResponse)
def register_assistant(assistant_in: AssistantCreate, db: Session = Depends(get_db)):
    return assistant_service.create_assistant(db, assistant_in)


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
