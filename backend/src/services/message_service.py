"""
消息服务
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Optional

from src.models.message import Message
from src.models.blacklist import Blacklist
from src.ai.minimax import get_minimax_client


class MessageService:
    """消息服务"""

    def __init__(self, db: Session):
        self.db = db

    def get_unread_messages(self, account_id: int) -> List[Message]:
        """获取未读消息"""
        return self.db.query(Message).filter(
            Message.account_id == account_id,
            Message.is_read == False
        ).order_by(Message.created_at.asc()).all()

    def get_conversation(
        self,
        account_id: int,
        from_user: str,
        limit: int = 50
    ) -> List[Message]:
        """获取与某用户的对话"""
        return self.db.query(Message).filter(
            Message.account_id == account_id,
            Message.from_user == from_user
        ).order_by(Message.created_at.asc()).limit(limit).all()

    def build_conversation_history(
        self,
        account_id: int,
        from_user: str,
        limit: int = 10
    ) -> List[Dict[str, str]]:
        """构建对话历史（用于 AI）"""
        messages = self.get_conversation(account_id, from_user, limit)

        history = []
        for msg in messages:
            role = "assistant" if msg.reply_content else "user"
            content = msg.reply_content if msg.reply_content else msg.content
            history.append({
                "role": role,
                "content": content
            })

        return history

    def is_blacklisted(self, nickname: str) -> bool:
        """检查用户是否在黑名单中"""
        return self.db.query(Blacklist).filter(
            Blacklist.nickname == nickname
        ).first() is not None

    def reply_message(
        self,
        message_id: int,
        content: str,
        is_auto: bool = True
    ) -> bool:
        """回复消息"""
        message = self.db.query(Message).filter(Message.id == message_id).first()
        if not message:
            return False

        # 检查黑名单
        if self.is_blacklisted(message.from_user):
            return False

        # 保存回复内容
        message.reply_content = content
        message.is_auto_reply = is_auto

        # 标记原消息为已读
        message.is_read = True

        self.db.commit()

        # TODO: 使用 Playwright 发送回复到闲鱼

        return True

    def auto_reply(self, message_id: int, product_info: Optional[str] = None) -> bool:
        """自动回复消息（AI）"""
        message = self.db.query(Message).filter(Message.id == message_id).first()
        if not message:
            return False

        # 检查黑名单
        if self.is_blacklisted(message.from_user):
            message.is_read = True
            self.db.commit()
            return False

        # 获取对话历史
        history = self.build_conversation_history(
            message.account_id,
            message.from_user
        )

        # 添加当前消息
        history.append({
            "role": "user",
            "content": message.content
        })

        try:
            # 调用 AI 生成回复
            client = get_minimax_client()
            reply_content = client.generate_customer_service_reply(
                conversation_history=history,
                product_info=product_info
            )

            # 保存回复
            return self.reply_message(message_id, reply_content, is_auto=True)

        except Exception as e:
            print(f"自动回复失败: {e}")
            return False

    def mark_as_read(self, message_id: int) -> bool:
        """标记消息为已读"""
        message = self.db.query(Message).filter(Message.id == message_id).first()
        if not message:
            return False

        message.is_read = True
        self.db.commit()
        return True
