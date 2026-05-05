from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.assistant_schema import AssistantCreate, AssistantResponse
from app.services import assistant_service

router = APIRouter()

@router.post("/", response_model=AssistantResponse)
def register_assistant(assistant_in: AssistantCreate, db: Session = Depends(get_db)):
    return assistant_service.create_assistant(db, assistant_in)