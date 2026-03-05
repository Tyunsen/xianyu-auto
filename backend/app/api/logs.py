from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LogResponse(BaseModel):
    id: int
    level: str
    type: str
    message: str
    account_id: Optional[int] = None
    order_id: Optional[int] = None
    extra: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LogListResponse(BaseModel):
    total: int
    items: list[LogResponse]
