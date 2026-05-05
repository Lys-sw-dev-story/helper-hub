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
    organization_id: int

class ClientResponse(BaseModel):
    client_id: int
    client_name: str

    class Config:
        from_attributes = True