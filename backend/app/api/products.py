from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============ Schemas ============

class ProductBase(BaseModel):
    title: str = Field(..., description="商品标题")
    description: Optional[str] = None
    price: int = Field(..., description="价格(分)")
    original_price: Optional[int] = None
    images: Optional[List[str]] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    stock: int = 0
    auto_publish: bool = True
    auto_offline: bool = False


class ProductCreate(ProductBase):
    account_id: Optional[int] = None


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    original_price: Optional[int] = None
    images: Optional[List[str]] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    stock: Optional[int] = None
    auto_publish: Optional[bool] = None
    auto_offline: Optional[bool] = None
    status: Optional[str] = None


class ProductResponse(ProductBase):
    id: int
    account_id: Optional[int] = None
    xianyu_id: Optional[str] = None
    xianyu_url: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    total: int
    items: list[ProductResponse]
