from sqlalchemy.orm import Session

from app.models.assistant import Assistant
from app.schemas.assistant_schema import AssistantCreate, AssistantUpdate


def create_assistant(
    db: Session, assistant_in: AssistantCreate, organization_id: int
) -> Assistant:
    db_assistant = Assistant(**assistant_in.model_dump(), organization_id=organization_id)
    db.add(db_assistant)
    db.commit()
    db.refresh(db_assistant)
    return db_assistant


def list_assistants(db: Session, organization_id: int) -> list[Assistant]:
    return (
        db.query(Assistant)
        .filter(Assistant.organization_id == organization_id)
        .order_by(Assistant.assistant_id.desc())
        .all()
    )


def get_assistant(
    db: Session, assistant_id: int, organization_id: int
) -> Assistant | None:
    return (
        db.query(Assistant)
        .filter(
            Assistant.assistant_id == assistant_id,
            Assistant.organization_id == organization_id,
        )
        .first()
    )


def update_assistant(
    db: Session,
    assistant_id: int,
    assistant_in: AssistantUpdate,
    organization_id: int,
) -> Assistant | None:
    db_assistant = get_assistant(db, assistant_id, organization_id)
    if db_assistant is None:
        return None

    update_data = assistant_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_assistant, field, value)

    db.commit()
    db.refresh(db_assistant)
    return db_assistant


def delete_assistant(db: Session, assistant_id: int, organization_id: int) -> bool:
    db_assistant = get_assistant(db, assistant_id, organization_id)
    if db_assistant is None:
        return False

    db.delete(db_assistant)
    db.commit()
    return True
