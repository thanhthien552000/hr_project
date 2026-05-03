from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.services.alert import AlertService
from app.common.pagination import PaginationParams
from app.common.response import success_response, paginated_response

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("")
async def list_alerts(
    pagination: PaginationParams = Depends(),
    alert_type: Optional[str] = Query(None),
    is_read: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    service = AlertService(db)
    items, total = await service.get_list(
        offset=pagination.offset, limit=pagination.page_size,
        alert_type=alert_type, is_read=is_read,
    )
    return paginated_response(items, total, pagination.page, pagination.page_size)


@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_alerts(
    month: Optional[str] = Query(None, description="Format: YYYY-MM"),
    db: AsyncSession = Depends(get_db),
):
    service = AlertService(db)
    result = await service.generate_alerts(month)
    return success_response(data=result, message="Alerts generated successfully")
