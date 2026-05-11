from datetime import datetime
from sqlalchemy import Integer, Unicode, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.database import HumanBase

class Position(HumanBase):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    position_name: Mapped[str] = mapped_column(Unicode(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    employees = relationship("Employee", back_populates="position")
