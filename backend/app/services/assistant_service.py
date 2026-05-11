from sqlalchemy.orm import Session
from app.models.assistant import Assistant
from app.schemas.assistant_schema import AssistantCreate

def create_assistant(db: Session, assistant_in: AssistantCreate):
    db_assistant = Assistant(**assistant_in.model_dump())
    db.add(db_assistant)
    db.commit()
    db.refresh(db_assistant)
    return db_assistant

def get_all_assistants(db: Session):
    return db.query(Assistant).all()