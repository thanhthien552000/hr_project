from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.services.payroll import PayrollService
from app.schemas.payroll import SalaryCreate, SalaryUpdate
from app.common.pagination import PaginationParams
from app.common.response import success_response, paginated_response

router = APIRouter(prefix="/payroll", tags=["Payroll"])


@router.get("")
async def list_payroll(
    pagination: PaginationParams = Depends(),
    month: Optional[str] = Query(None, description="Format: YYYY-MM"),
    department_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    service = PayrollService(db)
    items, total = await service.get_list(
        offset=pagination.offset, limit=pagination.page_size,
        month=month, department_id=department_id,
    )
    return paginated_response(items, total, pagination.page, pagination.page_size)


@router.get("/statistics")
async def payroll_statistics(
    month: str = Query(..., description="Format: YYYY-MM"),
    db: AsyncSession = Depends(get_db),
):
    service = PayrollService(db)
    stats = await service.get_statistics(month)
    return success_response(data=stats)


@router.get("/{salary_id}")
async def get_salary(
    salary_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = PayrollService(db)
    salary = await service.get_by_id(salary_id)
    return success_response(data=salary)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_salary(
    data: SalaryCreate,
    db: AsyncSession = Depends(get_db),
):
    service = PayrollService(db)
    salary = await service.create(data)
    return success_response(data=salary, message="Salary record created successfully")


@router.put("/{salary_id}")
async def update_salary(
    salary_id: int,
    data: SalaryUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = PayrollService(db)
    salary = await service.update(salary_id, data)
    return success_response(data=salary, message="Salary record updated successfully")
