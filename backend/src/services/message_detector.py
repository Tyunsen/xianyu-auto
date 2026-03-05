"""
消息检测服务
"""
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from src.models.message import Message
from src.models.account import Account
from src.services.message_service import MessageService


class MessageDetector:
    """消息检测服务"""

    def __init__(self, db: Session):
        self.db = db
        self.service = MessageService(db)

    async def check_new_messages(self, account_id: int) -> dict:
        """
        检查新消息

        Args:
            account_id: 账号 ID

        Returns:
            检查结果
        """
        # TODO: 使用 Playwright 检查闲鱼新消息
        # 1. 加载账号 cookies
        # 2. 访问消息页面
        # 3. 抓取新消息
        # 4. 保存到数据库

        # 暂时返回模拟结果
        return {
            "account_id": account_id,
            "new_messages": 0,
            "checked_at": datetime.now()
        }

    async def check_all_accounts(self) -> dict:
        """检查所有账号的新消息"""
        accounts = self.db.query(Account).filter(
            Account.status == "online"
        ).all()

        total_new = 0

        for account in accounts:
            result = await self.check_new_messages(account.id)
            total_new += result.get("new_messages", 0)

        return {
            "checked_accounts": len(accounts),
            "total_new_messages": total_new
        }

    async def auto_reply_new_messages(self, product_info: str = None) -> dict:
        """
        自动回复所有未回复的消息

        Args:
            product_info: 商品信息

        Returns:
            回复结果统计
        """
        accounts = self.db.query(Account).filter(
            Account.status == "online"
        ).all()

        success_count = 0
        failed_count = 0
        skipped_count = 0

        for account in accounts:
            # 获取未读消息
            unread_messages = self.service.get_unread_messages(account.id)

            for message in unread_messages:
                # 检查是否在黑名单
                if self.service.is_blacklisted(message.from_user):
                    skipped_count += 1
                    self.service.mark_as_read(message.id)
                    continue

                # 自动回复
                result = self.service.auto_reply(message.id, product_info)
                if result:
                    success_count += 1
                else:
                    failed_count += 1

        return {
            "total": success_count + failed_count + skipped_count,
            "success": success_count,
            "failed": failed_count,
            "skipped": skipped_count
        }

    def get_unread_count(self, account_id: int) -> int:
        """获取未读消息数量"""
        return self.db.query(Message).filter(
            Message.account_id == account_id,
            Message.is_read == False
        ).count()

    def get_conversation_count(self, account_id: int) -> int:
        """获取对话数量（去重）"""
        from sqlalchemy import func
        return self.db.query(
            func.count(func.distinct(Message.from_user))
        ).filter(
            Message.account_id == account_id
        ).scalar()
