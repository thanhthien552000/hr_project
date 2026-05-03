from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.services.status import StatusService
from app.common.response import success_response

router = APIRouter(prefix="/status", tags=["Status"])


@router.get("/overview")
async def status_overview(
    db: AsyncSession = Depends(get_db),
):
    service = StatusService(db)
    data = await service.get_overview()
    return success_response(data=data)
