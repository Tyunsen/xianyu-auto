from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.api.orders import OrderResponse, OrderListResponse
from app.services.order_service import OrderService

router = APIRouter()


@router.get("", response_model=OrderListResponse)
async def list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    account_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取订单列表"""
    service = OrderService(db)
    return service.list_orders(page, page_size, account_id, status)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """获取订单详情"""
    service = OrderService(db)
    return service.get_order(order_id)


@router.post("/{order_id}/deliver")
async def deliver_order(order_id: int, db: Session = Depends(get_db)):
    """手动发货"""
    service = OrderService(db)
    return service.deliver_order(order_id)
