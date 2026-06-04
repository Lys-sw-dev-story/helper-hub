from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff
from app.core.database import get_db
from app.models.staff import Staff
from app.models.assistant import Assistant
from app.schemas.assistant_schema import (
    AssistantCreate,
    AssistantDetailResponse,
    AssistantPayrollTenureResponse,
    AssistantResponse,
    AssistantUpdate,
    AssistantWorkHoursSummary,
    TenureInfo,
)
from app.services import assistant_service

router = APIRouter()


@router.get("/")
def read_assistants(
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    assistants = (
        db.query(Assistant)
        .filter(Assistant.organization_id == current_staff.organization_id)
        .order_by(Assistant.assistant_id.desc())
        .all()
    )

    return [
        {
            "assistant_id": assistant.assistant_id,
            "assistant_name": assistant.assistant_name,
            "assistant_phone": assistant.assistant_phone,
            "work_days": assistant.work_days,
            "work_start_date": assistant.work_start_date,
            "assistant_license": assistant.assistant_license,
            "assistant_memo": assistant.assistant_memo,
            "organization_id": assistant.organization_id,
        }
        for assistant in assistants
    ]


@router.post("/", response_model=AssistantResponse)
def register_assistant(
    assistant_in: AssistantCreate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff), # 🔐 여기에 로그인 토큰 필수 검증 레이어 추가!
):
    # 💡 프론트엔드 페이로드 의존성을 완전히 제거하고,
    # 서버 내부에서 인증된 스태프의 기관 ID로 덮어써서 철통 방어!
    assistant_in.organization_id = current_staff.organization_id
    
    return assistant_service.create_assistant(db, assistant_in)


@router.get("/payroll-tenure", response_model=AssistantPayrollTenureResponse)
def read_payroll_tenure(
    year: Optional[int] = Query(default=None, ge=2000, le=2100),
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    today = date.today()
    return assistant_service.build_payroll_tenure_list(
        db=db,
        organization_id=current_staff.organization_id,
        reference_date=today,
        year=year or today.year,
    )


@router.get("/{assistant_id}/tenure", response_model=TenureInfo)
def read_assistant_tenure(
    assistant_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return assistant_service.get_tenure(
        db=db,
        assistant_id=assistant_id,
        organization_id=current_staff.organization_id,
        reference_date=date.today(),
    )


@router.get(
    "/{assistant_id}/work-hours", response_model=AssistantWorkHoursSummary
)
def read_assistant_work_hours(
    assistant_id: int,
    year: Optional[int] = Query(default=None, ge=2000, le=2100),
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return assistant_service.compute_work_hours(
        db=db,
        assistant_id=assistant_id,
        organization_id=current_staff.organization_id,
        year=year or date.today().year,
    )


@router.get("/{assistant_id}", response_model=AssistantDetailResponse)
def read_assistant(
    assistant_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return assistant_service.get_assistant(
        db, assistant_id, current_staff.organization_id
    )


@router.patch("/{assistant_id}", response_model=AssistantDetailResponse)
def update_assistant(
    assistant_id: int,
    payload: AssistantUpdate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    return assistant_service.update_assistant(
        db, assistant_id, current_staff.organization_id, payload
    )


@router.delete("/{assistant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assistant(
    assistant_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    assistant_service.delete_assistant(
        db, assistant_id, current_staff.organization_id
    )
    return None