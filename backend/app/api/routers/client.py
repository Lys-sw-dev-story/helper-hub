from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.client_schema import ClientCreate, ClientResponse
from app.services import client_service

router = APIRouter()

@router.post("/", response_model=ClientResponse) # 고객추가
def register_client(client_in: ClientCreate, db: Session = Depends(get_db)):
    return client_service.create_client(db, client_in)