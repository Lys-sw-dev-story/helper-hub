from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff
from app.core.database import get_db
from app.models.staff import Staff
from app.models.assistant import Assistant
from app.schemas.assistant_schema import (
    AssistantCreate,
    AssistantResponse,
)
from app.services import assistant_service

router = APIRouter()


@router.get("/")
def read_assistants(
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    assistants = (
        db.query(Assistant)
        .filter(Assistant.organization_id == current_staff.organization_id)
        .order_by(Assistant.assistant_id.desc())
        .all()
    )

    return [
        {
            "assistant_id": assistant.assistant_id,
            "assistant_name": assistant.assistant_name,
            "assistant_phone": assistant.assistant_phone,
            "work_days": assistant.work_days,
            "work_start_date": assistant.work_start_date,
            "assistant_license": assistant.assistant_license,
            "assistant_memo": assistant.assistant_memo,
            "organization_id": assistant.organization_id,
        }
        for assistant in assistants
    ]


@router.post("/", response_model=AssistantResponse)
def register_assistant(
    assistant_in: AssistantCreate,
    db: Session = Depends(get_db),
):
    return assistant_service.create_assistant(db, assistant_in)