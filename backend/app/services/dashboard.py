from typing import Optional
from datetime import date
from dateutil.relativedelta import relativedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.employee import EmployeeRepository
from app.repositories.attendance import AttendanceRepository
from app.repositories.payroll import PayrollRepository


class DashboardService:
    """Service tổng hợp dữ liệu cho Dashboard - dùng nhiều Repository cùng lúc."""

    def __init__(self, db: AsyncSession):
        # Khác với các service khác: dùng 3 repo cùng lúc
        self.employee_repo = EmployeeRepository(db)
        self.attendance_repo = AttendanceRepository(db)
        self.payroll_repo = PayrollRepository(db)

    # =============================================
    # 1. SUMMARY: tổng quan nhân sự + so sánh với tháng trước
    # =============================================
    async def get_summary(self, month: Optional[str] = None) -> dict:
        # Nếu không truyền month, lấy tháng hiện tại
        if month:
            ref_date = date.fromisoformat(f"{month}-01")
        else:
            ref_date = date.today().replace(day=1)

        # Tính ngày cuối tháng: đầu tháng sau - 1 ngày
        month_end = (ref_date + relativedelta(months=1)) - relativedelta(days=1)

        # Đếm các chỉ số
        total = await self.employee_repo.count_total()
        active = await self.employee_repo.count_active()
        new_this_month = await self.employee_repo.count_new_in_month(ref_date, month_end)
        resigned = await self.employee_repo.count_resigned()

        # So sánh với tháng trước
        prev_start = ref_date - relativedelta(months=1)
        prev_end = ref_date - relativedelta(days=1)
        new_prev = await self.employee_repo.count_new_in_month(prev_start, prev_end)

        # Tính % thay đổi
        if new_prev > 0:
            change_pct = round((new_this_month - new_prev) / new_prev * 100, 2)
        else:
            # Edge case: tháng trước không có ai → tháng này tăng 100% nếu có ai
            change_pct = 100.0 if new_this_month > 0 else 0.0

        return {
            "total_employees": total,
            "active_employees": active,
            "new_employees_this_month": new_this_month,
            "resigned_employees": resigned,
            "change_percentage": abs(change_pct),
            "change_direction": "up" if change_pct >= 0 else "down",
        }

    # =============================================
    # 2. PERFORMANCE: hiệu suất làm việc tháng này so với tháng trước
    # =============================================
    async def get_performance(self, month: Optional[str] = None) -> dict:
        if month:
            current = date.fromisoformat(f"{month}-01")
        else:
            current = date.today().replace(day=1)

        previous = current - relativedelta(months=1)

        current_stats = await self.attendance_repo.get_month_stats(current)
        previous_stats = await self.attendance_repo.get_month_stats(previous)

        # Performance = (tổng work_days) / (số NV * 22 ngày chuẩn) * 100
        current_perf = 0.0
        if current_stats["record_count"] > 0:
            total_possible = current_stats["record_count"] * 22  # ~22 ngày làm việc/tháng
            current_perf = round(current_stats["total_work"] / total_possible * 100, 2)

        previous_perf = 0.0
        if previous_stats["record_count"] > 0:
            total_possible = previous_stats["record_count"] * 22
            previous_perf = round(previous_stats["total_work"] / total_possible * 100, 2)

        change = round(current_perf - previous_perf, 2)

        return {
            "current_month": str(current)[:7],
            "current_performance": current_perf,
            "previous_performance": previous_perf,
            "change_percentage": abs(change),
            "change_direction": "up" if change >= 0 else "down",
        }

    # =============================================
    # 3. PAYROLL THEO PHÒNG BAN (cho biểu đồ tròn)
    # =============================================
    async def get_payroll_by_department(self, month: Optional[str] = None) -> dict:
        if month:
            month_date = date.fromisoformat(f"{month}-01")
        else:
            month_date = date.today().replace(day=1)

        departments = await self.payroll_repo.get_payroll_by_department(month_date)
        total = await self.payroll_repo.get_total_payroll(month_date)
        total_float = float(total) if total else 0

        # Tính % của mỗi phòng ban so với tổng quỹ
        dept_list = []
        for row in departments:
            salary_float = float(row.total_salary) if row.total_salary else 0
            pct = round(salary_float / total_float * 100, 2) if total_float > 0 else 0
            dept_list.append({
                "department_id": row.department_id,
                "department_name": row.department_name,
                "total_salary": salary_float,
                "percentage": pct,
            })

        return {
            "month": str(month_date)[:7],
            "departments": dept_list,
            "total_payroll": total_float,
        }

    # =============================================
    # 4. HOẠT ĐỘNG GẦN ĐÂY (10 lương mới nhất, mỗi NV chỉ tính 1 lần)
    # =============================================
    async def get_recent_activities(self, limit: int = 10) -> dict:
        salaries = await self.payroll_repo.get_recent_salaries(limit)
        seen = set()                # set để check trùng employee_id
        items = []
        for s in salaries:
            if s.employee_id in seen:
                continue            # Bỏ qua nếu đã có NV này
            seen.add(s.employee_id)
            items.append({
                "employee_id": s.employee_id,
                "full_name": s.employee.full_name if s.employee else None,
                "department_name": (
                    s.employee.department.department_name
                    if s.employee and s.employee.department
                    else None
                ),
                "net_salary": float(s.net_salary),
                "last_activity_date": str(s.salary_month)[:7],
            })
        return {"items": items}

    # =============================================
    # 5. TOP NV VẮNG NHIỀU NHẤT
    # =============================================
    async def get_top_absent_employees(self, month: Optional[str] = None, limit: int = 5) -> dict:
        if month:
            month_date = date.fromisoformat(f"{month}-01")
        else:
            month_date = date.today().replace(day=1)

        rows = await self.attendance_repo.get_top_absent(month_date, limit)
        employees = []
        for row in rows:
            employees.append({
                "employee_id": row.employee_id,
                "full_name": row.full_name,
                "department_name": None,
                "absent_days": row.total_absent or 0,
                "leave_days": row.total_leave or 0,
            })

        return {
            "month": str(month_date)[:7],
            "employees": employees,
        }