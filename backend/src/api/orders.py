"""
订单管理 API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime

from src.database import get_db
from src.models.order import Order, OrderStatus
from src.schemas.order import OrderResponse, OrderCreate, OrderUpdate

router = APIRouter(prefix="/api/orders", tags=["订单管理"])


@router.get("", response_model=dict)
def list_orders(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    account_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取订单列表"""
    query = db.query(Order)

    if status:
        query = query.filter(Order.status == status)
    if account_id:
        query = query.filter(Order.account_id == account_id)

    total = query.count()
    items = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    return {"items": items, "total": total}


@router.post("", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """创建订单"""
    db_order = Order(
        account_id=order.account_id,
        product_id=order.product_id,
        buyer_nickname=order.buyer_nickname,
        amount=order.amount,
        xianyu_order_id=order.xianyu_order_id,
        status=OrderStatus.PENDING.value
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """获取单个订单"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    """更新订单"""
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="订单不存在")

    update_data = order.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return db_order


@router.post("/{order_id}/ship")
def ship_order(order_id: int, db: Session = Depends(get_db)):
    """手动发货"""
    from src.services.order_service import OrderService

    service = OrderService(db)
    result = service.ship_order(order_id)

    if not result:
        raise HTTPException(status_code=400, detail="发货失败")

    return {"status": "shipped", "message": "发货成功"}


@router.post("/{order_id}/confirm")
def confirm_shipment(order_id: int, db: Session = Depends(get_db)):
    """确认发货"""
    from src.services.order_service import OrderService

    service = OrderService(db)
    result = service.confirm_shipment(order_id)

    if not result:
        raise HTTPException(status_code=400, detail="确认失败")

    return {"status": "confirmed", "message": "确认发货成功"}


@router.post("/{order_id}/complete")
def complete_order(order_id: int, db: Session = Depends(get_db)):
    """完成订单"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    order.status = OrderStatus.COMPLETED.value
    order.completed_at = func.now()
    db.commit()

    return {"status": "completed", "message": "订单已完成"}
