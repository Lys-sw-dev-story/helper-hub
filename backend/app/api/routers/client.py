from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff
from app.core.database import get_db
from app.models.staff import Staff
from app.models.client import Client
from app.schemas.client_schema import (
    ClientCreate,
    ClientDetailResponse,
    ClientMemoResponse,
    ClientMemoUpdate,
    ClientResponse,
    ClientUpdate,
)
from app.services import client_service

router = APIRouter()


@router.get("/")
def read_clients(
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    clients = (
        db.query(Client)
        .filter(Client.organization_id == current_staff.organization_id)
        .order_by(Client.client_id.desc())
        .all()
    )

    return [
        {
            "client_id": client.client_id,
            "client_name": client.client_name,
            "client_birth_date": client.client_birth_date,
            "client_phone": client.client_phone,
            "client_address": client.client_address,
            "client_status": client.client_status,
            "client_memo": client.client_memo,
            "client_preferred_days": client.client_preferred_days,
            "client_support_types": client.client_support_types,
            "organization_id": client.organization_id,
        }
        for client in clients
    ]


@router.post("/", response_model=ClientResponse)
def register_client(
    client_in: ClientCreate, 
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff) # 🔐 로그인 토큰 필수 검증 추가!
):

    client_in.organization_id = current_staff.organization_id
    
    return client_service.create_client(db, client_in)


@router.get("/{client_id}", response_model=ClientDetailResponse)
def read_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return client_service.get_client(
        db, client_id, current_staff.organization_id
    )


@router.patch("/{client_id}", response_model=ClientDetailResponse)
def update_client(
    client_id: int,
    payload: ClientUpdate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return client_service.update_client(
        db, client_id, current_staff.organization_id, payload
    )


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    client_service.delete_client(
        db, client_id, current_staff.organization_id
    )
    return None


@router.patch("/{client_id}/memo", response_model=ClientMemoResponse)
def update_client_memo(
    client_id: int,
    payload: ClientMemoUpdate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return client_service.update_client_memo(
        db=db,
        organization_id=current_staff.organization_id,
        client_id=client_id,
        payload=payload,
    )