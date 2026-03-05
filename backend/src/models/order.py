"""
订单模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from src.database import Base
import enum


class OrderStatus(str, enum.Enum):
    """订单状态枚举"""
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Order(Base):
    """订单表"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, comment="账号ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="商品ID")
    xianyu_order_id = Column(String(100), nullable=True, comment="闲鱼订单ID")
    buyer_nickname = Column(String(100), nullable=False, comment="买家昵称")
    status = Column(String(20), default="pending", comment="订单状态")
    card_key_id = Column(Integer, nullable=True, comment="卡密ID")
    amount = Column(Numeric(10, 2), nullable=False, comment="订单金额")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    paid_at = Column(DateTime, nullable=True, comment="支付时间")
    shipped_at = Column(DateTime, nullable=True, comment="发货时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")
