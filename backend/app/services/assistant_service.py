from sqlalchemy.orm import Session
from app.models.assistant import Assistant
from app.schemas.assistant_schema import AssistantCreate

def create_assistant(db: Session, assistant_in: AssistantCreate):
    # 스키마 데이터를 언패킹해서 모델 생성
    db_assistant = Assistant(**assistant_in.model_dump())
    db.add(db_assistant)
    db.commit()
    db.refresh(db_assistant)
    return db_assistant