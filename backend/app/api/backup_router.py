"""
备份导出API
"""
import json
import csv
import io
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.models import Product, Card, Order, Account

router = APIRouter()


@router.get("/products")
async def export_products(
    format: str = Query("json", regex="^(json|csv)$"),
    db: Session = Depends(get_db)
):
    """导出商品数据"""
    products = db.query(Product).all()

    if format == "json":
        data = []
        for p in products:
            data.append({
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "price": p.price,
                "original_price": p.original_price,
                "stock": p.stock,
                "status": p.status,
                "created_at": p.created_at.isoformat() if p.created_at else None
            })

        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        return StreamingResponse(
            io.BytesIO(json_str.encode('utf-8')),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=products_{datetime.now().strftime('%Y%m%d')}.json"}
        )

    else:  # csv
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "标题", "描述", "价格", "原价", "库存", "状态", "创建时间"])

        for p in products:
            writer.writerow([
                p.id,
                p.title,
                p.description or "",
                p.price,
                p.original_price or "",
                p.stock,
                p.status,
                p.created_at.strftime('%Y-%m-%d %H:%M:%S') if p.created_at else ""
            ])

        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=products_{datetime.now().strftime('%Y%m%d')}.csv"}
        )


@router.get("/cards")
async def export_cards(
    format: str = Query("json", regex="^(json|csv)$"),
    db: Session = Depends(get_db)
):
    """导出卡密数据"""
    cards = db.query(Card).all()

    if format == "json":
        data = []
        for c in cards:
            data.append({
                "id": c.id,
                "product_id": c.product_id,
                "card_key": c.card_key,
                "card_type": c.card_type,
                "face_value": c.face_value,
                "status": c.status,
                "used_at": c.used_at.isoformat() if c.used_at else None,
                "created_at": c.created_at.isoformat() if c.created_at else None
            })

        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        return StreamingResponse(
            io.BytesIO(json_str.encode('utf-8')),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=cards_{datetime.now().strftime('%Y%m%d')}.json"}
        )

    else:  # csv
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "商品ID", "卡密", "类型", "面值", "状态", "使用时间", "创建时间"])

        for c in cards:
            writer.writerow([
                c.id,
                c.product_id,
                c.card_key,
                c.card_type or "",
                c.face_value or "",
                c.status,
                c.used_at.strftime('%Y-%m-%d %H:%M:%S') if c.used_at else "",
                c.created_at.strftime('%Y-%m-%d %H:%M:%S') if c.created_at else ""
            ])

        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=cards_{datetime.now().strftime('%Y%m%d')}.csv"}
        )


@router.get("/orders")
async def export_orders(
    format: str = Query("json", regex="^(json|csv)$"),
    db: Session = Depends(get_db)
):
    """导出订单数据"""
    orders = db.query(Order).all()

    if format == "json":
        data = []
        for o in orders:
            product = db.query(Product).filter(Product.id == o.product_id).first()
            data.append({
                "id": o.id,
                "product_title": product.title if product else "",
                "buyer_nick": o.buyer_nick,
                "price": o.price,
                "status": o.status,
                "delivery_status": o.delivery_status,
                "created_at": o.created_at.isoformat() if o.created_at else None,
                "paid_at": o.paid_at.isoformat() if o.paid_at else None,
                "shipped_at": o.shipped_at.isoformat() if o.shipped_at else None
            })

        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        return StreamingResponse(
            io.BytesIO(json_str.encode('utf-8')),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=orders_{datetime.now().strftime('%Y%m%d')}.json"}
        )

    else:  # csv
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["订单ID", "商品", "买家", "金额", "状态", "发货状态", "下单时间", "付款时间", "发货时间"])

        for o in orders:
            product = db.query(Product).filter(Product.id == o.product_id).first()
            writer.writerow([
                o.id,
                product.title if product else "",
                o.buyer_nick or "",
                o.price,
                o.status,
                o.delivery_status,
                o.created_at.strftime('%Y-%m-%d %H:%M:%S') if o.created_at else "",
                o.paid_at.strftime('%Y-%m-%d %H:%M:%S') if o.paid_at else "",
                o.shipped_at.strftime('%Y-%m-%d %H:%M:%S') if o.shipped_at else ""
            ])

        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=orders_{datetime.now().strftime('%Y%m%d')}.csv"}
        )


@router.get("/accounts")
async def export_accounts(
    db: Session = Depends(get_db)
):
    """导出账号数据（不含敏感cookie）"""
    accounts = db.query(Account).all()

    data = []
    for a in accounts:
        data.append({
            "id": a.id,
            "name": a.name,
            "status": a.status,
            "is_active": a.is_active,
            "last_login": a.last_login.isoformat() if a.last_login else None,
            "last_active": a.last_active.isoformat() if a.last_active else None,
            "created_at": a.created_at.isoformat() if a.created_at else None
        })

    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    return StreamingResponse(
        io.BytesIO(json_str.encode('utf-8')),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=accounts_{datetime.now().strftime('%Y%m%d')}.json"}
    )


@router.get("/all")
async def export_all(
    db: Session = Depends(get_db)
):
    """导出所有数据（JSON格式）"""
    # 商品
    products = db.query(Product).all()
    products_data = []
    for p in products:
        products_data.append({
            "id": p.id, "title": p.title, "price": p.price,
            "stock": p.stock, "status": p.status,
            "created_at": p.created_at.isoformat() if p.created_at else None
        })

    # 卡密
    cards = db.query(Card).all()
    cards_data = []
    for c in cards:
        cards_data.append({
            "id": c.id, "product_id": c.product_id,
            "status": c.status, "used_at": c.used_at.isoformat() if c.used_at else None
        })

    # 订单
    orders = db.query(Order).all()
    orders_data = []
    for o in orders:
        orders_data.append({
            "id": o.id, "product_id": o.product_id,
            "price": o.price, "status": o.status,
            "created_at": o.created_at.isoformat() if o.created_at else None
        })

    # 账号
    accounts = db.query(Account).all()
    accounts_data = []
    for a in accounts:
        accounts_data.append({
            "id": a.id, "name": a.name, "status": a.status,
            "is_active": a.is_active
        })

    export_data = {
        "export_time": datetime.now().isoformat(),
        "products": products_data,
        "cards": cards_data,
        "orders": orders_data,
        "accounts": accounts_data
    }

    json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
    return StreamingResponse(
        io.BytesIO(json_str.encode('utf-8')),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=xianyu_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"}
    )
