from typing import Optional, Tuple, List
from datetime import date
from decimal import Decimal
from dateutil.relativedelta import relativedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salary import Salary
from app.repositories.payroll import PayrollRepository
from app.schemas.payroll import SalaryCreate, SalaryUpdate
from app.common.exceptions import NotFoundException


class PayrollService:
    """Xử lý nghiệp vụ bảng lương."""

    def __init__(self, db: AsyncSession):
        self.repo = PayrollRepository(db)

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

        salaries, total = await self.repo.get_list(
            offset=offset, limit=limit, month=month, department_id=department_id,
        )
        items = []
        for s in salaries:
            item = self._to_response(s)
            # Tính tháng trước: relativedelta giúp trừ tháng đúng (vd: 03-01 → 02-01)
            current_month = s.salary_month
            prev_month = current_month - relativedelta(months=1)
            # Lấy lương tháng trước cùng nhân viên
            prev_salary = await self.repo.get_by_employee_month(s.employee_id, prev_month)
            if prev_salary:
                item["previous_month"] = {
                    "salary_month": str(prev_salary.salary_month)[:7],
                    "base_salary": float(prev_salary.base_salary),
                    "bonus": float(prev_salary.bonus),
                    "deductions": float(prev_salary.deductions),
                    "net_salary": float(prev_salary.net_salary),
                }
                # Tính % thay đổi
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
        return self._to_response(salary)

    # 3. Tạo bản ghi lương
    async def create(self, data: SalaryCreate) -> dict:
        month_date = date.fromisoformat(f"{data.salary_month}-01")
        # Always calculate net_salary = base + bonus - deductions
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
        # Nạp lại kèm relationship để tránh lazy-load trong async context
        salary = await self.repo.get_by_id(salary.id)
        return self._to_response(salary)

    # 4. Cập nhật lương
    async def update(self, salary_id: int, data: SalaryUpdate) -> dict:
        salary = await self.repo.get_by_id(salary_id)
        if not salary:
            raise NotFoundException("Salary", salary_id)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(salary, field, value)

        # Always recalculate net_salary = base + bonus - deductions
        salary.net_salary = salary.base_salary + salary.bonus - salary.deductions

        await self.repo.update(salary)
        salary = await self.repo.get_by_id(salary_id)
        return self._to_response(salary)

    # =============================================
    # 5. THỐNG KÊ LƯƠNG THEO PHÒNG BAN
    # =============================================
    async def get_statistics(self, month: str) -> List[dict]:
        month_date = date.fromisoformat(f"{month}-01")
        stats = await self.repo.get_statistics_by_department(month_date)
        # Convert Decimal → float để JSON encode được
        return [
            {
                "department_id": row.department_id,
                "department_name": row.department_name,
                "employee_count": row.employee_count,
                "total_salary": float(row.total_salary or 0),
                "avg_salary": float(row.avg_salary or 0),
                "min_salary": float(row.min_salary or 0),
                "max_salary": float(row.max_salary or 0),
            }
            for row in stats
        ]

    # =============================================
    # HELPER: convert Salary model → dict
    # =============================================
    def _to_response(self, salary: Salary) -> dict:
        # Trả về cấu trúc bao gồm cả "current_month" + chỗ trống cho "previous_month"
        # → để get_list có thể fill thêm previous_month
        result = {
            "id": salary.id,
            "salary_id": salary.id,
            "employee_id": salary.employee_id,
            "employee_name": salary.employee.full_name if salary.employee else None,
            "full_name": salary.employee.full_name if salary.employee else None,
            "department_name": (
                salary.employee.department.department_name
                if salary.employee and salary.employee.department
                else None
            ),
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
            "previous_month": None,        # sẽ fill ở get_list nếu có
            "change_percentage": None,
            "change_direction": None,
            "created_at": salary.created_at,
            "updated_at": salary.updated_at,
        }
        return result