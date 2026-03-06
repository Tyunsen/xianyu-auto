"""
账号管理 API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from src.database import get_db
from src.models.account import Account
from src.schemas.account import AccountCreate, AccountUpdate

router = APIRouter(prefix="/api/accounts", tags=["账号管理"])


def account_to_dict(account: Account) -> Dict[str, Any]:
    """将Account模型转换为字典"""
    return {
        "id": account.id,
        "nickname": account.nickname,
        "status": account.status,
        "last_login": account.last_login.isoformat() if account.last_login else None,
        "created_at": account.created_at.isoformat() if account.created_at else None,
        "updated_at": account.updated_at.isoformat() if account.updated_at else None,
    }


@router.get("")
def list_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取账号列表"""
    items = db.query(Account).offset(skip).limit(limit).all()
    total = db.query(Account).count()
    return {"items": [account_to_dict(a) for a in items], "total": total}


@router.post("")
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    """创建账号"""
    db_account = Account(
        nickname=account.nickname,
        cookies=account.cookies or "",
        status=account.status or "offline"
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return account_to_dict(db_account)


@router.get("/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db)):
    """获取单个账号"""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="账号不存在")
    return account_to_dict(account)


@router.put("/{account_id}")
def update_account(account_id: int, account: AccountUpdate, db: Session = Depends(get_db)):
    """更新账号"""
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="账号不存在")

    if account.nickname is not None:
        db_account.nickname = account.nickname
    if account.status is not None:
        db_account.status = account.status
    if account.cookies is not None:
        db_account.cookies = account.cookies

    db.commit()
    db.refresh(db_account)
    return account_to_dict(db_account)


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


# ==================== 二维码登录 API ====================

@router.post("/{account_id}/qr-login/start")
async def start_qr_login(account_id: int, db: Session = Depends(get_db)):
    """开始二维码登录"""
    from src.utils.playwright_helper import get_playwright_helper

    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="账号不存在")

    helper = get_playwright_helper()

    try:
        result = await helper.start_qr_login(account_id)
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message", "获取二维码失败"))

        return {
            "success": True,
            "qr_code": result.get("qr_code"),
            "message": "请使用闲鱼APP扫码登录"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动登录失败: {str(e)}")


@router.post("/{account_id}/qr-login/check")
async def check_qr_login(account_id: int, db: Session = Depends(get_db)):
    """检查二维码登录状态"""
    from src.utils.playwright_helper import get_playwright_helper
    from src.services.account_service import AccountService

    helper = get_playwright_helper()

    try:
        result = await helper.check_qr_login_status(account_id)
        status = result.get("status")

        if status == "success":
            cookies = result.get("cookies")
            service = AccountService(db)
            service.refresh_cookies(account_id, cookies)

            account = db.query(Account).filter(Account.id == account_id).first()
            if account:
                account.status = "online"
                db.commit()

            await helper.close_login(account_id)

            return {"success": True, "status": "success", "message": "登录成功"}
        elif status == "waiting":
            return {"success": True, "status": "waiting", "message": "等待扫码中..."}
        else:
            return {"success": False, "status": status, "message": result.get("message", "登录失败")}
    except Exception as e:
        return {"success": False, "status": "error", "message": str(e)}


@router.post("/{account_id}/qr-login/cancel")
async def cancel_qr_login(account_id: int):
    """取消二维码登录"""
    from src.utils.playwright_helper import get_playwright_helper
    helper = get_playwright_helper()
    await helper.close_login(account_id)
    return {"message": "已取消登录"}


# ==================== 旧接口兼容 ====================

@router.post("/{account_id}/start-login")
async def start_login(account_id: int, db: Session = Depends(get_db)):
    return await start_qr_login(account_id, db)


@router.post("/{account_id}/complete-login")
async def complete_login(account_id: int, db: Session = Depends(get_db)):
    from src.utils.playwright_helper import get_playwright_helper
    from src.services.account_service import AccountService

    helper = get_playwright_helper()
    result = await helper.check_qr_login_status(account_id)

    if result.get("status") != "success":
        raise HTTPException(status_code=400, detail="登录未完成")

    service = AccountService(db)
    service.refresh_cookies(account_id, result.get("cookies"))
    await helper.close_login(account_id)

    return {"message": "登录成功", "status": "online"}


@router.post("/check-all-status")
async def check_all_accounts_status():
    """手动触发所有账号的登录状态检查"""
    from src.tasks.login_check_task import check_all_accounts_login_status

    try:
        results = await check_all_accounts_login_status()
        return {"message": "检测完成", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
