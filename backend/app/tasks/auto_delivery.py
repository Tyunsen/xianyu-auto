"""
自动发货任务
"""
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Order, OrderStatus, Card
from app.services.order_service import OrderService
from app.services.card_service import CardService
from app.services.product_service import ProductService
from app.services.log_service import LogService
from app.services.alert_service import AlertService
from app.services.playwright_client import browser_pool
from app.tasks.scheduler import task


@task("auto_delivery")
async def auto_delivery_task(db: Session):
    """自动发货任务"""
    log_service = LogService(db)
    order_service = OrderService(db)
    card_service = CardService(db)
    product_service = ProductService(db)

    # 获取待发货订单
    pending_orders = order_service.get_pending_orders()

    if not pending_orders:
        return

    log_service.info("auto_delivery", f"开始处理 {len(pending_orders)} 个待发货订单")

    for order in pending_orders:
        try:
            # 获取商品信息
            product = product_service.get_product(order.product_id)
            if not product:
                log_service.warning("auto_delivery", f"订单 {order.id} 商品不存在")
                continue

            # 获取卡密
            card = card_service.get_random_unused_card(product.id)
            if not card:
                # 库存不足，创建告警
                alert_service = AlertService(db)
                alert_service.create_alert(
                    type="stock_low",
                    title="卡密库存不足",
                    content=f"商品 {product.title} 卡密库存为0",
                    account_id=order.account_id,
                    order_id=order.id
                )
                log_service.warning("auto_delivery", f"商品 {product.id} 库存不足")
                continue

            # 获取账号信息
            from app.models import Account
            account = db.query(Account).filter(Account.id == order.account_id).first()

            # 自动发货
            async with browser_pool.get_browser(account.id, account.cookie, account.user_agent) as browser:
                # 发送卡密给买家
                success = await browser.send_message(
                    order.buyer_id,
                    f"您好，您的订单已收到，卡密如下：\n\n{card.card_key}\n\n请妥善保管，使用后即失效。如有问题随时联系。"
                )

                if success:
                    # 标记卡密已使用
                    card_service.mark_card_used(card.id, order.id)

                    # 扣减库存
                    product_service.decrease_stock(product.id, 1)

                    # 标记订单已发货
                    order_service.deliver_order(order.id)

                    log_service.info("auto_delivery", f"订单 {order.id} 发货成功，卡密 {card.id}")
                else:
                    log_service.error("auto_delivery", f"订单 {order.id} 发货失败")

        except Exception as e:
            log_service.error("auto_delivery", f"处理订单 {order.id} 异常: {e}")


@task("auto_confirm_delivery")
async def auto_confirm_delivery_task(db: Session):
    """自动确认发货任务（针对已付款但未点击发货的订单）"""
    log_service = LogService(db)

    # TODO: 实现自动确认发货逻辑
    # 需要通过浏览器模拟点击"确认发货"按钮
    pass


@task("auto_no拼单发货")
async def auto_no拼单发货_task(db: Session):
    """自动免拼发货任务"""
    log_service = LogService(db)

    # TODO: 实现免拼发货逻辑
    # 闲鱼有"免拼单"功能，可以直接发货
    pass
