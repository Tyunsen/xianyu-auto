"""
告警模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from src.database import Base
import enum


class AlertType(str, enum.Enum):
    """告警类型枚举"""
    LOGIN_EXPIRED = "login_expired"
    SHIP_FAILED = "ship_failed"
    LOW_STOCK = "low_stock"
    SYSTEM_ERROR = "system_error"
    MESSAGE_FAILED = "message_failed"
    ACCOUNT_ERROR = "account_error"


class Alert(Base):
    """告警表"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False, comment="告警类型")
    content = Column(Text, nullable=False, comment="告警内容")
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True, comment="关联账号ID")
    is_resolved = Column(Boolean, default=False, comment="是否已解决")
    resolved_at = Column(DateTime, nullable=True, comment="解决时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
