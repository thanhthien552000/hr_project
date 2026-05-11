from datetime import date, datetime
from sqlalchemy import Integer, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import PayrollBase


class Attendance(PayrollBase):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    work_days: Mapped[int] = mapped_column(Integer, nullable=False)
    absent_days: Mapped[int] = mapped_column(Integer, default=0)
    leave_days: Mapped[int] = mapped_column(Integer, default=0)
    late_days: Mapped[int] = mapped_column(Integer, default=0)
    attendance_month: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
