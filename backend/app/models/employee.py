from datetime import date, datetime
from sqlalchemy import Integer, String, Unicode, DateTime, func, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import HumanBase

class Employee(HumanBase):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(Unicode(10), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hire_date: Mapped[date] = mapped_column(Date, nullable=False)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    position_id: Mapped[int] = mapped_column(Integer, ForeignKey("positions.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(Unicode(50), nullable=True, default="Đang làm việc", index=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships within Human DB only
    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")
    dividends = relationship("Dividend", back_populates="employee")
    
