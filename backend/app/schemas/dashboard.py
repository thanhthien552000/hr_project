from typing import Optional, List
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_employees: int
    active_employees: int
    new_employees_this_month: int
    resigned_employees: int
    change_percentage: float
    change_direction: str  # "up" or "down"


class PerformanceResponse(BaseModel):
    current_month: str
    current_performance: float
    previous_performance: float
    change_percentage: float
    change_direction: str


class DepartmentPayroll(BaseModel):
    department_id: int
    department_name: str
    total_salary: float
    percentage: float


class PayrollByDepartmentResponse(BaseModel):
    month: str
    departments: List[DepartmentPayroll]
    total_payroll: float


class RecentActivityItem(BaseModel):
    employee_id: int
    full_name: str
    department_name: Optional[str] = None
    net_salary: Optional[float] = None
    last_activity_date: Optional[str] = None


class TopAbsentEmployee(BaseModel):
    employee_id: int
    full_name: str
    department_name: Optional[str] = None
    absent_days: int
    leave_days: int


class TopAbsentResponse(BaseModel):
    month: str
    employees: List[TopAbsentEmployee]
