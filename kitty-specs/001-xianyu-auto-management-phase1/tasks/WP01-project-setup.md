---
work_package_id: WP01
title: 项目基础设置
lane: "doing"
dependencies: []
base_branch: master
base_commit: 6a45668897f403c3a61fce4c2b3d5a30dc1b41ce
created_at: '2026-03-05T05:57:07.563867+00:00'
subtasks: [T001, T002, T003, T004, T005]
shell_pid: "46996"
agent: "claude-code"
history:
- date: '2026-03-05'
  action: created
---

# WP01: 项目基础设置

## Objective

创建闲鱼自动管理系统的项目基础结构，包括后端和前端项目、Docker 配置、环境变量。

## Context

**项目技术栈**:
- 后端: Python 3.11 + FastAPI
- 前端: Vue 3 + Element Plus
- 数据库: PostgreSQL
- 浏览器自动化: Playwright
- 任务调度: APScheduler
- AI: MiniMax API
- 部署: Docker Compose

**数据规模**: 10-50个账号，中等规模
**定时任务**: 中午12-13点执行

## Subtasks

### T001: 创建后端项目结构 (backend/src/)

**Purpose**: 初始化 Python FastAPI 项目结构

**Steps**:
1. 创建 `backend/` 目录
2. 初始化 Python 虚拟环境
3. 安装基础依赖: fastapi, uvicorn, sqlalchemy, psycopg2-binary, alembic, pydantic, python-dotenv
4. 创建目录结构:
   ```
   backend/
   ├── src/
   │   ├── __init__.py
   │   ├── main.py           # FastAPI 入口
   │   ├── config.py         # 配置
   │   ├── database.py      # 数据库连接
   │   ├── models/           # 数据模型
   │   ├── schemas/         # Pydantic schemas
   │   ├── api/              # API 路由
   │   ├── services/         # 业务逻辑
   │   ├── tasks/            # 定时任务
   │   ├── browser/          # Playwright
   │   └── ai/               # AI 集成
   ├── tests/
   │   ├── unit/
   │   └── integration/
   ├── alembic/
   │   ├── env.py
   │   └── versions/
   ├── requirements.txt
   └── pyproject.toml
   ```
5. 创建 `src/__init__.py`
6. 创建 `src/main.py` 基础框架（包含健康检查端点）

**Files**:
- `backend/src/main.py` - 入口文件
- `backend/requirements.txt` - 依赖列表
- `backend/pyproject.toml` - 项目配置

**Validation**:
- [ ] Python 虚拟环境可正常创建
- [ ] `pip install -r requirements.txt` 成功
- [ ] `uvicorn src.main:app --reload` 能启动

---

### T002: 创建前端项目结构 (frontend/)

**Purpose**: 初始化 Vue 3 + Element Plus 项目

**Steps**:
1. 使用 Vite 创建 Vue 3 项目
   ```bash
   npm create vite@latest frontend -- --template vue
   cd frontend
   npm install
   ```
2. 安装依赖:
   - element-plus (UI 组件库)
   - vue-router (路由)
   - pinia (状态管理)
   - axios (HTTP 客户端)
   - @vueuse/core (工具函数)
3. 创建目录结构:
   ```
   frontend/
   ├── src/
   │   ├── api/              # API 调用
   │   ├── components/       # 组件
   │   ├── pages/            # 页面
   │   ├── stores/           # Pinia 状态
   │   ├── router/           # 路由配置
   │   ├── utils/            # 工具函数
   │   ├── App.vue
   │   └── main.ts
   ├── index.html
   ├── vite.config.ts
   └── package.json
   ```
4. 创建基础 Vue 组件结构

**Files**:
- `frontend/package.json` - 依赖列表
- `frontend/src/main.ts` - 入口文件
- `frontend/vite.config.ts` - Vite 配置

**Validation**:
- [ ] `npm install` 成功
- [ ] `npm run dev` 能启动开发服务器
- [ ] 浏览器能访问 http://localhost:5173

