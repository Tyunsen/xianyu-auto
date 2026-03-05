from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class AlertStatus(str, enum.Enum):
    PENDING = "pending"    # 待处理
    HANDLED = "handled"    # 已处理
    IGNORED = "ignored"    # 已忽略


class AlertType(str, enum.Enum):
    LOGIN_EXPIRED = "login_expired"    # 登录过期
    ORDER_FAILED = "order_failed"      # 订单失败
    DELIVERY_FAILED = "delivery_failed"  # 发货失败
    STOCK_LOW = "stock_low"           # 库存不足
    SYSTEM_ERROR = "system_error"      # 系统错误


class Alert(Base):
    """告警模型"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False, comment="告警类型")
    title = Column(String(200), nullable=False, comment="告警标题")
    content = Column(Text, nullable=False, comment="告警内容")
    account_id = Column(Integer, nullable=True, comment="关联账号ID")
    order_id = Column(Integer, nullable=True, comment="关联订单ID")
    status = Column(String(20), default=AlertStatus.PENDING.value, comment="状态")
    handled_at = Column(DateTime, nullable=True, comment="处理时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    def __repr__(self):
        return f"<Alert {self.id}: {self.type}>"
