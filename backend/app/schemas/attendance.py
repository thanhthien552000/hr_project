import re
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, field_validator

MONTH_REGEX = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
MAX_DAYS_IN_MONTH = 31


class AttendanceBase(BaseModel):
    employee_id: int
    work_days: int
    absent_days: int = 0
    leave_days: int = 0
    late_days: int = 0
    attendance_month: str

    @field_validator("employee_id")
    @classmethod
    def validate_employee_id(cls, v):
        if v <= 0:
            raise ValueError("Employee ID phải là số dương")
        return v

    @field_validator("attendance_month")
    @classmethod
    def validate_month(cls, v):
        v = v.strip()
        if not MONTH_REGEX.match(v):
            raise ValueError("Tháng chấm công phải đúng định dạng YYYY-MM")
        return v

    @field_validator("work_days")
    @classmethod
    def validate_work_days(cls, v):
        if v < 0:
            raise ValueError("Số ngày công không được âm")
        if v > MAX_DAYS_IN_MONTH:
            raise ValueError(f"Số ngày công không được vượt quá {MAX_DAYS_IN_MONTH}")
        return v

    @field_validator("absent_days")
    @classmethod
    def validate_absent_days(cls, v):
        if v < 0:
            raise ValueError("Số ngày vắng không được âm")
        if v > MAX_DAYS_IN_MONTH:
            raise ValueError(f"Số ngày vắng không được vượt quá {MAX_DAYS_IN_MONTH}")
        return v

    @field_validator("leave_days")
    @classmethod
    def validate_leave_days(cls, v):
        if v < 0:
            raise ValueError("Số ngày phép không được âm")
        if v > MAX_DAYS_IN_MONTH:
            raise ValueError(f"Số ngày phép không được vượt quá {MAX_DAYS_IN_MONTH}")
        return v

    @field_validator("late_days")
    @classmethod
    def validate_late_days(cls, v):
        if v < 0:
            raise ValueError("Số ngày đi muộn không được âm")
        if v > MAX_DAYS_IN_MONTH:
            raise ValueError(f"Số ngày đi muộn không được vượt quá {MAX_DAYS_IN_MONTH}")
        return v


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    work_days: Optional[int] = None
    absent_days: Optional[int] = None
    leave_days: Optional[int] = None
    late_days: Optional[int] = None

    @field_validator("work_days")
    @classmethod
    def validate_work_days(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Số ngày công không được âm")
            if v > MAX_DAYS_IN_MONTH:
                raise ValueError(f"Số ngày công không được vượt quá {MAX_DAYS_IN_MONTH}")
        return v

    @field_validator("absent_days")
    @classmethod
    def validate_absent_days(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Số ngày vắng không được âm")
            if v > MAX_DAYS_IN_MONTH:
                raise ValueError(f"Số ngày vắng không được vượt quá {MAX_DAYS_IN_MONTH}")
        return v

    @field_validator("leave_days")
    @classmethod
    def validate_leave_days(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Số ngày phép không được âm")
            if v > MAX_DAYS_IN_MONTH:
                raise ValueError(f"Số ngày phép không được vượt quá {MAX_DAYS_IN_MONTH}")
        return v

    @field_validator("late_days")
    @classmethod
    def validate_late_days(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Số ngày đi muộn không được âm")
            if v > MAX_DAYS_IN_MONTH:
                raise ValueError(f"Số ngày đi muộn không được vượt quá {MAX_DAYS_IN_MONTH}")
        return v


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
