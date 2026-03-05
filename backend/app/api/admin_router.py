"""
管理员认证API
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import hashlib
from app.core.database import get_db
from app.models import Admin

router = APIRouter()


def hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    id: int
    username: str
    nickname: str | None
    token: str


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    """管理员登录"""
    admin = db.query(Admin).filter(Admin.username == data.username).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用"
        )

    if admin.password != hash_password(data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 更新最后登录时间
    admin.last_login = datetime.now()
    db.commit()

    # 简单生成token
    token = f"admin_{admin.id}_{datetime.now().timestamp()}"

    return LoginResponse(
        id=admin.id,
        username=admin.username,
        nickname=admin.nickname,
        token=token
    )


@router.post("/init")
async def init_admin(
    username: str = "admin",
    password: str = "admin123",
    db: Session = Depends(get_db)
):
    """初始化管理员账号（仅在无管理员时可用）"""
    existing = db.query(Admin).first()
    if existing:
        return {"message": "管理员已存在，请直接登录"}

    admin = Admin(
        username=username,
        password=hash_password(password),
        nickname="管理员"
    )
    db.add(admin)
    db.commit()

    return {"message": f"管理员创建成功，用户名: {username}, 密码: {password}"}
