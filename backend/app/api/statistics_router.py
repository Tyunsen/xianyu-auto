from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.database import get_db
from app.api.statistics import StatisticsResponse, DashboardResponse
from app.models import (
    Account, Product, Card, Order, Message,
    Alert, AccountStatus, ProductStatus, OrderStatus, MessageStatus, AlertStatus
)

router = APIRouter()


@router.get("", response_model=StatisticsResponse)
async def get_statistics(db: Session = Depends(get_db)):
    """获取统计数据"""

    # 账号统计
    total_accounts = db.query(Account).count()
    active_accounts = db.query(Account).filter(
        Account.status == AccountStatus.NORMAL.value,
        Account.is_active == True
    ).count()

    # 商品统计
    total_products = db.query(Product).count()
    on_shelf_products = db.query(Product).filter(
        Product.status == ProductStatus.ON_SHELF.value
    ).count()

    # 卡密统计
    total_cards = db.query(Card).count()
    unused_cards = db.query(Card).filter(Card.status == "unused").count()

    # 订单统计
    total_orders = db.query(Order).count()
    pending_orders = db.query(Order).filter(Order.status == OrderStatus.PENDING.value).count()
    completed_orders = db.query(Order).filter(Order.status == OrderStatus.COMPLETED.value).count()

    # 营收统计
    total_revenue = db.query(func.sum(Order.price)).filter(
        Order.status.in_([OrderStatus.PAID.value, OrderStatus.SHIPPED.value, OrderStatus.COMPLETED.value])
    ).scalar() or 0

    # 今日订单
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_orders = db.query(Order).filter(Order.created_at >= today_start).count()
    today_revenue = db.query(func.sum(Order.price)).filter(
        Order.created_at >= today_start,
        Order.status.in_([OrderStatus.PAID.value, OrderStatus.SHIPPED.value, OrderStatus.COMPLETED.value])
    ).scalar() or 0

    # 未读消息
    unread_messages = db.query(Message).filter(Message.status == MessageStatus.UNREAD.value).count()

    # 待处理告警
    pending_alerts = db.query(Alert).filter(Alert.status == AlertStatus.PENDING.value).count()

    return StatisticsResponse(
        total_accounts=total_accounts,
        active_accounts=active_accounts,
        total_products=total_products,
        on_shelf_products=on_shelf_products,
        total_cards=total_cards,
        unused_cards=unused_cards,
        total_orders=total_orders,
        pending_orders=pending_orders,
        completed_orders=completed_orders,
        total_revenue=total_revenue,
        today_orders=today_orders,
        today_revenue=today_revenue,
        unread_messages=unread_messages,
        pending_alerts=pending_alerts
    )


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(db: Session = Depends(get_db)):
    """获取仪表盘数据"""

    # 获取统计数据
    stats_response = await get_statistics(db)

    # 最近订单
    recent_orders = db.query(Order).order_by(Order.created_at.desc()).limit(10).all()
    recent_orders_data = []
    for order in recent_orders:
        product = db.query(Product).filter(Product.id == order.product_id).first()
        recent_orders_data.append({
            "id": order.id,
            "product_title": product.title if product else "未知商品",
            "price": order.price,
            "status": order.status,
            "created_at": order.created_at.isoformat() if order.created_at else None
        })

    # 最近告警
    recent_alerts = db.query(Alert).filter(
        Alert.status == AlertStatus.PENDING.value
    ).order_by(Alert.created_at.desc()).limit(5).all()

    return DashboardResponse(
        statistics=stats_response,
        recent_orders=recent_orders_data,
        recent_alerts=[{
            "id": a.id,
            "type": a.type,
            "title": a.title,
            "content": a.content,
            "created_at": a.created_at.isoformat() if a.created_at else None
        } for a in recent_alerts]
    )


@router.get("/chart/orders")
async def get_order_chart(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db)
):
    """获取订单趋势数据"""
    start_date = datetime.now() - timedelta(days=days)

    # 按日期分组统计
    orders = db.query(
        func.date(Order.created_at).label('date'),
        func.count(Order.id).label('count'),
        func.sum(Order.price).label('revenue')
    ).filter(
        Order.created_at >= start_date
    ).group_by(func.date(Order.created_at)).all()

    return {
        "days": days,
        "data": [
            {
                "date": str(o.date),
                "count": o.count,
                "revenue": o.revenue or 0
            } for o in orders
        ]
    }
