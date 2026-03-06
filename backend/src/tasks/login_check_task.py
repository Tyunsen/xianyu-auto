"""
登录状态检测定时任务
"""
import asyncio
import logging
from typing import List
from datetime import datetime

from src.database import SessionLocal
from src.models.account import Account, AccountStatus
from src.services.account_service import AccountService
from src.utils.email_helper import send_login_expired_notification

logger = logging.getLogger(__name__)


async def check_all_accounts_login_status():
    """
    检测所有账号的登录状态
    这是一个定时任务，每6小时执行一次
    """
    logger.info("开始检测账号登录状态...")

    db = SessionLocal()
    try:
        service = AccountService(db)

        # 获取所有账号
        accounts = db.query(Account).all()

        results = []
        for account in accounts:
            # 只检查有cookies的账号
            if not account.cookies:
                logger.info(f"账号 {account.nickname} (ID: {account.id}) 没有登录凭证，跳过检测")
                continue

            # 使用Playwright检测登录状态
            try:
                from src.utils.playwright_helper import get_playwright_helper

                helper = get_playwright_helper()
                await helper.initialize()

                # 获取解密后的cookies
                cookies = service.get_decrypted_cookies(account.id)
                if not cookies:
                    continue

                # 检查登录状态
                status_result = await helper.check_login_status(cookies)

                old_status = account.status
                new_status = status_result.get("status", "unknown")

                if new_status == "online":
                    # 账号在线
                    account.status = "online"
                    logger.info(f"账号 {account.nickname} 登录状态: 在线")
                elif new_status == "expired":
                    # 登录已过期
                    account.status = "expired"
                    logger.warning(f"账号 {account.nickname} 登录已过期")

                    # 发送邮件通知
                    await send_login_expired_notification(account.nickname, account.id)
                else:
                    # 未知状态
                    account.status = "error"
                    logger.warning(f"账号 {account.nickname} 登录状态未知: {status_result.get('message')}")

                # 记录状态变更
                if old_status != account.status:
                    logger.info(f"账号 {account.nickname} 状态变更: {old_status} -> {account.status}")

                results.append({
                    "account_id": account.id,
                    "nickname": account.nickname,
                    "old_status": old_status,
                    "new_status": new_status,
                    "message": status_result.get("message", "")
                })

            except Exception as e:
                logger.error(f"检测账号 {account.nickname} 登录状态失败: {e}")
                account.status = "error"

        db.commit()
        logger.info(f"登录状态检测完成，共检测 {len(accounts)} 个账号")

        return results

    except Exception as e:
        logger.error(f"登录状态检测任务执行失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def run_login_check_task():
    """同步包装函数，用于APScheduler"""
    try:
        asyncio.run(check_all_accounts_login_status())
    except Exception as e:
        logger.error(f"登录状态检测任务失败: {e}")


if __name__ == "__main__":
    # 可以直接运行此脚本进行测试
    logging.basicConfig(level=logging.INFO)
    run_login_check_task()
