from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.api.cards import (
    CardCreate,
    CardUpdate,
    CardBatchCreate,
    CardResponse,
    CardListResponse
)
from app.services.card_service import CardService

router = APIRouter()


@router.get("", response_model=CardListResponse)
async def list_cards(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    product_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取卡密列表"""
    service = CardService(db)
    return service.list_cards(page, page_size, product_id, status)


@router.get("/{card_id}", response_model=CardResponse)
async def get_card(card_id: int, db: Session = Depends(get_db)):
    """获取卡密详情"""
    service = CardService(db)
    card = service.get_card(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="卡密不存在")
    return card


@router.post("", response_model=CardResponse)
async def create_card(card: CardCreate, db: Session = Depends(get_db)):
    """添加卡密"""
    service = CardService(db)
    return service.create_card(card)


@router.post("/batch")
async def batch_create_cards(cards: CardBatchCreate, db: Session = Depends(get_db)):
    """批量添加卡密"""
    service = CardService(db)
    return service.batch_create_cards(cards)


@router.put("/{card_id}", response_model=CardResponse)
async def update_card(
    card_id: int,
    card: CardUpdate,
    db: Session = Depends(get_db)
):
    """更新卡密"""
    service = CardService(db)
    updated = service.update_card(card_id, card)
    if not updated:
        raise HTTPException(status_code=404, detail="卡密不存在")
    return updated


@router.delete("/{card_id}")
async def delete_card(card_id: int, db: Session = Depends(get_db)):
    """删除卡密"""
    service = CardService(db)
    success = service.delete_card(card_id)
    if not success:
        raise HTTPException(status_code=404, detail="卡密不存在")
    return {"message": "删除成功"}


@router.get("/product/{product_id}/random")
async def get_random_card(product_id: int, db: Session = Depends(get_db)):
    """随机获取一个可用卡密"""
    service = CardService(db)
    card = service.get_random_unused_card(product_id)
    if not card:
        raise HTTPException(status_code=404, detail="没有可用卡密")
    return card
