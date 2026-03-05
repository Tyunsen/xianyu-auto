from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Blacklist(Base):
    """黑名单模型"""
    __tablename__ = "blacklist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, nullable=False, comment="用户ID")
    user_nick = Column(String(100), nullable=True, comment="用户昵称")
    reason = Column(String(500), nullable=True, comment="拉黑原因")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    def __repr__(self):
        return f"<Blacklist {self.id}: {self.user_nick}>"
