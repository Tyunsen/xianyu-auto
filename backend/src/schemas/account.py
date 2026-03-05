"""
账号 Schema
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AccountBase(BaseModel):
    """账号基础字段"""
    nickname: str


class AccountCreate(AccountBase):
    """创建账号请求"""
    pass


class AccountUpdate(BaseModel):
    """更新账号请求"""
    nickname: Optional[str] = None
    status: Optional[str] = None
    cookies: Optional[str] = None


class AccountResponse(AccountBase):
    """账号响应"""
    id: int
    status: str
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
