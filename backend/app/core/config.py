from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    """
    Quản lý toàn bộ cấu hình ứng dụng.
    Giá trị được đọc từ file .env hoặc biến môi trường hệ thống.
    Nếu không tìm thấy → dùng giá trị mặc định bên dưới.
    """

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/hr_db"
    DATABASE_URL_SYNC: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/hr_db"

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

    @property
    def cors_origins_list(self) -> List[str]:
        """Chuyển chuỗi JSON thành list Python."""
        return json.loads(self.CORS_ORIGINS)

    model_config = {"env_file": ".env", "extra": "ignore"}


# Tạo instance duy nhất — import ở bất kỳ đâu đều dùng chung 1 object
settings = Settings()
