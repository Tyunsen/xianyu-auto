"""
配置管理
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""

    # 数据库
    database_url: str = "postgresql://xianyu:xianyu123@localhost:5432/xianyu_auto"

    # 应用
    secret_key: str = "your-secret-key-change-in-production"
    debug: bool = True

    # MiniMax AI API
    minimax_api_key: str = ""
    minimax_model: str = "abab6.5s"

    # 邮件
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""

    # 前端
    api_base_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
