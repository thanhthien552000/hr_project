from typing import Optional, Tuple, List
from datetime import date
from decimal import Decimal
from dateutil.relativedelta import relativedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salary import Salary
from app.repositories.payroll import PayrollRepository
from app.repositories.employee import EmployeeRepository
from app.schemas.payroll import SalaryCreate, SalaryUpdate
from app.common.exceptions import NotFoundException


class PayrollService:
    """Xử lý nghiệp vụ bảng lương — cross-DB: Payroll (MySQL) + Human (SQL Server)."""

    def __init__(self, payroll_db: AsyncSession, human_db: AsyncSession):
        self.repo = PayrollRepository(payroll_db)
        self.employee_repo = EmployeeRepository(human_db)

    # =============================================
    # 1. DANH SÁCH LƯƠNG — kèm so sánh với tháng trước
    # =============================================
    async def get_list(
        self,
        offset: int = 0,
        limit: int = 20,
        month: Optional[str] = None,
        department_id: Optional[int] = None,
    ) -> Tuple[List[dict], int]:
        # Default to latest month with data if no month specified
        if not month:
            latest = await self.repo.get_latest_month()
            if latest:
                month = latest.strftime("%Y-%m")

        # If filtering by department, get employee_ids in that dept from Human DB
        employee_ids_in_dept = None
        if department_id:
            from sqlalchemy import select
            from app.models.employee import Employee
            result = await self.employee_repo.db.execute(
                select(Employee.id).where(
                    Employee.department_id == department_id,
                    Employee.is_deleted == False,
                )
            )
            employee_ids_in_dept = [row[0] for row in result.all()]
            if not employee_ids_in_dept:
                return [], 0

        salaries, total = await self.repo.get_list(
            offset=offset, limit=limit, month=month,
            employee_ids_in_dept=employee_ids_in_dept,
        )

        # Batch lookup employee info from Human DB
        emp_ids = {s.employee_id for s in salaries}
        emp_map = await self.employee_repo.get_employee_info_map(emp_ids)

        items = []
        for s in salaries:
            emp_info = emp_map.get(s.employee_id, {})
            item = self._to_response(s, emp_info)
            # Tính tháng trước
            current_month = s.salary_month
            prev_month = current_month - relativedelta(months=1)
            prev_salary = await self.repo.get_by_employee_month(s.employee_id, prev_month)
            if prev_salary:
                item["previous_month"] = {
                    "salary_month": str(prev_salary.salary_month)[:7],
                    "base_salary": float(prev_salary.base_salary),
                    "bonus": float(prev_salary.bonus),
                    "deductions": float(prev_salary.deductions),
                    "net_salary": float(prev_salary.net_salary),
                }
                if prev_salary.net_salary > 0:
                    change = float((s.net_salary - prev_salary.net_salary) / prev_salary.net_salary * 100)
                    item["change_percentage"] = round(abs(change), 2)
                    item["change_direction"] = "up" if change >= 0 else "down"
            items.append(item)
        return items, total

    # 2. Lấy 1 bản ghi lương
    async def get_by_id(self, salary_id: int) -> dict:
        salary = await self.repo.get_by_id(salary_id)
        if not salary:
            raise NotFoundException("Salary", salary_id)
        emp_map = await self.employee_repo.get_employee_info_map({salary.employee_id})
        emp_info = emp_map.get(salary.employee_id, {})
        return self._to_response(salary, emp_info)

    # 3. Tạo bản ghi lương
    async def create(self, data: SalaryCreate) -> dict:
        month_date = date.fromisoformat(f"{data.salary_month}-01")
        net_salary = data.base_salary + data.bonus - data.deductions
        salary = Salary(
            employee_id=data.employee_id,
            salary_month=month_date,
            base_salary=data.base_salary,
            bonus=data.bonus,
            deductions=data.deductions,
            net_salary=net_salary,
        )
        salary = await self.repo.create(salary)
        emp_map = await self.employee_repo.get_employee_info_map({salary.employee_id})
        emp_info = emp_map.get(salary.employee_id, {})
        return self._to_response(salary, emp_info)

    # 4. Cập nhật lương
    async def update(self, salary_id: int, data: SalaryUpdate) -> dict:
        salary = await self.repo.get_by_id(salary_id)
        if not salary:
            raise NotFoundException("Salary", salary_id)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(salary, field, value)

        salary.net_salary = salary.base_salary + salary.bonus - salary.deductions
        await self.repo.update(salary)

        salary = await self.repo.get_by_id(salary_id)
        emp_map = await self.employee_repo.get_employee_info_map({salary.employee_id})
        emp_info = emp_map.get(salary.employee_id, {})
        return self._to_response(salary, emp_info)

    # =============================================
    # 5. THỐNG KÊ LƯƠNG THEO PHÒNG BAN (cross-DB)
    # =============================================
    async def get_statistics(self, month: str) -> List[dict]:
        month_date = date.fromisoformat(f"{month}-01")
        salaries = await self.repo.get_salaries_by_month(month_date)

        if not salaries:
            return []

        # Get employee info from Human DB
        emp_ids = {s.employee_id for s in salaries}
        emp_map = await self.employee_repo.get_employee_info_map(emp_ids)

        # Group by department in Python
        dept_stats = {}
        for s in salaries:
            emp_info = emp_map.get(s.employee_id, {})
            if emp_info.get("is_deleted", False):
                continue
            dept_id = emp_info.get("department_id", 0)
            dept_name = emp_info.get("department_name", "Unknown")

            if dept_id not in dept_stats:
                dept_stats[dept_id] = {
                    "department_id": dept_id,
                    "department_name": dept_name,
                    "salaries": [],
                }
            dept_stats[dept_id]["salaries"].append(float(s.net_salary))

        result = []
        for dept in sorted(dept_stats.values(), key=lambda x: x["department_name"]):
            sals = dept["salaries"]
            result.append({
                "department_id": dept["department_id"],
                "department_name": dept["department_name"],
                "employee_count": len(sals),
                "total_salary": sum(sals),
                "avg_salary": round(sum(sals) / len(sals), 2) if sals else 0,
                "min_salary": min(sals) if sals else 0,
                "max_salary": max(sals) if sals else 0,
            })
        return result

    # =============================================
    # HELPER: convert Salary model → dict
    # =============================================
    def _to_response(self, salary: Salary, emp_info: dict = None) -> dict:
        emp_info = emp_info or {}
        return {
            "id": salary.id,
            "salary_id": salary.id,
            "employee_id": salary.employee_id,
            "employee_name": emp_info.get("full_name"),
            "full_name": emp_info.get("full_name"),
            "department_name": emp_info.get("department_name"),
            "salary_month": str(salary.salary_month)[:7],
            "base_salary": salary.base_salary,
            "bonus": salary.bonus,
            "deductions": salary.deductions,
            "net_salary": salary.net_salary,
            "current_month": {
                "salary_month": str(salary.salary_month)[:7],
                "base_salary": float(salary.base_salary),
                "bonus": float(salary.bonus),
                "deductions": float(salary.deductions),
                "net_salary": float(salary.net_salary),
            },
            "previous_month": None,
            "change_percentage": None,
            "change_direction": None,
            "created_at": salary.created_at,
            "updated_at": salary.updated_at,
        }