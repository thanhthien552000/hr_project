from datetime import date, datetime
from sqlalchemy import Integer, String, DateTime, func, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20),nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hire_date: Mapped[date] = mapped_column(Date, nullable=False)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id"), nullable=False, index = True)
    position_id: Mapped[int] =mapped_column(Integer, ForeignKey("positions.id"), nullable=False, index =True)
    status: Mapped[str] = mapped_column(String(50), nullable=True, default="Đang làm việc",index = True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    department = relationship("Department", back_populates="employees")
    position= relationship("Position", back_populates="employees")
    attendance_records = relationship("Attendance", back_populates="employee")
    salaries = relationship("Salary", back_populates="employee")
    dividends = relationship("Dividend", back_populates="employee")
    alerts = relationship("Alert", back_populates="employee")
    
