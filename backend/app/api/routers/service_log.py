from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff
from app.core.database import get_db
from app.models.staff import Staff
from app.schemas.service_log_schema import (
    ServiceLogCreate,
    ServiceLogResponse,
    ServiceLogUpdate,
)
from app.services import service_log_service


router = APIRouter()


@router.post(
    "", response_model=ServiceLogResponse, status_code=status.HTTP_201_CREATED
)
def create_service_log(
    payload: ServiceLogCreate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return service_log_service.create_log(
        db=db, payload=payload, organization_id=current_staff.organization_id
    )


@router.get("", response_model=list[ServiceLogResponse])
def list_service_logs(
    assignment_id: Optional[int] = None,
    client_id: Optional[int] = None,
    assistant_id: Optional[int] = None,
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return service_log_service.list_logs(
        db=db,
        organization_id=current_staff.organization_id,
        assignment_id=assignment_id,
        client_id=client_id,
        assistant_id=assistant_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{service_log_id}", response_model=ServiceLogResponse)
def get_service_log(
    service_log_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return service_log_service.get_log(
        db=db,
        service_log_id=service_log_id,
        organization_id=current_staff.organization_id,
    )


@router.patch("/{service_log_id}", response_model=ServiceLogResponse)
def update_service_log(
    service_log_id: int,
    payload: ServiceLogUpdate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return service_log_service.update_log(
        db=db,
        service_log_id=service_log_id,
        payload=payload,
        organization_id=current_staff.organization_id,
    )


@router.delete("/{service_log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_log(
    service_log_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    service_log_service.delete_log(
        db=db,
        service_log_id=service_log_id,
        organization_id=current_staff.organization_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
