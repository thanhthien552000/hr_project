from typing import Any, Generic, Optional, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class ResponseWrapper(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: str = "Success"


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    data: None = None
    error: ErrorDetail


class PaginatedData(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int


def success_response(data: Any = None, message: str = "Success") -> dict:
    return {"success": True, "data": data, "message": message}


def error_response(code: str, message: str) -> dict:
    return {"success": False, "data": None, "error": {"code": code, "message": message}}


def paginated_response(items: list, total: int, page: int, page_size: int) -> dict:
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    return success_response(
        data={
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }
    )
