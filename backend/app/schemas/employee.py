from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    full_name: str
    date_of_birth: str
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    hire_date: str
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    status: Optional[str] = "Đang làm việc"


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    hire_date: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    status: Optional[str] = None


class EmployeeResponse(BaseModel):
    id: int
    full_name: str
    date_of_birth: str
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    hire_date: str
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    department_name: Optional[str] = None
    position_name: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
