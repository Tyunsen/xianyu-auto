"""
运行日志模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from src.database import Base
import enum


class LogLevel(str, enum.Enum):
    """日志级别枚举"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class LogCategory(str, enum.Enum):
    """日志分类枚举"""
    TASK = "task"
    MESSAGE = "message"
    SHIP = "ship"
    SYSTEM = "system"
    ACCOUNT = "account"


class Log(Base):
    """运行日志表"""
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False, comment="日志级别")
    category = Column(String(50), nullable=False, comment="日志分类")
    content = Column(Text, nullable=False, comment="日志内容")
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True, comment="关联账号ID")
    created_at = Column(DateTime, server_default=func.now(), index=True, comment="创建时间")
