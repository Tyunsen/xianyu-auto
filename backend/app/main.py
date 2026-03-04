from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings

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


# 导入并注册路由（待实现）
# from app.api import accounts, products, cards, orders, messages, tasks
# app.include_router(accounts.router, prefix="/api/accounts", tags=["账号管理"])
# app.include_router(products.router, prefix="/api/products", tags=["商品管理"])
# app.include_router(cards.router, prefix="/api/cards", tags=["卡密管理"])
# app.include_router(orders.router, prefix="/api/orders", tags=["订单管理"])
# app.include_router(messages.router, prefix="/api/messages", tags=["消息管理"])
# app.include_router(tasks.router, prefix="/api/tasks", tags=["任务管理"])
