from typing import Optional, List, Tuple
from datetime import date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendance import Attendance


class AttendanceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(
        self,
        offset: int = 0,
        limit: int = 20,
        month: Optional[str] = None,
        employee_id: Optional[int] = None,
    ) -> Tuple[List[Attendance], int]:
        query = select(Attendance)

        if month:
            month_date = date.fromisoformat(f"{month}-01")
            query = query.where(Attendance.attendance_month == month_date)
        if employee_id:
            query = query.where(Attendance.employee_id == employee_id)

        count_query = select(func.count()).select_from(query.subquery())
        result = await self.db.execute(count_query)
        total = result.scalar() or 0

        query = query.order_by(Attendance.attendance_month.desc(), Attendance.id.desc())
        query = query.offset(offset).limit(limit)

        result = await self.db.execute(query)
        records = list(result.scalars().all())
        return records, total

    async def get_by_id(self, attendance_id: int) -> Optional[Attendance]:
        query = select(Attendance).where(Attendance.id == attendance_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_employee_month(self, employee_id: int, month_date: date) -> Optional[Attendance]:
        query = select(Attendance).where(
            Attendance.employee_id == employee_id,
            Attendance.attendance_month == month_date,
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, attendance: Attendance) -> Attendance:
        self.db.add(attendance)
        await self.db.flush()
        await self.db.refresh(attendance)
        return attendance

    async def update(self, attendance: Attendance) -> Attendance:
        await self.db.flush()
        await self.db.refresh(attendance)
        return attendance

    async def get_top_absent(self, month_date: date, limit: int = 5) -> List[dict]:
        """Get employees with most absent days — returns raw data without employee names."""
        query = (
            select(
                Attendance.employee_id,
                func.sum(Attendance.absent_days).label("total_absent"),
                func.sum(Attendance.leave_days).label("total_leave"),
            )
            .where(Attendance.attendance_month == month_date)
            .group_by(Attendance.employee_id)
            .order_by(func.sum(Attendance.absent_days).desc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        return [
            {
                "employee_id": row.employee_id,
                "total_absent": row.total_absent or 0,
                "total_leave": row.total_leave or 0,
            }
            for row in result.all()
        ]

    async def get_month_stats(self, month_date: date) -> dict:
        query = select(
            func.sum(Attendance.work_days).label("total_work"),
            func.sum(Attendance.absent_days).label("total_absent"),
            func.sum(Attendance.leave_days).label("total_leave"),
            func.sum(Attendance.late_days).label("total_late"),
            func.count(Attendance.id).label("record_count"),
        ).where(Attendance.attendance_month == month_date)

        result = await self.db.execute(query)
        row = result.one_or_none()
        if row:
            return {
                "total_work": int(row.total_work or 0),
                "total_absent": int(row.total_absent or 0),
                "total_leave": int(row.total_leave or 0),
                "total_late": int(row.total_late or 0),
                "record_count": int(row.record_count or 0),
            }
        return {"total_work": 0, "total_absent": 0, "total_leave": 0, "total_late": 0, "record_count": 0}

    async def get_excessive_absence(self, month_date: date, threshold: int = 5) -> List[dict]:
        """Get employees with absent_days > threshold — returns raw data without names."""
        query = (
            select(
                Attendance.employee_id,
                Attendance.absent_days,
                Attendance.leave_days,
            )
            .where(
                Attendance.attendance_month == month_date,
                Attendance.absent_days > threshold,
            )
        )
        result = await self.db.execute(query)
        return [
            {
                "employee_id": row.employee_id,
                "absent_days": row.absent_days,
                "leave_days": row.leave_days,
            }
            for row in result.all()
        ]
