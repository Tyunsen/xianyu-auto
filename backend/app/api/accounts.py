from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ============ Schemas ============

class AccountBase(BaseModel):
    name: str = Field(..., description="账号名称")
    cookie: str = Field(..., description="登录Cookie")
    user_agent: str = ""


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    cookie: Optional[str] = None
    user_agent: Optional[str] = None
    is_active: Optional[bool] = None


class AccountResponse(AccountBase):
    id: int
    status: str
    last_login: Optional[datetime] = None
    last_active: Optional[datetime] = None
    error_message: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AccountListResponse(BaseModel):
    total: int
    items: list[AccountResponse]
