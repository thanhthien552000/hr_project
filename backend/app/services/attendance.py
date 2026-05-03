from typing import Optional, Tuple, List
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendance import Attendance
from app.repositories.attendance import AttendanceRepository
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate
from app.common.exceptions import NotFoundException


class AttendanceService:
    """Xử lý nghiệp vụ chấm công."""

    def __init__(self, db: AsyncSession):
        self.repo = AttendanceRepository(db)

    # 1. Danh sách chấm công
    async def get_list(
        self,
        offset: int = 0,
        limit: int = 20,
        month: Optional[str] = None,
        employee_id: Optional[int] = None,
    ) -> Tuple[List[dict], int]:
        records, total = await self.repo.get_list(
            offset=offset, limit=limit, month=month, employee_id=employee_id,
        )
        items = [self._to_response(r) for r in records]
        return items, total

    # 2. Tạo bản ghi chấm công
    async def create(self, data: AttendanceCreate) -> dict:
        # Schema gửi "2026-03" → cần convert thành date(2026, 3, 1)
        month_date = date.fromisoformat(f"{data.attendance_month}-01")
        attendance = Attendance(
            employee_id=data.employee_id,
            work_days=data.work_days,
            absent_days=data.absent_days,
            leave_days=data.leave_days,
            late_days=data.late_days,
            attendance_month=month_date,
        )
        attendance = await self.repo.create(attendance)
        return self._to_response(attendance)

    # 3. Cập nhật chấm công
    async def update(self, attendance_id: int, data: AttendanceUpdate) -> dict:
        attendance = await self.repo.get_by_id(attendance_id)
        if not attendance:
            raise NotFoundException("Attendance", attendance_id)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(attendance, field, value)

        attendance = await self.repo.update(attendance)
        return self._to_response(attendance)

    # Helper: convert model → dict
    def _to_response(self, record: Attendance) -> dict:
        return {
            "id": record.id,
            "employee_id": record.employee_id,
            # Lấy tên nhân viên qua relationship
            "employee_name": record.employee.full_name if record.employee else None,
            "work_days": record.work_days,
            "absent_days": record.absent_days,
            "leave_days": record.leave_days,
            "late_days": record.late_days,
            # Convert date → "YYYY-MM" (chỉ lấy năm-tháng)
            "attendance_month": str(record.attendance_month)[:7],
            "created_at": record.created_at,
            "updated_at": record.updated_at,
        }