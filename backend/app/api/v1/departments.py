from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import success_response
from app.core.dependencies import get_human_db
from app.models.department import Department

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("")
async def list_departments(
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_human_db),
):
    query = select(Department)
    if search:
        query = query.where(Department.department_name.ilike(f"%{search}%"))
    query = query.order_by(Department.department_name.asc())

    result = await db.execute(query)
    departments = result.scalars().all()
    data = [
        {
            "id": department.id,
            "department_name": department.department_name,
            "created_at": department.created_at,
            "updated_at": department.updated_at,
        }
        for department in departments
    ]
    return success_response(data=data)
