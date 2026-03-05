from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.models import Order, OrderStatus


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def list_orders(
        self,
        page: int = 1,
        page_size: int = 20,
        account_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> dict:
        """获取订单列表"""
        query = self.db.query(Order)

        if account_id:
            query = query.filter(Order.account_id == account_id)
        if status:
            query = query.filter(Order.status == status)

        total = query.count()
        items = query.order_by(Order.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "total": total,
            "items": [OrderResponse.model_validate(item) for item in items]
        }

    def get_order(self, order_id: int) -> Optional[Order]:
        """获取订单详情"""
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_pending_orders(self) -> list[Order]:
        """获取待发货订单"""
        return self.db.query(Order).filter(
            Order.status == OrderStatus.PAID.value,
            Order.delivery_status == "pending"
        ).all()

    def create_order(self, data: dict) -> Order:
        """创建订单"""
        order = Order(**data)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def deliver_order(self, order_id: int) -> dict:
        """发货"""
        order = self.get_order(order_id)
        if not order:
            return {"success": False, "message": "订单不存在"}

        order.delivery_status = "success"
        order.shipped_at = datetime.now()
        order.status = OrderStatus.SHIPPED.value
        self.db.commit()
        return {"success": True, "message": "发货成功"}

    def mark_paid(self, order_id: int) -> bool:
        """标记已付款"""
        order = self.get_order(order_id)
        if not order:
            return False
        order.status = OrderStatus.PAID.value
        order.paid_at = datetime.now()
        self.db.commit()
        return True


from app.api.orders import OrderResponse
