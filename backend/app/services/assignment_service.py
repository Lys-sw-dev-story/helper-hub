from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.core.constants import (
    AssignmentStatus,
    SUPPORT_TYPE_ORDER,
    WEEKDAY_ORDER,
    parse_tags,
    sort_tags,
)
from app.models.assignment import Assignment
from app.models.assistant import Assistant
from app.models.client import Client
from app.models.staff import Staff
from app.schemas.assignment_schema import (
    AssignmentCreate,
    AssignmentEnd,
    MatchCandidate,
    MatchCandidatesResponse,
)


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


def get_match_candidates(
    db: Session, client_id: int, organization_id: int
) -> MatchCandidatesResponse:
    """이용자 태그(희망 요일·지원 분야)에 맞는 활동지원사 목록을 반환한다.

    매칭 규칙(분야 간 AND, 분야 내 OR):
      - 요일: 이용자 희망 요일과 1개 이상 겹치면 통과 (이용자가 요일 태그를 안 걸었으면 통과)
      - 지원 분야: 이용자 희망 분야와 1개 이상 겹치면 통과 (안 걸었으면 통과)
    두 조건을 모두 만족하는 활동지원사만 후보로 내려준다.
    """
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

    preferred_days = sort_tags(parse_tags(client.client_preferred_days), WEEKDAY_ORDER)
    preferred_support = sort_tags(
        parse_tags(client.client_support_types), SUPPORT_TYPE_ORDER
    )
    day_set = set(preferred_days)
    support_set = set(preferred_support)

    # 이 이용자와 현재 진행 중(active)인 배정을 가진 활동지원사
    active_assistant_ids = {
        row[0]
        for row in db.query(Assignment.assistant_id)
        .filter(
            Assignment.client_id == client_id,
            Assignment.assignment_status == AssignmentStatus.ACTIVE.value,
        )
        .all()
    }

    assistants = (
        db.query(Assistant)
        .filter(Assistant.organization_id == organization_id)
        .order_by(Assistant.assistant_id.desc())
        .all()
    )

    candidates: list[MatchCandidate] = []
    for assistant in assistants:
        work_days = sort_tags(parse_tags(assistant.work_days), WEEKDAY_ORDER)
        support_types = sort_tags(
            parse_tags(assistant.assistant_support_types), SUPPORT_TYPE_ORDER
        )
        work_day_set = set(work_days)
        support_type_set = set(support_types)

        matched_days = sort_tags(
            [d for d in preferred_days if d in work_day_set], WEEKDAY_ORDER
        )
        matched_support = sort_tags(
            [s for s in preferred_support if s in support_type_set],
            SUPPORT_TYPE_ORDER,
        )

        day_ok = not day_set or bool(matched_days)
        support_ok = not support_set or bool(matched_support)
        if not (day_ok and support_ok):
            continue

        is_full_match = day_set <= work_day_set and support_set <= support_type_set
        candidates.append(
            MatchCandidate(
                assistant_id=assistant.assistant_id,
                assistant_name=assistant.assistant_name,
                assistant_phone=assistant.assistant_phone,
                work_days=work_days,
                support_types=support_types,
                matched_days=matched_days,
                matched_support=matched_support,
                is_full_match=is_full_match,
                already_assigned=assistant.assistant_id in active_assistant_ids,
            )
        )

    # 완전 매칭 우선 → 겹친 태그 수 많은 순 → 이름순
    candidates.sort(
        key=lambda c: (
            not c.is_full_match,
            -(len(c.matched_days) + len(c.matched_support)),
            c.assistant_name,
        )
    )

    return MatchCandidatesResponse(
        client_id=client.client_id,
        client_name=client.client_name,
        preferred_days=preferred_days,
        support_types=preferred_support,
        candidate_count=len(candidates),
        candidates=candidates,
    )