---

### T003: 配置 Docker Compose

**Purpose**: 创建 Docker 部署配置

**Steps**:
1. 创建 `docker-compose.yml`:
   ```yaml
   version: '3.8'

   services:
     postgres:
       image: postgres:14
       environment:
         POSTGRES_DB: xianyu_auto
         POSTGRES_USER: xianyu
         POSTGRES_PASSWORD: xianyu123
       volumes:
         - postgres_data:/var/lib/postgresql/data
       ports:
         - "5432:5432"

     backend:
       build: ./backend
       ports:
         - "8000:8000"
       environment:
         - DATABASE_URL=postgresql://xianyu:xianyu123@postgres:5432/xianyu_auto
       depends_on:
         - postgres
       volumes:
         - ./backend:/app

     frontend:
       build: ./frontend
       ports:
         - "80:80"
       depends_on:
         - backend

   volumes:
     postgres_data:
   ```
2. 创建 `backend/Dockerfile`:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
   ```
3. 创建 `frontend/Dockerfile`:
   ```dockerfile
   FROM node:18-alpine as build
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   RUN npm run build

   FROM nginx:alpine
   COPY --from=build /app/dist /usr/share/nginx/html
   ```

**Files**:
- `docker-compose.yml`
- `backend/Dockerfile`
- `frontend/Dockerfile`

**Validation**:
- [ ] `docker-compose config` 验证通过
- [ ] 各服务能正常启动

---

### T004: 配置环境变量 (.env.example)

**Purpose**: 创建环境变量配置模板

**Steps**:
1. 创建 `.env.example`:
   ```env
   # 数据库
   DATABASE_URL=postgresql://xianyu:xianyu123@localhost:5432/xianyu_auto

   # 应用
   SECRET_KEY=your-secret-key-change-in-production
   DEBUG=true

   # MiniMax AI API
   MINIMAX_API_KEY=your_minimax_api_key
   MINIMAX_MODEL=abab6.5s

   # 邮件
   SMTP_HOST=smtp.example.com
   SMTP_PORT=587
   SMTP_USER=your_email@example.com
   SMTP_PASSWORD=your_email_password

   # 前端
   VITE_API_BASE_URL=http://localhost:8000
   ```
2. 创建 `.gitignore` 文件
3. 创建 `backend/.env` 用于本地开发

**Files**:
- `.env.example`
- `.gitignore`

**Validation**:
- [ ] .env.example 包含所有必要配置项
- [ ] .gitignore 正确配置

---

### T005: 安装基础依赖

**Purpose**: 确保所有依赖正确安装

**Steps**:
1. 后端依赖安装和验证:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   python -c "import fastapi; print('FastAPI OK')"
   ```
2. 前端依赖安装和验证:
   ```bash
   cd frontend
   npm install
   npm list vue element-plus
   ```

**Validation**:
- [ ] 后端依赖无冲突
- [ ] 前端依赖无冲突
- [ ] 版本兼容性检查通过

---

## Definition of Done

- [ ] 后端项目结构完整，FastAPI 可启动
- [ ] 前端项目结构完整，Vite 可启动
- [ ] Docker Compose 配置完整
- [ ] 环境变量配置模板完成
- [ ] 所有依赖可正常安装

## Risks

- 无重大风险
- 注意 Python 版本兼容性

## Reviewer Guidance

1. 验证目录结构是否符合项目规范
2. 检查依赖版本是否兼容
3. 确认 Docker 配置是否正确

## Implementation Command

```bash
# 无依赖，直接运行
spec-kitty implement WP01
```

## Activity Log

- 2026-03-05T05:57:10Z – claude – shell_pid=32364 – lane=doing – Assigned agent via workflow command
- 2026-03-05T06:04:03Z – claude – shell_pid=32364 – lane=for_review – Ready for review: 项目基础设置完成
- 2026-03-05T07:58:47Z – claude-code – shell_pid=46996 – lane=doing – Started review via workflow command
