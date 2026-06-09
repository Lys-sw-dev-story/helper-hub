from datetime import date
from typing import Optional

from pydantic import BaseModel


class AssignmentCreate(BaseModel):
    # staff_id 는 보내지 않으면 로그인한 staff(매칭 담당자)로 자동 설정된다.
    staff_id: Optional[int] = None
    client_id: int
    assistant_id: int
    start_date: date


class AssignmentEnd(BaseModel):
    end_date: date


class ClientSummary(BaseModel):
    client_id: int
    client_name: str

    class Config:
        from_attributes = True


class AssistantSummary(BaseModel):
    assistant_id: int
    assistant_name: str
    work_days: Optional[str] = None
    assistant_support_types: Optional[str] = None

    class Config:
        from_attributes = True


class StaffSummary(BaseModel):
    staff_id: int
    staff_name: str

    class Config:
        from_attributes = True


class AssignmentResponse(BaseModel):
    assignment_id: int
    staff_id: int
    client_id: int
    assistant_id: int
    start_date: date
    end_date: Optional[date] = None
    assignment_status: str

    class Config:
        from_attributes = True


class AssignmentDetail(AssignmentResponse):
    client: Optional[ClientSummary] = None
    assistant: Optional[AssistantSummary] = None
    staff: Optional[StaffSummary] = None


# ---- 태그 매칭(배정 후보) ----


class MatchCandidate(BaseModel):
    """이용자 태그 조건에 맞는 활동지원사 1명 + 어떤 태그가 겹쳤는지."""

    assistant_id: int
    assistant_name: str
    assistant_phone: Optional[str] = None
    work_days: list[str] = []          # 활동지원사 근무 가능 요일 (전체)
    support_types: list[str] = []      # 활동지원사 가능 지원 분야 (전체)
    matched_days: list[str] = []       # 이용자 희망과 겹친 요일
    matched_support: list[str] = []    # 이용자 희망과 겹친 지원 분야
    is_full_match: bool = False        # 이용자 희망 태그를 모두 충족
    already_assigned: bool = False     # 이 이용자와 이미 진행 중(active)인 배정 존재


class MatchCandidatesResponse(BaseModel):
    client_id: int
    client_name: str
    preferred_days: list[str] = []     # 이용자 희망 요일
    support_types: list[str] = []      # 이용자 희망 지원 분야
    candidate_count: int = 0
    candidates: list[MatchCandidate] = []
