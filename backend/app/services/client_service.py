from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client_schema import ClientCreate

def create_client(db: Session, client_in: ClientCreate): #고객추가
    db_client = Client(**client_in.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client