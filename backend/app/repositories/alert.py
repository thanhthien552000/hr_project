from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import Alert
from app.models.employee import Employee


class AlertRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(
        self,
        offset: int = 0,
        limit: int = 20,
        alert_type: Optional[str] = None,
        is_read: Optional[bool] = None,
    ) -> tuple:
        query = select(Alert)

        if alert_type:
            query = query.where(Alert.alert_type == alert_type)
        if is_read is not None:
            query = query.where(Alert.is_read == is_read)

        count_query = select(func.count()).select_from(query.subquery())
        result = await self.db.execute(count_query)
        total = result.scalar() or 0

        query = query.order_by(Alert.created_at.desc())
        query = query.offset(offset).limit(limit)

        result = await self.db.execute(query)
        alerts = list(result.scalars().all())
        return alerts, total

    async def create(self, alert: Alert) -> Alert:
        self.db.add(alert)
        await self.db.flush()
        await self.db.refresh(alert)
        return alert

    async def create_batch(self, alerts: List[Alert]) -> List[Alert]:
        self.db.add_all(alerts)
        await self.db.flush()
        return alerts

    async def get_employee_name(self, employee_id: int) -> Optional[str]:
        query = select(Employee.full_name).where(Employee.id == employee_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
