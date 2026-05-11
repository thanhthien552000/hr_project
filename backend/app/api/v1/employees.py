from typing import Optional
from io import BytesIO

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_human_db
from app.services.employee import EmployeeService
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.common.pagination import PaginationParams
from app.common.response import success_response, paginated_response

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("")
async def list_employees(
    pagination: PaginationParams = Depends(),
    search: Optional[str] = Query(None),
    department_id: Optional[int] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    sort_by: str = Query("id"),
    sort_order: str = Query("asc"),
    db: AsyncSession = Depends(get_human_db),
):
    service = EmployeeService(db)
    items, total = await service.get_list(
        offset=pagination.offset, limit=pagination.page_size,
        search=search, department_id=department_id,
        status=status_filter, sort_by=sort_by, sort_order=sort_order,
    )
    return paginated_response(items, total, pagination.page, pagination.page_size)


@router.get("/export/pdf")
async def export_employees_pdf(
    department_id: Optional[int] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_human_db),
):
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    import os

    service = EmployeeService(db)
    items, _ = await service.get_list(
        offset=0, limit=10000,
        department_id=department_id, status=status_filter,
    )

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Register Vietnamese-compatible font
    font_path = "C:/Windows/Fonts/arial.ttf"
    font_bold_path = "C:/Windows/Fonts/arialbd.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont("ArialUnicode", font_path))
        if os.path.exists(font_bold_path):
            pdfmetrics.registerFont(TTFont("ArialUnicode-Bold", font_bold_path))
        else:
            pdfmetrics.registerFont(TTFont("ArialUnicode-Bold", font_path))
    else:
        pdfmetrics.registerFont(TTFont("ArialUnicode", "DejaVuSans.ttf"))
        pdfmetrics.registerFont(TTFont("ArialUnicode-Bold", "DejaVuSans-Bold.ttf"))

    styles = getSampleStyleSheet()
    styles["Title"].fontName = "ArialUnicode-Bold"
    styles["Normal"].fontName = "ArialUnicode"

    elements = []
    elements.append(Paragraph("Danh sách nhân viên", styles["Title"]))

    from reportlab.platypus import Spacer
    elements.append(Spacer(1, 12))

    data = [["ID", "Họ tên", "Phòng ban", "Chức vụ", "Trạng thái", "Email", "SĐT"]]
    for emp in items:
        data.append([
            str(emp["id"]),
            emp["full_name"],
            emp.get("department_name") or "",
            emp.get("position_name") or "",
            emp.get("status") or "",
            emp.get("email") or "",
            emp.get("phone_number") or "",
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "ArialUnicode-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "ArialUnicode"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=employees.pdf"},
    )


@router.get("/{employee_id}")
async def get_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_human_db),
):
    service = EmployeeService(db)
    employee = await service.get_by_id(employee_id)
    return success_response(data=employee)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_employee(
    data: EmployeeCreate,
    db: AsyncSession = Depends(get_human_db),
):
    service = EmployeeService(db)
    employee = await service.create(data)
    return success_response(data=employee, message="Employee created successfully")


@router.put("/{employee_id}")
async def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: AsyncSession = Depends(get_human_db),
):
    service = EmployeeService(db)
    employee = await service.update(employee_id, data)
    return success_response(data=employee, message="Employee updated successfully")


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_human_db),
):
    service = EmployeeService(db)
    result = await service.delete(employee_id)
    return success_response(data=result, message="Employee deleted successfully")
