from sqlalchemy.orm import Session

from app.models.client import Client
from app.schemas.client_schema import ClientCreate, ClientUpdate


def create_client(db: Session, client_in: ClientCreate, organization_id: int) -> Client:
    db_client = Client(**client_in.model_dump(), organization_id=organization_id)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def list_clients(db: Session, organization_id: int) -> list[Client]:
    return (
        db.query(Client)
        .filter(Client.organization_id == organization_id)
        .order_by(Client.client_id.desc())
        .all()
    )


def get_client(db: Session, client_id: int, organization_id: int) -> Client | None:
    return (
        db.query(Client)
        .filter(
            Client.client_id == client_id,
            Client.organization_id == organization_id,
        )
        .first()
    )


def update_client(
    db: Session,
    client_id: int,
    client_in: ClientUpdate,
    organization_id: int,
) -> Client | None:
    db_client = get_client(db, client_id, organization_id)
    if db_client is None:
        return None

    update_data = client_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_client, field, value)

    db.commit()
    db.refresh(db_client)
    return db_client


def delete_client(db: Session, client_id: int, organization_id: int) -> bool:
    db_client = get_client(db, client_id, organization_id)
    if db_client is None:
        return False

    db.delete(db_client)
    db.commit()
    return True
