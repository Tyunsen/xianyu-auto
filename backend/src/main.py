"""
闲鱼自动管理系统 - 后端入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from src.config import settings
from src.database import engine, Base

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("应用启动中...")

    # 创建数据库表
    # Base.metadata.create_all(bind=engine)

    logger.info("应用启动完成")
    yield
    logger.info("应用关闭中...")


# 创建 FastAPI 应用
app = FastAPI(
    title="闲鱼自动管理系统 API",
    description="提供账号、商品、卡密、订单等管理功能",
    version="0.1.0",
    lifespan=lifespan,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径"""
    return {"message": "闲鱼自动管理系统 API", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


# API 路由
from src.api import accounts, products

app.include_router(accounts.router)
app.include_router(products.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
