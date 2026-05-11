from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


# ── Human DB (SQL Server) ─────────────────────────────────────────────
human_engine = create_async_engine(
    settings.HUMAN_DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)
HumanSessionLocal = async_sessionmaker(
    bind=human_engine, expire_on_commit=False, class_=AsyncSession
)


# ── Payroll DB (MySQL) ────────────────────────────────────────────────
payroll_engine = create_async_engine(
    settings.PAYROLL_DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)
PayrollSessionLocal = async_sessionmaker(
    bind=payroll_engine, expire_on_commit=False, class_=AsyncSession
)


# ── Declarative Bases ─────────────────────────────────────────────────
class HumanBase(DeclarativeBase):
    """Base class for all Human DB models (SQL Server)."""
    pass


class PayrollBase(DeclarativeBase):
    """Base class for all Payroll DB models (MySQL)."""
    pass


# ── Session generators ────────────────────────────────────────────────
async def get_human_db():
    async with HumanSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_payroll_db():
    async with PayrollSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise