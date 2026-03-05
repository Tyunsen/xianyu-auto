"""
定时任务调度器
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TaskScheduler:
    """定时任务调度器"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self._setup_jobs()

    def _setup_jobs(self):
        """设置定时任务"""
        # 自动擦亮任务 - 中午 12:00
        self.scheduler.add_job(
            self.auto_refresh,
            CronTrigger(hour=12, minute=0),
            id="auto_refresh",
            name="自动擦亮",
            replace_existing=True
        )

        # 自动签到任务 - 中午 12:30
        self.scheduler.add_job(
            self.auto_sign_in,
            CronTrigger(hour=12, minute=30),
            id="auto_sign_in",
            name="自动签到",
            replace_existing=True
        )

        # 订单检查任务 - 每 5 分钟
        self.scheduler.add_job(
            self.check_orders,
            "interval",
            minutes=5,
            id="check_orders",
            name="订单检查",
            replace_existing=True
        )

        # 消息检查任务 - 每 30 分钟
        self.scheduler.add_job(
            self.check_messages,
            "interval",
            minutes=30,
            id="check_messages",
            name="消息检查",
            replace_existing=True
        )

        # 登录状态检查 - 每小时
        self.scheduler.add_job(
            self.check_account_status,
            "interval",
            hours=1,
            id="check_account_status",
            name="账号状态检查",
            replace_existing=True
        )

    async def auto_refresh(self):
        """自动擦亮商品"""
        from src.database import SessionLocal
        from src.models.product import Product, ProductStatus

        db = SessionLocal()
        try:
            # 获取所有已发布的商品
            products = db.query(Product).filter(
                Product.status == ProductStatus.PUBLISHED.value
            ).all()

            for product in products:
                # TODO: 使用 Playwright 擦亮商品
                logger.info(f"擦亮商品: {product.title}")

                # 记录日志
                from src.services.log_service import log_task
                log_task(
                    db=db,
                    category="task",
                    level="info",
                    content=f"自动擦亮商品: {product.title}",
                    account_id=product.account_id
                )
        finally:
            db.close()

    async def auto_sign_in(self):
        """自动签到"""
        from src.database import SessionLocal
        from src.models.account import Account

        db = SessionLocal()
        try:
            # 获取所有在线账号
            accounts = db.query(Account).filter(
                Account.status == "online"
            ).all()

            for account in accounts:
                # TODO: 使用 Playwright 签到
                logger.info(f"账号签到: {account.nickname}")

                # 记录日志
                from src.services.log_service import log_task
                log_task(
                    db=db,
                    category="task",
                    level="info",
                    content=f"自动签到: {account.nickname}",
                    account_id=account.id
                )
        finally:
            db.close()

    async def check_orders(self):
        """检查订单"""
        from src.database import SessionLocal
        from src.services.order_monitor import OrderMonitor

        db = SessionLocal()
        try:
            monitor = OrderMonitor(db)
            result = await monitor.auto_ship_pending_orders()

            logger.info(f"订单检查完成: {result}")

            # 记录日志
            from src.services.log_service import log_task
            log_task(
                db=db,
                category="task",
                level="info",
                content=f"订单检查: 处理 {result.get('total', 0)} 个订单"
            )
        finally:
            db.close()

    async def check_messages(self):
        """检查消息"""
        from src.database import SessionLocal
        from src.services.message_detector import MessageDetector

        db = SessionLocal()
        try:
            detector = MessageDetector(db)
            result = await detector.check_all_accounts()

            logger.info(f"消息检查完成: {result}")

            # 如果有新消息，进行自动回复
            if result.get("total_new_messages", 0) > 0:
                await detector.auto_reply_new_messages()

            # 记录日志
            from src.services.log_service import log_task
            log_task(
                db=db,
                category="task",
                level="info",
                content=f"消息检查: 发现 {result.get('total_new_messages', 0)} 条新消息"
            )
        finally:
            db.close()

    async def check_account_status(self):
        """检查账号状态"""
        from src.database import SessionLocal
        from src.models.account import Account
        from src.services.account_service import AccountService

        db = SessionLocal()
        try:
            service = AccountService(db)
            accounts = db.query(Account).filter(
                Account.status == "online"
            ).all()

            for account in accounts:
                status = service.check_login_status(account.id)
                if status.get("status") == "expired":
                    service.create_expired_alert(account, "登录状态过期")
                    logger.warning(f"账号登录失效: {account.nickname}")

            # 记录日志
            from src.services.log_service import log_task
            log_task(
                db=db,
                category="task",
                level="info",
                content=f"账号状态检查: 检查了 {len(accounts)} 个账号"
            )
        finally:
            db.close()

    def start(self):
        """启动调度器"""
        self.scheduler.start()
        logger.info("定时任务调度器已启动")

    def shutdown(self):
        """关闭调度器"""
        self.scheduler.shutdown()
        logger.info("定时任务调度器已关闭")

    def get_jobs(self):
        """获取所有任务"""
        return self.scheduler.get_jobs()


# 全局调度器实例
scheduler = None


def get_scheduler() -> TaskScheduler:
    """获取调度器实例"""
    global scheduler
    if scheduler is None:
        scheduler = TaskScheduler()
    return scheduler
