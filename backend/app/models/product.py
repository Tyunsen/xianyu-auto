from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ProductStatus(str, enum.Enum):
    DRAFT = "draft"        # 草稿
    ON_SHELF = "on_shelf"  # 上架中
    OFF_SHELF = "off_shelf"  # 已下架
    SOLD_OUT = "sold_out"  # 售罄


class Product(Base):
    """商品模型"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True, comment="所属账号")
    title = Column(String(200), nullable=False, comment="商品标题")
    description = Column(Text, nullable=True, comment="商品描述")
    price = Column(Integer, nullable=False, comment="价格(分)")
    original_price = Column(Integer, nullable=True, comment="原价(分)")
    images = Column(Text, nullable=True, comment="图片URL列表(JSON)")
    category = Column(String(50), nullable=True, comment="分类")
    tags = Column(String(200), nullable=True, comment="标签")
    stock = Column(Integer, default=0, comment="库存数量")
    auto_publish = Column(Boolean, default=True, comment="自动上架")
    auto_offline = Column(Boolean, default=False, comment="自动下架")
    xianyu_id = Column(String(100), nullable=True, comment="咸鱼商品ID")
    xianyu_url = Column(String(500), nullable=True, comment="咸鱼商品链接")
    status = Column(String(20), default=ProductStatus.DRAFT.value, comment="状态")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<Product {self.id}: {self.title}>"
