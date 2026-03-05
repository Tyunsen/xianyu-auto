from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderResponse(BaseModel):
    id: int
    account_id: int
    product_id: int
    xianyu_order_id: Optional[str] = None
    buyer_id: Optional[str] = None
    buyer_nick: Optional[str] = None
    price: int
    status: str
    card_id: Optional[int] = None
    delivery_content: Optional[str] = None
    delivery_status: str
    paid_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    total: int
    items: list[OrderResponse]
