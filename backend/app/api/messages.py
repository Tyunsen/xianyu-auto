from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageResponse(BaseModel):
    id: int
    account_id: int
    xianyu_message_id: Optional[str] = None
    from_user_id: Optional[str] = None
    from_user_nick: Optional[str] = None
    content: str
    type: str
    product_id: Optional[int] = None
    reply_content: Optional[str] = None
    status: str
    created_at: datetime
    replied_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    total: int
    items: list[MessageResponse]
