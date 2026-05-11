import re
import unicodedata
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, model_validator

VALID_STATUSES = ["Đang làm việc", "Nghỉ việc", "Nghỉ phép", "Thử việc", "Thực tập"]
VALID_GENDERS = ["Nam", "Nữ"]
STATUS_ALIASES = {
    "Äang lÃ m viá»‡c": "Đang làm việc",
    "Nghá»‰ viá»‡c": "Nghỉ việc",
    "Ngh? vi?c": "Nghỉ việc",
    "Nghá»‰ phÃ©p": "Nghỉ phép",
    "Thá»­ viá»‡c": "Thử việc",
    "Thá»±c táº­p": "Thực tập",
    "dang lam viec": "Đang làm việc",
    "nghi viec": "Nghỉ việc",
    "nghi phep": "Nghỉ phép",
    "thu viec": "Thử việc",
    "thuc tap": "Thực tập",
}
PHONE_REGEX = re.compile(r"^0\d{9}$")
# Allows letters (Vietnamese + Latin), spaces, hyphens, apostrophes
NAME_REGEX = re.compile(r"^[a-zA-ZÀ-ỹà-ỹĐđ\s'\-]+$")


def _fold_vietnamese(value: str) -> str:
    value = unicodedata.normalize("NFD", value)
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    return value.replace("đ", "d").replace("Đ", "D").lower().strip()


STATUS_BY_FOLDED_VALUE = {_fold_vietnamese(status): status for status in VALID_STATUSES}


def _normalize_status(v: Optional[str]) -> Optional[str]:
    if v is None:
        return v
    v = v.strip()
    if not v:
        return None
    if v in VALID_STATUSES:
        return v
    return (
        STATUS_ALIASES.get(v)
        or STATUS_ALIASES.get(v.lower())
        or STATUS_BY_FOLDED_VALUE.get(_fold_vietnamese(v))
        or v
    )


def _validate_date_str(v: str, field_label: str) -> str:
    """Validate date string format YYYY-MM-DD and reasonable range."""
    try:
        parsed = datetime.strptime(v, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise ValueError(f"{field_label} phải đúng định dạng YYYY-MM-DD")
    if parsed.year < 1900 or parsed > date.today():
        raise ValueError(f"{field_label} không hợp lệ")
    return v


def _validate_gmail_email(v: Optional[EmailStr]) -> Optional[EmailStr]:
    if v is None:
        return v
    if not str(v).strip().lower().endswith("@gmail.com"):
        raise ValueError("Email phải dùng đuôi @gmail.com")
    return v


class EmployeeBase(BaseModel):
    full_name: str
    date_of_birth: str
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    hire_date: str
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    status: Optional[str] = "Đang làm việc"

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Họ và tên không được để trống")
        if len(v) < 2:
            raise ValueError("Họ và tên phải có ít nhất 2 ký tự")
        if len(v) > 100:
            raise ValueError("Họ và tên không được quá 100 ký tự")
        if not NAME_REGEX.match(v):
            raise ValueError("Họ và tên chỉ được chứa chữ cái và khoảng trắng")
        return v

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v):
        v = v.strip()
        _validate_date_str(v, "Ngày sinh")
        dob = datetime.strptime(v, "%Y-%m-%d").date()
        age = (date.today() - dob).days // 365
        if age < 16:
            raise ValueError("Nhân viên phải đủ 16 tuổi trở lên")
        if age > 100:
            raise ValueError("Ngày sinh không hợp lệ")
        return v

    @field_validator("hire_date")
    @classmethod
    def validate_hire_date(cls, v):
        v = v.strip()
        _validate_date_str(v, "Ngày vào làm")
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        if v is None or v.strip() == "":
            return v
        v = v.strip()
        if not PHONE_REGEX.match(v):
            raise ValueError("Số điện thoại phải gồm 10 chữ số, bắt đầu bằng 0 (VD: 0912345678)")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return _validate_gmail_email(v)

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v):
        if v is not None and v not in VALID_GENDERS:
            raise ValueError(f"Giới tính phải là một trong: {', '.join(VALID_GENDERS)}")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        v = _normalize_status(v)
        if v is not None and v not in VALID_STATUSES:
            raise ValueError(f"Trạng thái phải là một trong: {', '.join(VALID_STATUSES)}")
        return v

    @field_validator("department_id", "position_id")
    @classmethod
    def validate_positive_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID phải là số dương")
        return v


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    hire_date: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    status: Optional[str] = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Họ và tên không được để trống")
        if len(v) < 2:
            raise ValueError("Họ và tên phải có ít nhất 2 ký tự")
        if len(v) > 100:
            raise ValueError("Họ và tên không được quá 100 ký tự")
        if not NAME_REGEX.match(v):
            raise ValueError("Họ và tên chỉ được chứa chữ cái và khoảng trắng")
        return v

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v):
        if v is None:
            return v
        v = v.strip()
        _validate_date_str(v, "Ngày sinh")
        dob = datetime.strptime(v, "%Y-%m-%d").date()
        age = (date.today() - dob).days // 365
        if age < 16:
            raise ValueError("Nhân viên phải đủ 16 tuổi trở lên")
        if age > 100:
            raise ValueError("Ngày sinh không hợp lệ")
        return v

    @field_validator("hire_date")
    @classmethod
    def validate_hire_date(cls, v):
        if v is None:
            return v
        v = v.strip()
        _validate_date_str(v, "Ngày vào làm")
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        if v is None or v.strip() == "":
            return v
        v = v.strip()
        if not PHONE_REGEX.match(v):
            raise ValueError("Số điện thoại phải gồm 10 chữ số, bắt đầu bằng 0 (VD: 0912345678)")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return _validate_gmail_email(v)

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v):
        if v is not None and v not in VALID_GENDERS:
            raise ValueError(f"Giới tính phải là một trong: {', '.join(VALID_GENDERS)}")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        v = _normalize_status(v)
        if v is not None and v not in VALID_STATUSES:
            raise ValueError(f"Trạng thái phải là một trong: {', '.join(VALID_STATUSES)}")
        return v

    @field_validator("department_id", "position_id")
    @classmethod
    def validate_positive_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("ID phải là số dương")
        return v


class EmployeeResponse(BaseModel):
    id: int
    full_name: str
    date_of_birth: str
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    hire_date: str
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    department_name: Optional[str] = None
    position_name: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
