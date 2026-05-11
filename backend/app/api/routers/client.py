from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List # List 타입을 위해 추가
from app.core.database import get_db
from app.schemas.client_schema import ClientCreate, ClientResponse
from app.services import client_service

router = APIRouter()

@router.post("/", response_model=ClientResponse) # 고객 추가
def register_client(client_in: ClientCreate, db: Session = Depends(get_db)):
    return client_service.create_client(db, client_in)

# --- 🆕 여기부터 추가해줘! ---
@router.get("/", response_model=List[ClientResponse]) # 고객 목록 조회
def get_clients(db: Session = Depends(get_db)):
    # 서비스 레이어에서 모든 고객을 가져오는 함수를 호출해
    return client_service.get_all_clients(db)