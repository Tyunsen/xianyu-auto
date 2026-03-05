from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class AccountStatus(str, enum.Enum):
    NORMAL = "normal"      # 正常
    LOGIN_EXPIRED = "login_expired"  # 登录过期
    DISABLED = "disabled"  # 已禁用
    ERROR = "error"        # 异常


class Account(Base):
    """咸鱼账号模型"""
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="账号名称/备注")
    cookie = Column(Text, nullable=False, comment="登录Cookie")
    user_agent = Column(String(500), default="", comment="User-Agent")
    status = Column(String(20), default=AccountStatus.NORMAL.value, comment="账号状态")
    last_login = Column(DateTime, nullable=True, comment="最后登录时间")
    last_active = Column(DateTime, nullable=True, comment="最后活跃时间")
    error_message = Column(String(500), nullable=True, comment="错误信息")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<Account {self.id}: {self.name}>"
