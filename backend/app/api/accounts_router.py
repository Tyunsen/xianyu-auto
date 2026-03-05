from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.models import Account
from app.api.accounts import (
    AccountCreate,
    AccountUpdate,
    AccountResponse,
    AccountListResponse
)
from app.services.account_service import AccountService

router = APIRouter()


@router.get("", response_model=AccountListResponse)
async def list_accounts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """获取账号列表"""
    service = AccountService(db)
    return service.list_accounts(page, page_size, status, is_active)


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(account_id: int, db: Session = Depends(get_db)):
    """获取账号详情"""
    service = AccountService(db)
    account = service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="账号不存在")
    return account


@router.post("", response_model=AccountResponse)
async def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db)
):
    """添加账号"""
    service = AccountService(db)
    return service.create_account(account)


@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: int,
    account: AccountUpdate,
    db: Session = Depends(get_db)
):
    """更新账号"""
    service = AccountService(db)
    updated = service.update_account(account_id, account)
    if not updated:
        raise HTTPException(status_code=404, detail="账号不存在")
    return updated


@router.delete("/{account_id}")
async def delete_account(account_id: int, db: Session = Depends(get_db)):
    """删除账号"""
    service = AccountService(db)
    success = service.delete_account(account_id)
    if not success:
        raise HTTPException(status_code=404, detail="账号不存在")
    return {"message": "删除成功"}


@router.post("/{account_id}/test-login")
async def test_login(account_id: int, db: Session = Depends(get_db)):
    """测试账号登录状态"""
    service = AccountService(db)
    result = service.test_login_status(account_id)
    return result


@router.post("/{account_id}/refresh-cookie")
async def refresh_cookie(
    account_id: int,
    db: Session = Depends(get_db)
):
    """刷新账号Cookie"""
    service = AccountService(db)
    result = service.refresh_cookie(account_id)
    return result
