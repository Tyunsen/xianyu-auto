from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models import Card
from app.api.cards import CardCreate, CardUpdate


from app.api.cards import CardResponse

class CardService:
    def __init__(self, db: Session):
        self.db = db

    def list_cards(
        self,
        page: int = 1,
        page_size: int = 20,
        product_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> dict:
        """获取卡密列表"""
        query = self.db.query(Card)

        if product_id:
            query = query.filter(Card.product_id == product_id)
        if status:
            query = query.filter(Card.status == status)

        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()

        return {
            "total": total,
            "items": [CardResponse.model_validate(item) for item in items]
        }

    def get_card(self, card_id: int) -> Optional[Card]:
        """获取卡密详情"""
        return self.db.query(Card).filter(Card.id == card_id).first()

    def create_card(self, data: CardCreate) -> Card:
        """创建卡密"""
        card = Card(
            product_id=data.product_id,
            card_key=data.card_key,
            card_type=data.card_type,
            face_value=data.face_value,
            status="unused"
        )
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def batch_create_cards(self, data) -> dict:
        """批量创建卡密"""
        cards = []
        for card_key in data.cards:
            card = Card(
                product_id=data.product_id,
                card_key=card_key,
                card_type=data.card_type,
                face_value=data.face_value,
                status="unused"
            )
            cards.append(card)

        self.db.add_all(cards)
        self.db.commit()
        return {"created": len(cards)}

    def update_card(self, card_id: int, data: CardUpdate) -> Optional[Card]:
        """更新卡密"""
        card = self.get_card(card_id)
        if not card:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(card, key, value)

        self.db.commit()
        self.db.refresh(card)
        return card

    def delete_card(self, card_id: int) -> bool:
        """删除卡密"""
        card = self.get_card(card_id)
        if not card:
            return False
        self.db.delete(card)
        self.db.commit()
        return True

    def get_random_unused_card(self, product_id: int) -> Optional[Card]:
        """随机获取一个未使用的卡密"""
        return self.db.query(Card).filter(
            Card.product_id == product_id,
            Card.status == "unused"
        ).first()

    def mark_card_used(self, card_id: int, order_id: int) -> bool:
        """标记卡密已使用"""
        card = self.get_card(card_id)
        if not card:
            return False
        card.status = "used"
        card.order_id = order_id
        card.used_at = datetime.now()
        self.db.commit()
        return True

    def get_product_stock(self, product_id: int) -> int:
        """获取商品卡密库存"""
        return self.db.query(Card).filter(
            Card.product_id == product_id,
            Card.status == "unused"
        ).count()
