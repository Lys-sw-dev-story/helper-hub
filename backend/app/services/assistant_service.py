from datetime import date
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.core.constants import AssignmentStatus
from app.models.assignment import Assignment
from app.models.assistant import Assistant
from app.models.service_log import ServiceLog
from app.schemas.assistant_schema import (
    AssistantCreate,
    AssistantMemoUpdate,
    AssistantPayrollTenureItem,
    AssistantPayrollTenureResponse,
    AssistantUpdate,
    AssistantWorkHoursSummary,
    MonthlyWorkHours,
    TenureInfo,
)


def _get_owned_assistant(
    db: Session, assistant_id: int, organization_id: int
) -> Assistant:
    assistant = (
        db.query(Assistant)
        .filter(
            Assistant.assistant_id == assistant_id,
            Assistant.organization_id == organization_id,
        )
        .one_or_none()
    )
    if assistant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 활동지원사를 찾을 수 없습니다.",
        )
    return assistant


def create_assistant(db: Session, assistant_in: AssistantCreate):
    # 스키마 데이터를 언패킹해서 모델 생성
    db_assistant = Assistant(**assistant_in.model_dump())
    db.add(db_assistant)
    db.commit()
    db.refresh(db_assistant)
    return db_assistant


def get_assistant(
    db: Session, assistant_id: int, organization_id: int
) -> Assistant:
    return _get_owned_assistant(db, assistant_id, organization_id)


def update_assistant(
    db: Session,
    assistant_id: int,
    organization_id: int,
    payload: AssistantUpdate,
) -> Assistant:
    assistant = _get_owned_assistant(db, assistant_id, organization_id)
    update_data = payload.model_dump(exclude_unset=True)
    if "assistant_name" in update_data and not update_data["assistant_name"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이름은 필수 입력 사항입니다.",
        )
    for field, value in update_data.items():
        setattr(assistant, field, value)
    db.commit()
    db.refresh(assistant)
    return assistant


def delete_assistant(
    db: Session, assistant_id: int, organization_id: int
) -> None:
    assistant = _get_owned_assistant(db, assistant_id, organization_id)
    has_assignment = (
        db.query(Assignment.assignment_id)
        .filter(Assignment.assistant_id == assistant_id)
        .first()
        is not None
    )
    if has_assignment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="배정 이력이 있는 활동지원사는 삭제할 수 없습니다.",
        )
    db.delete(assistant)
    db.commit()


def update_assistant_memo(
    db: Session,
    organization_id: int,
    assistant_id: int,
    payload: AssistantMemoUpdate,
) -> Assistant:
    assistant = (
        db.query(Assistant)
        .filter(
            Assistant.assistant_id == assistant_id,
            Assistant.organization_id == organization_id,
        )
        .one_or_none()
    )
    if assistant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="활동지원사를 찾을 수 없습니다.",
        )
    assistant.assistant_memo = payload.assistant_memo
    db.commit()
    db.refresh(assistant)
    return assistant


def compute_tenure(
    work_start_date: Optional[date], reference_date: date
) -> TenureInfo:
    """근속 기간을 년/월/일로 분해해 반환. 미래 입사일이면 0으로 떨어뜨린다."""
    if work_start_date is None or work_start_date > reference_date:
        return TenureInfo(
            work_start_date=work_start_date,
            reference_date=reference_date,
            years=0,
            months=0,
            days=0,
            total_days=0,
        )

    years = reference_date.year - work_start_date.year
    months = reference_date.month - work_start_date.month
    days = reference_date.day - work_start_date.day

    if days < 0:
        months -= 1
        prev_month = reference_date.month - 1 or 12
        prev_year = reference_date.year if reference_date.month != 1 else reference_date.year - 1
        try:
            prev_month_last_day = date(prev_year, prev_month + 1, 1).toordinal() - date(
                prev_year, prev_month, 1
            ).toordinal()
        except ValueError:
            prev_month_last_day = 30
        days += prev_month_last_day
    if months < 0:
        years -= 1
        months += 12

    total_days = (reference_date - work_start_date).days
    return TenureInfo(
        work_start_date=work_start_date,
        reference_date=reference_date,
        years=years,
        months=months,
        days=days,
        total_days=total_days,
    )


