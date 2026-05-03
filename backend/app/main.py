from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.common.exceptions import AppException, app_exception_handler, generic_exception_handler
from app.api.v1 import (
    alerts,
    attendance,
    dashboard,
    departments,
    employees,
    payroll,
    positions,
    status,
)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include routers
prefix = settings.API_V1_PREFIX
app.include_router(dashboard.router, prefix=prefix)
app.include_router(employees.router, prefix=prefix)
app.include_router(payroll.router, prefix=prefix)
app.include_router(attendance.router, prefix=prefix)
app.include_router(status.router, prefix=prefix)
app.include_router(alerts.router, prefix=prefix)
app.include_router(departments.router, prefix=prefix)
app.include_router(positions.router, prefix=prefix)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
