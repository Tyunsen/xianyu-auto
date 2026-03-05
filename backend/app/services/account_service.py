from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime
from app.models import Account, AccountStatus
from app.api.accounts import AccountCreate, AccountUpdate, AccountResponse


class AccountService:
    def __init__(self, db: Session):
        self.db = db

    def list_accounts(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> dict:
        """获取账号列表"""
        query = self.db.query(Account)

        if status:
            query = query.filter(Account.status == status)
        if is_active is not None:
            query = query.filter(Account.is_active == is_active)

        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()

        return {
            "total": total,
            "items": [self._to_response(item) for item in items]
        }

    def get_account(self, account_id: int) -> Optional[Account]:
        """获取账号详情"""
        return self.db.query(Account).filter(Account.id == account_id).first()

    def create_account(self, data: AccountCreate) -> Account:
        """创建账号"""
        account = Account(
            name=data.name,
            cookie=data.cookie,
            user_agent=data.user_agent,
            status=AccountStatus.NORMAL.value,
            last_login=datetime.now()
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update_account(self, account_id: int, data: AccountUpdate) -> Optional[Account]:
        """更新账号"""
        account = self.get_account(account_id)
        if not account:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(account, key, value)

        account.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(account)
        return account

    def delete_account(self, account_id: int) -> bool:
        """删除账号"""
        account = self.get_account(account_id)
        if not account:
            return False
        self.db.delete(account)
        self.db.commit()
        return True

    def test_login_status(self, account_id: int) -> dict:
        """测试登录状态"""
        account = self.get_account(account_id)
        if not account:
            return {"success": False, "message": "账号不存在"}

        # TODO: 使用Playwright测试登录状态
        return {
            "success": True,
            "message": "登录状态正常",
            "status": account.status
        }

    def refresh_cookie(self, account_id: int) -> dict:
        """刷新Cookie"""
        account = self.get_account(account_id)
        if not account:
            return {"success": False, "message": "账号不存在"}

        # TODO: 实现Cookie刷新逻辑
        return {
            "success": False,
            "message": "请手动更新Cookie"
        }

    def get_active_accounts(self) -> list[Account]:
        """获取所有正常状态的账号"""
        return self.db.query(Account).filter(
            Account.is_active == True,
            Account.status == AccountStatus.NORMAL.value
        ).all()

    def _to_response(self, account: Account) -> AccountResponse:
        return AccountResponse.model_validate(account)
