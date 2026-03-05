"""
卡密 Schema
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CardKeyBase(BaseModel):
    """卡密基础字段"""
    key: str
    product_id: int


class CardKeyCreate(CardKeyBase):
    """创建卡密请求"""
    pass


class CardKeyUpdate(BaseModel):
    """更新卡密请求"""
    status: Optional[str] = None


class CardKeyResponse(CardKeyBase):
    """卡密响应"""
    id: int
    status: str
    used_at: Optional[datetime] = None
    used_order_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CardKeyStats(BaseModel):
    """卡密统计"""
    total: int
    available: int
    used: int
