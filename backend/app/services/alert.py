from typing import Optional, Tuple, List
from datetime import date
from dateutil.relativedelta import relativedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import Alert
from app.repositories.alert import AlertRepository
from app.repositories.attendance import AttendanceRepository
from app.repositories.payroll import PayrollRepository
from app.core.config import settings


class AlertService:
    """Service xử lý cảnh báo — có thể auto-generate cảnh báo từ data."""

    def __init__(self, db: AsyncSession):
        self.repo = AlertRepository(db)
        # Cần thêm 2 repo này để quét absence + salary changes
        self.attendance_repo = AttendanceRepository(db)
        self.payroll_repo = PayrollRepository(db)

    # =============================================
    # 1. DANH SÁCH CẢNH BÁO (kèm tên nhân viên)
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
        items = []
        for a in alerts:
            # Lấy tên NV cho mỗi cảnh báo
            name = await self.repo.get_employee_name(a.employee_id)
            items.append({
                "id": a.id,
                "employee_id": a.employee_id,
                "employee_name": name,
                "alert_type": a.alert_type,
                "message": a.message,
                "severity": a.severity,
                "is_read": a.is_read,
                "created_at": a.created_at,
            })
        return items, total

    # =============================================
    # 2. AUTO-GENERATE CẢNH BÁO (gọi định kỳ hoặc thủ công)
    # =============================================
    async def generate_alerts(self, month: Optional[str] = None) -> dict:
        """
        Quét dữ liệu của 1 tháng và sinh cảnh báo:
        - Loại 1: NV vắng quá ngưỡng (settings.ALERT_ABSENCE_THRESHOLD = 5)
        - Loại 2: Lương thay đổi > ngưỡng (settings.ALERT_SALARY_CHANGE_THRESHOLD = 20%)
        """
        # Xác định tháng cần quét
        if month:
            current = date.fromisoformat(f"{month}-01")
        else:
            current = date.today().replace(day=1)
        previous = current - relativedelta(months=1)

        alerts_created = []  # Gom tất cả cảnh báo rồi insert batch

        # ===== Loại 1: Vắng quá nhiều =====
        excessive = await self.attendance_repo.get_excessive_absence(
            current, settings.ALERT_ABSENCE_THRESHOLD
        )
        for row in excessive:
            alert = Alert(
                employee_id=row.employee_id,
                alert_type="excessive_absence",
                message=(
                    f"{row.full_name} nghỉ {row.absent_days} ngày "
                    f"trong tháng {str(current)[:7]} "
                    f"(ngưỡng: {settings.ALERT_ABSENCE_THRESHOLD})"
                ),
                severity="warning",
            )
            alerts_created.append(alert)

        # ===== Loại 2: Lương thay đổi bất thường =====
        salary_changes = await self.payroll_repo.get_salary_changes(
            current, previous, settings.ALERT_SALARY_CHANGE_THRESHOLD
        )
        for row in salary_changes:
            if row.previous_salary and row.previous_salary > 0:
                pct = abs(float(row.current_salary - row.previous_salary) / float(row.previous_salary) * 100)
                # Tăng/giảm để hiện trong message
                direction = "tăng" if row.current_salary > row.previous_salary else "giảm"
                alert = Alert(
                    employee_id=row.employee_id,
                    alert_type="salary_change",
                    message=f"Lương {row.full_name} {direction} {pct:.1f}% so với tháng trước",
                    # Severity = "high" nếu > 50%, ngược lại "warning"
                    severity="high" if pct > 50 else "warning",
                )
                alerts_created.append(alert)

        # Lọc trùng: bỏ qua alert đã tồn tại trong tháng này
        existing_keys = await self.repo.get_existing_keys_for_month(current.year, current.month)
        alerts_to_insert = [
            a for a in alerts_created
            if (a.employee_id, a.alert_type) not in existing_keys
        ]

        if alerts_to_insert:
            await self.repo.create_batch(alerts_to_insert)

        return {
            "alerts_generated": len(alerts_to_insert),
            "month": str(current)[:7],
        }