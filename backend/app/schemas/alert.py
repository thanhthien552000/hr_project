from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AlertBase(BaseModel):
    employee_id: int
    alert_type: str
    message: str
    severity: str = "warning"


class AlertResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: Optional[str] = None
    alert_type: str
    message: str
    severity: str
    is_read: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
