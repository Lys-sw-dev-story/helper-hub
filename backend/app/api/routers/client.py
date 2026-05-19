from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff
from app.core.database import get_db
from app.models.staff import Staff
from app.schemas.client_schema import (
    ClientCreate,
    ClientDetail,
    ClientMemoResponse,
    ClientMemoUpdate,
    ClientResponse,
    ClientUpdate,
)
from app.services import client_service

router = APIRouter()


@router.post("/", response_model=ClientResponse)
def register_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return client_service.create_client(db, client_in, current_staff.organization_id)


@router.get("/", response_model=list[ClientDetail])
def read_clients(
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return client_service.list_clients(db, current_staff.organization_id)


@router.get("/{client_id}", response_model=ClientDetail)
def read_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    db_client = client_service.get_client(db, client_id, current_staff.organization_id)
    if db_client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 이용자를 찾을 수 없습니다.",
        )
    return db_client


@router.patch("/{client_id}", response_model=ClientDetail)
def update_client(
    client_id: int,
    client_in: ClientUpdate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    db_client = client_service.update_client(
        db, client_id, client_in, current_staff.organization_id
    )
    if db_client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 이용자를 찾을 수 없습니다.",
        )
    return db_client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    deleted = client_service.delete_client(
        db, client_id, current_staff.organization_id
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 이용자를 찾을 수 없습니다.",
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
