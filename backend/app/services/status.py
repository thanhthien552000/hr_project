from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.employee import EmployeeRepository


class StatusService:
    """Service ngắn — chỉ thống kê trạng thái nhân viên. Chỉ dùng Human DB."""

    def __init__(self, human_db: AsyncSession):
        self.employee_repo = EmployeeRepository(human_db)

    async def get_overview(self) -> dict:
        # Đếm theo trạng thái + đếm tổng
        status_counts = await self.employee_repo.count_by_status()
        total = await self.employee_repo.count_total()

        # Tính % cho từng trạng thái
        statuses = []
        for row in status_counts:
            status_name = row[0] or "Không xác định"   # row[0] = status (có thể NULL)
            count = row[1]                              # row[1] = count
            pct = round(count / total * 100, 2) if total > 0 else 0
            statuses.append({
                "status": status_name,
                "count": count,
                "percentage": pct,
            })

        return {
            "total_employees": total,
            "statuses": statuses,
        }