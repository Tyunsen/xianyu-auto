from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.api.messages import MessageResponse, MessageListResponse
from app.services.message_service import MessageService

router = APIRouter()


@router.get("", response_model=MessageListResponse)
async def list_messages(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    account_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取消息列表"""
    service = MessageService(db)
    return service.list_messages(page, page_size, account_id, status)


@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(message_id: int, db: Session = Depends(get_db)):
    """获取消息详情"""
    service = MessageService(db)
    return service.get_message(message_id)


@router.post("/{message_id}/reply")
async def reply_message(
    message_id: int,
    content: str,
    db: Session = Depends(get_db)
):
    """回复消息"""
    service = MessageService(db)
    return service.reply_message(message_id, content)
