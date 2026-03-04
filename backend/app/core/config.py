from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # 数据库
    database_url: str = "mysql+pymysql://xianyu:xianyu123@mysql:3306/xianyu"

    # Redis
    redis_url: str = "redis://redis:6379/0"

    # 应用
    secret_key: str = "xianyu-secret-key-change-in-production"
    debug: bool = False

    # Claude Code
    claude_api_key: str = ""

    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache()
def get_settings():
    return Settings()
