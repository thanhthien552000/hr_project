from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DepartmentResponse(BaseModel):
    id: int
    department_name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
