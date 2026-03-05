"""
黑名单管理API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.core.database import get_db
from app.models import Blacklist

router = APIRouter()


# Schemas
class BlacklistCreate(BaseModel):
    user_id: str
    user_nick: Optional[str] = None
    reason: Optional[str] = None


class BlacklistResponse(BaseModel):
    id: int
    user_id: str
    user_nick: Optional[str]
    reason: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


class BlacklistListResponse(BaseModel):
    total: int
    items: list[BlacklistResponse]


@router.get("", response_model=BlacklistListResponse)
async def list_blacklist(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取黑名单列表"""
    total = db.query(Blacklist).count()
    items = db.query(Blacklist).order_by(
        Blacklist.created_at.desc()
    ).offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "items": [
            BlacklistResponse(
                id=i.id,
                user_id=i.user_id,
                user_nick=i.user_nick,
                reason=i.reason,
                created_at=i.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ) for i in items
        ]
    }


@router.post("", response_model=BlacklistResponse)
async def add_to_blacklist(
    data: BlacklistCreate,
    db: Session = Depends(get_db)
):
    """添加黑名单"""
    # 检查是否已存在
    existing = db.query(Blacklist).filter(Blacklist.user_id == data.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="该用户已在黑名单中")

    blacklist = Blacklist(
        user_id=data.user_id,
        user_nick=data.user_nick,
        reason=data.reason
    )
    db.add(blacklist)
    db.commit()
    db.refresh(blacklist)

    return BlacklistResponse(
        id=blacklist.id,
        user_id=blacklist.user_id,
        user_nick=blacklist.user_nick,
        reason=blacklist.reason,
        created_at=blacklist.created_at.strftime('%Y-%m-%d %H:%M:%S')
    )


@router.delete("/{user_id}")
async def remove_from_blacklist(user_id: str, db: Session = Depends(get_db)):
    """移除黑名单"""
    blacklist = db.query(Blacklist).filter(Blacklist.user_id == user_id).first()
    if not blacklist:
        raise HTTPException(status_code=404, detail="用户不在黑名单中")

    db.delete(blacklist)
    db.commit()
    return {"message": "移除成功"}


@router.get("/check/{user_id}")
async def check_blacklist(user_id: str, db: Session = Depends(get_db)):
    """检查用户是否在黑名单"""
    exists = db.query(Blacklist).filter(Blacklist.user_id == user_id).first() is not None
    return {"in_blacklist": exists}
