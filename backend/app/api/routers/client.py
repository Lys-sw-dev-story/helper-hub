from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff
from app.core.database import get_db
from app.models.staff import Staff
from app.schemas.client_schema import (
    ClientCreate,
    ClientMemoResponse,
    ClientMemoUpdate,
    ClientResponse,
)
from app.services import client_service

router = APIRouter()

@router.post("/", response_model=ClientResponse) # 고객추가
def register_client(client_in: ClientCreate, db: Session = Depends(get_db)):
    return client_service.create_client(db, client_in)


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
