from pydantic import BaseModel
from typing import Optional
from datetime import date

class ClientCreate(BaseModel): # 고객 추가
    client_name: str
    client_birth_date: Optional[date] = None
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    client_status: Optional[str] = None
    client_memo: Optional[str] = None
    client_preferred_days: Optional[str] = None   # 매칭 태그: 희망 요일 CSV
    client_support_types: Optional[str] = None     # 매칭 태그: 희망 지원 분야 CSV
    organization_id: int

class ClientResponse(BaseModel):
    client_id: int
    client_name: str

    class Config:
        from_attributes = True


class ClientDetailResponse(BaseModel):
    client_id: int
    client_name: str
    client_birth_date: Optional[date] = None
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    client_status: Optional[str] = None
    client_memo: Optional[str] = None
    client_preferred_days: Optional[str] = None
    client_support_types: Optional[str] = None
    organization_id: int

    class Config:
        from_attributes = True


class ClientUpdate(BaseModel):
    client_name: Optional[str] = None
    client_birth_date: Optional[date] = None
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    client_status: Optional[str] = None
    client_memo: Optional[str] = None
    client_preferred_days: Optional[str] = None
    client_support_types: Optional[str] = None


class ClientMemoUpdate(BaseModel):
    client_memo: Optional[str] = None


class ClientMemoResponse(BaseModel):
    client_id: int
    client_memo: Optional[str] = None

    class Config:
        from_attributes = True