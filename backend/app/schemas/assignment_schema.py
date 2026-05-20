from datetime import date
from typing import Optional

from pydantic import BaseModel


class AssignmentCreate(BaseModel):
    staff_id: int
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
