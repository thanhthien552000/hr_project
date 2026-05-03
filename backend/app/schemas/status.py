from typing import List
from pydantic import BaseModel


class StatusItem(BaseModel):
    status: str
    count: int
    percentage: float


class StatusOverviewResponse(BaseModel):
    total_employees: int
    statuses: List[StatusItem]
