from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    应用配置
    """
    # 项目信息
    PROJECT_NAME: str = "FastAPI Template"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "FastAPI 项目模板"
    API_V1_STR: str = "/api/v1"
    
    # CORS配置
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # 数据库配置
    # MySQL 配置（默认）
    # DATABASE_URL: str = "mysql://user:password@localhost/fastapi_demo"
    # PostgreSQL 配置：
    # DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    # SQLite 配置（开发和测试）：
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # JWT配置
    SECRET_KEY: str = "aB3$kL9#xZ7!qW2@eR5^tY8*uI1&pO4X"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 环境配置
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
