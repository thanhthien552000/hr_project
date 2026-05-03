from typing import Optional, List, Tuple
from datetime import date
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.employee import Employee
from app.models.department import Department
from app.models.position import Position


class EmployeeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(
        self,
        offset: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        department_id: Optional[int] = None,
        status: Optional[str] = None,
        sort_by: str = "id",
        sort_order: str = "asc",
    ) -> Tuple[List[Employee], int]:
        query = select(Employee).where(Employee.is_deleted == False)

        if search:
            query = query.where(
                or_(
                    Employee.full_name.ilike(f"%{search}%"),
                    Employee.email.ilike(f"%{search}%"),
                    Employee.phone_number.ilike(f"%{search}%"),
                )
            )
        if department_id:
            query = query.where(Employee.department_id == department_id)
        if status:
            query = query.where(Employee.status == status)

        # Count
        count_query = select(func.count()).select_from(query.subquery())
        result = await self.db.execute(count_query)
        total = result.scalar() or 0

        # Sort
        sort_column = getattr(Employee, sort_by, Employee.id)
        if sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # Paginate
        query = query.offset(offset).limit(limit)
        query = query.options(selectinload(Employee.department), selectinload(Employee.position))

        result = await self.db.execute(query)
        employees = list(result.scalars().all())
        return employees, total

    async def get_by_id(self, employee_id: int) -> Optional[Employee]:
        query = (
            select(Employee)
            .where(Employee.id == employee_id, Employee.is_deleted == False)
            .options(selectinload(Employee.department), selectinload(Employee.position))
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[Employee]:
        query = select(Employee).where(Employee.email == email, Employee.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, employee: Employee) -> Employee:
        self.db.add(employee)
        await self.db.flush()
        await self.db.refresh(employee)
        return employee

    async def update(self, employee: Employee) -> Employee:
        await self.db.flush()
        await self.db.refresh(employee)
        return employee

    async def soft_delete(self, employee: Employee) -> Employee:
        employee.is_deleted = True
        employee.status = "Nghỉ việc"
        await self.db.flush()
        return employee

    async def count_by_status(self) -> List:
        query = (
            select(Employee.status, func.count(Employee.id).label("count"))
            .where(Employee.is_deleted == False)
            .group_by(Employee.status)
        )
        result = await self.db.execute(query)
        return list(result.all())

    async def count_active(self) -> int:
        query = select(func.count()).where(
            Employee.is_deleted == False,
            Employee.status == "Đang làm việc",
        )
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def count_total(self) -> int:
        query = select(func.count()).where(Employee.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def count_new_in_month(self, month_start: date, month_end: date) -> int:
        query = select(func.count()).where(
            Employee.is_deleted == False,
            Employee.hire_date >= month_start,
            Employee.hire_date <= month_end,
        )
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def count_resigned(self) -> int:
        query = select(func.count()).where(Employee.status == "Nghỉ việc")
        result = await self.db.execute(query)
        return result.scalar() or 0

    async def get_all_active(self) -> List[Employee]:
        query = (
            select(Employee)
            .where(Employee.is_deleted == False)
            .options(selectinload(Employee.department), selectinload(Employee.position))
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
