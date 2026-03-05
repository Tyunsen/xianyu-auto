from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class MessageStatus(str, enum.Enum):
    UNREAD = "unread"      # 未读
    READ = "read"          # 已读
    REPLIED = "replied"    # 已回复
    IGNORED = "ignored"    # 已忽略


class Message(Base):
    """消息模型"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, comment="账号ID")
    xianyu_message_id = Column(String(100), nullable=True, comment="咸鱼消息ID")
    from_user_id = Column(String(100), nullable=True, comment="发送人ID")
    from_user_nick = Column(String(100), nullable=True, comment="发送人昵称")
    content = Column(Text, nullable=False, comment="消息内容")
    type = Column(String(50), default="text", comment="消息类型: text/image")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True, comment="关联商品")
    reply_content = Column(Text, nullable=True, comment="回复内容")
    status = Column(String(20), default=MessageStatus.UNREAD.value, comment="状态")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    replied_at = Column(DateTime, nullable=True, comment="回复时间")

    def __repr__(self):
        return f"<Message {self.id}: {self.content[:30]}...>"
