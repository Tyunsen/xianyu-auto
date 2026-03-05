"""
卡密管理 API
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import csv
import io

from src.database import get_db
from src.models.card_key import CardKey, CardKeyStatus
from src.schemas.card_key import CardKeyResponse, CardKeyCreate, CardKeyUpdate, CardKeyStats

router = APIRouter(prefix="/api/card-keys", tags=["卡密管理"])


@router.get("", response_model=dict)
def list_card_keys(
    skip: int = 0,
    limit: int = 100,
    product_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取卡密列表"""
    query = db.query(CardKey)

    if product_id:
        query = query.filter(CardKey.product_id == product_id)
    if status:
        query = query.filter(CardKey.status == status)

    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return {"items": items, "total": total}


@router.post("", response_model=CardKeyResponse)
def create_card_key(card_key: CardKeyCreate, db: Session = Depends(get_db)):
    """创建卡密"""
    db_card_key = CardKey(
        key=card_key.key,
        product_id=card_key.product_id,
        status=CardKeyStatus.AVAILABLE.value
    )
    db.add(db_card_key)
    db.commit()
    db.refresh(db_card_key)
    return db_card_key


@router.delete("/{card_key_id}")
def delete_card_key(card_key_id: int, db: Session = Depends(get_db)):
    """删除卡密"""
    db_card_key = db.query(CardKey).filter(CardKey.id == card_key_id).first()
    if not db_card_key:
        raise HTTPException(status_code=404, detail="卡密不存在")

    # 只有未使用的卡密可以删除
    if db_card_key.status == CardKeyStatus.USED.value:
        raise HTTPException(status_code=400, detail="已使用的卡密无法删除")

    db.delete(db_card_key)
    db.commit()
    return {"message": "卡密已删除"}


@router.get("/stats", response_model=CardKeyStats)
def get_card_key_stats(
    product_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取卡密库存统计"""
    query = db.query(CardKey)

    if product_id:
        query = query.filter(CardKey.product_id == product_id)

    total = query.count()
    available = query.filter(CardKey.status == CardKeyStatus.AVAILABLE.value).count()
    used = total - available

    return CardKeyStats(total=total, available=available, used=used)


@router.post("/import")
async def import_card_keys(
    file: UploadFile = File(...),
    product_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """批量导入卡密"""
    content = await file.read()

    # 解析 CSV（每行一个卡密）
    lines = content.decode('utf-8').strip().split('\n')
    imported = 0
    failed = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        try:
            card_key = CardKey(
                key=line,
                product_id=product_id,
                status=CardKeyStatus.AVAILABLE.value
            )
            db.add(card_key)
            imported += 1
        except Exception:
            failed += 1

    db.commit()
    return {"imported": imported, "failed": failed}


@router.post("/allocate")
def allocate_card_key(product_id: int, order_id: int, db: Session = Depends(get_db)):
    """为订单分配卡密"""
    # 查找一个可用的卡密
    card_key = db.query(CardKey).filter(
        CardKey.product_id == product_id,
        CardKey.status == CardKeyStatus.AVAILABLE.value
    ).first()

    if not card_key:
        raise HTTPException(status_code=400, detail="该商品没有可用的卡密")

    # 更新卡密状态
    card_key.status = CardKeyStatus.USED.value
    card_key.used_order_id = order_id
    card_key.used_at = func.now()

    db.commit()

    return {
        "card_key_id": card_key.id,
        "key": card_key.key
    }
