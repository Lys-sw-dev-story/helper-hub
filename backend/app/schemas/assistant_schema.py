from decimal import Decimal
from typing import Optional
from datetime import date

from pydantic import BaseModel

# 등록할 때 받는 데이터
class AssistantCreate(BaseModel):
    assistant_name: str
    assistant_phone: Optional[str] = None
    work_days: Optional[str] = None  # 매칭 태그: 근무 가능 요일 CSV
    assistant_support_types: Optional[str] = None  # 매칭 태그: 가능 지원 분야 CSV
    work_start_date: Optional[date] = None
    assistant_license: Optional[str] = None
    assistant_memo: Optional[str] = None
    organization_id: int

# 등록 후 응답할 때 데이터
class AssistantResponse(BaseModel):
    assistant_id: int
    assistant_name: str
    status: str = "success"

    class Config:
        from_attributes = True


class AssistantDetailResponse(BaseModel):
    assistant_id: int
    assistant_name: str
    assistant_phone: Optional[str] = None
    work_days: Optional[str] = None
    assistant_support_types: Optional[str] = None
    work_start_date: Optional[date] = None
    assistant_license: Optional[str] = None
    assistant_memo: Optional[str] = None
    organization_id: int

    class Config:
        from_attributes = True


class AssistantUpdate(BaseModel):
    assistant_name: Optional[str] = None
    assistant_phone: Optional[str] = None
    work_days: Optional[str] = None
    assistant_support_types: Optional[str] = None
    work_start_date: Optional[date] = None
    assistant_license: Optional[str] = None
    assistant_memo: Optional[str] = None


class AssistantMemoUpdate(BaseModel):
    assistant_memo: Optional[str] = None


class AssistantMemoResponse(BaseModel):
    assistant_id: int
    assistant_memo: Optional[str] = None

    class Config:
        from_attributes = True


class TenureInfo(BaseModel):
    work_start_date: Optional[date] = None
    reference_date: date
    years: int
    months: int
    days: int
    total_days: int


class MonthlyWorkHours(BaseModel):
    month: int
    service_hours: Decimal
    service_count: int


class AssistantWorkHoursSummary(BaseModel):
    assistant_id: int
    assistant_name: str
    year: int
    yearly_hours: Decimal
    yearly_count: int
    cumulative_hours: Decimal
    cumulative_count: int
    monthly: list[MonthlyWorkHours]


class AssistantPayrollTenureItem(BaseModel):
    assistant_id: int
    assistant_name: str
    work_start_date: Optional[date] = None
    work_days: Optional[str] = None
    tenure: TenureInfo
    yearly_hours: Decimal
    cumulative_hours: Decimal
    active_assignment_count: int
    assistant_memo: Optional[str] = None


class AssistantPayrollTenureResponse(BaseModel):
    year: int
    reference_date: date
    items: list[AssistantPayrollTenureItem]