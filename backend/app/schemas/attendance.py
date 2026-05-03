from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class AttendanceBase(BaseModel):
    employee_id: int
    work_days: int
    absent_days: int = 0
    leave_days: int = 0
    late_days: int = 0
    attendance_month: str


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    work_days: Optional[int] = None
    absent_days: Optional[int] = None
    leave_days: Optional[int] = None
    late_days: Optional[int] = None


class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: Optional[str] = None
    work_days: int
    absent_days: int
    leave_days: int
    late_days: int
    attendance_month: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
