from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AlertResponse(BaseModel):
    id: int
    type: str
    title: str
    content: str
    account_id: Optional[int] = None
    order_id: Optional[int] = None
    status: str
    handled_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AlertListResponse(BaseModel):
    total: int
    items: list[AlertResponse]
