from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Admin(Base):
    """管理员账号模型"""
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码(加密)")
    nickname = Column(String(100), nullable=True, comment="昵称")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    last_login = Column(DateTime, nullable=True, comment="最后登录时间")

    def __repr__(self):
        return f"<Admin {self.username}>"
