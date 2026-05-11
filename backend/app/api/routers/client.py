from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List # List 타입을 위해 추가
from app.core.database import get_db
from app.schemas.client_schema import ClientCreate, ClientResponse
from app.services import client_service

router = APIRouter()

@router.post("/", response_model=ClientResponse) # client 추가
def register_client(client_in: ClientCreate, db: Session = Depends(get_db)):
    return client_service.create_client(db, client_in)

@router.get("/", response_model=List[ClientResponse]) # client 목록 조회
def get_clients(db: Session = Depends(get_db)):
    return client_service.get_all_clients(db)