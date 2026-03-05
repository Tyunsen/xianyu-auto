from sqlalchemy.orm import Session
from typing import Optional
from app.models import Log


class LogService:
    def __init__(self, db: Session):
        self.db = db

    def list_logs(
        self,
        page: int = 1,
        page_size: int = 20,
        level: Optional[str] = None,
        type: Optional[str] = None,
        account_id: Optional[int] = None
    ) -> dict:
        """获取日志列表"""
        query = self.db.query(Log)

        if level:
            query = query.filter(Log.level == level)
        if type:
            query = query.filter(Log.type == type)
        if account_id:
            query = query.filter(Log.account_id == account_id)

        total = query.count()
        items = query.order_by(Log.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "total": total,
            "items": [LogResponse.model_validate(item) for item in items]
        }

    def create_log(
        self,
        level: str,
        type: str,
        message: str,
        account_id: Optional[int] = None,
        order_id: Optional[int] = None,
        extra: Optional[str] = None
    ) -> Log:
        """创建日志"""
        log = Log(
            level=level,
            type=type,
            message=message,
            account_id=account_id,
            order_id=order_id,
            extra=extra
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def info(self, type: str, message: str, **kwargs):
        """快捷方法：记录INFO日志"""
        return self.create_log("INFO", type, message, **kwargs)

    def error(self, type: str, message: str, **kwargs):
        """快捷方法：记录ERROR日志"""
        return self.create_log("ERROR", type, message, **kwargs)

    def warning(self, type: str, message: str, **kwargs):
        """快捷方法：记录WARNING日志"""
        return self.create_log("WARNING", type, message, **kwargs)


from app.api.logs import LogResponse
