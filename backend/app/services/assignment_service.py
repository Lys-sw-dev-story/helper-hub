from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.core.constants import AssignmentStatus
from app.models.assignment import Assignment
from app.models.assistant import Assistant
from app.models.client import Client
from app.models.staff import Staff
from app.schemas.assignment_schema import AssignmentCreate, AssignmentEnd


def _ensure_entities_in_org(
    db: Session,
    organization_id: int,
    staff_id: int,
    client_id: int,
    assistant_id: int,
) -> None:
    staff_exists = (
        db.query(Staff.staff_id)
        .filter(Staff.staff_id == staff_id, Staff.organization_id == organization_id)
        .first()
    )
    if staff_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="없는 staff입니다."
        )

    client_exists = (
        db.query(Client.client_id)
        .filter(Client.client_id == client_id, Client.organization_id == organization_id)
        .first()
    )
    if client_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="없는 client입니다."
        )

    assistant_exists = (
        db.query(Assistant.assistant_id)
        .filter(
            Assistant.assistant_id == assistant_id,
            Assistant.organization_id == organization_id,
        )
        .first()
    )
    if assistant_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="없는 assistant입니다."
        )


def _base_query(db: Session, organization_id: int):
    return (
        db.query(Assignment)
        .join(Client, Assignment.client_id == Client.client_id)
        .filter(Client.organization_id == organization_id)
        .options(
            joinedload(Assignment.client),
            joinedload(Assignment.assistant),
            joinedload(Assignment.staff),
        )
    )


def create_assignment(
    db: Session, payload: AssignmentCreate, organization_id: int
) -> Assignment:
    _ensure_entities_in_org(
        db,
        organization_id=organization_id,
        staff_id=payload.staff_id,
        client_id=payload.client_id,
        assistant_id=payload.assistant_id,
    )

    assignment = Assignment(
        staff_id=payload.staff_id,
        client_id=payload.client_id,
        assistant_id=payload.assistant_id,
        start_date=payload.start_date,
        assignment_status=AssignmentStatus.ACTIVE.value,
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return get_assignment(db, assignment.assignment_id, organization_id)


def list_assignments(
    db: Session,
    organization_id: int,
    *,
    status_filter: Optional[str] = None,
    client_id: Optional[int] = None,
    assistant_id: Optional[int] = None,
) -> list[Assignment]:
    query = _base_query(db, organization_id)

    if status_filter is not None:
        query = query.filter(Assignment.assignment_status == status_filter)
    if client_id is not None:
        query = query.filter(Assignment.client_id == client_id)
    if assistant_id is not None:
        query = query.filter(Assignment.assistant_id == assistant_id)

    return query.order_by(Assignment.assignment_id.desc()).all()


def get_assignment(
    db: Session, assignment_id: int, organization_id: int
) -> Assignment:
    assignment = (
        _base_query(db, organization_id)
        .filter(Assignment.assignment_id == assignment_id)
        .first()
    )
    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 배정을 찾을 수 없습니다.",
        )
    return assignment


def end_assignment(
    db: Session,
    assignment_id: int,
    payload: AssignmentEnd,
    organization_id: int,
) -> Assignment:
    assignment = get_assignment(db, assignment_id, organization_id)

    if assignment.start_date and payload.end_date < assignment.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="종료일은 시작일보다 이전일 수 없습니다.",
        )

    assignment.assignment_status = AssignmentStatus.ENDED.value
    assignment.end_date = payload.end_date
    db.commit()
    db.refresh(assignment)
    return assignment
