from typing import Optional, List, Tuple
from datetime import date
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.salary import Salary
from app.models.employee import Employee
from app.models.department import Department


class PayrollRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(
        self,
        offset: int = 0,
        limit: int = 20,
        month: Optional[str] = None,
        department_id: Optional[int] = None,
    ) -> Tuple[List[Salary], int]:
        query = select(Salary).join(Employee, Salary.employee_id == Employee.id)

        if month:
            month_date = date.fromisoformat(f"{month}-01")
            query = query.where(Salary.salary_month == month_date)
        if department_id:
            query = query.where(Employee.department_id == department_id)

        count_query = select(func.count()).select_from(query.subquery())
        result = await self.db.execute(count_query)
        total = result.scalar() or 0

        query = query.order_by(Salary.salary_month.desc(), Salary.id.desc())
        query = query.offset(offset).limit(limit)
        query = query.options(selectinload(Salary.employee).selectinload(Employee.department))

        result = await self.db.execute(query)
        salaries = list(result.scalars().all())
        return salaries, total

    async def get_by_id(self, salary_id: int) -> Optional[Salary]:
        query = (
            select(Salary)
            .where(Salary.id == salary_id)
            .options(selectinload(Salary.employee).selectinload(Employee.department))
        )
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

    async def get_payroll_by_department(self, month_date: date) -> List:
        query = (
            select(
                Department.id.label("department_id"),
                Department.department_name,
                func.sum(Salary.net_salary).label("total_salary"),
            )
            .join(Employee, Salary.employee_id == Employee.id)
            .join(Department, Employee.department_id == Department.id)
            .where(Salary.salary_month == month_date, Employee.is_deleted == False)
            .group_by(Department.id, Department.department_name)
            .order_by(func.sum(Salary.net_salary).desc())
        )
        result = await self.db.execute(query)
        return list(result.all())

    async def get_total_payroll(self, month_date: date) -> Decimal:
        query = select(func.sum(Salary.net_salary)).where(Salary.salary_month == month_date)
        result = await self.db.execute(query)
        return result.scalar() or Decimal("0")

    async def get_salary_changes(self, current_month: date, previous_month: date, threshold: float = 20.0) -> List:
        """Get employees with salary changes above threshold between two months."""
        current_alias = select(
            Salary.employee_id,
            Salary.net_salary.label("current_salary"),
        ).where(Salary.salary_month == current_month).subquery()

        previous_alias = select(
            Salary.employee_id,
            Salary.net_salary.label("previous_salary"),
        ).where(Salary.salary_month == previous_month).subquery()

        query = (
            select(
                Employee.id.label("employee_id"),
                Employee.full_name,
                current_alias.c.current_salary,
                previous_alias.c.previous_salary,
            )
            .join(current_alias, Employee.id == current_alias.c.employee_id)
            .join(previous_alias, Employee.id == previous_alias.c.employee_id)
            .where(Employee.is_deleted == False)
        )
        result = await self.db.execute(query)
        all_rows = result.all()

        # Filter by threshold in Python to avoid complex SQL
        changes = []
        for row in all_rows:
            if row.previous_salary and row.previous_salary > 0:
                pct = abs(float(row.current_salary - row.previous_salary) / float(row.previous_salary) * 100)
                if pct > threshold:
                    changes.append(row)
        return changes

    async def get_latest_month(self) -> Optional[date]:
        """Get the latest salary_month that has data."""
        query = select(func.max(Salary.salary_month))
        result = await self.db.execute(query)
        return result.scalar()

    async def get_recent_salaries(self, limit: int = 10) -> List[Salary]:
        query = (
            select(Salary)
            .options(selectinload(Salary.employee).selectinload(Employee.department))
            .order_by(Salary.salary_month.desc(), Salary.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_statistics_by_department(self, month_date: date) -> List:
        query = (
            select(
                Department.id.label("department_id"),
                Department.department_name,
                func.count(Salary.id).label("employee_count"),
                func.sum(Salary.net_salary).label("total_salary"),
                func.avg(Salary.net_salary).label("avg_salary"),
                func.min(Salary.net_salary).label("min_salary"),
                func.max(Salary.net_salary).label("max_salary"),
            )
            .join(Employee, Salary.employee_id == Employee.id)
            .join(Department, Employee.department_id == Department.id)
            .where(Salary.salary_month == month_date, Employee.is_deleted == False)
            .group_by(Department.id, Department.department_name)
            .order_by(Department.department_name)
        )
        result = await self.db.execute(query)
        return list(result.all())
