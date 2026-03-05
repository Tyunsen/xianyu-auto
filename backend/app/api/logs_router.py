from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.api.logs import LogResponse, LogListResponse
from app.services.log_service import LogService

router = APIRouter()


@router.get("", response_model=LogListResponse)
async def list_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    level: Optional[str] = None,
    type: Optional[str] = None,
    account_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取日志列表"""
    service = LogService(db)
    return service.list_logs(page, page_size, level, type, account_id)


@router.post("")
async def create_log(
    level: str,
    type: str,
    message: str,
    account_id: Optional[int] = None,
    order_id: Optional[int] = None,
    extra: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """创建日志"""
    service = LogService(db)
    return service.create_log(level, type, message, account_id, order_id, extra)
