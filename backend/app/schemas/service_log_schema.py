from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ServiceLogCreate(BaseModel):
    assignment_id: int
    service_date: date
    service_hours: Decimal = Field(..., gt=0)
    service_count: Optional[int] = Field(default=None, ge=0)
    service_content: Optional[str] = None


class ServiceLogUpdate(BaseModel):
    service_date: Optional[date] = None
    service_hours: Optional[Decimal] = Field(default=None, gt=0)
    service_count: Optional[int] = Field(default=None, ge=0)
    service_content: Optional[str] = None


class ServiceLogResponse(BaseModel):
    service_log_id: int
    assignment_id: int
    service_date: date
    service_hours: Decimal
    service_count: Optional[int] = None
    service_content: Optional[str] = None
    client_id: int
    client_name: str
    assistant_id: int
    assistant_name: str

    class Config:
        from_attributes = True
