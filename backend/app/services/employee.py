from typing import Optional, Tuple, List
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee
from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.common.exceptions import NotFoundException, AlreadyExistsException


class EmployeeService:
    """Xử lý nghiệp vụ liên quan đến nhân viên."""

    def __init__(self, db: AsyncSession):
        # Tạo Repository — Service không dùng db trực tiếp, chỉ dùng qua repo
        self.repo = EmployeeRepository(db)

    # =============================================
    # 1. LẤY DANH SÁCH (chuyển model → dict response)
    # =============================================
    async def get_list(
        self,
        offset: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        department_id: Optional[int] = None,
        status: Optional[str] = None,
        sort_by: str = "id",
        sort_order: str = "asc",
    ) -> Tuple[List[dict], int]:
        # Gọi repo lấy raw model objects
        employees, total = await self.repo.get_list(
            offset=offset, limit=limit, search=search,
            department_id=department_id, status=status,
            sort_by=sort_by, sort_order=sort_order,
        )
        # Convert mỗi Employee model → dict (dùng helper bên dưới)
        items = [self._to_response(e) for e in employees]
        return items, total

    # =============================================
    # 2. LẤY 1 NHÂN VIÊN — throw 404 nếu không tìm thấy
    # =============================================
    async def get_by_id(self, employee_id: int) -> dict:
        employee = await self.repo.get_by_id(employee_id)
        if not employee:
            # Raise exception → API sẽ tự bắt và trả 404
            raise NotFoundException("Employee", employee_id)
        return self._to_response(employee)

    # =============================================
    # 3. TẠO MỚI — kiểm tra email trùng trước khi tạo
    # =============================================
    async def create(self, data: EmployeeCreate) -> dict:
        # Business rule: email phải unique
        if data.email:
            existing = await self.repo.get_by_email(data.email)
            if existing:
                raise AlreadyExistsException("Employee", "email", data.email)

        # Convert schema (Pydantic) → model (SQLAlchemy)
        # Lưu ý: schema dùng string "YYYY-MM-DD", model dùng date object
        employee = Employee(
            full_name=data.full_name,
            date_of_birth=date.fromisoformat(data.date_of_birth),
            gender=data.gender,
            phone_number=data.phone_number,
            email=data.email,
            hire_date=date.fromisoformat(data.hire_date),
            department_id=data.department_id,
            position_id=data.position_id,
            status=data.status,
        )
        employee = await self.repo.create(employee)
        return self._to_response(employee)

    # =============================================
    # 4. CẬP NHẬT — partial update (chỉ update field được gửi)
    # =============================================
    async def update(self, employee_id: int, data: EmployeeUpdate) -> dict:
        employee = await self.repo.get_by_id(employee_id)
        if not employee:
            raise NotFoundException("Employee", employee_id)

        # exclude_unset=True: chỉ lấy field user thực sự gửi (bỏ field không gửi)
        # → cho phép PATCH/partial update
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            # Convert string date → date object nếu cần
            if field in ("date_of_birth", "hire_date") and value:
                value = date.fromisoformat(value)
            # setattr: gán động property theo tên
            setattr(employee, field, value)

        employee = await self.repo.update(employee)
        return self._to_response(employee)

    # =============================================
    # 5. XOÁ MỀM
    # =============================================
    async def delete(self, employee_id: int) -> dict:
        employee = await self.repo.get_by_id(employee_id)
        if not employee:
            raise NotFoundException("Employee", employee_id)
        await self.repo.soft_delete(employee)
        return {"message": f"Employee {employee_id} deleted successfully"}

    # =============================================
    # 6. LẤY TẤT CẢ NHÂN VIÊN ĐANG LÀM (cho dropdown, báo cáo...)
    # =============================================
    async def get_all_active(self) -> List[dict]:
        employees = await self.repo.get_all_active()
        return [self._to_response(e) for e in employees]

    # =============================================
    # HELPER: Convert Employee model → dict response
    # =============================================
    def _to_response(self, employee: Employee) -> dict:
        # Dùng helper này để tránh lặp code ở mọi method trên
        return {
            "id": employee.id,
            "full_name": employee.full_name,
            "date_of_birth": str(employee.date_of_birth),
            "gender": employee.gender,
            "phone_number": employee.phone_number,
            "email": employee.email,
            "hire_date": str(employee.hire_date),
            "department_id": employee.department_id,
            "position_id": employee.position_id,
            # Lấy tên phòng ban / chức vụ qua relationship (đã eager load ở repo)
            "department_name": employee.department.department_name if employee.department else None,
            "position_name": employee.position.position_name if employee.position else None,
            "status": employee.status,
            "created_at": employee.created_at,
            "updated_at": employee.updated_at,
        }