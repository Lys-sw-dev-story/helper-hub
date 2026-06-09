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
    MatchCandidatesResponse,
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
    # 매칭 담당자는 로그인한 staff 로 강제(클라이언트가 보낸 staff_id 는 신뢰하지 않음)
    payload.staff_id = current_staff.staff_id
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


@router.get("/match-candidates", response_model=MatchCandidatesResponse)
def match_candidates(
    client_id: int = Query(..., description="배정 대상 이용자 ID"),
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    """이용자 태그(희망 요일·지원 분야) 조건에 맞는 활동지원사 후보 목록."""
    return assignment_service.get_match_candidates(
        db=db,
        client_id=client_id,
        organization_id=current_staff.organization_id,
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
