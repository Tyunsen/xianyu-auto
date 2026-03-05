"""
账号管理 API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.account import Account
from src.schemas.account import AccountResponse, AccountCreate, AccountUpdate

router = APIRouter(prefix="/api/accounts", tags=["账号管理"])


@router.get("", response_model=dict)
def list_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取账号列表"""
    items = db.query(Account).offset(skip).limit(limit).all()
    total = db.query(Account).count()
    return {"items": items, "total": total}


@router.post("", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    """创建账号"""
    db_account = Account(
        nickname=account.nickname,
        cookies="",
        status="offline"
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    """获取单个账号"""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="账号不存在")
    return account


@router.put("/{account_id}", response_model=AccountResponse)
def update_account(account_id: int, account: AccountUpdate, db: Session = Depends(get_db)):
    """更新账号"""
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="账号不存在")

    update_data = account.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_account, key, value)

    db.commit()
    db.refresh(db_account)
    return db_account


@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    """删除账号"""
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="账号不存在")

    db.delete(db_account)
    db.commit()
    return {"message": "账号已删除"}


@router.post("/{account_id}/refresh-cookies")
def refresh_cookies(account_id: int, cookies: str, db: Session = Depends(get_db)):
    """刷新账号 Cookies"""
    from src.services.account_service import AccountService

    service = AccountService(db)
    success = service.refresh_cookies(account_id, cookies)
    if not success:
        raise HTTPException(status_code=404, detail="账号不存在")
    return {"message": "Cookies 更新成功"}


@router.get("/{account_id}/status")
def check_status(account_id: int, db: Session = Depends(get_db)):
    """检查账号登录状态"""
    from src.services.account_service import AccountService

    service = AccountService(db)
    result = service.check_login_status(account_id)
    return result
