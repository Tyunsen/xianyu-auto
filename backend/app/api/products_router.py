from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.models import Product
from app.api.products import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse
)
from app.services.product_service import ProductService

router = APIRouter()


@router.get("", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    account_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取商品列表"""
    service = ProductService(db)
    return service.list_products(page, page_size, account_id, status)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """获取商品详情"""
    service = ProductService(db)
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product


@router.post("", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """添加商品"""
    service = ProductService(db)
    return service.create_product(product)


@router.post("/batch")
async def batch_create_products(
    products: list[ProductCreate],
    db: Session = Depends(get_db)
):
    """批量添加商品"""
    service = ProductService(db)
    return service.batch_create_products(products)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    """更新商品"""
    service = ProductService(db)
    updated = service.update_product(product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="商品不存在")
    return updated


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """删除商品"""
    service = ProductService(db)
    success = service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="商品不存在")
    return {"message": "删除成功"}


@router.post("/{product_id}/publish")
async def publish_product(product_id: int, db: Session = Depends(get_db)):
    """上架商品"""
    service = ProductService(db)
    result = service.publish_product(product_id)
    return result


@router.post("/{product_id}/unpublish")
async def unpublish_product(product_id: int, db: Session = Depends(get_db)):
    """下架商品"""
    service = ProductService(db)
    result = service.unpublish_product(product_id)
    return result
