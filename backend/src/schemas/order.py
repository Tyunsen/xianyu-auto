"""
订单 Schema
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal


class OrderBase(BaseModel):
    """订单基础字段"""
    account_id: int
    product_id: int
    buyer_nickname: str
    amount: Decimal


class OrderCreate(OrderBase):
    """创建订单请求"""
    xianyu_order_id: Optional[str] = None


class OrderUpdate(BaseModel):
    """更新订单请求"""
    status: Optional[str] = None
    card_key_id: Optional[int] = None


class OrderResponse(OrderBase):
    """订单响应"""
    id: int
    xianyu_order_id: Optional[str] = None
    status: str
    card_key_id: Optional[int] = None
    created_at: datetime
    paid_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
