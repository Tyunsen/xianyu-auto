"""
消息 Schema
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    """消息基础字段"""
    account_id: int
    from_user: str
    to_user: str
    content: str


class MessageCreate(MessageBase):
    """创建消息请求"""
    xianyu_message_id: Optional[str] = None


class MessageUpdate(BaseModel):
    """更新消息请求"""
    is_read: Optional[bool] = None
    reply_content: Optional[str] = None


class MessageResponse(MessageBase):
    """消息响应"""
    id: int
    xianyu_message_id: Optional[str] = None
    is_read: bool
    reply_content: Optional[str] = None
    is_auto_reply: bool
    created_at: datetime

    class Config:
        from_attributes = True
