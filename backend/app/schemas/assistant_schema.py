from pydantic import BaseModel
from typing import Optional
from datetime import date


# 등록할 때 받는 데이터
class AssistantCreate(BaseModel):
    assistant_name: str
    assistant_phone: Optional[str] = None
    work_days: Optional[str] = None
    work_start_date: Optional[date] = None
    assistant_license: Optional[str] = None
    assistant_memo: Optional[str] = None


# 수정할 때 받는 데이터 (모든 필드 선택)
class AssistantUpdate(BaseModel):
    assistant_name: Optional[str] = None
    assistant_phone: Optional[str] = None
    work_days: Optional[str] = None
    work_start_date: Optional[date] = None
    assistant_license: Optional[str] = None
    assistant_memo: Optional[str] = None


# 등록 후 응답할 때 데이터
class AssistantResponse(BaseModel):
    assistant_id: int
    assistant_name: str
    status: str = "success"

    class Config:
        from_attributes = True


# 조회 응답 (전체 필드)
class AssistantDetail(BaseModel):
    assistant_id: int
    assistant_name: str
    assistant_phone: Optional[str] = None
    work_days: Optional[str] = None
    work_start_date: Optional[date] = None
    assistant_license: Optional[str] = None
    assistant_memo: Optional[str] = None

    class Config:
        from_attributes = True
