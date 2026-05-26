from datetime import date
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.assignment import Assignment
from app.models.client import Client
from app.models.service_log import ServiceLog
from app.schemas.service_log_schema import (
    ServiceLogCreate,
    ServiceLogResponse,
    ServiceLogUpdate,
)


def _to_response(log: ServiceLog) -> ServiceLogResponse:
    assignment = log.assignment
    return ServiceLogResponse(
        service_log_id=log.service_log_id,
        assignment_id=log.assignment_id,
        service_date=log.service_date,
        service_hours=log.service_hours,
        service_count=log.service_count,
        service_content=log.service_content,
        client_id=assignment.client_id,
        client_name=assignment.client.client_name,
        assistant_id=assignment.assistant_id,
        assistant_name=assignment.assistant.assistant_name,
    )


def _get_assignment_in_org(
    db: Session, assignment_id: int, organization_id: int
) -> Assignment:
    assignment = (
        db.query(Assignment)
        .join(Client, Assignment.client_id == Client.client_id)
        .filter(
            Assignment.assignment_id == assignment_id,
            Client.organization_id == organization_id,
        )
        .options(joinedload(Assignment.client), joinedload(Assignment.assistant))
        .first()
    )
    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 배정을 찾을 수 없습니다.",
        )
    return assignment


def _get_log_in_org(
    db: Session, service_log_id: int, organization_id: int
) -> ServiceLog:
    log = (
        db.query(ServiceLog)
        .join(Assignment, ServiceLog.assignment_id == Assignment.assignment_id)
        .join(Client, Assignment.client_id == Client.client_id)
        .filter(
            ServiceLog.service_log_id == service_log_id,
            Client.organization_id == organization_id,
        )
        .options(
            joinedload(ServiceLog.assignment).joinedload(Assignment.client),
            joinedload(ServiceLog.assignment).joinedload(Assignment.assistant),
        )
        .first()
    )
    if log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="이용일지를 찾을 수 없습니다.",
        )
    return log


def create_log(
    db: Session, payload: ServiceLogCreate, organization_id: int
) -> ServiceLogResponse:
    assignment = _get_assignment_in_org(db, payload.assignment_id, organization_id)

    if assignment.start_date and payload.service_date < assignment.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="서비스 날짜는 배정 시작일 이후여야 합니다.",
        )
    if assignment.end_date and payload.service_date > assignment.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="서비스 날짜는 배정 종료일 이전이어야 합니다.",
        )

    log = ServiceLog(
        assignment_id=payload.assignment_id,
        service_date=payload.service_date,
        service_hours=payload.service_hours,
        service_count=payload.service_count,
        service_content=payload.service_content,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return _to_response(_get_log_in_org(db, log.service_log_id, organization_id))


def list_logs(
    db: Session,
    organization_id: int,
    *,
    assignment_id: Optional[int] = None,
    client_id: Optional[int] = None,
    assistant_id: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> list[ServiceLogResponse]:
    query = (
        db.query(ServiceLog)
        .join(Assignment, ServiceLog.assignment_id == Assignment.assignment_id)
        .join(Client, Assignment.client_id == Client.client_id)
        .filter(Client.organization_id == organization_id)
        .options(
            joinedload(ServiceLog.assignment).joinedload(Assignment.client),
            joinedload(ServiceLog.assignment).joinedload(Assignment.assistant),
        )
    )
    if assignment_id is not None:
        query = query.filter(ServiceLog.assignment_id == assignment_id)
    if client_id is not None:
        query = query.filter(Assignment.client_id == client_id)
    if assistant_id is not None:
        query = query.filter(Assignment.assistant_id == assistant_id)
    if date_from is not None:
        query = query.filter(ServiceLog.service_date >= date_from)
    if date_to is not None:
        query = query.filter(ServiceLog.service_date <= date_to)

    logs = query.order_by(
        ServiceLog.service_date.desc(), ServiceLog.service_log_id.desc()
    ).all()
    return [_to_response(log) for log in logs]


def get_log(
    db: Session, service_log_id: int, organization_id: int
) -> ServiceLogResponse:
    return _to_response(_get_log_in_org(db, service_log_id, organization_id))


def update_log(
    db: Session,
    service_log_id: int,
    payload: ServiceLogUpdate,
    organization_id: int,
) -> ServiceLogResponse:
    log = _get_log_in_org(db, service_log_id, organization_id)
    data = payload.model_dump(exclude_unset=True)

    new_date = data.get("service_date", log.service_date)
    assignment = log.assignment
    if assignment.start_date and new_date < assignment.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="서비스 날짜는 배정 시작일 이후여야 합니다.",
        )
    if assignment.end_date and new_date > assignment.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="서비스 날짜는 배정 종료일 이전이어야 합니다.",
        )

    for field, value in data.items():
        setattr(log, field, value)

    db.commit()
    db.refresh(log)
    return _to_response(_get_log_in_org(db, service_log_id, organization_id))


def delete_log(db: Session, service_log_id: int, organization_id: int) -> None:
    log = _get_log_in_org(db, service_log_id, organization_id)
    db.delete(log)
    db.commit()
