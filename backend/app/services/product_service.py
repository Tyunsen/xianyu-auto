from sqlalchemy.orm import Session
from typing import Optional, List
import json
from datetime import datetime
from app.models import Product, ProductStatus


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def list_products(
        self,
        page: int = 1,
        page_size: int = 20,
        account_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> dict:
        """获取商品列表"""
        query = self.db.query(Product)

        if account_id:
            query = query.filter(Product.account_id == account_id)
        if status:
            query = query.filter(Product.status == status)

        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()

        return {
            "total": total,
            "items": [self._to_response(item) for item in items]
        }

    def get_product(self, product_id: int) -> Optional[Product]:
        """获取商品详情"""
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create_product(self, data) -> Product:
        """创建商品"""
        product = Product(
            account_id=data.account_id,
            title=data.title,
            description=data.description,
            price=data.price,
            original_price=data.original_price,
            images=json.dumps(data.images) if data.images else None,
            category=data.category,
            tags=data.tags,
            stock=data.stock,
            auto_publish=data.auto_publish,
            auto_offline=data.auto_offline,
            status=ProductStatus.DRAFT.value
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def batch_create_products(self, products_data: List) -> dict:
        """批量创建商品"""
        products = []
        for data in products_data:
            product = Product(
                account_id=data.account_id,
                title=data.title,
                description=data.description,
                price=data.price,
                original_price=data.original_price,
                images=json.dumps(data.images) if data.images else None,
                category=data.category,
                tags=data.tags,
                stock=data.stock,
                auto_publish=data.auto_publish,
                auto_offline=data.auto_offline,
                status=ProductStatus.DRAFT.value
            )
            products.append(product)

        self.db.add_all(products)
        self.db.commit()
        return {"created": len(products)}

    def update_product(self, product_id: int, data) -> Optional[Product]:
        """更新商品"""
        product = self.get_product(product_id)
        if not product:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if 'images' in update_data and update_data['images']:
            update_data['images'] = json.dumps(update_data['images'])

        for key, value in update_data.items():
            setattr(product, key, value)

        product.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: int) -> bool:
        """删除商品"""
        product = self.get_product(product_id)
        if not product:
            return False
        self.db.delete(product)
        self.db.commit()
        return True

    def publish_product(self, product_id: int) -> dict:
        """上架商品"""
        product = self.get_product(product_id)
        if not product:
            return {"success": False, "message": "商品不存在"}

        # TODO: 调用Playwright发布商品
        product.status = ProductStatus.ON_SHELF.value
        self.db.commit()
        return {"success": True, "message": "商品已上架"}

    def unpublish_product(self, product_id: int) -> dict:
        """下架商品"""
        product = self.get_product(product_id)
        if not product:
            return {"success": False, "message": "商品不存在"}

        product.status = ProductStatus.OFF_SHELF.value
        self.db.commit()
        return {"success": True, "message": "商品已下架"}

    def get_products_need_publish(self) -> List[Product]:
        """获取需要自动上架的商品"""
        return self.db.query(Product).filter(
            Product.stock > 0,
            Product.auto_publish == True,
            Product.status.in_([ProductStatus.DRAFT.value, ProductStatus.OFF_SHELF.value, ProductStatus.SOLD_OUT.value])
        ).all()

    def get_products_need_offline(self) -> List[Product]:
        """获取需要自动下架的商品"""
        return self.db.query(Product).filter(
            Product.stock == 0,
            Product.auto_offline == True,
            Product.status == ProductStatus.ON_SHELF.value
        ).all()

    def decrease_stock(self, product_id: int, quantity: int = 1) -> bool:
        """扣减库存"""
        product = self.get_product(product_id)
        if not product or product.stock < quantity:
            return False
        product.stock -= quantity
        if product.stock == 0:
            product.status = ProductStatus.SOLD_OUT.value
        self.db.commit()
        return True

    def increase_stock(self, product_id: int, quantity: int = 1) -> bool:
        """增加库存"""
        product = self.get_product(product_id)
        if not product:
            return False
        product.stock += quantity
        if product.stock > 0 and product.status == ProductStatus.SOLD_OUT.value:
            product.status = ProductStatus.DRAFT.value
        self.db.commit()
        return True

    def _to_response(self, product: Product) -> dict:
        return {
            **Product.model_validate(product).model_dump(),
            "images": json.loads(product.images) if product.images else []
        }
