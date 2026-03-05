# 闲鱼自动管理系统

闲鱼自动化运营管理系统，支持账号管理、商品管理、卡密管理、订单自动发货、智能客服等功能。

## 功能特性

- **账号管理**: 批量管理闲鱼账号，支持 Cookies 加密存储
- **商品管理**: 商品发布、编辑、上下架
- **卡密管理**: 卡密批量生成、库存管理
- **订单自动发货**: 订单支付后自动发送卡密
- **智能客服 (CC)**: 基于 MiniMax AI 的自动回复
- **定时任务**: 自动擦亮、自动签到、订单监控
- **数据备份**: 支持导出/导入 JSON 数据

## 技术栈

- 后端: Python 3.11 + FastAPI + SQLAlchemy
- 前端: Vue 3 + Element Plus
- 数据库: PostgreSQL
- 任务调度: APScheduler
- AI: MiniMax API

## 快速开始

### Docker 启动（推荐）

```bash
# 克隆项目
git clone https://github.com/Tyunsen/xianyu-auto.git
cd xianyu-auto

# 启动服务
docker-compose up -d
```

访问 http://localhost

### 本地开发

```bash
# 后端
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload

# 前端
cd frontend
npm install
npm run dev
```

## 配置说明

在 `backend/.env` 中配置：

```env
DATABASE_URL=postgresql://xianyu:xianyu123@postgres:5432/xianyu_auto
MINIMAX_API_KEY=your_api_key
SMTP_HOST=smtp.example.com
SMTP_USER=your_email@example.com
SMTP_PASSWORD=your_password
```

## API 文档

启动后访问: http://localhost:8000/docs

## 目录结构

```
xianyu-auto/
├── backend/           # 后端代码
│   ├── src/
│   │   ├── api/      # API 路由
│   │   ├── models/   # 数据模型
│   │   ├── services/ # 业务逻辑
│   │   └── tasks/    # 定时任务
│   └── tests/        # 单元测试
├── frontend/         # 前端代码
├── docker-compose.yml
└── README.md
```

## License

MIT
