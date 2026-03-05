from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.database import init_db
from app.api.admin_router import router as admin_router
from app.api.accounts_router import router as accounts_router
from app.api.products_router import router as products_router
from app.api.cards_router import router as cards_router
from app.api.orders_router import router as orders_router
from app.api.messages_router import router as messages_router
from app.api.logs_router import router as logs_router
from app.api.alerts_router import router as alerts_router
from app.api.statistics_router import router as statistics_router
from app.api.backup_router import router as backup_router
from app.api.blacklist_router import router as blacklist_router

settings = get_settings()

# 初始化数据库表
init_db()

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
app.include_router(admin_router, prefix="/api/admin", tags=["管理员"])
app.include_router(accounts_router, prefix="/api/accounts", tags=["账号管理"])
app.include_router(products_router, prefix="/api/products", tags=["商品管理"])
app.include_router(cards_router, prefix="/api/cards", tags=["卡密管理"])
app.include_router(orders_router, prefix="/api/orders", tags=["订单管理"])
app.include_router(messages_router, prefix="/api/messages", tags=["消息管理"])
app.include_router(logs_router, prefix="/api/logs", tags=["日志管理"])
app.include_router(alerts_router, prefix="/api/alerts", tags=["告警管理"])
app.include_router(statistics_router, prefix="/api/statistics", tags=["数据统计"])
app.include_router(backup_router, prefix="/api/backup", tags=["备份导出"])
app.include_router(blacklist_router, prefix="/api/blacklist", tags=["黑名单管理"])
