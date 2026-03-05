"""
商品 Schema
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal


class ProductBase(BaseModel):
    """商品基础字段"""
    title: str
    price: Decimal = Decimal("0.00")
    description: Optional[str] = None
    images: Optional[str] = None


class ProductCreate(ProductBase):
    """创建商品请求"""
    account_id: Optional[int] = None


class ProductUpdate(BaseModel):
    """更新商品请求"""
    title: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    images: Optional[str] = None
    status: Optional[str] = None
    account_id: Optional[int] = None


class ProductResponse(ProductBase):
    """商品响应"""
    id: int
    status: str
    xianyu_id: Optional[str] = None
    account_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
