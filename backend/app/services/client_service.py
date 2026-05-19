from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.client import Client
from app.schemas.client_schema import ClientCreate, ClientMemoUpdate


def create_client(db: Session, client_in: ClientCreate): #고객추가
    db_client = Client(**client_in.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def update_client_memo(
    db: Session,
    organization_id: int,
    client_id: int,
    payload: ClientMemoUpdate,
) -> Client:
    client = (
        db.query(Client)
        .filter(
            Client.client_id == client_id,
            Client.organization_id == organization_id,
        )
        .one_or_none()
    )
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="이용자를 찾을 수 없습니다.",
        )
    client.client_memo = payload.client_memo
    db.commit()
    db.refresh(client)
    return client
