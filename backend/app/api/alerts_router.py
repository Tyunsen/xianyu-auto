from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.api.alerts import AlertResponse, AlertListResponse
from app.services.alert_service import AlertService

router = APIRouter()


@router.get("", response_model=AlertListResponse)
async def list_alerts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取告警列表"""
    service = AlertService(db)
    return service.list_alerts(page, page_size, status, type)


@router.get("/unhandled-count")
async def get_unhandled_count(db: Session = Depends(get_db)):
    """获取未处理告警数量"""
    service = AlertService(db)
    return {"count": service.get_unhandled_count()}


@router.post("/{alert_id}/handle")
async def handle_alert(alert_id: int, db: Session = Depends(get_db)):
    """处理告警"""
    service = AlertService(db)
    return service.handle_alert(alert_id)


@router.post("/{alert_id}/ignore")
async def ignore_alert(alert_id: int, db: Session = Depends(get_db)):
    """忽略告警"""
    service = AlertService(db)
    return service.ignore_alert(alert_id)
