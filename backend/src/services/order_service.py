"""
订单服务
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from src.models.order import Order, OrderStatus
from src.models.card_key import CardKey, CardKeyStatus
from src.models.alert import Alert, AlertType


class OrderService:
    """订单服务"""

    def __init__(self, db: Session):
        self.db = db

    def get_pending_orders(self) -> List[Order]:
        """获取待发货订单"""
        return self.db.query(Order).filter(
            Order.status == OrderStatus.PAID.value
        ).all()

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """获取订单"""
        return self.db.query(Order).filter(Order.id == order_id).first()

    def allocate_card_key(self, order_id: int) -> Optional[CardKey]:
        """为订单分配卡密"""
        order = self.get_order_by_id(order_id)
        if not order:
            return None

        # 查找可用卡密
        card_key = self.db.query(CardKey).filter(
            CardKey.product_id == order.product_id,
            CardKey.status == CardKeyStatus.AVAILABLE.value
        ).first()

        if not card_key:
            # 创建低库存告警
            self.create_low_stock_alert(order.product_id)
            return None

        # 更新卡密状态
        card_key.status = CardKeyStatus.USED.value
        card_key.used_order_id = order_id
        card_key.used_at = func.now()

        # 更新订单
        order.card_key_id = card_key.id

        self.db.commit()
        return card_key

    def ship_order(self, order_id: int) -> bool:
        """发货"""
        order = self.get_order_by_id(order_id)
        if not order:
            return False

        # 分配卡密
        card_key = self.allocate_card_key(order_id)
        if not card_key:
            return False

        # TODO: 发送消息给买家
        # 使用 Playwright 发送消息

        # 更新订单状态
        order.status = OrderStatus.SHIPPED.value
        order.shipped_at = func.now()
        self.db.commit()

        return True

    def confirm_shipment(self, order_id: int) -> bool:
        """确认发货（点击确认发货按钮）"""
        order = self.get_order_by_id(order_id)
        if not order:
            return False

        # TODO: 使用 Playwright 确认发货
        # 1. 登录闲鱼
        # 2. 访问订单页面
        # 3. 点击确认发货

        order.status = OrderStatus.SHIPPED.value
        self.db.commit()
        return True

    def direct_ship(self, order_id: int) -> bool:
        """免拼发货（跳过拼单直接发货）"""
        order = self.get_order_by_id(order_id)
        if not order:
            return False

        # TODO: 使用 Playwright 跳过拼单
        return self.ship_order(order_id)

    def create_low_stock_alert(self, product_id: int) -> Alert:
        """创建低库存告警"""
        alert = Alert(
            type=AlertType.LOW_STOCK.value,
            content=f"商品 ID {product_id} 卡密库存不足",
        )
        self.db.add(alert)
        self.db.commit()
        return alert

    def create_ship_failed_alert(self, order_id: int, reason: str) -> Alert:
        """创建发货失败告警"""
        alert = Alert(
            type=AlertType.SHIP_FAILED.value,
            content=f"订单 {order_id} 发货失败: {reason}",
        )
        self.db.add(alert)
        self.db.commit()
        return alert
