from pydantic import BaseModel
from typing import Optional
from datetime import date


class ClientCreate(BaseModel):  # 고객 추가
    client_name: str
    client_birth_date: Optional[date] = None
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    client_status: Optional[str] = None
    client_memo: Optional[str] = None


class ClientUpdate(BaseModel):  # 고객 수정 (모든 필드 선택)
    client_name: Optional[str] = None
    client_birth_date: Optional[date] = None
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    client_status: Optional[str] = None
    client_memo: Optional[str] = None


class ClientResponse(BaseModel):
    client_id: int
    client_name: str
    client_birth_date: Optional[date] = None
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    client_status: Optional[str] = None
    client_memo: Optional[str] = None
    organization_id: int

    class Config:
        from_attributes = True


class ClientDetail(BaseModel):  # 조회 응답 (전체 필드)
    client_id: int
    client_name: str
    client_birth_date: Optional[date] = None
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    client_status: Optional[str] = None
    client_memo: Optional[str] = None

    class Config:
        from_attributes = True


class ClientMemoUpdate(BaseModel):
    client_memo: Optional[str] = None


class ClientMemoResponse(BaseModel):
    client_id: int
    client_memo: Optional[str] = None

    class Config:
        from_attributes = True
