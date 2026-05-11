from typing import Optional, List, Tuple
from datetime import date
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.salary import Salary


class PayrollRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(
        self,
        offset: int = 0,
        limit: int = 20,
        month: Optional[str] = None,
        employee_ids_in_dept: Optional[List[int]] = None,
    ) -> Tuple[List[Salary], int]:
        query = select(Salary)

        if month:
            month_date = date.fromisoformat(f"{month}-01")
            query = query.where(Salary.salary_month == month_date)
        if employee_ids_in_dept is not None:
            query = query.where(Salary.employee_id.in_(employee_ids_in_dept))

        count_query = select(func.count()).select_from(query.subquery())
        result = await self.db.execute(count_query)
        total = result.scalar() or 0

        query = query.order_by(Salary.salary_month.desc(), Salary.id.desc())
        query = query.offset(offset).limit(limit)

        result = await self.db.execute(query)
        salaries = list(result.scalars().all())
        return salaries, total

    async def get_by_id(self, salary_id: int) -> Optional[Salary]:
        query = select(Salary).where(Salary.id == salary_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_employee_month(self, employee_id: int, month_date: date) -> Optional[Salary]:
        query = select(Salary).where(
            Salary.employee_id == employee_id,
            Salary.salary_month == month_date,
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, salary: Salary) -> Salary:
        self.db.add(salary)
        await self.db.flush()
        await self.db.refresh(salary)
        return salary

    async def update(self, salary: Salary) -> Salary:
        await self.db.flush()
        await self.db.refresh(salary)
        return salary

    async def get_salaries_by_month(self, month_date: date) -> List[Salary]:
        """Get all salary records for a given month."""
        query = select(Salary).where(Salary.salary_month == month_date)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_total_payroll(self, month_date: date) -> Decimal:
        query = select(func.sum(Salary.net_salary)).where(Salary.salary_month == month_date)
        result = await self.db.execute(query)
        return result.scalar() or Decimal("0")

    async def get_salary_changes(self, current_month: date, previous_month: date) -> List[dict]:
        """Get employees with salary data in both months (for comparison)."""
        current_q = select(
            Salary.employee_id,
            Salary.net_salary.label("current_salary"),
        ).where(Salary.salary_month == current_month).subquery()

        previous_q = select(
            Salary.employee_id,
            Salary.net_salary.label("previous_salary"),
        ).where(Salary.salary_month == previous_month).subquery()

        query = select(
            current_q.c.employee_id,
            current_q.c.current_salary,
            previous_q.c.previous_salary,
        ).join(previous_q, current_q.c.employee_id == previous_q.c.employee_id)

        result = await self.db.execute(query)
        return [
            {
                "employee_id": row.employee_id,
                "current_salary": row.current_salary,
                "previous_salary": row.previous_salary,
            }
            for row in result.all()
        ]

    async def get_latest_month(self) -> Optional[date]:
        """Get the latest salary_month that has data."""
        query = select(func.max(Salary.salary_month))
        result = await self.db.execute(query)
        return result.scalar()

    async def get_recent_salaries(self, limit: int = 10) -> List[Salary]:
        query = (
            select(Salary)
            .order_by(Salary.salary_month.desc(), Salary.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
