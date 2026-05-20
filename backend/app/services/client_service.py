from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.assignment import Assignment
from app.models.client import Client
from app.schemas.client_schema import ClientCreate, ClientMemoUpdate, ClientUpdate


def _get_owned_client(db: Session, client_id: int, organization_id: int) -> Client:
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
            detail="해당 이용자를 찾을 수 없습니다.",
        )
    return client


def create_client(db: Session, client_in: ClientCreate): #고객추가
    db_client = Client(**client_in.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def get_client(db: Session, client_id: int, organization_id: int) -> Client:
    return _get_owned_client(db, client_id, organization_id)


def update_client(
    db: Session,
    client_id: int,
    organization_id: int,
    payload: ClientUpdate,
) -> Client:
    client = _get_owned_client(db, client_id, organization_id)
    update_data = payload.model_dump(exclude_unset=True)
    if "client_name" in update_data and not update_data["client_name"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이름은 필수 입력 사항입니다.",
        )
    for field, value in update_data.items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client_id: int, organization_id: int) -> None:
    client = _get_owned_client(db, client_id, organization_id)
    has_assignment = (
        db.query(Assignment.assignment_id)
        .filter(Assignment.client_id == client_id)
        .first()
        is not None
    )
    if has_assignment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="배정 이력이 있는 이용자는 삭제할 수 없습니다.",
        )
    db.delete(client)
    db.commit()


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
