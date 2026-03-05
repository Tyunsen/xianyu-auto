"""
日志服务
"""
from sqlalchemy.orm import Session
from src.models.log import Log, LogLevel, LogCategory


def log_task(
    db: Session,
    category: str,
    content: str,
    level: str = "info",
    account_id: int = None
):
    """
    记录任务日志

    Args:
        db: 数据库会话
        category: 日志分类 (task, message, ship, system, account)
        content: 日志内容
        level: 日志级别 (debug, info, warning, error)
        account_id: 关联账号 ID
    """
    log = Log(
        level=level,
        category=category,
        content=content,
        account_id=account_id
    )
    db.add(log)
    db.commit()
    return log


def log_message(
    db: Session,
    content: str,
    account_id: int = None,
    is_auto: bool = False
):
    """
    记录消息日志

    Args:
        db: 数据库会话
        content: 日志内容
        account_id: 关联账号 ID
        is_auto: 是否自动消息
    """
    return log_task(
        db=db,
        category=LogCategory.MESSAGE.value,
        content=content,
        level=LogLevel.INFO.value,
        account_id=account_id
    )


def log_ship(
    db: Session,
    content: str,
    account_id: int = None
):
    """
    记录发货日志

    Args:
        db: 数据库会话
        content: 日志内容
        account_id: 关联账号 ID
    """
    return log_task(
        db=db,
        category=LogCategory.SHIP.value,
        content=content,
        level=LogLevel.INFO.value,
        account_id=account_id
    )


def log_error(
    db: Session,
    content: str,
    category: str = LogCategory.SYSTEM.value,
    account_id: int = None
):
    """
    记录错误日志

    Args:
        db: 数据库会话
        content: 错误内容
        category: 日志分类
        account_id: 关联账号 ID
    """
    return log_task(
        db=db,
        category=category,
        content=content,
        level=LogLevel.ERROR.value,
        account_id=account_id
    )


def get_recent_logs(
    db: Session,
    category: str = None,
    limit: int = 100
):
    """
    获取最近日志

    Args:
        db: 数据库会话
        category: 日志分类筛选
        limit: 返回数量

    Returns:
        日志列表
    """
    query = db.query(Log)

    if category:
        query = query.filter(Log.category == category)

    return query.order_by(Log.created_at.desc()).limit(limit).all()
