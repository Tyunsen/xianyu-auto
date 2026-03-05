from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ============ Schemas ============

class CardBase(BaseModel):
    card_key: str = Field(..., description="卡密内容")
    product_id: int = Field(..., description="所属商品ID")
    card_type: Optional[str] = None
    face_value: Optional[str] = None


class CardCreate(CardBase):
    pass


class CardBatchCreate(BaseModel):
    product_id: int
    cards: list[str] = Field(..., description="卡密列表，每行一个")
    card_type: Optional[str] = None
    face_value: Optional[str] = None


class CardUpdate(BaseModel):
    card_key: Optional[str] = None
    card_type: Optional[str] = None
    face_value: Optional[str] = None


class CardResponse(CardBase):
    id: int
    status: str
    order_id: Optional[int] = None
    used_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CardListResponse(BaseModel):
    total: int
    items: list[CardResponse]
