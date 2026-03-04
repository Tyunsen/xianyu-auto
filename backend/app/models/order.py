from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class OrderStatus(str, enum.Enum):
    PENDING = "pending"        # 待付款
    PAID = "paid"              # 已付款
    SHIPPING = "shipping"      # 发货中
    SHIPPED = "shipped"        # 已发货
    COMPLETED = "completed"    # 已完成
    REFUNDED = "refunded"      # 已退款
    CANCELLED = "cancelled"    # 已取消


class Order(Base):
    """订单模型"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, comment="账号ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="商品ID")
    xianyu_order_id = Column(String(100), nullable=True, comment="咸鱼订单ID")
    buyer_id = Column(String(100), nullable=True, comment="买家ID")
    buyer_nick = Column(String(100), nullable=True, comment="买家昵称")
    price = Column(Integer, nullable=False, comment="金额(分)")
    status = Column(String(20), default=OrderStatus.PENDING.value, comment="订单状态")
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=True, comment="使用卡密ID")
    delivery_content = Column(Text, nullable=True, comment="发货内容")
    delivery_status = Column(String(20), default="pending", comment="发货状态: pending/success/failed")
    paid_at = Column(DateTime, nullable=True, comment="付款时间")
    shipped_at = Column(DateTime, nullable=True, comment="发货时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<Order {self.id}: {self.status}>"
