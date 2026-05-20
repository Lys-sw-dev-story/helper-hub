from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff
from app.core.constants import AssignmentStatus
from app.core.database import get_db
from app.models.staff import Staff
from app.schemas.assignment_schema import (
    AssignmentCreate,
    AssignmentDetail,
    AssignmentEnd,
)
from app.services import assignment_service


router = APIRouter()


@router.post(
    "", response_model=AssignmentDetail, status_code=status.HTTP_201_CREATED
)
def create_assignment(
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return assignment_service.create_assignment(
        db=db, payload=payload, organization_id=current_staff.organization_id
    )


@router.get("", response_model=list[AssignmentDetail])
def list_assignments(
    status_filter: Optional[AssignmentStatus] = Query(None, alias="status"),
    client_id: Optional[int] = None,
    assistant_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return assignment_service.list_assignments(
        db=db,
        organization_id=current_staff.organization_id,
        status_filter=status_filter.value if status_filter else None,
        client_id=client_id,
        assistant_id=assistant_id,
    )


@router.get("/{assignment_id}", response_model=AssignmentDetail)
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return assignment_service.get_assignment(
        db=db,
        assignment_id=assignment_id,
        organization_id=current_staff.organization_id,
    )


@router.patch("/{assignment_id}/end", response_model=AssignmentDetail)
def end_assignment(
    assignment_id: int,
    payload: AssignmentEnd,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return assignment_service.end_assignment(
        db=db,
        assignment_id=assignment_id,
        payload=payload,
        organization_id=current_staff.organization_id,
    )
