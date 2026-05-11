from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_human_db, get_payroll_db
from app.services.alert import AlertService
from app.common.pagination import PaginationParams
from app.common.response import success_response, paginated_response

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("")
async def list_alerts(
    pagination: PaginationParams = Depends(),
    alert_type: Optional[str] = Query(None),
    is_read: Optional[bool] = Query(None),
    payroll_db: AsyncSession = Depends(get_payroll_db),
    human_db: AsyncSession = Depends(get_human_db),
):
    service = AlertService(payroll_db, human_db)
    items, total = await service.get_list(
        offset=pagination.offset, limit=pagination.page_size,
        alert_type=alert_type, is_read=is_read,
    )
    return paginated_response(items, total, pagination.page, pagination.page_size)


@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_alerts(
    month: Optional[str] = Query(None, description="Format: YYYY-MM"),
    payroll_db: AsyncSession = Depends(get_payroll_db),
    human_db: AsyncSession = Depends(get_human_db),
):
    service = AlertService(payroll_db, human_db)
    result = await service.generate_alerts(month)
    return success_response(data=result, message="Alerts generated successfully")