def _aggregate_hours_query(
    db: Session, organization_id: int, assistant_id: Optional[int] = None
):
    query = (
        db.query(
            Assignment.assistant_id.label("assistant_id"),
            extract("year", ServiceLog.service_date).label("year"),
            extract("month", ServiceLog.service_date).label("month"),
            func.coalesce(func.sum(ServiceLog.service_hours), 0).label("hours"),
            func.coalesce(func.sum(ServiceLog.service_count), 0).label("count"),
        )
        .join(ServiceLog, ServiceLog.assignment_id == Assignment.assignment_id)
        .join(Assistant, Assistant.assistant_id == Assignment.assistant_id)
        .filter(Assistant.organization_id == organization_id)
    )
    if assistant_id is not None:
        query = query.filter(Assignment.assistant_id == assistant_id)
    return query.group_by(
        Assignment.assistant_id,
        extract("year", ServiceLog.service_date),
        extract("month", ServiceLog.service_date),
    )


def compute_work_hours(
    db: Session,
    assistant_id: int,
    organization_id: int,
    year: int,
) -> AssistantWorkHoursSummary:
    assistant = _get_owned_assistant(db, assistant_id, organization_id)

    rows = _aggregate_hours_query(db, organization_id, assistant_id=assistant_id).all()

    monthly_map: dict[int, MonthlyWorkHours] = {}
    yearly_hours = Decimal("0")
    yearly_count = 0
    cumulative_hours = Decimal("0")
    cumulative_count = 0

    for row in rows:
        hours = Decimal(row.hours)
        count = int(row.count or 0)
        cumulative_hours += hours
        cumulative_count += count
        if int(row.year) == year:
            yearly_hours += hours
            yearly_count += count
            monthly_map[int(row.month)] = MonthlyWorkHours(
                month=int(row.month),
                service_hours=hours,
                service_count=count,
            )

    monthly = [
        monthly_map.get(
            m, MonthlyWorkHours(month=m, service_hours=Decimal("0"), service_count=0)
        )
        for m in range(1, 13)
    ]

    return AssistantWorkHoursSummary(
        assistant_id=assistant.assistant_id,
        assistant_name=assistant.assistant_name,
        year=year,
        yearly_hours=yearly_hours,
        yearly_count=yearly_count,
        cumulative_hours=cumulative_hours,
        cumulative_count=cumulative_count,
        monthly=monthly,
    )


def build_payroll_tenure_list(
    db: Session,
    organization_id: int,
    reference_date: date,
    year: int,
) -> AssistantPayrollTenureResponse:
    assistants = (
        db.query(Assistant)
        .filter(Assistant.organization_id == organization_id)
        .order_by(Assistant.assistant_id.desc())
        .all()
    )

    rows = _aggregate_hours_query(db, organization_id).all()
    yearly_map: dict[int, Decimal] = {}
    cumulative_map: dict[int, Decimal] = {}
    for row in rows:
        aid = int(row.assistant_id)
        hours = Decimal(row.hours)
        cumulative_map[aid] = cumulative_map.get(aid, Decimal("0")) + hours
        if int(row.year) == year:
            yearly_map[aid] = yearly_map.get(aid, Decimal("0")) + hours

    active_rows = (
        db.query(Assignment.assistant_id, func.count(Assignment.assignment_id))
        .join(Assistant, Assistant.assistant_id == Assignment.assistant_id)
        .filter(
            Assistant.organization_id == organization_id,
            Assignment.assignment_status == AssignmentStatus.ACTIVE.value,
        )
        .group_by(Assignment.assistant_id)
        .all()
    )
    active_map = {int(aid): int(count) for aid, count in active_rows}

    items = [
        AssistantPayrollTenureItem(
            assistant_id=a.assistant_id,
            assistant_name=a.assistant_name,
            work_start_date=a.work_start_date,
            work_days=a.work_days,
            tenure=compute_tenure(a.work_start_date, reference_date),
            yearly_hours=yearly_map.get(a.assistant_id, Decimal("0")),
            cumulative_hours=cumulative_map.get(a.assistant_id, Decimal("0")),
            active_assignment_count=active_map.get(a.assistant_id, 0),
            assistant_memo=a.assistant_memo,
        )
        for a in assistants
    ]

    return AssistantPayrollTenureResponse(
        year=year,
        reference_date=reference_date,
        items=items,
    )


def get_tenure(
    db: Session, assistant_id: int, organization_id: int, reference_date: date
) -> TenureInfo:
    assistant = _get_owned_assistant(db, assistant_id, organization_id)
    return compute_tenure(assistant.work_start_date, reference_date)
