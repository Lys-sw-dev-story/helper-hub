from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.assistant_schema import AssistantCreate, AssistantResponse
from app.services import assistant_service

router = APIRouter()

@router.post("/", response_model=AssistantResponse) # assistant 추가
def register_assistant(assistant_in: AssistantCreate, db: Session = Depends(get_db)):
    return assistant_service.create_assistant(db, assistant_in)

@router.get("/", response_model=List[AssistantResponse]) # assistant 목록 조회
def get_assistants(db: Session = Depends(get_db)):
    return assistant_service.get_all_assistants(db)