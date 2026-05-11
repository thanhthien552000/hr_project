from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    """
    Quản lý toàn bộ cấu hình ứng dụng.
    Giá trị được đọc từ file .env hoặc biến môi trường hệ thống.
    Nếu không tìm thấy → dùng giá trị mặc định bên dưới.
    """

    # Human Database (SQL Server - Docker)
    HUMAN_DATABASE_URL: str = "mssql+aioodbc://sa:YourPassword123!@localhost:1433/HumanDB?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    HUMAN_DATABASE_URL_SYNC: str = "mssql+pyodbc://sa:YourPassword123!@localhost:1433/HumanDB?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"

    # Payroll Database (MySQL - Docker)
    PAYROLL_DATABASE_URL: str = "mysql+aiomysql://root:root@localhost:3306/payroll_db?charset=utf8mb4"
    PAYROLL_DATABASE_URL_SYNC: str = "mysql+pymysql://root:root@localhost:3306/payroll_db?charset=utf8mb4"

    # JWT 
    SECRET_KEY: str = "change-this-to-a-random-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # App
    APP_NAME: str = "HR Management System"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: str = '["http://localhost:3000","http://localhost:5173"]'

    # Alert thresholds
    ALERT_ABSENCE_THRESHOLD: int = 5
    ALERT_SALARY_CHANGE_THRESHOLD: int = 20

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"release", "prod", "production"}:
                return False
            if normalized in {"debug", "dev", "development"}:
                return True
        return value

    @property
    def cors_origins_list(self) -> List[str]:
        """Chuyển chuỗi JSON thành list Python."""
        return json.loads(self.CORS_ORIGINS)

    model_config = {"env_file": ".env", "extra": "ignore"}


# Tạo instance duy nhất — import ở bất kỳ đâu đều dùng chung 1 object
settings = Settings()
