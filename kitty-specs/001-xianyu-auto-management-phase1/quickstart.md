# Quickstart: 闲鱼自动管理系统

## 环境要求

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Docker & Docker Compose

---

## 快速开始

### 1. 克隆项目

```bash
git clone <project-url>
cd auto_xianyu
```

### 2. 配置环境

复制环境配置文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下内容：

```env
# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/xianyu_auto

# MiniMax AI API
MINIMAX_API_KEY=your_api_key_here
MINIMAX_MODEL=abab6.5s

# 应用配置
SECRET_KEY=your_secret_key_here
DEBUG=true
```

### 3. 启动数据库（可选）

使用 Docker 启动 PostgreSQL：

```bash
docker run -d \
  --name xianyu-postgres \
  -e POSTGRES_DB=xianyu_auto \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:14
```

### 4. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python -m alembic upgrade head

# 启动服务
uvicorn src.main:app --reload
```

后端服务将在 http://localhost:8000 运行

### 5. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 http://localhost:5173 运行

### 6. 使用 Docker Compose 启动（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

访问 http://localhost 进行使用。

---

## 首次使用流程

### 1. 添加账号

1. 打开 Web 管理后台
2. 进入「账号管理」
3. 点击「添加账号」
4. 使用闲鱼 App 扫码登录

### 2. 添加商品

1. 进入「商品管理」
2. 点击「添加商品」
3. 填写商品信息
4. 保存后可以手动上架

### 3. 添加卡密

1. 进入「卡密管理」
2. 点击「添加卡密」或「批量导入」
3. 设置关联商品

### 4. 配置自动任务

1. 进入「系统设置」
2. 开启需要的自动功能：
   - 自动发货
   - 自动签到
   - 自动擦亮
   - AI 智能回复

---

## 开发指南

### 运行测试

```bash
# 后端测试
cd backend
pytest --cov=src tests/

# 运行覆盖率检查
pytest --cov=src --cov-report=html tests/
```

### 代码规范

- 使用 Black 格式化代码
- 使用 Flake8 检查代码
- 提交前运行测试

```bash
# 格式化
black src/ tests/

# 检查
flake8 src/ tests/
```

---

## 常见问题

### Q: 如何查看运行日志？

A: 在 Web 后台进入「运行日志」页面，或查看 `logs/` 目录下的日志文件。

### Q: AI 回复不工作怎么办？

A: 检查 `.env` 中的 `MINIMAX_API_KEY` 是否正确配置。

### Q: 账号登录失效怎么办？

A: 进入「账号管理」，点击账号右侧的「重新登录」按钮，重新扫码登录。

---

## API 文档

启动后端服务后，访问 http://localhost:8000/docs 查看完整的 API 文档（Swagger UI）。

---

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端 | Python 3.11, FastAPI |
| 前端 | Vue 3, Element Plus |
| 数据库 | PostgreSQL |
| 浏览器自动化 | Playwright |
| 任务调度 | APScheduler |
| AI | MiniMax API |
| 部署 | Docker Compose |
