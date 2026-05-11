from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import HumanSessionLocal, PayrollSessionLocal
from app.core.security import decode_access_token

security_scheme = HTTPBearer()


async def get_human_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency — yields a session connected to Human DB (SQL Server)."""
    async with HumanSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_payroll_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency — yields a session connected to Payroll DB (MySQL)."""
    async with PayrollSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return {"user_id": int(sub), "email": payload.get("email"), "role": payload.get("role")}
