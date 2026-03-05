from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class LogLevel(str, enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class LogType(str, enum.Enum):
    SYSTEM = "system"
    ACCOUNT = "account"
    ORDER = "order"
    MESSAGE = "message"
    TASK = "task"
    ERROR = "error"


class Log(Base):
    """日志模型"""
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), default=LogLevel.INFO.value, comment="日志级别")
    type = Column(String(20), default=LogType.SYSTEM.value, comment="日志类型")
    message = Column(Text, nullable=False, comment="日志内容")
    account_id = Column(Integer, nullable=True, comment="关联账号ID")
    order_id = Column(Integer, nullable=True, comment="关联订单ID")
    extra = Column(Text, nullable=True, comment="额外信息(JSON)")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    def __repr__(self):
        return f"<Log {self.id}: {self.level} - {self.message[:30]}>"
