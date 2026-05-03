from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.services.dashboard import DashboardService
from app.common.response import success_response

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
async def dashboard_summary(
    month: Optional[str] = Query(None, description="Format: YYYY-MM"),
    db: AsyncSession = Depends(get_db),
):
    service = DashboardService(db)
    data = await service.get_summary(month)
    return success_response(data=data)


@router.get("/performance")
async def dashboard_performance(
    month: Optional[str] = Query(None, description="Format: YYYY-MM"),
    db: AsyncSession = Depends(get_db),
):
    service = DashboardService(db)
    data = await service.get_performance(month)
    return success_response(data=data)


@router.get("/payroll-by-department")
async def dashboard_payroll_by_department(
    month: Optional[str] = Query(None, description="Format: YYYY-MM"),
    db: AsyncSession = Depends(get_db),
):
    service = DashboardService(db)
    data = await service.get_payroll_by_department(month)
    return success_response(data=data)


@router.get("/recent-activities")
async def dashboard_recent_activities(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    service = DashboardService(db)
    data = await service.get_recent_activities(limit)
    return success_response(data=data)


@router.get("/top-absent-employees")
async def dashboard_top_absent(
    month: Optional[str] = Query(None, description="Format: YYYY-MM"),
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    service = DashboardService(db)
    data = await service.get_top_absent_employees(month, limit)
    return success_response(data=data)
