"""
消息模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from src.database import Base


class Message(Base):
    """消息表"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, comment="账号ID")
    xianyu_message_id = Column(String(100), nullable=True, comment="闲鱼消息ID")
    from_user = Column(String(100), nullable=False, comment="发送者")
    to_user = Column(String(100), nullable=False, comment="接收者")
    content = Column(Text, nullable=False, comment="消息内容")
    is_read = Column(Boolean, default=False, comment="是否已读")
    reply_content = Column(Text, nullable=True, comment="回复内容")
    is_auto_reply = Column(Boolean, default=False, comment="是否自动回复")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
