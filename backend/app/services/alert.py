from typing import Optional, Tuple, List
from datetime import date
from dateutil.relativedelta import relativedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import Alert
from app.repositories.alert import AlertRepository
from app.repositories.attendance import AttendanceRepository
from app.repositories.payroll import PayrollRepository
from app.repositories.employee import EmployeeRepository
from app.core.config import settings


class AlertService:
    """Service xử lý cảnh báo — cross-DB: Payroll (MySQL) + Human (SQL Server)."""

    def __init__(self, payroll_db: AsyncSession, human_db: AsyncSession):
        self.repo = AlertRepository(payroll_db)
        self.attendance_repo = AttendanceRepository(payroll_db)
        self.payroll_repo = PayrollRepository(payroll_db)
        self.employee_repo = EmployeeRepository(human_db)

    # =============================================
    # 1. DANH SÁCH CẢNH BÁO (kèm tên nhân viên từ Human DB)
    # =============================================
    async def get_list(
        self,
        offset: int = 0,
        limit: int = 20,
        alert_type: Optional[str] = None,
        is_read: Optional[bool] = None,
    ) -> Tuple[List[dict], int]:
        alerts, total = await self.repo.get_list(
            offset=offset, limit=limit, alert_type=alert_type, is_read=is_read,
        )

        # Batch lookup employee names from Human DB
        emp_ids = {a.employee_id for a in alerts}
        emp_map = await self.employee_repo.get_employee_info_map(emp_ids)

        items = []
        for a in alerts:
            emp_info = emp_map.get(a.employee_id, {})
            items.append({
                "id": a.id,
                "employee_id": a.employee_id,
                "employee_name": emp_info.get("full_name"),
                "alert_type": a.alert_type,
                "message": a.message,
                "severity": a.severity,
                "is_read": a.is_read,
                "created_at": a.created_at,
            })
        return items, total

    # =============================================
    # 2. AUTO-GENERATE CẢNH BÁO (cross-DB)
    # =============================================
    async def generate_alerts(self, month: Optional[str] = None) -> dict:
        if month:
            current = date.fromisoformat(f"{month}-01")
        else:
            current = date.today().replace(day=1)
        previous = current - relativedelta(months=1)

        alerts_created = []

        # ===== Loại 1: Vắng quá nhiều =====
        excessive = await self.attendance_repo.get_excessive_absence(
            current, settings.ALERT_ABSENCE_THRESHOLD
        )
        # Get employee names for alert messages
        excessive_emp_ids = {row["employee_id"] for row in excessive}
        emp_map = await self.employee_repo.get_employee_info_map(excessive_emp_ids)

        for row in excessive:
            emp_info = emp_map.get(row["employee_id"], {})
            full_name = emp_info.get("full_name", f"NV#{row['employee_id']}")
            alert = Alert(
                employee_id=row["employee_id"],
                alert_type="excessive_absence",
                message=(
                    f"{full_name} nghỉ {row['absent_days']} ngày "
                    f"trong tháng {str(current)[:7]} "
                    f"(ngưỡng: {settings.ALERT_ABSENCE_THRESHOLD})"
                ),
                severity="warning",
            )
            alerts_created.append(alert)

        # ===== Loại 2: Lương thay đổi bất thường =====
        salary_changes = await self.payroll_repo.get_salary_changes(current, previous)
        change_emp_ids = {row["employee_id"] for row in salary_changes}
        change_emp_map = await self.employee_repo.get_employee_info_map(change_emp_ids)

        for row in salary_changes:
            prev_sal = row["previous_salary"]
            curr_sal = row["current_salary"]
            if prev_sal and prev_sal > 0:
                pct = abs(float(curr_sal - prev_sal) / float(prev_sal) * 100)
                if pct > settings.ALERT_SALARY_CHANGE_THRESHOLD:
                    emp_info = change_emp_map.get(row["employee_id"], {})
                    full_name = emp_info.get("full_name", f"NV#{row['employee_id']}")
                    direction = "tăng" if curr_sal > prev_sal else "giảm"
                    alert = Alert(
                        employee_id=row["employee_id"],
                        alert_type="salary_change",
                        message=f"Lương {full_name} {direction} {pct:.1f}% so với tháng trước",
                        severity="high" if pct > 50 else "warning",
                    )
                    alerts_created.append(alert)

        # Lọc trùng
        existing_keys = await self.repo.get_existing_keys()
        alerts_to_insert = [
            a for a in alerts_created
            if (a.employee_id, a.alert_type, a.message) not in existing_keys
        ]

        if alerts_to_insert:
            await self.repo.create_batch(alerts_to_insert)

        return {
            "alerts_generated": len(alerts_to_insert),
            "month": str(current)[:7],
        }