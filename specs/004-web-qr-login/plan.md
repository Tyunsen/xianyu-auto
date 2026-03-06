# Implementation Plan: 网页端咸鱼扫码登录

**Branch**: `004-web-qr-login` | **Date**: 2026-03-06 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/004-web-qr-login/spec.md`

## Summary

在网页前端实现咸鱼账号扫码登录功能，无需用户手动复制Cookie。通过后端Playwright浏览器自动化生成二维码，前端轮询检测登录状态，完成后自动保存加密Cookie到数据库。同时实现定时登录状态检测和过期告警通知。

## Technical Context

**Language/Version**: Python 3.11, Vue 3.4, TypeScript 5.3
**Primary Dependencies**: FastAPI, Vue 3, Element Plus, Playwright 1.41, SQLAlchemy 2.0, PostgreSQL 14+
**Storage**: PostgreSQL (数据库存储账号和加密Cookie)
**Testing**: pytest, pytest-asyncio
**Target Platform**: Linux Server (Docker容器部署)
**Project Type**: Web Service + Web Application
**Performance Goals**: 二维码生成响应 < 2s, 登录状态检测 < 5s
**Constraints**: 无头模式浏览器运行，需要正确安装系统依赖
**Scale/Scope**: 多账号管理（支持同时多个账号登录流程）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| 1. 小步提交 | ✅ Pass | 每个功能点独立提交 |
| 2. 完成即检查 | ✅ Pass | Task完成后立即验证 |
| 3. 文档同步 | ✅ Pass | 同步更新相关文档 |

**Constitution Check Result**: ✅ PASSED - 可以继续进行设计阶段

## Project Structure

### Documentation (this feature)

```text
specs/004-web-qr-login/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

> **Note**: 不需要 contracts/ 目录 - 本功能是内部 Web 应用，API 已直接在代码中定义

### Source Code (repository root)

```text
# Backend - 咸鱼自动管理后端
backend/
├── src/
│   ├── api/
│   │   ├── accounts.py          # 账号管理API（含二维码登录端点）
│   │   └── ...
│   ├── models/
│   │   └── account.py          # 账号数据模型
│   ├── services/
│   │   ├── account_service.py  # 账号服务
│   │   └── email_service.py    # 邮件通知服务
│   ├── tasks/
│   │   ├── scheduler.py        # 定时任务调度器
│   │   └── login_check_task.py # 登录状态检测任务
│   ├── utils/
│   │   ├── playwright_helper.py # Playwright浏览器辅助
│   │   └── encryption.py       # Cookie加密工具
│   ├── main.py
│   └── config.py
├── Dockerfile                   # 已包含Playwright依赖
└── requirements.txt             # 已包含playwright==1.41.0

# Frontend - Vue 3管理前端
frontend/
├── src/
│   ├── api/
│   │   └── client.ts           # API客户端（含二维码登录方法）
│   ├── pages/
│   │   └── Accounts.vue        # 账号管理页面（需修改）
│   └── ...
├── nginx.conf
└── Dockerfile
```

**Structure Decision**: 使用前后端分离架构，后端使用Playwright无头浏览器实现二维码登录，前端Vue 3页面调用API实现扫码流程

## Phase 0 - Research Findings

### Research 1: Playwright Docker 安装

**Decision**: 使用 `python:3.11-slim` 基础镜像 + Playwright Python包 + 系统依赖

**Rationale**:
- Python slim镜像体积最小
- Playwright官方支持headless模式，无需显示器
- 系统依赖已包含在Dockerfile中

**关键依赖**:
```dockerfile
# 安装 Playwright Python 包
RUN pip install playwright==1.41.0

# 安装 Chromium 浏览器
RUN playwright install chromium

# 安装 Chromium 运行所需的系统库（无头模式必需）
RUN apt-get install -y \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2.0 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libpango-1.0-0 libcairo2 libasound2
```

**Alternatives considered**:
- puppeteer: 不支持Python
- selenium: 需要额外安装浏览器driver

### Research 2: 前端二维码登录流程

**Decision**: 前端轮询模式 - 调用start接口获取二维码，setInterval轮询check接口

**Rationale**:
- 简单可靠，易于实现
- 后端已有API支持
- WebSocket会增加复杂度

**流程**:
1. 用户点击"扫码登录" → 前端调用 `POST /api/accounts/{id}/qr-login/start`
2. 后端返回二维码base64图片
3. 前端在对话框中显示二维码
4. 前端每2秒调用 `POST /api/accounts/{id}/qr-login/check` 轮询状态
5. 登录成功后自动关闭对话框，刷新账号列表

### Research 3: 登录状态保持与检测

**Decision**: APScheduler定时任务 + 邮件通知

**Rationale**:
- 已有APScheduler框架
- 邮件通知是标准做法

**实现**:
- 每6小时执行一次登录状态检测
- 检测到过期发送邮件告警
- 支持手动触发检测

## Phase 1 - Design

### 数据模型

见 `data-model.md`

### API 契约

见 `contracts/` 目录

### 快速开始

见 `quickstart.md`

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

无复杂度违规
