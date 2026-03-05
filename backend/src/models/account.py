"""
账号模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from src.database import Base
import enum


class AccountStatus(str, enum.Enum):
    """账号状态枚举"""
    ONLINE = "online"
    OFFLINE = "offline"
    EXPIRED = "expired"
    ERROR = "error"


class Account(Base):
    """账号表"""
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(100), nullable=False, comment="昵称")
    cookies = Column(Text, nullable=False, comment="Cookies (加密存储)")
    status = Column(String(20), default="offline", comment="账号状态")
    last_login = Column(DateTime, nullable=True, comment="最后登录时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
