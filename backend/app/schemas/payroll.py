import re
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, field_validator

MONTH_REGEX = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
MAX_SALARY = Decimal("999999999999")


class SalaryBase(BaseModel):
    employee_id: int
    salary_month: str
    base_salary: Decimal
    bonus: Decimal = Decimal("0")
    deductions: Decimal = Decimal("0")
    net_salary: Decimal

    @field_validator("employee_id")
    @classmethod
    def validate_employee_id(cls, v):
        if v <= 0:
            raise ValueError("Employee ID phải là số dương")
        return v

    @field_validator("salary_month")
    @classmethod
    def validate_month(cls, v):
        v = v.strip()
        if not MONTH_REGEX.match(v):
            raise ValueError("Tháng lương phải đúng định dạng YYYY-MM")
        return v

    @field_validator("base_salary")
    @classmethod
    def validate_base_salary(cls, v):
        if v < 0:
            raise ValueError("Lương cơ bản không được âm")
        if v > MAX_SALARY:
            raise ValueError("Lương cơ bản vượt quá giới hạn cho phép")
        return v

    @field_validator("bonus")
    @classmethod
    def validate_bonus(cls, v):
        if v < 0:
            raise ValueError("Thưởng không được âm")
        if v > MAX_SALARY:
            raise ValueError("Thưởng vượt quá giới hạn cho phép")
        return v

    @field_validator("deductions")
    @classmethod
    def validate_deductions(cls, v):
        if v < 0:
            raise ValueError("Khấu trừ không được âm")
        if v > MAX_SALARY:
            raise ValueError("Khấu trừ vượt quá giới hạn cho phép")
        return v

    @field_validator("net_salary")
    @classmethod
    def validate_net_salary(cls, v):
        if v < 0:
            raise ValueError("Lương thực nhận không được âm")
        return v


class SalaryCreate(SalaryBase):
    pass


class SalaryUpdate(BaseModel):
    base_salary: Optional[Decimal] = None
    bonus: Optional[Decimal] = None
    deductions: Optional[Decimal] = None
    net_salary: Optional[Decimal] = None

    @field_validator("base_salary")
    @classmethod
    def validate_base_salary(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Lương cơ bản không được âm")
            if v > MAX_SALARY:
                raise ValueError("Lương cơ bản vượt quá giới hạn cho phép")
        return v

    @field_validator("bonus")
    @classmethod
    def validate_bonus(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Thưởng không được âm")
            if v > MAX_SALARY:
                raise ValueError("Thưởng vượt quá giới hạn cho phép")
        return v

    @field_validator("deductions")
    @classmethod
    def validate_deductions(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Khấu trừ không được âm")
            if v > MAX_SALARY:
                raise ValueError("Khấu trừ vượt quá giới hạn cho phép")
        return v

    @field_validator("net_salary")
    @classmethod
    def validate_net_salary(cls, v):
        if v is not None and v < 0:
            raise ValueError("Lương thực nhận không được âm")
        return v


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
