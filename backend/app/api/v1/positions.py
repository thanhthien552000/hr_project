from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import success_response
from app.core.dependencies import get_db
from app.models.position import Position

router = APIRouter(prefix="/positions", tags=["Positions"])


@router.get("")
async def list_positions(
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Position)
    if search:
        query = query.where(Position.position_name.ilike(f"%{search}%"))
    query = query.order_by(Position.position_name.asc())

    result = await db.execute(query)
    positions = result.scalars().all()
    data = [
        {
            "id": position.id,
            "position_name": position.position_name,
            "created_at": position.created_at,
            "updated_at": position.updated_at,
        }
        for position in positions
    ]
    return success_response(data=data)
