from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.models import Message, MessageStatus


class MessageService:
    def __init__(self, db: Session):
        self.db = db

    def list_messages(
        self,
        page: int = 1,
        page_size: int = 20,
        account_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> dict:
        """获取消息列表"""
        query = self.db.query(Message)

        if account_id:
            query = query.filter(Message.account_id == account_id)
        if status:
            query = query.filter(Message.status == status)

        total = query.count()
        items = query.order_by(Message.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "total": total,
            "items": [MessageResponse.model_validate(item) for item in items]
        }

    def get_message(self, message_id: int) -> Optional[Message]:
        """获取消息详情"""
        return self.db.query(Message).filter(Message.id == message_id).first()

    def get_unread_messages(self, account_id: int) -> list[Message]:
        """获取未读消息"""
        return self.db.query(Message).filter(
            Message.account_id == account_id,
            Message.status == MessageStatus.UNREAD.value
        ).all()

    def reply_message(self, message_id: int, content: str) -> dict:
        """回复消息"""
        message = self.get_message(message_id)
        if not message:
            return {"success": False, "message": "消息不存在"}

        message.reply_content = content
        message.status = MessageStatus.REPLIED.value
        message.replied_at = datetime.now()
        self.db.commit()
        return {"success": True, "message": "回复成功"}

    def mark_as_read(self, message_id: int) -> bool:
        """标记已读"""
        message = self.get_message(message_id)
        if not message:
            return False
        message.status = MessageStatus.READ.value
        self.db.commit()
        return True


from app.api.messages import MessageResponse
