from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Integer, Date, DateTime, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import PayrollBase


class Salary(PayrollBase):
    __tablename__ = "salaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    salary_month: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    base_salary: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    bonus: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    deductions: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    net_salary: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
