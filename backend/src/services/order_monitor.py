"""
订单监控服务
"""
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from src.models.order import Order, OrderStatus
from src.models.account import Account


class OrderMonitor:
    """订单监控服务"""

    def __init__(self, db: Session):
        self.db = db

    async def check_pending_orders(self) -> dict:
        """
        检查待处理订单

        Returns:
            检查结果统计
        """
        # TODO: 使用 Playwright 检查闲鱼订单
        # 1. 登录每个账号
        # 2. 访问订单页面
        # 3. 检查是否有新订单
        # 4. 同步到本地数据库

        return {
            "checked_accounts": 0,
            "new_orders": 0,
            "updated_orders": 0
        }

    async def check_paid_orders(self) -> List[Order]:
        """
        检查已支付订单（待发货）

        Returns:
            待发货订单列表
        """
        return self.db.query(Order).filter(
            Order.status == OrderStatus.PAID.value
        ).all()

    async def auto_ship_pending_orders(self) -> dict:
        """
        自动发货待处理订单

        Returns:
            发货结果统计
        """
        from src.services.order_service import OrderService

        service = OrderService(self.db)
        pending_orders = await self.check_paid_orders()

        success_count = 0
        failed_count = 0

        for order in pending_orders:
            result = service.ship_order(order.id)
            if result:
                success_count += 1
            else:
                failed_count += 1
                service.create_ship_failed_alert(order.id, "自动发货失败")

        return {
            "total": len(pending_orders),
            "success": success_count,
            "failed": failed_count
        }

    def get_orders_by_account(self, account_id: int) -> List[Order]:
        """获取账号的订单列表"""
        return self.db.query(Order).filter(
            Order.account_id == account_id
        ).order_by(Order.created_at.desc()).all()

    def get_recent_orders(self, hours: int = 24) -> List[Order]:
        """获取最近一段时间的订单"""
        since = datetime.now() - timedelta(hours=hours)
        return self.db.query(Order).filter(
            Order.created_at >= since
        ).order_by(Order.created_at.desc()).all()
