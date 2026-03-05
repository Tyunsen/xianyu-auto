"""
告警服务
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from src.models.alert import Alert, AlertType
from src.models.settings import Setting


class AlertService:
    """告警服务"""

    def __init__(self, db: Session):
        self.db = db

    def create_alert(
        self,
        alert_type: str,
        content: str,
        account_id: int = None
    ) -> Alert:
        """创建告警"""
        alert = Alert(
            type=alert_type,
            content=content,
            account_id=account_id
        )
        self.db.add(alert)
        self.db.commit()

        # 尝试发送邮件通知
        self._send_notification(alert_type, content)

        return alert

    def get_unresolved_alerts(self) -> List[Alert]:
        """获取未解决的告警"""
        return self.db.query(Alert).filter(
            Alert.is_resolved == False
        ).order_by(Alert.created_at.desc()).all()

    def get_alerts(
        self,
        resolved: bool = None,
        limit: int = 100
    ) -> List[Alert]:
        """获取告警列表"""
        query = self.db.query(Alert)

        if resolved is not None:
            query = query.filter(Alert.is_resolved == resolved)

        return query.order_by(Alert.created_at.desc()).limit(limit).all()

    def resolve_alert(self, alert_id: int) -> bool:
        """解决告警"""
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return False

        alert.is_resolved = True
        alert.resolved_at = datetime.now()
        self.db.commit()
        return True

    def get_notification_email(self) -> Optional[str]:
        """获取通知邮箱"""
        setting = self.db.query(Setting).filter(
            Setting.key == "notification_email"
        ).first()
        return setting.value if setting else None

    def set_notification_email(self, email: str) -> bool:
        """设置通知邮箱"""
        setting = self.db.query(Setting).filter(
            Setting.key == "notification_email"
        ).first()

        if setting:
            setting.value = email
        else:
            setting = Setting(key="notification_email", value=email)
            self.db.add(setting)

        self.db.commit()
        return True

    async def _send_notification(self, alert_type: str, content: str):
        """发送邮件通知"""
        email = self.get_notification_email()
        if not email:
            return

        try:
            from src.services.email_service import get_email_service
            email_service = get_email_service()
            await email_service.send_alert_email(email, alert_type, content)
        except Exception as e:
            print(f"发送告警邮件失败: {e}")

    async def check_and_notify(self):
        """检查并发送通知"""
        alerts = self.get_unresolved_alerts()
        if not alerts:
            return

        email = self.get_notification_email()
        if not email:
            return

        # 发送汇总通知
        try:
            from src.services.email_service import get_email_service
            email_service = get_email_service()

            content = f"有 {len(alerts)} 条未处理告警:\n"
            for alert in alerts[:5]:
                content += f"- [{alert.type}] {alert.content}\n"

            await email_service.send_alert_email(
                email,
                "告警汇总",
                content
            )
        except Exception as e:
            print(f"发送汇总邮件失败: {e}")
