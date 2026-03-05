from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Card(Base):
    """卡密模型"""
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="所属商品")
    card_key = Column(String(500), nullable=False, comment="卡密内容")
    card_type = Column(String(50), nullable=True, comment="卡密类型")
    face_value = Column(String(100), nullable=True, comment="面值")
    status = Column(String(20), default="unused", comment="状态: unused/used/expired")
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True, comment="使用订单ID")
    used_at = Column(DateTime, nullable=True, comment="使用时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    def __repr__(self):
        return f"<Card {self.id}: {self.card_key[:20]}...>"
