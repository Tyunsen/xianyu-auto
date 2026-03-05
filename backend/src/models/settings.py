"""
系统配置模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from src.database import Base


class Setting(Base):
    """系统配置表"""
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True, comment="配置键")
    value = Column(Text, nullable=True, comment="配置值")
    description = Column(String(255), nullable=True, comment="配置描述")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
