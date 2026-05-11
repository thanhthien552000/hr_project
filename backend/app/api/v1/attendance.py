from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_human_db, get_payroll_db
from app.services.attendance import AttendanceService
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate
from app.common.pagination import PaginationParams
from app.common.response import success_response, paginated_response

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.get("")
async def list_attendance(
    pagination: PaginationParams = Depends(),
    month: Optional[str] = Query(None, description="Format: YYYY-MM"),
    employee_id: Optional[int] = Query(None),
    payroll_db: AsyncSession = Depends(get_payroll_db),
    human_db: AsyncSession = Depends(get_human_db),
):
    service = AttendanceService(payroll_db, human_db)
    items, total = await service.get_list(
        offset=pagination.offset, limit=pagination.page_size,
        month=month, employee_id=employee_id,
    )
    return paginated_response(items, total, pagination.page, pagination.page_size)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_attendance(
    data: AttendanceCreate,
    payroll_db: AsyncSession = Depends(get_payroll_db),
    human_db: AsyncSession = Depends(get_human_db),
):
    service = AttendanceService(payroll_db, human_db)
    record = await service.create(data)
    return success_response(data=record, message="Attendance created successfully")


@router.put("/{attendance_id}")
async def update_attendance(
    attendance_id: int,
    data: AttendanceUpdate,
    payroll_db: AsyncSession = Depends(get_payroll_db),
    human_db: AsyncSession = Depends(get_human_db),
):
    service = AttendanceService(payroll_db, human_db)
    record = await service.update(attendance_id, data)
    return success_response(data=record, message="Attendance updated successfully")
