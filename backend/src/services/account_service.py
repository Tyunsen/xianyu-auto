"""
账号服务
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from datetime import datetime

from src.models.account import Account
from src.models.alert import Alert, AlertType
from src.utils.encryption import get_encryptor


class AccountService:
    """账号服务"""

    def __init__(self, db: Session):
        self.db = db
        self.encryptor = get_encryptor()

    def check_login_status(self, account_id: int) -> dict:
        """
        检测账号登录状态

        Args:
            account_id: 账号 ID

        Returns:
            状态信息字典
        """
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return {"status": "not_found", "message": "账号不存在"}

        # 检查是否有 cookies
        if not account.cookies:
            return {"status": "no_cookies", "message": "未设置登录凭证"}

        # TODO: 使用 Playwright 实际检测登录状态
        # 1. 解密 cookies
        # 2. 使用 Playwright 加载 cookies 并访问闲鱼
        # 3. 检查是否需要重新登录

        # 暂时返回账号状态
        return {
            "status": account.status,
            "last_login": account.last_login,
            "message": "状态检测需要浏览器环境"
        }

    def refresh_cookies(self, account_id: int, cookies: str) -> bool:
        """
        刷新登录凭证

        Args:
            account_id: 账号 ID
            cookies: 新的 cookies 字符串

        Returns:
            是否成功
        """
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return False

        # 加密存储 cookies
        account.cookies = self.encryptor.encrypt(cookies)
        account.status = "online"
        account.last_login = func.now()
        self.db.commit()
        return True

    def get_decrypted_cookies(self, account_id: int) -> Optional[str]:
        """
        获取解密的 cookies

        Args:
            account_id: 账号 ID

        Returns:
            解密后的 cookies 或 None
        """
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account or not account.cookies:
            return None

        return self.encryptor.decrypt(account.cookies)

    def detect_expired_accounts(self) -> List[Account]:
        """
        检测所有失效账号（状态为 offline 或 error）

        Returns:
            失效账号列表
        """
        expired = self.db.query(Account).filter(
            Account.status.in_(["offline", "error"])
        ).all()
        return expired

    def create_expired_alert(self, account: Account, reason: str = "登录失效") -> Alert:
        """
        为失效账号创建告警

        Args:
            account: 账号对象
            reason: 告警原因

        Returns:
            创建的告警对象
        """
        alert = Alert(
            type=AlertType.LOGIN_EXPIRED.value,
            content=f"账号 [{account.nickname}] 登录失效: {reason}",
            account_id=account.id
        )
        self.db.add(alert)
        self.db.commit()
        return alert

    def update_status(self, account_id: int, status: str) -> bool:
        """
        更新账号状态

        Args:
            account_id: 账号 ID
            status: 新状态

        Returns:
            是否成功
        """
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return False

        account.status = status
        self.db.commit()
        return True
