"""
自动回复任务
"""
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Account, Message, MessageStatus
from app.services.account_service import AccountService
from app.services.message_service import MessageService
from app.services.log_service import LogService
from app.services.claude_client import claude_client
from app.services.playwright_client import browser_pool
from app.tasks.scheduler import task


@task("auto_reply")
async def auto_reply_task(db: Session):
    """自动回复任务"""
    log_service = LogService(db)
    account_service = AccountService(db)
    message_service = MessageService(db)

    # 获取所有正常状态的账号
    accounts = account_service.get_active_accounts()

    if not accounts:
        log_service.info("auto_reply", "没有活跃账号")
        return

    log_service.info("auto_reply", f"开始处理 {len(accounts)} 个账号的消息")

    for account in accounts:
        try:
            await process_account_messages(db, account)
        except Exception as e:
            log_service.error("auto_reply", f"处理账号 {account.id} 消息失败: {e}")


async def process_account_messages(db: Session, account: Account):
    """处理单个账号的消息"""
    message_service = MessageService(db)
    log_service = LogService(db)

    # 获取未读消息
    unread_messages = message_service.get_unread_messages(account.id)

    if not unread_messages:
        return

    log_service.info("auto_reply", f"账号 {account.id} 有 {len(unread_messages)} 条未读消息")

    # 使用浏览器获取最新消息
    try:
        async with browser_pool.get_browser(account.id, account.cookie, account.user_agent) as browser:
            # 获取最新消息列表
            online_messages = await browser.get_messages()

            # 处理每条消息
            for msg_data in online_messages:
                # 检查是否已处理
                existing = db.query(Message).filter(
                    Message.account_id == account.id,
                    Message.xianyu_message_id == msg_data.get("message_id")
                ).first()

                if not existing:
                    # 保存到数据库
                    message = Message(
                        account_id=account.id,
                        xianyu_message_id=msg_data.get("message_id"),
                        from_user_id=msg_data.get("from_user_id"),
                        from_user_nick=msg_data.get("from_user"),
                        content=msg_data.get("content"),
                        type="text",
                        status=MessageStatus.UNREAD.value
                    )
                    db.add(message)
                    db.commit()
                    db.refresh(message)

                    # 生成回复
                    await reply_message(db, message, browser)
                else:
                    # 已存在的消息，检查是否需要回复
                    if existing.status == MessageStatus.UNREAD.value:
                        async with browser_pool.get_browser(account.id, account.cookie, account.user_agent) as br:
                            await reply_message(db, existing, br)

    except Exception as e:
        log_service.error("auto_reply", f"获取消息失败: {e}")


async def reply_message(db: Session, message: Message, browser):
    """回复单条消息"""
    message_service = MessageService(db)
    log_service = LogService(db)

    try:
        # 调用Claude生成回复
        reply_content = await claude_client.generate_reply(
            message=message.content,
            context=None,
            product_info=None
        )

        # 发送回复
        success = await browser.send_message(
            message.from_user_id,
            reply_content
        )

        if success:
            # 更新消息状态
            message_service.reply_message(message.id, reply_content)
            log_service.info("auto_reply", f"回复消息 {message.id} 成功")
        else:
            log_service.warning("auto_reply", f"回复消息 {message.id} 失败")

    except Exception as e:
        log_service.error("auto_reply", f"回复消息 {message.id} 异常: {e}")
