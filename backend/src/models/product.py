"""
商品模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.sql import func
from src.database import Base
import enum


class ProductStatus(str, enum.Enum):
    """商品状态枚举"""
    DRAFT = "draft"
    PUBLISHED = "published"
    OFFLINE = "offline"
    DELETED = "deleted"


class Product(Base):
    """商品表"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="商品标题")
    price = Column(Numeric(10, 2), nullable=False, comment="价格")
    description = Column(Text, nullable=True, comment="商品描述")
    images = Column(Text, nullable=True, comment="图片列表 (JSON数组)")
    status = Column(String(20), default="draft", comment="商品状态")
    xianyu_id = Column(String(100), nullable=True, comment="闲鱼商品ID")
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True, comment="所属账号ID")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
