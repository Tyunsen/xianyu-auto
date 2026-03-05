"""
商品管理 API
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import json
import csv
import io

from src.database import get_db
from src.models.product import Product, ProductStatus
from src.schemas.product import ProductResponse, ProductCreate, ProductUpdate

router = APIRouter(prefix="/api/products", tags=["商品管理"])


@router.get("", response_model=dict)
def list_products(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取商品列表"""
    query = db.query(Product)

    if status:
        query = query.filter(Product.status == status)
    if search:
        query = query.filter(Product.title.contains(search))

    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return {"items": items, "total": total}


@router.post("", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """创建商品"""
    db_product = Product(
        title=product.title,
        price=product.price,
        description=product.description,
        images=product.images,
        status=ProductStatus.DRAFT.value,
        account_id=product.account_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """获取单个商品"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """更新商品"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="商品不存在")

    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """删除商品"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="商品不存在")

    db.delete(db_product)
    db.commit()
    return {"message": "商品已删除"}


@router.post("/import")
async def import_products(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """批量导入商品（支持 CSV）"""
    content = await file.read()

    # 解析 CSV
    reader = csv.DictReader(io.StringIO(content.decode('utf-8')))
    imported = 0
    failed = 0
    errors = []

    for row in reader:
        try:
            product = Product(
                title=row.get('title', ''),
                price=float(row.get('price', 0)),
                description=row.get('description', ''),
                images=row.get('images', ''),
                status=ProductStatus.DRAFT.value
            )
            db.add(product)
            imported += 1
        except Exception as e:
            failed += 1
            errors.append(f"行 {imported + failed}: {str(e)}")

    db.commit()
    return {
        "imported": imported,
        "failed": failed,
        "errors": errors[:10]  # 最多返回10个错误
    }


@router.post("/{product_id}/publish")
async def publish_product(product_id: int, db: Session = Depends(get_db)):
    """上架商品到闲鱼"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    if not product.account_id:
        raise HTTPException(status_code=400, detail="商品未关联账号")

    # TODO: 使用 Playwright 发布到闲鱼
    # 1. 加载账号 cookies
    # 2. 访问发布页面
    # 3. 填写商品信息
    # 4. 发布并获取 xianyu_id

    # 暂时模拟发布成功
    product.status = ProductStatus.PUBLISHED.value
    product.xianyu_id = f"xy{product.id}"
    db.commit()

    return {
        "status": "published",
        "xianyu_id": product.xianyu_id,
        "message": "商品上架成功（模拟）"
    }


@router.post("/{product_id}/unpublish")
async def unpublish_product(product_id: int, db: Session = Depends(get_db)):
    """下架商品"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    # TODO: 使用 Playwright 下架商品
    product.status = ProductStatus.OFFLINE.value
    db.commit()

    return {"status": "offline", "message": "商品下架成功（模拟）"}
