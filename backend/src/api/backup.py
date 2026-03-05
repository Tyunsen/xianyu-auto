"""
数据备份导出 API
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import StringIO
import csv
import json

from src.database import get_db
from src.models.product import Product
from src.models.card_key import CardKey
from src.models.order import Order
from src.models.settings import Setting

router = APIRouter(prefix="/api/backup", tags=["备份导出"])


@router.get("/export/{data_type}")
async def export_data(
    data_type: str,
    format: str = Query("csv", enum=["csv", "json"]),
    db: Session = Depends(get_db)
):
    """
    导出数据

    Args:
        data_type: 数据类型 (products, card_keys, orders, settings)
        format: 导出格式 (csv, json)
    """
    if data_type == "products":
        items = db.query(Product).all()
        data = [{
            "id": p.id,
            "title": p.title,
            "price": str(p.price),
            "status": p.status,
            "xianyu_id": p.xianyu_id,
            "created_at": p.created_at.isoformat() if p.created_at else ""
        } for p in items]

    elif data_type == "card_keys":
        items = db.query(CardKey).all()
        data = [{
            "id": c.id,
            "key": c.key,
            "product_id": c.product_id,
            "status": c.status,
            "used_at": c.used_at.isoformat() if c.used_at else "",
            "created_at": c.created_at.isoformat() if c.created_at else ""
        } for c in items]

    elif data_type == "orders":
        items = db.query(Order).all()
        data = [{
            "id": o.id,
            "account_id": o.account_id,
            "product_id": o.product_id,
            "buyer_nickname": o.buyer_nickname,
            "status": o.status,
            "amount": str(o.amount),
            "created_at": o.created_at.isoformat() if o.created_at else ""
        } for o in items]

    elif data_type == "settings":
        items = db.query(Setting).all()
        data = [{
            "key": s.key,
            "value": s.value,
            "description": s.description
        } for s in items]

    else:
        return {"error": "不支持的数据类型"}

    if format == "json":
        return StreamingResponse(
            iter([json.dumps(data, ensure_ascii=False, indent=2)]),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={data_type}.json"}
        )

    # CSV 格式
    if not data:
        return {"error": "没有数据"}

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={data_type}.csv"}
    )
