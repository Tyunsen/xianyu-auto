"""
黑名单模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from src.database import Base


class Blacklist(Base):
    """黑名单表"""
    __tablename__ = "blacklist"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(100), unique=True, nullable=False, index=True, comment="用户昵称")
    reason = Column(Text, nullable=True, comment="拉黑原因")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
