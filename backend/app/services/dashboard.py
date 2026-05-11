from typing import Optional
from datetime import date
from decimal import Decimal
from dateutil.relativedelta import relativedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.employee import EmployeeRepository
from app.repositories.attendance import AttendanceRepository
from app.repositories.payroll import PayrollRepository


class DashboardService:
    """Service tổng hợp dữ liệu cho Dashboard — cross-DB: Human + Payroll."""

    def __init__(self, human_db: AsyncSession, payroll_db: AsyncSession):
        self.employee_repo = EmployeeRepository(human_db)
        self.attendance_repo = AttendanceRepository(payroll_db)
        self.payroll_repo = PayrollRepository(payroll_db)

    # =============================================
    # 1. SUMMARY: tổng quan nhân sự + so sánh với tháng trước
    # =============================================
    async def get_summary(self, month: Optional[str] = None) -> dict:
        if month:
            ref_date = date.fromisoformat(f"{month}-01")
        else:
            ref_date = date.today().replace(day=1)

        month_end = (ref_date + relativedelta(months=1)) - relativedelta(days=1)

        total = await self.employee_repo.count_total()
        active = await self.employee_repo.count_active()
        new_this_month = await self.employee_repo.count_new_in_month(ref_date, month_end)
        resigned = await self.employee_repo.count_resigned()

        prev_start = ref_date - relativedelta(months=1)
        prev_end = ref_date - relativedelta(days=1)
        new_prev = await self.employee_repo.count_new_in_month(prev_start, prev_end)

        if new_prev > 0:
            change_pct = round((new_this_month - new_prev) / new_prev * 100, 2)
        else:
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

        current_perf = 0.0
        if current_stats["record_count"] > 0:
            total_possible = current_stats["record_count"] * 22
            current_perf = round(float(current_stats["total_work"]) / total_possible * 100, 2)

        previous_perf = 0.0
        if previous_stats["record_count"] > 0:
            total_possible = previous_stats["record_count"] * 22
            previous_perf = round(float(previous_stats["total_work"]) / total_possible * 100, 2)

        change = round(current_perf - previous_perf, 2)

        return {
            "current_month": str(current)[:7],
            "current_performance": current_perf,
            "previous_performance": previous_perf,
            "change_percentage": abs(change),
            "change_direction": "up" if change >= 0 else "down",
        }

    # =============================================
    # 3. PAYROLL THEO PHÒNG BAN (cross-DB)
    # =============================================
    async def get_payroll_by_department(self, month: Optional[str] = None) -> dict:
        if month:
            month_date = date.fromisoformat(f"{month}-01")
        else:
            month_date = date.today().replace(day=1)

        salaries = await self.payroll_repo.get_salaries_by_month(month_date)
        total = await self.payroll_repo.get_total_payroll(month_date)
        total_float = float(total) if total else 0

        if not salaries:
            return {"month": str(month_date)[:7], "departments": [], "total_payroll": 0}

        # Get employee info from Human DB
        emp_ids = {s.employee_id for s in salaries}
        emp_map = await self.employee_repo.get_employee_info_map(emp_ids)

        # Group by department in Python
        dept_totals = {}
        for s in salaries:
            emp_info = emp_map.get(s.employee_id, {})
            if emp_info.get("is_deleted", False):
                continue
            dept_id = emp_info.get("department_id", 0)
            dept_name = emp_info.get("department_name", "Unknown")

            if dept_id not in dept_totals:
                dept_totals[dept_id] = {"department_id": dept_id, "department_name": dept_name, "total_salary": 0.0}
            dept_totals[dept_id]["total_salary"] += float(s.net_salary)

        dept_list = []
        for dept in sorted(dept_totals.values(), key=lambda x: x["total_salary"], reverse=True):
            pct = round(dept["total_salary"] / total_float * 100, 2) if total_float > 0 else 0
            dept_list.append({
                "department_id": dept["department_id"],
                "department_name": dept["department_name"],
                "total_salary": dept["total_salary"],
                "percentage": pct,
            })

        return {
            "month": str(month_date)[:7],
            "departments": dept_list,
            "total_payroll": total_float,
        }

    # =============================================
    # 4. HOẠT ĐỘNG GẦN ĐÂY (cross-DB)
    # =============================================
    async def get_recent_activities(self, limit: int = 10) -> dict:
        salaries = await self.payroll_repo.get_recent_salaries(limit * 2)

        # Deduplicate by employee
        seen = set()
        unique_salaries = []
        for s in salaries:
            if s.employee_id not in seen:
                seen.add(s.employee_id)
                unique_salaries.append(s)
            if len(unique_salaries) >= limit:
                break

        # Batch lookup employee info
        emp_ids = {s.employee_id for s in unique_salaries}
        emp_map = await self.employee_repo.get_employee_info_map(emp_ids)

        items = []
        for s in unique_salaries:
            emp_info = emp_map.get(s.employee_id, {})
            items.append({
                "employee_id": s.employee_id,
                "full_name": emp_info.get("full_name"),
                "department_name": emp_info.get("department_name"),
                "net_salary": float(s.net_salary),
                "last_activity_date": str(s.salary_month)[:7],
            })
        return {"items": items}

    # =============================================
    # 5. TOP NV VẮNG NHIỀU NHẤT (cross-DB)
    # =============================================
    async def get_top_absent_employees(self, month: Optional[str] = None, limit: int = 5) -> dict:
        if month:
            month_date = date.fromisoformat(f"{month}-01")
        else:
            month_date = date.today().replace(day=1)

        rows = await self.attendance_repo.get_top_absent(month_date, limit)

        # Batch lookup employee info
        emp_ids = {row["employee_id"] for row in rows}
        emp_map = await self.employee_repo.get_employee_info_map(emp_ids)

        employees = []
        for row in rows:
            emp_info = emp_map.get(row["employee_id"], {})
            employees.append({
                "employee_id": row["employee_id"],
                "full_name": emp_info.get("full_name"),
                "department_name": emp_info.get("department_name"),
                "absent_days": row["total_absent"],
                "leave_days": row["total_leave"],
            })

        return {
            "month": str(month_date)[:7],
            "employees": employees,
        }