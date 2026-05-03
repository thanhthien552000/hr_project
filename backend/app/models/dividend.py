from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Integer, Date, DateTime, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Dividend(Base):
    __tablename__ = "dividends"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    dividend_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    dividend_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    employee = relationship("Employee", back_populates="dividends")
