from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

VALID_ALERT_TYPES = ["absence", "late", "salary", "contract", "other"]
VALID_SEVERITIES = ["low", "warning", "high"]


class AlertBase(BaseModel):
    employee_id: int
    alert_type: str
    message: str
    severity: str = "warning"

    @field_validator("employee_id")
    @classmethod
    def validate_employee_id(cls, v):
        if v <= 0:
            raise ValueError("Employee ID phải là số dương")
        return v

    @field_validator("alert_type")
    @classmethod
    def validate_alert_type(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Loại cảnh báo không được để trống")
        return v

    @field_validator("message")
    @classmethod
    def validate_message(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Nội dung cảnh báo không được để trống")
        if len(v) > 500:
            raise ValueError("Nội dung cảnh báo không được quá 500 ký tự")
        return v

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, v):
        if v not in VALID_SEVERITIES:
            raise ValueError(f"Mức độ phải là một trong: {', '.join(VALID_SEVERITIES)}")
        return v


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
