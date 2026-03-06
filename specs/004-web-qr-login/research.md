# Research: 网页端咸鱼扫码登录

**Phase**: 0 - Research | **Date**: 2026-03-06 | **Feature**: 004-web-qr-login

---

## 研究主题 1: Playwright 在 Docker 中无头模式运行

### 问题
如何在 Linux 服务器（无显示器）的 Docker 容器中安装和使用 Playwright 浏览器？

### 调研结果

**Decision**: 使用 `python:3.11-slim` 基础镜像 + Playwright Python包 + 系统依赖

**Rationale**:
- Python slim镜像体积最小（约140MB）
- Playwright官方完全支持headless模式，不需要显示器
- 需要的系统依赖已在Dockerfile中列出

**关键依赖** (Dockerfile中已配置):
```dockerfile
# 1. 安装 Playwright Python 包
RUN pip install playwright==1.41.0

# 2. 安装 Chromium 浏览器
RUN playwright install chromium

# 3. 安装 Chromium 运行所需的系统库（无头模式必需）
RUN apt-get install -y \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2.0 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libpango-1.0-0 libcairo2 libasound2
```

**启动参数** (playwright_helper.py中已配置):
```python
self.browser = await self.playwright.chromium.launch(
    headless=True,  # 无头模式
    args=[
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox',           # Docker中必需
        '--disable-setuid-sandbox',
    ]
)
```

**Alternatives considered**:
| 方案 | 优点 | 缺点 |
|------|------|------|
| Selenium | 成熟稳定 | 需要额外安装浏览器driver，配置复杂 |
| Puppeteer | Node.js生态好 | 不支持Python |
| Playwright (当前) | 官方支持好，Python原生 | 需要系统依赖 |

---

## 研究主题 2: 前端二维码登录流程实现

### 问题
前端如何与后端Playwright生成的二维码进行交互？

### 调研结果

**Decision**: 前端轮询模式 - 调用start接口获取二维码，setInterval轮询check接口

**Rationale**:
- 简单可靠，易于实现
- 后端已有完整API支持
- WebSocket会增加不必要的复杂度

**API 契约**:

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/accounts/{id}/qr-login/start` | POST | 启动二维码登录，返回二维码base64 |
| `/api/accounts/{id}/qr-login/check` | POST | 检查登录状态，返回status: waiting/success/error |
| `/api/accounts/{id}/qr-login/cancel` | POST | 取消登录 |

**前端流程**:
```
1. 用户点击"扫码登录"
   ↓
2. 调用 startQRLogin(id) → 获取二维码base64
   ↓
3. 在对话框中显示二维码图片
   ↓
4. setInterval 每2秒调用 checkQRLogin(id)
   ↓
5. 状态为 "success" → 关闭对话框，刷新列表
   ↓
6. 状态为 "error" → 显示错误，提示重试
```

**Alternatives considered**:
| 方案 | 优点 | 缺点 |
|------|------|------|
| WebSocket | 实时推送 | 需要后端支持WS，增加复杂度 |
| 轮询 (当前) | 实现简单 | 需要前端定时器 |
| Server-Sent Events | 单向推送 | 需要后端支持SSE |

---

## 研究主题 3: 登录状态保持与自动检测

### 问题
如何保持账号登录状态？检测到过期后如何处理？

### 调研结果

**Decision**: APScheduler定时任务 + 邮件通知

**Rationale**:
- 项目已有APScheduler框架
- 邮件通知是标准做法
- 6小时间隔符合Cookie有效期

**实现方案**:

1. **定时检测任务** (login_check_task.py):
   - 间隔: 6小时
   - 动作: 使用Cookie访问咸鱼API验证有效性
   - 结果: 更新账号状态，标记过期账号

2. **邮件通知** (email_service.py):
   - 触发: 检测到账号过期
   - 内容: 账号昵称、过期时间、重新登录指引

3. **手动刷新**:
   - 用户可随时点击"刷新状态"按钮
   - 用户可点击"重新登录"重新扫码

**Alternatives considered**:
| 方案 | 优点 | 缺点 |
|------|------|------|
| 每次操作前检测 | 及时发现 | 每次请求都检测，增加延迟 |
| 定时检测 (当前) | 统一处理，可批量 | 有一定延迟 |
| 被动检测 | 无额外开销 | 不够及时 |

---

## 研究结论总结

| 研究项 | 决定 | 状态 |
|--------|------|------|
| Playwright Docker安装 | python:3.11-slim + 系统依赖 | ✅ 已有实现 |
| 前端二维码流程 | 轮询模式 | ⚠️ 需完善前端UI |
| 登录状态检测 | APScheduler + 邮件 | ✅ 已有实现 |

**关键待办**:
1. 完善前端Accounts.vue，添加二维码登录对话框
2. 验证Docker构建成功
3. 端到端测试扫码登录流程
