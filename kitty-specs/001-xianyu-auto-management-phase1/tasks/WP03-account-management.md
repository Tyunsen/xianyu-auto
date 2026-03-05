---
work_package_id: WP03
title: 账号管理模块（后端）
lane: "doing"
dependencies: [WP02]
base_branch: 001-xianyu-auto-management-phase1-WP02
base_commit: e7826b8acee95959df53463c6f1e97a3439968cb
created_at: '2026-03-05T06:58:21.881132+00:00'
subtasks: [T011, T012, T013, T014]
shell_pid: "48636"
agent: "claude-code"
history:
- date: '2026-03-05'
  action: created
---

# WP03: 账号管理模块（后端）

## Objective

实现闲鱼账号的后端管理功能，包括 CRUD、登录状态检测、Cookie 加密存储。

## Context

**登录方式**: 扫码+账密登录（暂定）
**账号规模**: 10-50个

## Subtasks

### T011: 创建账号 API 路由 (CRUD)

**Purpose**: 提供账号管理的 REST API

**Steps**:
1. 创建 `backend/src/schemas/account.py`:
   ```python
   from pydantic import BaseModel
   from datetime import datetime
   from typing import Optional

   class AccountBase(BaseModel):
       nickname: str

   class AccountCreate(AccountBase):
       pass

   class AccountUpdate(BaseModel):
       nickname: Optional[str] = None
       status: Optional[str] = None

   class AccountResponse(AccountBase):
       id: int
       status: str
       last_login: Optional[datetime]
       created_at: datetime

       class Config:
           from_attributes = True
   ```
2. 创建 `backend/src/api/accounts.py`:
   ```python
   from fastapi import APIRouter, Depends, HTTPException
   from sqlalchemy.orm import Session
   from src.database import get_db
   from src.models.account import Account
   from src.schemas.account import AccountResponse, AccountCreate, AccountUpdate

   router = APIRouter(prefix="/api/accounts", tags=["accounts"])

   @router.get("", response_model=dict)
   def list_accounts(db: Session = Depends(get_db)):
       items = db.query(Account).all()
       return {"items": items, "total": len(items)}

   @router.post("", response_model=AccountResponse)
   def create_account(account: AccountCreate, db: Session = Depends(get_db)):
       db_account = Account(nickname=account.nickname, cookies="", status="pending_login")
       db.add(db_account)
       db.commit()
       db.refresh(db_account)
       return db_account

   @router.get("/{account_id}", response_model=AccountResponse)
   def get_account(account_id: int, db: Session = Depends(get_db)):
       account = db.query(Account).filter(Account.id == account_id).first()
       if not account:
           raise HTTPException(status_code=404, detail="Account not found")
       return account

   @router.put("/{account_id}", response_model=AccountResponse)
   def update_account(account_id: int, account: AccountUpdate, db: Session = Depends(get_db)):
       db_account = db.query(Account).filter(Account.id == account_id).first()
       if not db_account:
           raise HTTPException(status_code=404, detail="Account not found")
       for key, value in account.model_dump(exclude_unset=True).items():
           setattr(db_account, key, value)
       db.commit()
       db.refresh(db_account)
       return db_account

   @router.delete("/{account_id}")
   def delete_account(account_id: int, db: Session = Depends(get_db)):
       db_account = db.query(Account).filter(Account.id == account_id).first()
       if not db_account:
           raise HTTPException(status_code=404, detail="Account not found")
       db.delete(db_account)
       db.commit()
       return {"message": "Account deleted"}
   ```

**Files**:
- `backend/src/schemas/account.py`
- `backend/src/api/accounts.py`

**Validation**:
- [ ] API 路由注册到 main.py
- [ ] CRUD 功能测试通过

---

### T012: 实现登录状态检测服务

**Purpose**: 检测账号登录状态

**Steps**:
1. 创建 `backend/src/services/account_service.py`:
   ```python
   from sqlalchemy.orm import Session
   from src.models.account import Account

   class AccountService:
       def __init__(self, db: Session):
           self.db = db

       async def check_login_status(self, account_id: int) -> dict:
           """检测账号登录状态"""
           account = self.db.query(Account).filter(Account.id == account_id).first()
           if not account:
               return {"status": "not_found"}

           # TODO: 使用 Playwright 检查登录状态
           # 1. 加载 cookies
           # 2. 访问闲鱼首页
           # 3. 检查是否需要登录

           return {"status": account.status}

       async def refresh_cookies(self, account_id: int, cookies: str) -> bool:
           """刷新登录凭证"""
           account = self.db.query(Account).filter(Account.id == account_id).first()
           if not account:
               return False

           # 加密存储 cookies
           account.cookies = self._encrypt_cookies(cookies)
           account.status = "online"
           account.last_login = func.now()
           self.db.commit()
           return True

       def _encrypt_cookies(self, cookies: str) -> str:
           """加密 cookies"""
           # TODO: 实现加密
           return cookies
   ```

**Files**:
- `backend/src/services/account_service.py`

**Validation**:
- [ ] 服务类创建完成
- [ ] 与 Playwright 集成

---

### T013: 实现 Cookie 加密存储

**Purpose**: 安全存储登录凭证

**Steps**:
1. 创建 `backend/src/utils/encryption.py`:
   ```python
   from cryptography.fernet import Fernet
   import os

   class CookieEncryptor:
       def __init__(self):
           key = os.getenv("ENCRYPTION_KEY")
           if not key:
               key = Fernet.generate_key()
               # 提示用户设置环境变量
           self.cipher = Fernet(key.encode())

       def encrypt(self, data: str) -> str:
           return self.cipher.encrypt(data.encode()).decode()

       def decrypt(self, encrypted_data: str) -> str:
           return self.cipher.decrypt(encrypted_data.encode()).decode()
   ```

**Files**:
- `backend/src/utils/encryption.py`

**Validation**:
- [ ] 加密/解密功能正常

---

### T014: 实现登录失效告警

**Purpose**: 检测并告警登录失效

**Steps**:
1. 在 `account_service.py` 添加:
   ```python
   async def detect_expired_accounts(self) -> list:
       """检测所有失效账号"""
       expired = self.db.query(Account).filter(
           Account.status == "expired"
       ).all()
       return expired
   ```
2. 创建告警逻辑

**Validation**:
- [ ] 登录失效能正确检测

---

## Definition of Done

- [ ] 账号 CRUD API 完成
- [ ] 登录状态检测服务完成
- [ ] Cookie 加密存储完成
- [ ] 登录失效告警完成

## Dependencies

- WP02: 数据库模型和迁移

## Risks

- Playwright 浏览器环境配置

## Reviewer Guidance

1. 检查 API 响应格式
2. 检查加密实现安全性

## Implementation Command

```bash
spec-kitty implement WP03 --base WP02
```

## Activity Log

- 2026-03-05T06:58:23Z – claude-code – shell_pid=37996 – lane=doing – Assigned agent via workflow command
- 2026-03-05T07:03:05Z – claude-code – shell_pid=37996 – lane=for_review – Ready for review: 账号管理后端模块已完成
- 2026-03-05T08:00:53Z – claude-code – shell_pid=48636 – lane=doing – Started review via workflow command
