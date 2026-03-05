"""
系统设置 API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from src.database import get_db
from src.models.settings import Setting

router = APIRouter(prefix="/api/settings", tags=["系统设置"])


@router.get("")
def list_settings(db: Session = Depends(get_db)):
    """获取所有设置"""
    settings = db.query(Setting).all()
    return {"items": [{"key": s.key, "value": s.value, "description": s.description} for s in settings]}


@router.get("/{key}")
def get_setting(key: str, db: Session = Depends(get_db)):
    """获取单个设置"""
    setting = db.query(Setting).filter(Setting.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="设置不存在")
    return {"key": setting.key, "value": setting.value, "description": setting.description}


@router.post("")
def create_setting(key: str, value: str, description: str = "", db: Session = Depends(get_db)):
    """创建/更新设置"""
    setting = db.query(Setting).filter(Setting.key == key).first()
    if setting:
        setting.value = value
        setting.description = description
    else:
        setting = Setting(key=key, value=value, description=description)
        db.add(setting)
    db.commit()
    return {"key": key, "value": value}


@router.delete("/{key}")
def delete_setting(key: str, db: Session = Depends(get_db)):
    """删除设置"""
    setting = db.query(Setting).filter(Setting.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="设置不存在")
    db.delete(setting)
    db.commit()
    return {"message": "设置已删除"}


# 默认设置项
DEFAULT_SETTINGS = {
    "auto_ship": {"value": "true", "description": "自动发货开关"},
    "auto_signin": {"value": "true", "description": "自动签到开关"},
    "ai_reply": {"value": "true", "description": "AI 自动回复开关"},
    "stock_alert_threshold": {"value": "10", "description": "库存预警阈值"},
    "notification_email": {"value": "", "description": "通知邮箱"},
    "refresh_interval": {"value": "60", "description": "刷新间隔（分钟）"},
    "message_check_interval": {"value": "30", "description": "消息检查间隔（分钟）"},
}


@router.post("/init")
def init_default_settings(db: Session = Depends(get_db)):
    """初始化默认设置"""
    for key, config in DEFAULT_SETTINGS.items():
        existing = db.query(Setting).filter(Setting.key == key).first()
        if not existing:
            setting = Setting(key=key, value=config["value"], description=config["description"])
            db.add(setting)
    db.commit()
    return {"message": "默认设置已初始化"}
