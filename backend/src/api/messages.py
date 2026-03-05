"""
消息管理 API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from src.database import get_db
from src.models.message import Message
from src.schemas.message import MessageResponse, MessageCreate, MessageUpdate

router = APIRouter(prefix="/api/messages", tags=["消息管理"])


@router.get("", response_model=dict)
def list_messages(
    skip: int = 0,
    limit: int = 100,
    account_id: Optional[int] = None,
    is_read: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """获取消息列表"""
    query = db.query(Message)

    if account_id:
        query = query.filter(Message.account_id == account_id)
    if is_read is not None:
        query = query.filter(Message.is_read == is_read)

    total = query.count()
    items = query.order_by(Message.created_at.desc()).offset(skip).limit(limit).all()

    return {"items": items, "total": total}


@router.get("/conversation", response_model=dict)
def get_conversation(
    account_id: int,
    from_user: str,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """获取与某个用户的对话记录"""
    messages = db.query(Message).filter(
        Message.account_id == account_id,
        Message.from_user == from_user
    ).order_by(Message.created_at.asc()).offset(skip).limit(limit).all()

    return {"items": messages, "total": len(messages)}


@router.post("", response_model=MessageResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    """创建消息"""
    db_message = Message(
        account_id=message.account_id,
        from_user=message.from_user,
        to_user=message.to_user,
        content=message.content,
        xianyu_message_id=message.xianyu_message_id,
        is_read=False,
        is_auto_reply=False
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(message_id: int, db: Session = Depends(get_db)):
    """获取单条消息"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")
    return message


@router.put("/{message_id}", response_model=MessageResponse)
def update_message(message_id: int, message: MessageUpdate, db: Session = Depends(get_db)):
    """更新消息"""
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="消息不存在")

    update_data = message.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_message, key, value)

    db.commit()
    db.refresh(db_message)
    return db_message


@router.post("/{message_id}/reply")
def reply_message(message_id: int, content: str, db: Session = Depends(get_db)):
    """手动回复消息"""
    from src.services.message_service import MessageService

    service = MessageService(db)
    result = service.reply_message(message_id, content, is_auto=False)

    if not result:
        raise HTTPException(status_code=400, detail="回复失败")

    return {"status": "replied", "message": "回复成功"}


@router.post("/{message_id}/mark-read")
def mark_as_read(message_id: int, db: Session = Depends(get_db)):
    """标记消息为已读"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")

    message.is_read = True
    db.commit()

    return {"status": "marked", "message": "已标记为已读"}
