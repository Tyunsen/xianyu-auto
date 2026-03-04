# 咸鱼自动管理项目

基于 Playwright + Claude Code 的咸鱼自动化管理系统，支持自动回复、自动发货、多账号管理等功能。

## 技术栈

- 后端: FastAPI + Python
- 前端: Vue3 + Vite
- 浏览器: Playwright
- 数据库: MySQL
- AI: Claude Code

## 功能特性

- 商品管理（手动/批量）
- 卡密管理（手动/批量）
- 多账号支持（环境隔离）
- 自动回复（AI智能回复）
- 自动发货
- 自动确认/免拼发货
- 自动擦亮/签到
- 邮件通知
- 数据统计
- 风控保护

## 快速开始

```bash
# 1. 克隆项目
git clone <this-repo>

# 2. 配置环境变量
cp .env.example .env

# 3. 启动服务
docker-compose up -d
```

## 项目结构

```
xianyu-auto/
├── backend/           # 后端服务
├── frontend/         # 前端界面
├── playwright/       # 浏览器配置
├── data/            # 数据目录
└── docker-compose.yml
```
