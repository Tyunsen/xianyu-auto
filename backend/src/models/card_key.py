"""
卡密模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from src.database import Base
import enum


class CardKeyStatus(str, enum.Enum):
    """卡密状态枚举"""
    AVAILABLE = "available"
    USED = "used"
    EXPIRED = "expired"


class CardKey(Base):
    """卡密表"""
    __tablename__ = "card_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(Text, nullable=False, comment="卡密内容")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="所属商品ID")
    status = Column(String(20), default="available", comment="卡密状态")
    used_at = Column(DateTime, nullable=True, comment="使用时间")
    used_order_id = Column(Integer, nullable=True, comment="使用的订单ID")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
