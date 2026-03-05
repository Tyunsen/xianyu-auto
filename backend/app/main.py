from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.accounts_router import router as accounts_router
from app.api.products_router import router as products_router
from app.api.cards_router import router as cards_router
from app.api.orders_router import router as orders_router
from app.api.messages_router import router as messages_router
from app.api.logs_router import router as logs_router
from app.api.alerts_router import router as alerts_router

settings = get_settings()

# 创建FastAPI应用
app = FastAPI(
    title="咸鱼自动管理系统",
    description="基于Claude Code的咸鱼自动化管理后端",
    version="1.0.0",
    debug=settings.debug
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "咸鱼自动管理系统 API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# 注册路由
app.include_router(accounts_router, prefix="/api/accounts", tags=["账号管理"])
app.include_router(products_router, prefix="/api/products", tags=["商品管理"])
app.include_router(cards_router, prefix="/api/cards", tags=["卡密管理"])
app.include_router(orders_router, prefix="/api/orders", tags=["订单管理"])
app.include_router(messages_router, prefix="/api/messages", tags=["消息管理"])
app.include_router(logs_router, prefix="/api/logs", tags=["日志管理"])
app.include_router(alerts_router, prefix="/api/alerts", tags=["告警管理"])
