from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.models import Alert, AlertStatus


class AlertService:
    def __init__(self, db: Session):
        self.db = db

    def list_alerts(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        type: Optional[str] = None
    ) -> dict:
        """获取告警列表"""
        query = self.db.query(Alert)

        if status:
            query = query.filter(Alert.status == status)
        if type:
            query = query.filter(Alert.type == type)

        total = query.count()
        items = query.order_by(Alert.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "total": total,
            "items": [AlertResponse.model_validate(item) for item in items]
        }

    def get_unhandled_count(self) -> int:
        """获取未处理告警数量"""
        return self.db.query(Alert).filter(
            Alert.status == AlertStatus.PENDING.value
        ).count()

    def create_alert(
        self,
        type: str,
        title: str,
        content: str,
        account_id: Optional[int] = None,
        order_id: Optional[int] = None
    ) -> Alert:
        """创建告警"""
        alert = Alert(
            type=type,
            title=title,
            content=content,
            account_id=account_id,
            order_id=order_id,
            status=AlertStatus.PENDING.value
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def handle_alert(self, alert_id: int) -> dict:
        """处理告警"""
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return {"success": False, "message": "告警不存在"}

        alert.status = AlertStatus.HANDLED.value
        alert.handled_at = datetime.now()
        self.db.commit()
        return {"success": True, "message": "处理成功"}

    def ignore_alert(self, alert_id: int) -> dict:
        """忽略告警"""
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return {"success": False, "message": "告警不存在"}

        alert.status = AlertStatus.IGNORED.value
        alert.handled_at = datetime.now()
        self.db.commit()
        return {"success": True, "message": "已忽略"}


from app.api.alerts import AlertResponse
