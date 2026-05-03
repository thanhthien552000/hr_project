from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class SalaryBase(BaseModel):
    employee_id: int
    salary_month: str
    base_salary: Decimal
    bonus: Decimal = Decimal("0")
    deductions: Decimal = Decimal("0")
    net_salary: Decimal


class SalaryCreate(SalaryBase):
    pass


class SalaryUpdate(BaseModel):
    base_salary: Optional[Decimal] = None
    bonus: Optional[Decimal] = None
    deductions: Optional[Decimal] = None
    net_salary: Optional[Decimal] = None


class SalaryMonthDetail(BaseModel):
    salary_month: str
    base_salary: Decimal
    bonus: Decimal
    deductions: Decimal
    net_salary: Decimal


class SalaryResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: Optional[str] = None
    department_name: Optional[str] = None
    salary_month: str
    base_salary: Decimal
    bonus: Decimal
    deductions: Decimal
    net_salary: Decimal
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PayrollCompareResponse(BaseModel):
    salary_id: int
    employee_id: int
    full_name: str
    department_name: Optional[str] = None
    current_month: Optional[SalaryMonthDetail] = None
    previous_month: Optional[SalaryMonthDetail] = None
    change_percentage: Optional[float] = None
    change_direction: Optional[str] = None
